import json
import importlib.metadata
import importlib.util
import frappe
from frappe import _
from frappe.utils import cint, getdate, nowdate
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
            if not employee_name:
                employee_name = frappe.db.get_value("Hns Web Page Employee", {"employee": web_code})
            if employee_name:
                emp_pwd = get_decrypted_doc_password("Hns Web Page Employee", employee_name)
                if emp_pwd:
                    return True, emp_pwd, "employee"

    if page_doc and page_doc.name:
        wp_pwd = get_decrypted_doc_password("Hns Web Page Creation", page_doc.name)
        if wp_pwd:
            return True, wp_pwd, "web_page"

    return False, None, None


def check_is_deactivated(page_doc, web_code=None):
    today = getdate(nowdate())

    if web_code:
        cust_deact = frappe.db.get_value(
            "Hns Web Page Customer",
            {"web_code": web_code},
            "deactivation_date",
        )
        if cust_deact and getdate(cust_deact) <= today:
            return True

        emp_deact = frappe.db.get_value(
            "Hns Web Page Employee",
            {"web_code": web_code},
            "deactivation_date",
        )
        if not emp_deact:
            emp_deact = frappe.db.get_value(
                "Hns Web Page Employee",
                {"employee": web_code},
                "deactivation_date",
            )
        if emp_deact and getdate(emp_deact) <= today:
            return True

    if page_doc and page_doc.deactivation_date and getdate(page_doc.deactivation_date) <= today:
        return True

    return False


def fetch_page_doc(name):
    if not name:
        return None
    doc_name = frappe.db.get_value("Hns Web Page Creation", {"route": name}, "name")
    if not doc_name and frappe.db.exists("Hns Web Page Creation", name):
        doc_name = name
    if not doc_name:
        frappe.throw(_("Page not found"), frappe.DoesNotExistError)
    return frappe.get_doc("Hns Web Page Creation", doc_name)


def get_effective_feedback_allow(page_doc, web_code=None):
    try:
        if page_doc and cint(page_doc.feedback_allow) == 1:
            return 1

        if web_code:
            cust_allow = frappe.db.get_value(
                "Hns Web Page Customer",
                {"web_code": web_code},
                "feedback_allow",
            )
            if cust_allow and cint(cust_allow) == 1:
                return 1

            emp_allow = frappe.db.get_value(
                "Hns Web Page Employee",
                {"web_code": web_code},
                "feedback_allow",
            )
            if emp_allow and cint(emp_allow) == 1:
                return 1
    except Exception as e:
        frappe.log_error(f"Error checking feedback_allow: {str(e)}", "get_effective_feedback_allow")

    return 0


def append_page_settings(page_data):
    try:
        settings = frappe.get_cached_doc("Hns Web Page Settings")
        page_data["content_word_limit"] = cint(settings.content_word_limit)
        page_data["content_word_mobile_factor"] = cint(settings.content_word_mobile_factor)
        page_data["read_more_text"] = settings.read_more_text or ""
    except Exception as e:
        frappe.log_error(f"Error fetching web page settings: {str(e)}", "get_custom_web_pages")
        page_data["content_word_limit"] = 0
        page_data["content_word_mobile_factor"] = 0
        page_data["read_more_text"] = ""


def create_web_page_session(user_doc, page_name):
    token = frappe.generate_hash(length=48)
    session_data = {
        "user_name": user_doc.user_name,
        "email": user_doc.email,
        "role": user_doc.role,
        "company": user_doc.company,
        "page_name": page_name,
    }
    frappe.cache().set_value(f"hns_session:{token}", session_data, expires_in_sec=7 * 86400)
    return token


def get_web_page_session(token):
    if not token:
        return None
    return frappe.cache().get_value(f"hns_session:{token}")


def delete_web_page_session(token):
    if not token:
        return
    frappe.cache().delete_value(f"hns_session:{token}")


@frappe.whitelist(allow_guest=True)
def logout_web_page_user(session_token=None):
    try:
        if session_token:
            delete_web_page_session(session_token)
        return {"success": True}
    except Exception as e:
        frappe.log_error(f"Error logging out user: {str(e)}", "logout_web_page_user")
        return {"success": False}


def filter_disallowed_page_groups(page_name, page_data, user_role):
    try:
        if not user_role:
            return

        disallowed_parents = frappe.get_all(
            "Hns Web Page Group Access",
            filters={
                "user_role_group": user_role,
                "parentfield": "disallowed_roles",
            },
            pluck="parent",
            distinct=True,
        )
        if not disallowed_parents:
            return

        disallowed_groups = frappe.get_all(
            "Hns Web Page Group",
            filters={
                "name": ["in", disallowed_parents],
                "web_page": page_name,
            },
            fields=["name", "group_name", "category"],
        )
        if not disallowed_groups:
            return

        disallowed_sections = set()
        disallowed_tabs = set()
        disallowed_attachments = set()

        for group in disallowed_groups:
            category = (group.category or "").strip()
            names = {group.name, group.group_name} - {None, ""}
            if category == "Section":
                disallowed_sections.update(names)
            elif category == "Tab":
                disallowed_tabs.update(names)
            elif category == "Attachment":
                disallowed_attachments.update(names)

        if disallowed_sections and page_data.section:
            filtered_sections = [
                s for s in page_data.section
                if s.section_group not in disallowed_sections
            ]
            page_data.section = filtered_sections
            page_data.sections = filtered_sections

        if disallowed_tabs and page_data.tabs:
            page_data.tabs = [
                t for t in page_data.tabs
                if t.group_name not in disallowed_tabs
            ]

        if disallowed_attachments and page_data.attachment:
            page_data.attachment = [
                a for a in page_data.attachment
                if a.group_title not in disallowed_attachments
            ]
    except Exception as e:
        frappe.log_error(f"Error filtering disallowed page groups: {str(e)}", "filter_disallowed_page_groups")


