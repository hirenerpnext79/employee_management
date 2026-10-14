import json
import importlib.metadata
import importlib.util
import frappe
from frappe import _
from frappe.utils import cint
from frappe.utils.password import get_decrypted_password


def get_vcard_doc(token):
    if not token:
        return None
    token_str = str(token).strip()
    vcard_name = None
    if token_str.isdigit():
        vcard_name = frappe.db.get_value("VCard", {"vcard_id": token_str}, "name")
    if not vcard_name and frappe.db.exists("VCard", token_str):
        vcard_name = token_str
    if not vcard_name:
        return None
    return frappe.get_doc("VCard", vcard_name)


def append_vcard_meta(vcard, vcard_doc):
    theme_name = vcard.get("theme")
    if theme_name:
        theme_path = frappe.db.get_value("VCard Theme", theme_name, "path", cache=True)
        vcard["theme"] = theme_path if theme_path else theme_name

    if vcard_doc.physical_card_theme:
        try:
            physical_theme_doc = frappe.get_cached_doc("Physical Card Theme", vcard_doc.physical_card_theme)
            vcard["physical_theme"] = physical_theme_doc.as_dict()
        except Exception:
            pass

    attachments = vcard_doc.get("attachment") or []
    vcard["attachments"] = [a.as_dict() for a in attachments]

    personal_social = (
        vcard_doc.get("table_shmz")
        or vcard_doc.get("personal_social_media")
        or vcard_doc.get("social_media")
        or []
    )
    vcard["personal_social_media"] = [s.as_dict() for s in personal_social]

    if vcard.get("company_page"):
        try:
            vcard["company_page_route"] = frappe.db.get_value(
                "Hns Web Page Creation", vcard.get("company_page"), "route", cache=True
            )
        except Exception:
            pass

    if vcard.get("product_page"):
        try:
            vcard["product_page_route"] = frappe.db.get_value(
                "Hns Web Page Creation", vcard.get("product_page"), "route", cache=True
            )
        except Exception:
            pass

    try:
        vcard_setting = frappe.get_cached_doc("Hns Web Page Settings")
        vcard["global_company_name"] = vcard_setting.company_name
        company_social = vcard_setting.get("company_social_media") or []
        vcard["company_social_media"] = [s.as_dict() for s in company_social]
    except Exception:
        vcard["global_company_name"] = None
        vcard["company_social_media"] = []


@frappe.whitelist(allow_guest=True)
def get_vcard_details(token):
    if not token:
        frappe.throw(_("Token is required"), frappe.ValidationError)

    try:
        vcard_doc = get_vcard_doc(token)
        if not vcard_doc:
            frappe.throw(_("VCard not found or invalid token"), frappe.PermissionError)

        vcard = vcard_doc.as_dict()
        append_vcard_meta(vcard, vcard_doc)
        return vcard
    except (frappe.ValidationError, frappe.PermissionError):
        raise
    except Exception as e:
        frappe.log_error(f"Error fetching vcard details: {str(e)}", "get_vcard_details")
        frappe.throw(_("Failed to fetch VCard details"))


@frappe.whitelist(allow_guest=True)
def get_csrf_token():
    return frappe.sessions.get_csrf_token()


def parse_event_log(log):
    log_dict = {}
    log_text = log
    if log:
        if isinstance(log, str):
            try:
                log_dict = json.loads(log)
                log_text = json.dumps(log_dict, indent=4)
            except Exception:
                log_text = log
        elif isinstance(log, dict):
            log_dict = log
            try:
                log_text = json.dumps(log, indent=4)
            except Exception:
                log_text = str(log)
        else:
            log_text = str(log)
    return log_dict, log_text


