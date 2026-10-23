import json
import urllib.parse
import importlib.metadata
import importlib.util
import frappe
from frappe import _
from frappe.utils import cint, getdate, nowdate, now_datetime
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


def resolve_party_by_web_code(web_code):
    try:
        if not web_code:
            return None, None

        cleaned_code = str(web_code).strip()
        if not cleaned_code:
            return None, None

        cust_match = frappe.db.get_value("Hns Web Page Customer", {"web_code": cleaned_code}, "name")
        if not cust_match and frappe.db.exists("Hns Web Page Customer", cleaned_code):
            cust_match = cleaned_code
        if not cust_match:
            cust_match = frappe.db.get_value("Hns Web Page Customer", {"party_name": cleaned_code}, "name")

        if cust_match:
            return cust_match, None

        emp_match = frappe.db.get_value("Hns Web Page Employee", {"web_code": cleaned_code}, "name")
        if not emp_match and frappe.db.exists("Hns Web Page Employee", cleaned_code):
            emp_match = cleaned_code
        if not emp_match:
            emp_match = frappe.db.get_value("Hns Web Page Employee", {"employee": cleaned_code}, "name")

        if emp_match:
            return None, emp_match

        return None, None
    except Exception as e:
        frappe.log_error(f"Error resolving party by web code: {str(e)}", "resolve_party_by_web_code")
        return None, None


def extract_web_code_from_url(url):
    try:
        if not url:
            return None
        parsed = urllib.parse.urlparse(str(url))
        qs = urllib.parse.parse_qs(parsed.query)
        for key in ["web_code", "token"]:
            val = qs.get(key)
            if val and val[0]:
                return val[0].strip()
        if parsed.fragment and "?" in parsed.fragment:
            frag_qs = urllib.parse.parse_qs(parsed.fragment.split("?", 1)[1])
            for key in ["web_code", "token"]:
                val = frag_qs.get(key)
                if val and val[0]:
                    return val[0].strip()
        return None
    except Exception:
        return None