def resolve_group_display_names(page_data):
    try:
        group_ids = set()
        for sec in page_data.get("section") or []:
            if sec.get("section_group"):
                group_ids.add(sec["section_group"])
        for tab in page_data.get("tabs") or []:
            if tab.get("group_name"):
                group_ids.add(tab["group_name"])
        for att in page_data.get("attachment") or []:
            if att.get("group_title"):
                group_ids.add(att["group_title"])

        if not group_ids:
            return

        groups = frappe.get_all(
            "Hns Web Page Group",
            filters={"name": ["in", list(group_ids)]},
            fields=["name", "group_name"],
        )
        group_name_map = {g.name: g.group_name for g in groups if g.get("group_name")}

        if not group_name_map:
            return

        for sec in page_data.get("section") or []:
            if sec.get("section_group") in group_name_map:
                sec["section_group"] = group_name_map[sec["section_group"]]

        for sec in page_data.get("sections") or []:
            if sec.get("section_group") in group_name_map:
                sec["section_group"] = group_name_map[sec["section_group"]]

        for tab in page_data.get("tabs") or []:
            if tab.get("group_name") in group_name_map:
                tab["group_name"] = group_name_map[tab["group_name"]]

        for att in page_data.get("attachment") or []:
            if att.get("group_title") in group_name_map:
                att["group_title"] = group_name_map[att["group_title"]]

        page_data["group_name_map"] = group_name_map
    except Exception as e:
        frappe.log_error(f"Error resolving group display names: {str(e)}", "resolve_group_display_names")


def resolve_employee_info(web_code):
    try:
        if not web_code:
            return None, None, None

        emp_web_doc = frappe.db.get_value(
            "Hns Web Page Employee",
            {"web_code": web_code},
            ["name", "employee", "web_code"],
            as_dict=True,
        )
        if not emp_web_doc:
            emp_web_doc = frappe.db.get_value(
                "Hns Web Page Employee",
                {"employee": web_code},
                ["name", "employee", "web_code"],
                as_dict=True,
            )

        if emp_web_doc and emp_web_doc.employee:
            emp_name = frappe.db.get_value("Employee", emp_web_doc.employee, "employee_name")
            return emp_name or emp_web_doc.employee, emp_web_doc.employee, emp_web_doc.web_code

        if frappe.db.exists("Employee", web_code):
            emp_name = frappe.db.get_value("Employee", web_code, "employee_name")
            return emp_name or web_code, web_code, web_code

        return None, None, None
    except Exception as e:
        frappe.log_error(f"Error resolving employee info: {str(e)}", "resolve_employee_info")
        return None, None, None