@frappe.whitelist(allow_guest=True)
def track_vcard_event(vcard, event_type, action_details=None, log=None):
    if not vcard or not event_type:
        frappe.throw(_("Missing required parameters"))

    try:
        if not frappe.db.exists("VCard", vcard):
            return {"status": "ignored"}

        log_dict, log_text = parse_event_log(log)
        location_data = log_dict.get("location") if isinstance(log_dict.get("location"), dict) else {}
        user_agent_val = log_dict.get("userAgent") or frappe.request.environ.get("HTTP_USER_AGENT", "")
        ip_address_val = location_data.get("ip") or frappe.local.request_ip

        doc = frappe.get_doc({
            "doctype": "VCard Analytics Log",
            "vcard": vcard,
            "event_type": event_type,
            "action_details": action_details,
            "user_agent": user_agent_val,
            "ip_address": ip_address_val,
            "city": location_data.get("city"),
            "state": location_data.get("region"),
            "country": location_data.get("country_name"),
            "latitude": location_data.get("latitude"),
            "longitude": location_data.get("longitude"),
            "pincode": location_data.get("postal"),
            "device_type": log_dict.get("device_type"),
            "platform": log_dict.get("platform"),
            "log": log_text,
        })
        doc.insert(ignore_permissions=True)

        if event_type == "View":
            current_views = frappe.db.get_value("VCard", vcard, "total_views") or 0
            frappe.db.set_value("VCard", vcard, "total_views", current_views + 1, update_modified=False)
        elif event_type == "Click":
            current_clicks = frappe.db.get_value("VCard", vcard, "total_clicks") or 0
            frappe.db.set_value("VCard", vcard, "total_clicks", current_clicks + 1, update_modified=False)

        return {"status": "success"}
    except Exception as e:
        frappe.log_error(f"Error tracking vcard event: {str(e)}", "track_vcard_event")
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def download_vcard(employee):
    if not employee:
        frappe.throw(_("Employee is required"))

    try:
        if not frappe.db.exists("VCard", employee):
            frappe.throw(_("VCard not found"), frappe.DoesNotExistError)

        vcard = frappe.get_doc("VCard", employee)
        vcf = ["BEGIN:VCARD", "VERSION:3.0"]

        first_name = vcard.first_name or vcard.full_name or "Contact"
        last_name = vcard.last_name or ""
        vcf.append(f"N:{last_name};{first_name};;;")
        vcf.append(f"FN:{vcard.full_name or first_name}")

        if vcard.company:
            vcf.append(f"ORG:{vcard.company}")
        if vcard.designation:
            vcf.append(f"TITLE:{vcard.designation}")
        if vcard.mobile_no:
            vcf.append(f"TEL;TYPE=CELL,VOICE:{vcard.mobile_no}")
        if vcard.phone:
            vcf.append(f"TEL;TYPE=WORK,VOICE:{vcard.phone}")
        if vcard.email:
            vcf.append(f"EMAIL;TYPE=WORK,INTERNET:{vcard.email}")
        if vcard.personal_email:
            vcf.append(f"EMAIL;TYPE=HOME,INTERNET:{vcard.personal_email}")
        if vcard.company_website:
            vcf.append(f"URL:{vcard.company_website}")

        vcf.append("END:VCARD")
        vcf_data = "\n".join(vcf)

        frappe.local.response.filename = f"{vcard.full_name or 'contact'}.vcf"
        frappe.local.response.filecontent = vcf_data.encode("utf-8")
        frappe.local.response.type = "download"
    except frappe.DoesNotExistError:
        raise
    except Exception as e:
        frappe.log_error(f"Error downloading vcard: {str(e)}", "download_vcard")
        frappe.throw(_("Failed to download VCard"))


def get_decrypted_doc_password(doctype, docname):
    try:
        return get_decrypted_password(doctype, docname, "password", raise_exception=False)
    except Exception:
        return None


def get_effective_page_password(page_doc, web_code=None):
    if web_code:
        customer_name = frappe.db.get_value("Hns Web Page Customer", {"web_code": web_code})
        if customer_name:
            cust_pwd = get_decrypted_doc_password("Hns Web Page Customer", customer_name)
            if cust_pwd:
                return True, cust_pwd, "customer"
        else:
            employee_name = frappe.db.get_value("Hns Web Page Employee", {"web_code": web_code})
            if employee_name:
                emp_pwd = get_decrypted_doc_password("Hns Web Page Employee", employee_name)
                if emp_pwd:
                    return True, emp_pwd, "employee"

    if page_doc and page_doc.name:
        wp_pwd = get_decrypted_doc_password("Hns Web Page Creation", page_doc.name)
        if wp_pwd:
            return True, wp_pwd, "web_page"

    return False, None, None


def fetch_page_doc(name):
    if not name:
        return None
    doc_name = frappe.db.get_value("Hns Web Page Creation", {"route": name}, "name")
    if not doc_name and frappe.db.exists("Hns Web Page Creation", name):
        doc_name = name
    if not doc_name:
        frappe.throw(_("Page not found"), frappe.DoesNotExistError)
    return frappe.get_doc("Hns Web Page Creation", doc_name)


def append_page_settings(page_data):
    try:
        settings = frappe.get_cached_doc("Hns Web Page Settings")
        page_data["content_word_limit"] = cint(settings.content_word_limit)
        page_data["content_word_mobile_factor"] = cint(settings.content_word_mobile_factor)
    except Exception as e:
        frappe.log_error(f"Error fetching web page settings: {str(e)}", "get_custom_web_pages")
        page_data["content_word_limit"] = 0
        page_data["content_word_mobile_factor"] = 0