def log_web_page_activity(
    web_page=None,
    section=None,
    tab=None,
    attachment=None,
    event_type="Feedback",
    log=None,
    session_token=None,
    user=None,
    web_code=None,
    customer=None,
    employee=None,
):
    try:
        log_dict, log_text = parse_event_log(log)
        location_data = log_dict.get("location") if isinstance(log_dict.get("location"), dict) else {}
        user_agent_val = log_dict.get("userAgent") or (frappe.request.environ.get("HTTP_USER_AGENT", "") if frappe.request else "")
        ip_address_val = location_data.get("ip") or frappe.local.request_ip

        eff_session_token = session_token or log_dict.get("session_token")
        if not eff_session_token and frappe.request:
            eff_session_token = frappe.request.headers.get("X-Session-Token") or frappe.request.cookies.get("session_token")

        user_link = None
        if eff_session_token:
            sess = get_web_page_session(eff_session_token)
            if sess:
                candidate = sess.get("user")
                if candidate and frappe.db.exists("Hns Web Page User", candidate):
                    user_link = candidate
                elif sess.get("email"):
                    user_link = frappe.db.get_value("Hns Web Page User", {"email": sess.get("email")}, "name")
                elif sess.get("user_name"):
                    user_link = frappe.db.get_value("Hns Web Page User", {"user_name": sess.get("user_name")}, "name")
                elif candidate:
                    user_link = (
                        frappe.db.get_value("Hns Web Page User", {"email": candidate}, "name")
                        or frappe.db.get_value("Hns Web Page User", {"user_name": candidate}, "name")
                    )

        if not user_link:
            candidate_user = user or log_dict.get("user") or log_dict.get("username") or log_dict.get("email")
            if candidate_user:
                candidate_user = str(candidate_user).strip()
                if frappe.db.exists("Hns Web Page User", candidate_user):
                    user_link = candidate_user
                else:
                    user_link = (
                        frappe.db.get_value("Hns Web Page User", {"email": candidate_user}, "name")
                        or frappe.db.get_value("Hns Web Page User", {"user_name": candidate_user}, "name")
                    )

        eff_web_code = web_code or log_dict.get("web_code")
        if not eff_web_code and frappe.form_dict:
            eff_web_code = (
                frappe.form_dict.get("web_code")
                or frappe.form_dict.get("token")
            )
        if not eff_web_code and log_dict.get("url"):
            eff_web_code = extract_web_code_from_url(log_dict.get("url"))
        if not eff_web_code and frappe.request:
            eff_web_code = (
                extract_web_code_from_url(frappe.request.environ.get("HTTP_REFERER"))
                or extract_web_code_from_url(frappe.request.environ.get("REQUEST_URI"))
            )

        resolved_customer = customer or log_dict.get("customer") or frappe.form_dict.get("customer")
        resolved_employee = employee or log_dict.get("employee") or frappe.form_dict.get("employee")

        if eff_web_code:
            party_cust, party_emp = resolve_party_by_web_code(eff_web_code)
            if not resolved_customer and party_cust:
                resolved_customer = party_cust
            if not resolved_employee and party_emp:
                resolved_employee = party_emp

        if resolved_customer and not frappe.db.exists("Hns Web Page Customer", resolved_customer):
            resolved_customer = (
                frappe.db.get_value("Hns Web Page Customer", {"web_code": str(resolved_customer).strip()}, "name")
                or frappe.db.get_value("Hns Web Page Customer", {"party_name": str(resolved_customer).strip()}, "name")
            )

        if resolved_employee and not frappe.db.exists("Hns Web Page Employee", resolved_employee):
            resolved_employee = (
                frappe.db.get_value("Hns Web Page Employee", {"web_code": str(resolved_employee).strip()}, "name")
                or frappe.db.get_value("Hns Web Page Employee", {"employee": str(resolved_employee).strip()}, "name")
            )

        if event_type == "Logout":
            recent_time = frappe.utils.add_to_date(now_datetime(), seconds=-10)
            filters = {
                "web_page": web_page,
                "event_type": "Logout",
                "creation": [">=", recent_time],
            }
            if user_link:
                filters["user"] = user_link
            elif ip_address_val:
                filters["ip_address"] = ip_address_val
            if resolved_customer:
                filters["customer"] = resolved_customer
            if resolved_employee:
                filters["employee"] = resolved_employee

            if frappe.db.exists("Hns Web Page Activity", filters):
                return {"status": "ignored", "message": "Logout already recorded recently"}

        if event_type == "View":
            today_date = frappe.utils.today()
            filters = {
                "web_page": web_page,
                "event_type": "View",
                "creation": [">=", today_date],
            }
            if user_link:
                filters["user"] = user_link
            elif ip_address_val:
                filters["ip_address"] = ip_address_val
            elif user_agent_val:
                filters["user_agent"] = user_agent_val
            if resolved_customer:
                filters["customer"] = resolved_customer
            if resolved_employee:
                filters["employee"] = resolved_employee

            if frappe.db.exists("Hns Web Page Activity", filters):
                return {"status": "ignored", "message": "View already recorded today"}

        if event_type == "Login":
            recent_time = frappe.utils.add_to_date(now_datetime(), seconds=-10)
            filters = {
                "web_page": web_page,
                "event_type": "Login",
                "creation": [">=", recent_time],
            }
            if user_link:
                filters["user"] = user_link
            elif ip_address_val:
                filters["ip_address"] = ip_address_val
            if resolved_customer:
                filters["customer"] = resolved_customer
            if resolved_employee:
                filters["employee"] = resolved_employee

            if frappe.db.exists("Hns Web Page Activity", filters):
                return {"status": "ignored", "message": "Login already recorded recently"}

        resolved_web_page = web_page
        if web_page:
            wp_title = frappe.db.get_value("Hns Web Page Creation", {"route": web_page}, "title")
            if not wp_title:
                wp_title = frappe.db.get_value("Hns Web Page Creation", web_page, "title")
            if wp_title:
                resolved_web_page = wp_title

        resolved_tab = tab
        if tab:
            t_title = frappe.db.get_value("Hns Web Page Tab Details", {"tab_code": tab}, "page_title")
            if not t_title:
                t_title = frappe.db.get_value("Hns Web Page Tab Details", tab, "page_title")
            if t_title:
                resolved_tab = t_title

        resolved_section = section
        if section:
            s_title = frappe.db.get_value("Hns Web Page Section Details", {"section_code": section}, "page_title")
            if not s_title:
                s_title = frappe.db.get_value("Hns Web Page Section Details", section, "page_title")
            if not s_title:
                s_title = frappe.db.get_value("Hns Web Page Group", section, "group_name")
            if s_title:
                resolved_section = s_title

        activity_data = {
            "doctype": "Hns Web Page Activity",
            "web_page": resolved_web_page,
            "section": resolved_section,
            "tab": resolved_tab,
            "attachment": attachment,
            "event_type": event_type,
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
        }
        if user_link and frappe.db.exists("Hns Web Page User", user_link):
            activity_data["user"] = user_link
        if resolved_customer and frappe.db.exists("Hns Web Page Customer", resolved_customer):
            activity_data["customer"] = resolved_customer
        if resolved_employee and frappe.db.exists("Hns Web Page Employee", resolved_employee):
            activity_data["employee"] = resolved_employee

        doc = frappe.get_doc(activity_data)
        doc.insert(ignore_permissions=True)
        return {"status": "success", "name": doc.name}
    except Exception as e:
        frappe.log_error(f"Error logging web page activity: {str(e)}", "log_web_page_activity")
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def track_web_page_activity(
    web_page=None,
    section=None,
    tab=None,
    attachment=None,
    event_type="Feedback",
    log=None,
    session_token=None,
    user=None,
    web_code=None,
    customer=None,
    employee=None,
):
    try:
        eff_web_code = web_code or frappe.form_dict.get("web_code")
        eff_customer = customer or frappe.form_dict.get("customer")
        eff_employee = employee or frappe.form_dict.get("employee")
        return log_web_page_activity(
            web_page=web_page,
            section=section,
            tab=tab,
            attachment=attachment,
            event_type=event_type,
            log=log,
            session_token=session_token,
            user=user,
            web_code=eff_web_code,
            customer=eff_customer,
            employee=eff_employee,
        )
    except Exception as e:
        frappe.log_error(f"Error in track_web_page_activity: {str(e)}", "track_web_page_activity")
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
    try:
        if not page_doc or not page_doc.name:
            return False, None, None

        if web_code:
            for doctype, ptype in (("Hns Web Page Customer", "customer"), ("Hns Web Page Employee", "employee")):
                party = frappe.db.get_value(doctype, {"web_code": web_code}, ["name", "select_portal"], as_dict=True)
                if party and (not party.select_portal or party.select_portal == page_doc.name):
                    pwd = get_decrypted_doc_password(doctype, party.name)
                    if pwd:
                        return True, pwd, ptype

        wp_pwd = get_decrypted_doc_password("Hns Web Page Creation", page_doc.name)
        if wp_pwd:
            return True, wp_pwd, "web_page"

        return False, None, None
    except Exception as e:
        frappe.log_error(f"Error fetching page password: {str(e)}", "get_effective_page_password")
        return False, None, None