@frappe.whitelist(allow_guest=True)
def get_custom_web_pages(name, password=None, web_code=None, username=None, session_token=None, token=None):
    if not name:
        return None

    try:
        effective_code = web_code or token
        emp_name, emp_id, emp_code = resolve_employee_info(effective_code)
        doc = fetch_page_doc(name)

        if check_is_deactivated(doc, web_code):
            return {
                "name": doc.name,
                "title": doc.title or doc.name,
                "route": doc.route,
                "is_deactivated": True,
                "deactivation_message": _(
                    "This page is currently inactive. Please contact your administrator."
                ),
                "is_protected": False,
                "is_authorized": False,
            }

        is_protected, required_pwd, protection_type = get_effective_page_password(doc, web_code)
        user_role = None
        login_user = None
        new_session_token = None

        if session_token:
            sess = get_web_page_session(session_token)
            if sess:
                user_role = sess.get("role")
                login_user = {
                    "user_name": sess.get("user_name"),
                    "email": sess.get("email"),
                    "role": user_role,
                    "company": sess.get("company"),
                }
            else:
                return {
                    "name": doc.name,
                    "title": doc.title or doc.name,
                    "route": doc.route,
                    "is_protected": True,
                    "is_authorized": False,
                    "session_expired": True,
                    "protection_type": protection_type or "user",
                }
        elif username:
            user_doc = frappe.db.get_value(
                "Hns Web Page User",
                {"email": username.strip()},
                ["name", "user_name", "email", "role", "company"],
                as_dict=True,
            )
            if not user_doc:
                user_doc = frappe.db.get_value(
                    "Hns Web Page User",
                    {"user_name": username.strip()},
                    ["name", "user_name", "email", "role", "company"],
                    as_dict=True,
                )

            if not user_doc:
                return {
                    "name": doc.name,
                    "title": doc.title or doc.name,
                    "route": doc.route,
                    "is_protected": True,
                    "is_authorized": False,
                    "protection_type": protection_type or "user",
                    "error": _("User does not exist."),
                }

            user_pwd = get_decrypted_doc_password("Hns Web Page User", user_doc["name"])
            if not user_pwd or str(password).strip() != str(user_pwd).strip():
                return {
                    "name": doc.name,
                    "title": doc.title or doc.name,
                    "route": doc.route,
                    "is_protected": True,
                    "is_authorized": False,
                    "protection_type": protection_type or "user",
                    "error": _("Password does not match."),
                }

            user_role = user_doc.role
            login_user = {
                "user_name": user_doc.user_name,
                "email": user_doc.email,
                "role": user_role,
                "company": user_doc.company,
            }
            new_session_token = create_web_page_session(user_doc, doc.name)
        elif is_protected:
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
                if emp_name:
                    response["employee_name"] = emp_name
                    response["employee"] = emp_id
                    response["employee_code"] = emp_code
                if password:
                    response["error"] = _("Password does not match.")
                return response

        page_data = doc.as_dict()
        page_data.pop("password", None)
        if "section" in page_data and "sections" not in page_data:
            page_data["sections"] = page_data["section"]
        page_data["is_protected"] = is_protected or bool(username) or bool(session_token)
        page_data["is_authorized"] = True
        if is_protected:
            page_data["protection_type"] = protection_type
        page_data["feedback_allow"] = get_effective_feedback_allow(doc, web_code)
        if login_user:
            page_data["login_user"] = login_user
        if new_session_token:
            page_data["session_token"] = new_session_token
        elif session_token:
            page_data["session_token"] = session_token

        if user_role:
            filter_disallowed_page_groups(doc.name, page_data, user_role)

        resolve_group_display_names(page_data)

        if not page_data.get("group_title_color"):
            page_data["group_title_color"] = "#1e3a8a"
        if not page_data.get("sub_group_title_color"):
            page_data["sub_group_title_color"] = "#118ab2"

        if emp_name:
            page_data["employee_name"] = emp_name
            page_data["employee"] = emp_id
            page_data["employee_code"] = emp_code

        append_page_settings(page_data)
        return page_data
    except frappe.DoesNotExistError:
        raise
    except Exception as e:
        frappe.log_error(f"Error fetching custom web page: {str(e)}", "get_custom_web_pages")
        frappe.throw(_("Failed to fetch web page"))


def get_party_web_doc(web_code):
    customer_name = frappe.db.get_value("Hns Web Page Customer", {"web_code": web_code})
    if not customer_name:
        customer_name = frappe.db.get_value("Hns Web Page Customer", {"party_name": web_code})
    if customer_name:
        return frappe.get_doc("Hns Web Page Customer", customer_name), "Hns Web Page Customer"

    employee_name = frappe.db.get_value("Hns Web Page Employee", {"web_code": web_code})
    if not employee_name:
        employee_name = frappe.db.get_value("Hns Web Page Employee", {"employee": web_code})
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

        if doc.deactivation_date and getdate(doc.deactivation_date) <= getdate(nowdate()):
            return {"_is_deactivated": True, "_is_authorized": False}

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

        if doctype == "Hns Web Page Employee" and doc.employee:
            emp_name = frappe.db.get_value("Employee", doc.employee, "employee_name")
            price_map["_employee_name"] = emp_name or doc.employee
            price_map["_employee"] = doc.employee
            price_map["_employee_code"] = doc.web_code

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

@frappe.whitelist(allow_guest=True)
def get_user_feedback_history(email, web_page=None, tab_code=None):
    try:
        clean_email = (email or "").strip()
        if not clean_email:
            return []

        filters = {"email": clean_email}
        if web_page:
            filters["web_page"] = web_page
        if tab_code:
            filters["tab_code"] = tab_code

        feedbacks = frappe.db.get_all(
            "Hns Web Page Feedback",
            filters=filters,
            fields=[
                "name",
                "email",
                "mobile_no",
                "rating",
                "message",
                "reply",
                "creation",
                "modified",
                "tab_code",
                "tab_title",
                "web_page",
            ],
            order_by="creation desc",
            limit=50,
        )

        for fb in feedbacks:
            raw_rating = fb.get("rating") or 0.0
            stars = int(round(float(raw_rating) * 5.0)) if raw_rating <= 1.0 else int(round(float(raw_rating)))
            fb["stars"] = max(1, min(5, stars))
            if fb.get("creation"):
                fb["formatted_date"] = frappe.utils.format_datetime(fb["creation"], "dd MMM yyyy, hh:mm a")
            if fb.get("modified") and fb.get("reply"):
                fb["formatted_reply_date"] = frappe.utils.format_datetime(fb["modified"], "dd MMM yyyy, hh:mm a")

        return feedbacks
    except Exception as e:
        frappe.log_error(f"Error fetching user feedback history: {str(e)}", "get_user_feedback_history")
        return []