@frappe.whitelist(allow_guest=True)
def get_custom_web_pages(name, password=None, web_code=None):
    if not name:
        return None

    try:
        doc = fetch_page_doc(name)
        is_protected, required_pwd, protection_type = get_effective_page_password(doc, web_code)

        if is_protected:
            is_authorized = bool(password and str(password).strip() == str(required_pwd).strip())
            if not is_authorized:
                response = {
                    "name": doc.name,
                    "title": doc.title or doc.name,
                    "route": doc.route,
                    "is_protected": True,
                    "is_authorized": False,
                    "protection_type": protection_type,
                }
                if password:
                    response["error"] = _("Incorrect password. Please try again.")
                return response

        page_data = doc.as_dict()
        page_data.pop("password", None)
        page_data["is_protected"] = is_protected
        page_data["is_authorized"] = True
        if is_protected:
            page_data["protection_type"] = protection_type

        append_page_settings(page_data)
        return page_data
    except frappe.DoesNotExistError:
        raise
    except Exception as e:
        frappe.log_error(f"Error fetching custom web page: {str(e)}", "get_custom_web_pages")
        frappe.throw(_("Failed to fetch web page"))


def get_party_web_doc(web_code):
    customer_name = frappe.db.get_value("Hns Web Page Customer", {"web_code": web_code})
    if customer_name:
        return frappe.get_doc("Hns Web Page Customer", customer_name), "Hns Web Page Customer"

    employee_name = frappe.db.get_value("Hns Web Page Employee", {"web_code": web_code})
    if employee_name:
        return frappe.get_doc("Hns Web Page Employee", employee_name), "Hns Web Page Employee"

    return None, None


@frappe.whitelist(allow_guest=True)
def get_web_price_list(web_code, password=None):
    try:
        if not web_code:
            return {}

        doc, doctype = get_party_web_doc(web_code)
        if not doc:
            return {}

        pwd = get_decrypted_doc_password(doctype, doc.name)
        if pwd and str(password or "").strip() != str(pwd).strip():
            return {"_is_protected": True, "_is_authorized": False}

        price_map = {}
        items = (
            doc.get("hns_price_list_details")
            or doc.get("hns_web_page_employee_details")
            or doc.get("customer_details")
            or []
        )

        for item in items:
            code = item.web_page_code or item.get("tab_code") or item.get("web_section_code")
            if not code:
                continue

            item_dict = dict(item.as_dict())
            if code not in price_map:
                price_map[code] = dict(item_dict)
                price_map[code]["child_items"] = [dict(item_dict)]
            else:
                price_map[code]["child_items"].append(dict(item_dict))

        return price_map
    except Exception as e:
        frappe.log_error(f"Error fetching web price list: {str(e)}", "get_web_price_list")
        return {}


@frappe.whitelist()
def check_python_package(package_name):
    name = (package_name or "").strip()
    if not name:
        frappe.throw(_("Package name is required"))

    result = {
        "package": name,
        "installed": False,
        "version": None,
        "error": None,
    }

    try:
        spec = importlib.util.find_spec(name)
        if spec is None:
            result["error"] = _("Module not found")
            return result

        result["installed"] = True
        try:
            result["version"] = importlib.metadata.version(name)
        except Exception:
            result["version"] = "unknown"
    except Exception as e:
        result["error"] = str(e)

    return result


@frappe.whitelist(allow_guest=True)
def submit_web_page_feedback(
    email=None, rating=None, message=None, tab_code=None, tab_title=None, web_page=None, mobile_no=None
):
    try:
        if not email:
            frappe.throw(_("Email is required"))
        if not rating:
            frappe.throw(_("Rating is required"))
        if not message:
            frappe.throw(_("Message is required"))

        try:
            numeric_rating = float(rating)
        except (ValueError, TypeError):
            frappe.throw(_("Invalid rating"))

        if numeric_rating > 1.0:
            numeric_rating = numeric_rating / 5.0
        numeric_rating = max(0.2, min(1.0, numeric_rating))

        formatted_mobile = (mobile_no or "").strip()
        if formatted_mobile and not formatted_mobile.startswith("+"):
            formatted_mobile = f"+91{formatted_mobile}"

        doc = frappe.get_doc({
            "doctype": "Hns Web Page Feedback",
            "email": email.strip(),
            "rating": numeric_rating,
            "message": message.strip(),
            "tab_code": tab_code,
            "tab_title": tab_title,
            "web_page": web_page,
            "mobile_no": formatted_mobile or None,
        })
        doc.insert(ignore_permissions=True)
        return {"status": "success", "message": _("Thank you for your feedback!")}
    except frappe.ValidationError:
        raise
    except Exception as e:
        frappe.log_error(f"Error submitting feedback: {str(e)}", "submit_web_page_feedback")
        return {"status": "error", "message": str(e)}