def check_is_deactivated(page_doc, web_code=None):
    try:
        today = getdate(nowdate())

        if web_code and page_doc and page_doc.name:
            cust = frappe.db.get_value(
                "Hns Web Page Customer",
                {"web_code": web_code},
                ["name", "select_portal", "deactivation_date"],
                as_dict=True,
            )
            if cust and cust.select_portal == page_doc.name and cust.deactivation_date and getdate(cust.deactivation_date) <= today:
                return True

            emp = frappe.db.get_value(
                "Hns Web Page Employee",
                {"web_code": web_code},
                ["name", "select_portal", "deactivation_date"],
                as_dict=True,
            )
            if emp and emp.select_portal == page_doc.name and emp.deactivation_date and getdate(emp.deactivation_date) <= today:
                return True

        if page_doc and page_doc.deactivation_date and getdate(page_doc.deactivation_date) <= today:
            return True

        return False
    except Exception as e:
        frappe.log_error(f"Error checking deactivation: {str(e)}", "check_is_deactivated")
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
        if not page_doc:
            return 0
        return 1 if cint(page_doc.feedback_allow) else 0
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


def resolve_request_session_token(session_token=None):
    try:
        if session_token:
            return session_token
        if frappe.request:
            token = (
                frappe.request.headers.get("X-Session-Token")
                or frappe.request.cookies.get("hns_session_token")
            )
            if token:
                return token
        return None
    except Exception as e:
        frappe.log_error(f"Error resolving session token: {str(e)}", "resolve_request_session_token")
        return None


def resolve_active_web_session(session_token=None):
    try:
        token = resolve_request_session_token(session_token)
        if not token:
            return None, None, None, False

        sess = get_web_page_session(token)
        if sess:
            login_user = {
                "user_name": sess.get("user_name"),
                "email": sess.get("email"),
                "role": sess.get("role"),
                "company": sess.get("company"),
                "party_doctype": sess.get("party_doctype"),
                "party_name": sess.get("party_name"),
            }
            return token, sess.get("role"), login_user, False

        return token, None, None, True
    except Exception as e:
        frappe.log_error(f"Error resolving active web session: {str(e)}", "resolve_active_web_session")
        return None, None, None, False


@frappe.whitelist(allow_guest=True)
def check_web_page_session(session_token=None):
    try:
        active_token, role, login_user, is_expired = resolve_active_web_session(session_token)
        if active_token and login_user:
            return {
                "logged_in": True,
                "session_token": active_token,
                "role": role,
                "user": login_user,
            }
        return {"logged_in": False, "session_expired": is_expired}
    except Exception as e:
        frappe.log_error(f"Error checking web page session: {str(e)}", "check_web_page_session")
        return {"logged_in": False}


def create_web_page_session(user_doc, page_name=None):
    token = frappe.generate_hash(length=48)
    user_id = user_doc.get("name")
    session_data = {
        "user": user_id,
        "user_name": user_doc.get("user_name"),
        "email": user_doc.get("email"),
        "role": user_doc.get("role"),
        "company": user_doc.get("company"),
        "party_doctype": user_doc.get("party_doctype"),
        "party_name": user_doc.get("party_name"),
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
def logout_web_page_user(
    session_token=None,
    web_page=None,
    user=None,
    log=None,
    web_code=None,
    customer=None,
    employee=None,
):
    try:
        eff_token = session_token or resolve_request_session_token()
        if not eff_token:
            eff_token = frappe.form_dict.get("session_token")
        if not web_page:
            web_page = frappe.form_dict.get("web_page")
        if not user:
            user = frappe.form_dict.get("user")
        if not log:
            log = frappe.form_dict.get("log")
        eff_web_code = web_code or frappe.form_dict.get("web_code")
        eff_customer = customer or frappe.form_dict.get("customer")
        eff_employee = employee or frappe.form_dict.get("employee")

        page_name = web_page
        user_id = user

        if eff_token:
            sess = get_web_page_session(eff_token)
            if sess:
                if not page_name:
                    page_name = sess.get("page_name")
                if not user_id:
                    user_id = sess.get("user")
                if not user_id and sess.get("email"):
                    user_id = frappe.db.get_value("Hns Web Page User", {"email": sess.get("email")}, "name")
            delete_web_page_session(eff_token)

        try:
            frappe.local.cookie_manager.delete_cookie("hns_session_token")
        except Exception:
            pass

        log_web_page_activity(
            web_page=page_name,
            event_type="Logout",
            user=user_id,
            session_token=eff_token,
            log=log,
            web_code=eff_web_code,
            customer=eff_customer,
            employee=eff_employee,
        )
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
            },
            fields=["name", "group_name", "category", "web_page", "is_generic"],
        )
        disallowed_groups = [
            g for g in disallowed_groups
            if g.is_generic or g.web_page == page_name
        ]
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

        if page_data.section:
            filtered_sections = []
            for s in page_data.section:
                if s.is_tab_section:
                    if disallowed_tabs and s.tab_group in disallowed_tabs:
                        continue
                elif s.is_attachment_section:
                    if disallowed_attachments and s.attachment_group in disallowed_attachments:
                        continue
                else:
                    if disallowed_sections and s.section_group in disallowed_sections:
                        continue
                filtered_sections.append(s)
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
            if sec.get("tab_group"):
                group_ids.add(sec["tab_group"])
            if sec.get("attachment_group"):
                group_ids.add(sec["attachment_group"])
        for tab in page_data.get("tabs") or []:
            if tab.get("group_name"):
                group_ids.add(tab["group_name"])
        for att in page_data.get("attachment") or []:
            if att.get("group_title"):
                group_ids.add(att["group_title"])

        page_name = page_data.get("name")
        page_title = page_data.get("title")

        groups = []
        if group_ids:
            groups = frappe.get_all(
                "Hns Web Page Group",
                filters={"name": ["in", list(group_ids)]},
                fields=["name", "group_name", "sort_order", "category"],
            )

        page_keys = [k for k in [page_name, page_title] if k]
        if page_keys:
            extra_groups = frappe.get_all(
                "Hns Web Page Group",
                filters={"web_page": ["in", page_keys]},
                fields=["name", "group_name", "sort_order", "category"],
            )
            existing_names = {g.name for g in groups}
            for eg in extra_groups:
                if eg.name not in existing_names:
                    groups.append(eg)

        group_name_map = {g.name: g.group_name for g in groups if g.get("group_name")}
        group_sort_order_map = {}
        section_group_sort_order_map = {}
        tab_group_sort_order_map = {}
        attachment_group_sort_order_map = {}

        for g in groups:
            so = int(g.get("sort_order") or 0)
            cat = (g.get("category") or "").strip().lower()
            group_sort_order_map[g.name] = so
            if g.get("group_name"):
                group_sort_order_map[g.group_name] = so

            if cat == "section":
                section_group_sort_order_map[g.name] = so
                if g.get("group_name"):
                    section_group_sort_order_map[g.group_name] = so
            elif cat == "tab":
                tab_group_sort_order_map[g.name] = so
                if g.get("group_name"):
                    tab_group_sort_order_map[g.group_name] = so
            elif cat == "attachment":
                attachment_group_sort_order_map[g.name] = so
                if g.get("group_name"):
                    attachment_group_sort_order_map[g.group_name] = so

        for sec in page_data.get("section") or []:
            raw_grp = sec.get("section_group") or sec.get("tab_group") or sec.get("attachment_group")
            if raw_grp:
                sec["group_sort_order"] = group_sort_order_map.get(raw_grp, 0)
            if sec.get("section_group") in group_name_map:
                sec["raw_section_group"] = sec["section_group"]
                sec["section_group"] = group_name_map[sec["section_group"]]
            if sec.get("tab_group") in group_name_map:
                sec["raw_tab_group"] = sec["tab_group"]
                sec["tab_group"] = group_name_map[sec["tab_group"]]
            if sec.get("attachment_group") in group_name_map:
                sec["raw_attachment_group"] = sec["attachment_group"]
                sec["attachment_group"] = group_name_map[sec["attachment_group"]]

        for tab in page_data.get("tabs") or []:
            if tab.get("group_name"):
                tab["group_sort_order"] = tab_group_sort_order_map.get(tab.get("group_name"), 0)
            if tab.get("group_name") in group_name_map:
                tab["raw_group_name"] = tab["group_name"]
                tab["group_name"] = group_name_map[tab["group_name"]]

        for att in page_data.get("attachment") or []:
            if att.get("group_title"):
                att["group_sort_order"] = attachment_group_sort_order_map.get(att.get("group_title"), 0)
            if att.get("group_title") in group_name_map:
                att["raw_group_title"] = att["group_title"]
                att["group_title"] = group_name_map[att["group_title"]]

        page_data["group_name_map"] = group_name_map
        page_data["group_sort_order_map"] = group_sort_order_map
        page_data["section_group_sort_order_map"] = section_group_sort_order_map
        page_data["tab_group_sort_order_map"] = tab_group_sort_order_map
        page_data["attachment_group_sort_order_map"] = attachment_group_sort_order_map
        page_data["groups_meta"] = [
            {
                "name": g.name,
                "group_name": g.group_name,
                "sort_order": int(g.get("sort_order") or 0),
                "category": g.get("category"),
            }
            for g in groups
        ]
    except Exception as e:
        frappe.log_error(f"Error resolving group display names: {str(e)}", "resolve_group_display_names")


def resolve_customer_info(web_code):
    try:
        if not web_code:
            return None
        return frappe.db.get_value("Hns Web Page Customer", {"web_code": str(web_code).strip()}, "party_name")
    except Exception as e:
        frappe.log_error(f"Error resolving customer info: {str(e)}", "resolve_customer_info")
        return None


def resolve_employee_info(web_code):
    try:
        if not web_code:
            return None
        return frappe.db.get_value("Hns Web Page Employee", {"web_code": str(web_code).strip()}, "employee_name")
    except Exception as e:
        frappe.log_error(f"Error resolving employee info: {str(e)}", "resolve_employee_info")
        return None


def get_base_page_response(doc, **kwargs):
    response = {
        "name": doc.name,
        "title": doc.title or doc.name,
        "route": doc.route,
        "is_protected": False,
        "is_authorized": False,
    }
    response.update(kwargs)
    return response


def append_party_info(data, effective_code, web_code=None):
    if not data:
        return
    emp_name = resolve_employee_info(effective_code)
    cust_name = resolve_customer_info(effective_code)
    if emp_name:
        data["employee_name"] = emp_name
    if cust_name:
        data["customer_name"] = cust_name
    if web_code:
        data["web_code"] = web_code


def start_user_session(user_data, page_name):
    token = create_web_page_session(user_data, page_name)
    user_dict = {
        "user_name": user_data.user_name,
        "email": user_data.email,
        "role": user_data.role,
        "company": user_data.company,
        "party_doctype": user_data.get("party_doctype"),
        "party_name": user_data.get("party_name"),
    }
    return user_dict, token


def authenticate_web_page_user(username, password):
    if not username or not password:
        return None
    user = frappe.db.get_value(
        "Hns Web Page User",
        {"email": username},
        ["name", "user_name", "email", "role", "company"],
        as_dict=True,
    ) or frappe.db.get_value(
        "Hns Web Page User",
        {"user_name": username},
        ["name", "user_name", "email", "role", "company"],
        as_dict=True,
    )
    if user:
        pwd = get_decrypted_doc_password("Hns Web Page User", user.name)
        if pwd and password == str(pwd).strip():
            return user
    return None


def authenticate_customer(page_name, web_code, username, password):
    if not password or not web_code:
        return None
    cust = frappe.db.get_value(
        "Hns Web Page Customer",
        {"web_code": web_code},
        ["name", "party_name"],
        as_dict=True,
    )
    if cust:
        pwd = get_decrypted_doc_password("Hns Web Page Customer", cust.name)
        if pwd and password == str(pwd).strip():
            return frappe._dict(
                user_name=cust.party_name or username,
                email="",
                role=None,
                company=None,
                party_doctype="Hns Web Page Customer",
                party_name=cust.name,
            )
    return None


def authenticate_employee(page_name, web_code, username, password):
    if not password or not web_code:
        return None
    emp = frappe.db.get_value(
        "Hns Web Page Employee",
        {"web_code": web_code},
        ["name", "employee", "employee_name"],
        as_dict=True,
    )
    if emp:
        pwd = get_decrypted_doc_password("Hns Web Page Employee", emp.name)
        if pwd and password == str(pwd).strip():
            return frappe._dict(
                user_name=emp.employee_name or emp.employee or username,
                email="",
                role=None,
                company=None,
                party_doctype="Hns Web Page Employee",
                party_name=emp.name,
            )
    return None


def authenticate_page(page_name, username, password):
    if not page_name or not password:
        return None
    pwd = get_decrypted_doc_password("Hns Web Page Creation", page_name)
    if pwd and password == str(pwd).strip():
        return frappe._dict(
            user_name=username or "Portal User",
            email=username if "@" in (username or "") else "",
            role=None,
            company=None,
        )
    return None


def check_page_authorization(doc, password, username, session_token, effective_code=None, web_code=None):
    try:
        is_protected, required_pwd, protection_type = get_effective_page_password(doc, web_code)
        active_token, role, login_user, is_expired = resolve_active_web_session(session_token)

        if not is_protected:
            res = {"authorized": True, "is_protected": False}
            if active_token and login_user:
                res["login_user"] = login_user
                res["session_token"] = active_token
            return res

        def build_auth_error(error_msg=None, session_expired=False):
            err = get_base_page_response(
                doc,
                is_protected=True,
                protection_type=protection_type or "user",
                session_expired=session_expired,
                error=error_msg,
            )
            append_party_info(err, effective_code, web_code)
            return {"authorized": False, "error_response": err}

        # 1. Authorize active session if valid
        if active_token and login_user and not is_expired:
            session_valid = True
            if protection_type == "customer":
                cust_name = frappe.db.get_value("Hns Web Page Customer", {"web_code": effective_code}, "name")
                if login_user.get("party_doctype") == "Hns Web Page Customer":
                    if cust_name and login_user.get("party_name") and login_user.get("party_name") != cust_name:
                        session_valid = False
                elif not login_user.get("user_name"):
                    session_valid = False
            elif protection_type == "employee":
                emp_name = frappe.db.get_value("Hns Web Page Employee", {"web_code": effective_code}, "name")
                if login_user.get("party_doctype") == "Hns Web Page Employee":
                    if emp_name and login_user.get("party_name") and login_user.get("party_name") != emp_name:
                        session_valid = False
                elif not login_user.get("user_name"):
                    session_valid = False

            if session_valid:
                return {
                    "authorized": True,
                    "is_protected": True,
                    "protection_type": protection_type or "user",
                    "login_user": login_user,
                    "session_token": active_token,
                }

        clean_pwd = str(password).strip() if password else ""
        clean_user = str(username).strip() if username else ""

        # 2. If session expired but password provided, allow seamless password auth instead of blocking
        if is_expired and not clean_pwd:
            return build_auth_error(session_expired=True)

        if not clean_pwd:
            return build_auth_error()

        user_data = None
        ptype = protection_type or "user"

        if protection_type == "customer":
            user_data = authenticate_customer(doc.name, effective_code, clean_user, clean_pwd)
        elif protection_type == "employee":
            user_data = authenticate_employee(doc.name, effective_code, clean_user, clean_pwd)
        else:
            if clean_user:
                user_data = authenticate_web_page_user(clean_user, clean_pwd)
                ptype = "user"
            if not user_data:
                user_data = authenticate_page(doc.name, clean_user, clean_pwd)
                ptype = "web_page"

        if user_data:
            if active_token and login_user:
                token = active_token
            else:
                login_user, token = start_user_session(user_data, doc.name)
            return {
                "authorized": True,
                "is_protected": True,
                "protection_type": ptype,
                "login_user": login_user,
                "session_token": token,
            }

        return build_auth_error(error_msg=_("Password does not match."))

    except Exception as e:
        frappe.log_error(f"Error checking page authorization: {str(e)}", "check_page_authorization")
        err = get_base_page_response(doc, is_protected=True, error=_("Authentication failed."))
        append_party_info(err, effective_code, web_code)
        return {"authorized": False, "error_response": err}


@frappe.whitelist(allow_guest=True)
def get_custom_web_pages(name, password=None, web_code=None, username=None, session_token=None, token=None):
    if not name:
        return None

    try:
        effective_code = web_code or token
        doc = fetch_page_doc(name)

        if check_is_deactivated(doc, web_code):
            return get_base_page_response(
                doc,
                is_deactivated=True,
                deactivation_message=_(
                    "This page is currently inactive. Please contact your administrator."
                ),
            )

        auth = check_page_authorization(doc, password, username, session_token, effective_code, web_code)
        if not auth.get("authorized"):
            return auth.get("error_response")

        page_data = doc.as_dict()
        page_data.pop("password", None)
        if "section" in page_data and "sections" not in page_data:
            page_data["sections"] = page_data["section"]

        page_data["is_protected"] = bool(auth.get("is_protected"))
        page_data["is_authorized"] = True
        if auth.get("protection_type"):
            page_data["protection_type"] = auth["protection_type"]

        page_data["feedback_allow"] = get_effective_feedback_allow(doc, effective_code)

        active_token = auth.get("session_token")
        if active_token:
            page_data["session_token"] = active_token
            try:
                frappe.local.cookie_manager.set_cookie("hns_session_token", active_token, max_age=7 * 86400)
            except Exception:
                pass

        login_user = auth.get("login_user")
        if login_user:
            page_data["login_user"] = login_user
            if login_user.get("role"):
                filter_disallowed_page_groups(doc.name, page_data, login_user["role"])

        resolve_group_display_names(page_data)

        if not page_data.get("group_title_color"):
            page_data["group_title_color"] = "#1e3a8a"
        if not page_data.get("sub_group_title_color"):
            page_data["sub_group_title_color"] = "#118ab2"

        append_party_info(page_data, effective_code, web_code)

        doc_party = None
        doctype_party = None
        if effective_code:
            doc_party, doctype_party = get_party_web_doc(effective_code)
        elif login_user and login_user.get("party_doctype") and login_user.get("party_name"):
            doc_party = frappe.get_doc(login_user["party_doctype"], login_user["party_name"])
            doctype_party = login_user["party_doctype"]

        if doc_party:
            page_data["price_list"] = build_price_map(doc_party, doctype_party)
            if not doc_party.show_complete_portal:
                filter_party_portal_items(page_data, doc_party)

        append_page_settings(page_data)
        return page_data
    except frappe.DoesNotExistError:
        raise
    except Exception as e:
        frappe.log_error(f"Error fetching custom web page: {str(e)}", "get_custom_web_pages")
        frappe.throw(_("Failed to fetch web page"))


def get_code_variants(code):
    variants = set()
    if not code:
        return variants
    clean = str(code).strip().lower()
    variants.add(clean)
    variants.add(clean.replace(" ", "_"))
    variants.add(clean.replace("_", " "))
    variants.add(clean.replace("-", "_"))
    variants.add(clean.replace(" ", ""))
    return variants


def get_portal_item_identifiers(item, code_field):
    ids = set()
    for key in [code_field, "name", "page_title"]:
        val = item.get(key)
        if val:
            clean = str(val).strip().lower()
            ids.add(clean)
            ids.add(clean.replace(" ", "_"))
            ids.add(clean.replace("_", " "))
            ids.add(clean.replace("-", "_"))
            ids.add(clean.replace(" ", ""))
    title = item.get("page_title")
    if title:
        try:
            scrubbed = frappe.scrub(title).strip().lower()
            ids.add(scrubbed)
            ids.add(scrubbed.replace("_", " "))
        except Exception:
            pass
    return ids


def filter_party_portal_items(page_data, doc_party):
    try:
        if not doc_party or doc_party.show_complete_portal:
            return

        child_items = (
            doc_party.get("hns_price_list_details")
            or doc_party.get("hns_web_page_employee_details")
            or doc_party.get("customer_details")
            or []
        )

        allowed_section_codes = set()
        allowed_tab_codes = set()
        allowed_attachment_codes = set()

        for row in child_items:
            code = row.get("web_page_code") or row.get("tab_code") or row.get("item")
            code_type = row.get("web_page_code_type")

            if code:
                variants = get_code_variants(code)
                if code_type == "Section":
                    allowed_section_codes.update(variants)
                elif code_type == "Tab":
                    allowed_tab_codes.update(variants)
                elif code_type == "Attachment":
                    allowed_attachment_codes.update(variants)
                else:
                    allowed_section_codes.update(variants)
                    allowed_tab_codes.update(variants)
                    allowed_attachment_codes.update(variants)

        # 1. Filter sections
        if page_data.get("section"):
            filtered_sections = []
            for s in page_data["section"]:
                is_tab_sec = bool(s.get("is_tab_section"))
                is_att_sec = bool(s.get("is_attachment_section"))

                if not is_tab_sec and not is_att_sec:
                    s_ids = get_portal_item_identifiers(s, "section_code")
                    if s_ids & allowed_section_codes:
                        filtered_sections.append(s)
                elif is_tab_sec:
                    t_code = s.get("tab_code") or s.get("section_code")
                    if allowed_tab_codes and (get_code_variants(t_code) & allowed_tab_codes):
                        filtered_sections.append(s)
                elif is_att_sec:
                    if allowed_attachment_codes:
                        filtered_sections.append(s)

            page_data["section"] = filtered_sections
            page_data["sections"] = filtered_sections

        # 2. Filter tabs
        if page_data.get("tabs"):
            filtered_tabs = []
            if allowed_tab_codes:
                for t in page_data["tabs"]:
                    t_ids = get_portal_item_identifiers(t, "tab_code")
                    if t_ids & allowed_tab_codes:
                        filtered_tabs.append(t)
            page_data["tabs"] = filtered_tabs

        # 3. Filter attachments
        if page_data.get("attachment"):
            filtered_attachments = []
            if allowed_attachment_codes:
                for a in page_data["attachment"]:
                    label = (
                        a.get("group_sub_title")
                        or a.get("drive_label")
                        or a.get("pdf_label")
                        or a.get("image_text")
                        or (a.get("attachment") or "").split("/")[-1]
                        or a.get("name")
                    )
                    a_ids = get_code_variants(label)
                    if a.get("group_sub_title"):
                        a_ids.update(get_code_variants(a.get("group_sub_title")))
                    if a.get("attachment"):
                        a_ids.update(get_code_variants(a.get("attachment")))
                        a_ids.update(get_code_variants(a.get("attachment").split("/")[-1]))
                    if a.get("name"):
                        a_ids.update(get_code_variants(a.get("name")))
                    if a_ids & allowed_attachment_codes:
                        filtered_attachments.append(a)
            page_data["attachment"] = filtered_attachments

    except Exception as e:
        frappe.log_error(f"Error filtering party portal items: {str(e)}", "filter_party_portal_items")


def get_party_web_doc(web_code):
    try:
        if not web_code:
            return None, None
        customer_name = frappe.db.get_value("Hns Web Page Customer", {"web_code": web_code})
        if customer_name:
            return frappe.get_doc("Hns Web Page Customer", customer_name), "Hns Web Page Customer"

        employee_name = frappe.db.get_value("Hns Web Page Employee", {"web_code": web_code})
        if employee_name:
            return frappe.get_doc("Hns Web Page Employee", employee_name), "Hns Web Page Employee"

        return None, None
    except Exception as e:
        frappe.log_error(f"Error fetching party web doc: {str(e)}", "get_party_web_doc")
        return None, None


def build_price_map(doc, doctype):
    try:
        price_map = {}
        items = (
            doc.get("hns_price_list_details")
            or doc.get("hns_web_page_employee_details")
            or doc.get("customer_details")
            or []
        )

        for item in items:
            code = item.web_page_code or item.get("tab_code") or item.get("web_section_code") or item.get("item")
            if not code:
                continue

            item_dict = dict(item.as_dict())
            if code not in price_map:
                price_map[code] = dict(item_dict)
                price_map[code]["child_items"] = [dict(item_dict)]
            else:
                price_map[code]["child_items"].append(dict(item_dict))

            if item.get("item") and item.get("item") not in price_map:
                price_map[item.get("item")] = price_map[code]

        return price_map
    except Exception as e:
        frappe.log_error(f"Error building price map: {str(e)}", "build_price_map")
        return {}


@frappe.whitelist(allow_guest=True)
def get_web_price_list(web_code, password=None, session_token=None):
    try:
        if not web_code:
            return {}

        doc, doctype = get_party_web_doc(web_code)
        if not doc:
            return {}

        if doc.deactivation_date and getdate(doc.deactivation_date) <= getdate(nowdate()):
            return {"_is_deactivated": True, "_is_authorized": False}

        eff_token = session_token or resolve_request_session_token()
        is_authorized = False
        if eff_token:
            sess = get_web_page_session(eff_token)
            if sess:
                is_authorized = True

        pwd = get_decrypted_doc_password(doctype, doc.name)
        if pwd:
            if password and str(password).strip() == str(pwd).strip():
                is_authorized = True
        else:
            is_authorized = True

        if not is_authorized:
            return {"_is_protected": True, "_is_authorized": False}

        return build_price_map(doc, doctype)
    except Exception as e:
        frappe.log_error(f"Error fetching web price list: {str(e)}", "get_web_price_list")
        return {}

@frappe.whitelist(allow_guest=True)
def submit_web_page_feedback(
    email=None,
    rating=None,
    message=None,
    tab_code=None,
    tab_title=None,
    web_page=None,
    section=None,
    tab=None,
    attachment=None,
    mobile_no=None,
    log=None,
    session_token=None,
    user=None,
    web_code=None,
    customer=None,
    employee=None,
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

        resolved_web_page = web_page
        if web_page:
            wp_title = frappe.db.get_value("Hns Web Page Creation", {"route": web_page}, "title")
            if not wp_title:
                wp_title = frappe.db.get_value("Hns Web Page Creation", web_page, "title")
            if wp_title:
                resolved_web_page = wp_title

        resolved_tab_title = tab_title
        if tab_code and not resolved_tab_title:
            t_title = frappe.db.get_value("Hns Web Page Tab Details", {"tab_code": tab_code}, "page_title")
            if not t_title:
                t_title = frappe.db.get_value("Hns Web Page Tab Details", tab_code, "page_title")
            if t_title:
                resolved_tab_title = t_title

        doc = frappe.get_doc({
            "doctype": "Hns Web Page Feedback",
            "email": email.strip(),
            "rating": numeric_rating,
            "message": message.strip(),
            "tab_code": tab_code,
            "tab_title": resolved_tab_title,
            "web_page": resolved_web_page,
            "mobile_no": formatted_mobile or None,
        })
        doc.insert(ignore_permissions=True)

        resolved_section = (section or "").strip()
        resolved_tab = (tab or "").strip()
        resolved_attachment = (attachment or "").strip()

        if not resolved_section and not resolved_tab and not resolved_attachment:
            resolved_tab = resolved_tab_title or tab_code

        eff_web_code = web_code or frappe.form_dict.get("web_code")
        eff_customer = customer or frappe.form_dict.get("customer")
        eff_employee = employee or frappe.form_dict.get("employee")

        log_web_page_activity(
            web_page=web_page,
            section=resolved_section or None,
            tab=resolved_tab or None,
            attachment=resolved_attachment or None,
            event_type="Feedback",
            log=log,
            session_token=session_token,
            user=user,
            web_code=eff_web_code,
            customer=eff_customer,
            employee=eff_employee,
        )

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

        or_filters = None
        if tab_code:
            clean_tab = str(tab_code).strip()
            or_filters = [
                {"tab_code": clean_tab},
                {"tab_title": clean_tab},
            ]

        feedbacks = frappe.db.get_all(
            "Hns Web Page Feedback",
            filters=filters,
            or_filters=or_filters,
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

