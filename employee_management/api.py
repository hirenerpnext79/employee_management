import datetime
import json
import re
import urllib.parse
import frappe
from frappe import _
from frappe.utils import cint, getdate, nowdate, now_datetime
from frappe.utils.password import get_decrypted_password

SESSION_USER_FIELDS = (
    "user_name",
    "email",
    "role",
    "company",
    "party_doctype",
    "party_name",
    "web_code",
    "select_portal",
)

PARTY_PROTECTION_DOCTYPES = {
    "customer": "Hns Web Page Customer",
    "employee": "Hns Web Page Employee",
}

MCQ_OPTION_TO_RATING = {"A": 0.2, "B": 0.4, "C": 0.6, "D": 0.8}
RATING_STARS_TO_MCQ = {1: "A", 2: "B", 3: "C", 4: "D"}


def clean_str(value, lower=False):
    if not value:
        return ""
    text = str(value).strip()
    return text.lower() if lower else text


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

    for page_field in ("company_page", "product_page"):
        if vcard.get(page_field):
            try:
                vcard[f"{page_field}_route"] = frappe.db.get_value(
                    "Hns Web Page Creation", vcard.get(page_field), "route", cache=True
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
        try:
            log_dict = frappe.parse_json(log)
            log_text = json.dumps(log_dict, indent=4)
        except Exception:
            log_text = str(log)
    return log_dict or {}, log_text


def extract_client_metadata(log):
    log_dict, log_text = parse_event_log(log)
    location = log_dict.get("location") or {}
    user_agent = log_dict.get("userAgent") or (
        frappe.request.environ.get("HTTP_USER_AGENT", "") if frappe.request else ""
    )
    ip_address = location.get("ip") or frappe.local.request_ip
    meta = {
        "user_agent": user_agent,
        "ip_address": ip_address,
        "city": location.get("city"),
        "state": location.get("region"),
        "country": location.get("country_name"),
        "latitude": location.get("latitude"),
        "longitude": location.get("longitude"),
        "pincode": location.get("postal"),
        "device_type": log_dict.get("device_type"),
        "platform": log_dict.get("platform"),
        "log": log_text,
    }
    return log_dict, meta


@frappe.whitelist(allow_guest=True)
def track_vcard_event(vcard, event_type, action_details=None, log=None):
    if not vcard or not event_type:
        frappe.throw(_("Missing required parameters"))

    try:
        if not frappe.db.exists("VCard", vcard):
            return {"status": "ignored"}

        _, client_meta = extract_client_metadata(log)
        doc = frappe.get_doc({
            "doctype": "VCard Analytics Log",
            "vcard": vcard,
            "event_type": event_type,
            "action_details": action_details,
            **client_meta,
        })
        doc.insert(ignore_permissions=True)

        counter_field = {"View": "total_views", "Click": "total_clicks"}.get(event_type)
        if counter_field:
            current_count = frappe.db.get_value("VCard", vcard, counter_field) or 0
            frappe.db.set_value("VCard", vcard, counter_field, current_count + 1, update_modified=False)

        return {"status": "success"}
    except Exception as e:
        frappe.log_error(f"Error tracking vcard event: {str(e)}", "track_vcard_event")
        return {"status": "error", "message": str(e)}


def find_party_name(doctype, web_code):
    code = clean_str(web_code)
    if not code:
        return None
    name = frappe.db.get_value(doctype, {"web_code": code}, "name")
    if not name:
        frappe.throw(_("{0} not found for web code: {1}").format(doctype, code))
    return name


def resolve_party_by_web_code(web_code):
    try:
        code = clean_str(web_code)
        if not code:
            return None, None
        cust = frappe.db.get_value("Hns Web Page Customer", {"web_code": code}, "name")
        if cust:
            return cust, None
        emp = frappe.db.get_value("Hns Web Page Employee", {"web_code": code}, "name")
        if emp:
            return None, emp
        frappe.throw(_("No Customer or Employee found for web code: {0}").format(code))
    except Exception as e:
        frappe.log_error(f"Error resolving party by web code: {str(e)}", "resolve_party_by_web_code")
        return None, None


def extract_web_code_from_url(url):
    try:
        if not url:
            return None
        parsed = urllib.parse.urlparse(str(url))
        frag_query = parsed.fragment.split("?", 1)[1] if (parsed.fragment and "?" in parsed.fragment) else ""
        for raw_qs in (parsed.query, frag_query):
            if not raw_qs:
                continue
            qs = urllib.parse.parse_qs(raw_qs)
            for key in ("web_code", "token"):
                val = qs.get(key)
                if val and val[0]:
                    return val[0].strip()
        return None
    except Exception:
        return None


def find_web_page_user(candidate):
    user = clean_str(candidate)
    if not user:
        return None
    if frappe.db.exists("Hns Web Page User", user):
        return user
    return (
        frappe.db.get_value("Hns Web Page User", {"email": user}, "name")
        or frappe.db.get_value("Hns Web Page User", {"user_name": user}, "name")
    )


def resolve_activity_user(session_token, user, log_dict):
    eff_token = session_token or log_dict.get("session_token")
    if not eff_token and frappe.request:
        eff_token = frappe.request.headers.get("X-Session-Token") or frappe.request.cookies.get("session_token")

    if eff_token:
        sess = get_web_page_session(eff_token)
        if sess:
            for candidate in (sess.get("user"), sess.get("email"), sess.get("user_name")):
                found = find_web_page_user(candidate)
                if found:
                    return found

    for candidate in (user, log_dict.get("user"), log_dict.get("username"), log_dict.get("email")):
        found = find_web_page_user(candidate)
        if found:
            return found

    return None


def resolve_activity_web_code(web_code, log_dict):
    candidates = [
        web_code,
        log_dict.get("web_code"),
        frappe.form_dict.get("web_code") if frappe.form_dict else None,
        frappe.form_dict.get("token") if frappe.form_dict else None,
        extract_web_code_from_url(log_dict.get("url")),
    ]
    if frappe.request:
        candidates.append(extract_web_code_from_url(frappe.request.environ.get("HTTP_REFERER")))
        candidates.append(extract_web_code_from_url(frappe.request.environ.get("REQUEST_URI")))
    return next((c for c in candidates if c), None)


def is_duplicate_activity(
    event_type,
    web_page,
    user_link,
    ip_address,
    user_agent,
    customer,
    employee,
    user_email=None,
):
    if event_type not in ("Login", "Logout", "View"):
        return False, None

    since = frappe.utils.today() if event_type == "View" else frappe.utils.add_to_date(now_datetime(), seconds=-10)
    filters = {
        "web_page": web_page,
        "event_type": event_type,
        "creation": [">=", since],
    }
    if user_email:
        filters["user_email"] = user_email
    elif user_link:
        filters["user"] = user_link
    elif ip_address:
        filters["ip_address"] = ip_address
    elif event_type == "View" and user_agent:
        filters["user_agent"] = user_agent
    if customer:
        filters["customer"] = customer
    if employee:
        filters["employee"] = employee

    if frappe.db.exists("Hns Web Page Activity", filters):
        msg = "View already recorded today" if event_type == "View" else f"{event_type} already recorded recently"
        return True, msg
    return False, None


def resolve_tab_title(tab_code):
    if not tab_code:
        return None
    return frappe.db.get_value("Hns Web Page Tab Details", {"tab_code": tab_code}, "page_title")


def extract_dynamic_password_from_request(pw=None):
    try:
        val = pw or (frappe.form_dict.get("pw") if getattr(frappe, "form_dict", None) else None)
        return urllib.parse.unquote(str(val).strip()) if val else None
    except Exception as e:
        frappe.log_error(f"Error extracting dynamic password: {str(e)}", "extract_dynamic_password_from_request")
        return None


def extract_dynamic_user_email(pw):
    try:
        pw = clean_str(pw)
        if pw and "^^" in pw:
            return clean_str(pw.rsplit("^^", 1)[1])
        return None
    except Exception as e:
        frappe.log_error(f"Error extracting dynamic user email: {str(e)}", "extract_dynamic_user_email")
        return None


def is_web_page_dynamic(web_page):
    try:
        page = clean_str(web_page)
        if not page:
            return False
        return bool(cint(frappe.db.get_value("Hns Web Page Creation", {"route": page}, "dynamic_password")))
    except Exception as e:
        frappe.log_error(f"Error checking page dynamic status: {str(e)}", "is_web_page_dynamic")
        return False


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
    dynamic=None,
    user_email=None,
):
    try:
        log_dict, client_meta = extract_client_metadata(log)
        user_link = resolve_activity_user(session_token, user, log_dict)
        eff_web_code = resolve_activity_web_code(web_code, log_dict)

        resolved_customer = customer or (log_dict.get("customer") if log_dict else None) or frappe.form_dict.get("customer")
        resolved_employee = employee or (log_dict.get("employee") if log_dict else None) or frappe.form_dict.get("employee")
        if eff_web_code:
            party_cust, party_emp = resolve_party_by_web_code(eff_web_code)
            resolved_customer = resolved_customer or party_cust
            resolved_employee = resolved_employee or party_emp

        resolved_web_page = (frappe.db.get_value("Hns Web Page Creation", {"route": web_page}, "title") if web_page else None) or web_page

        is_dynamic = bool(cint(dynamic)) or is_web_page_dynamic(web_page)
        effective_email = clean_str(user_email or user or (user_link if user_link and "@" in str(user_link) else None)) if is_dynamic else None

        is_dup, dup_msg = is_duplicate_activity(
            event_type,
            resolved_web_page,
            user_link,
            client_meta["ip_address"],
            client_meta["user_agent"],
            resolved_customer,
            resolved_employee,
            effective_email,
        )
        if is_dup:
            return {"status": "ignored", "message": dup_msg}

        resolved_tab = resolve_tab_title(tab) or tab
        resolved_section = (frappe.db.get_value("Hns Web Page Section Details", {"section_code": section}, "page_title") if section else None) or section

        activity_data = {
            "doctype": "Hns Web Page Activity",
            "web_page": resolved_web_page,
            "section": resolved_section,
            "tab": resolved_tab,
            "attachment": attachment,
            "event_type": event_type,
            **client_meta,
        }
        if user_link:
            activity_data["user"] = user_link
        if resolved_customer:
            activity_data["customer"] = resolved_customer
        if resolved_employee:
            activity_data["employee"] = resolved_employee
        if is_dynamic:
            activity_data["dynamic"] = 1
            if effective_email:
                activity_data["user_email"] = effective_email
        else:
            activity_data["dynamic"] = 0

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
    dynamic=None,
    user_email=None,
):
    try:
        eff_web_code = web_code or frappe.form_dict.get("web_code")
        eff_customer = customer or frappe.form_dict.get("customer")
        eff_employee = employee or frappe.form_dict.get("employee")
        eff_dynamic = dynamic if dynamic is not None else frappe.form_dict.get("dynamic")
        eff_user_email = user_email or frappe.form_dict.get("user_email")
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
            dynamic=eff_dynamic,
            user_email=eff_user_email,
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
            for doctype in PARTY_PROTECTION_DOCTYPES.values():
                party = frappe.db.get_value(
                    doctype,
                    {"web_code": web_code},
                    ["name", "select_portal", "deactivation_date"],
                    as_dict=True,
                )
                if party and party.select_portal == page_doc.name and party.deactivation_date and getdate(party.deactivation_date) <= today:
                    return True

        if page_doc and page_doc.deactivation_date and getdate(page_doc.deactivation_date) <= today:
            return True

        return False
    except Exception as e:
        frappe.log_error(f"Error checking deactivation: {str(e)}", "check_is_deactivated")
        return False


def is_valid_dynamic_user(user, doc):
    try:
        user = clean_str(user, lower=True)
        if not user:
            return False
        sess_user = getattr(frappe.session, "user", None) if getattr(frappe, "session", None) else None
        if sess_user and sess_user.lower() == user:
            return True
        if doc and getattr(doc, "owner", None) and doc.owner.lower() == user:
            return True
        if getattr(frappe, "db", None):
            return bool(frappe.db.exists("User", user) or frappe.db.exists("User", {"email": user}))
        return True
    except Exception as e:
        frappe.log_error(f"Error validating dynamic user: {str(e)}", "is_valid_dynamic_user")
        return False


def is_valid_dynamic_password(pw, doc):
    try:
        pw = clean_str(pw)
        if not pw or "^^" not in pw:
            return False

        date_part, user = pw.rsplit("^^", 1)

        if not is_valid_dynamic_user(user, doc):
            return False

        try:
            today = getdate(nowdate())
        except Exception:
            today = datetime.date.today()

        mm_regex = rf"(?:{today.month:02d}|{today.month})"
        dd_regex = rf"(?:{today.day:02d}|{today.day})"
        last_digit = str(today.year)[-1]
        yy = f"{today.year % 100:02d}"
        yyy = f"{today.year % 1000:03d}"
        yyyy = str(today.year)

        year_regex = rf"(?:{yyyy}|{yyy}|{yy}|{last_digit}|y)"
        rand_delim = r"(?:\d{2}|\?{2})"
        pattern_mm_dd = rf"^{rand_delim}{mm_regex}{rand_delim}{dd_regex}{rand_delim}{year_regex}$"

        date_part = clean_str(date_part)
        if re.match(pattern_mm_dd, date_part, re.IGNORECASE):
            return True

        return False
    except Exception as e:
        frappe.log_error(f"Error validating dynamic password: {str(e)}", "is_valid_dynamic_password")
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


def resolve_party_doc(web_code=None):
    try:
        eff_code = web_code or frappe.form_dict.get("web_code") or frappe.form_dict.get("token")
        if not eff_code:
            return None, None

        return get_party_web_doc(eff_code)
    except Exception as e:
        frappe.log_error(f"Error resolving party doc: {str(e)}", "resolve_party_doc")
        return None, None


def apply_party_answer_visibility(page_data, doc_party, is_party_matching_portal):
    try:
        show_answer = 0
        show_explanation = 0
        if doc_party and is_party_matching_portal:
            show_answer = 1 if cint(doc_party.show_answer) else 0
            show_explanation = 1 if cint(doc_party.show_explanation) else 0

        page_data["show_answer"] = show_answer
        page_data["show_explanation"] = show_explanation

        for tab in page_data.get("tabs") or []:
            if not show_answer:
                tab["answer"] = ""
            if not show_explanation:
                tab["explanation"] = ""
    except Exception as e:
        frappe.log_error(f"Error applying party answer visibility: {str(e)}", "apply_party_answer_visibility")
        page_data["show_answer"] = 0
        page_data["show_explanation"] = 0


def get_effective_feedback_allow(page_doc, web_code=None, login_user=None, party_doc=None):
    try:
        if not page_doc:
            return 0

        doc_party = party_doc
        if not doc_party:
            doc_party, _ = resolve_party_doc(web_code)

        if doc_party and doc_party.feedback_allow is not None:
            return 1 if cint(doc_party.feedback_allow) else 0

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


def build_session_user_dict(source):
    return {field: source.get(field) for field in SESSION_USER_FIELDS}


def get_name_variants(value):
    if not value:
        return set()
    text = str(value).strip()
    return {text.lower(), frappe.scrub(text)}


def resolve_active_web_session(session_token=None):
    try:
        token = resolve_request_session_token(session_token)
        if not token:
            return None, None, None, False

        sess = get_web_page_session(token)
        if sess:
            return token, sess.get("role"), build_session_user_dict(sess), False

        return token, None, None, True
    except Exception as e:
        frappe.log_error(f"Error resolving active web session: {str(e)}", "resolve_active_web_session")
        return None, None, None, False


def is_party_matching_portal_doc(party_doc, page_doc):
    try:
        if not party_doc or not page_doc:
            return False
        if not party_doc.select_portal:
            return True

        portal_variants = get_name_variants(party_doc.select_portal)
        page_variants = (
            get_name_variants(page_doc.name)
            | get_name_variants(page_doc.title)
            | get_name_variants(page_doc.route)
        )
        return bool(portal_variants & page_variants)
    except Exception as e:
        frappe.log_error(f"Error checking party portal match: {str(e)}", "is_party_matching_portal_doc")
        return False


def resolve_session_party_doc(login_user):
    try:
        if not login_user:
            return None, None
        party_doctype = login_user.get("party_doctype")
        party_name = login_user.get("party_name")
        if party_doctype in PARTY_PROTECTION_DOCTYPES.values() and party_name:
            if frappe.db.exists(party_doctype, party_name):
                return frappe.get_doc(party_doctype, party_name), party_doctype
        return None, None
    except Exception as e:
        frappe.log_error(f"Error resolving session party doc: {str(e)}", "resolve_session_party_doc")
        return None, None


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
    session_data = {"user": user_doc.get("name"), **build_session_user_dict(user_doc)}
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
        category_sort_maps = {"section": {}, "tab": {}, "attachment": {}}

        for g in groups:
            so = int(g.get("sort_order") or 0)
            cat = (g.get("category") or "").strip().lower()
            keys = [k for k in (g.name, g.get("group_name")) if k]
            for key in keys:
                group_sort_order_map[key] = so
                if cat in category_sort_maps:
                    category_sort_maps[cat][key] = so

        section_group_sort_order_map = category_sort_maps["section"]
        tab_group_sort_order_map = category_sort_maps["tab"]
        attachment_group_sort_order_map = category_sort_maps["attachment"]

        for sec in page_data.get("section") or []:
            raw_grp = sec.get("section_group") or sec.get("tab_group") or sec.get("attachment_group")
            if raw_grp:
                sec["group_sort_order"] = group_sort_order_map.get(raw_grp, 0)
            for field in ("section_group", "tab_group", "attachment_group"):
                if sec.get(field) in group_name_map:
                    sec[f"raw_{field}"] = sec[field]
                    sec[field] = group_name_map[sec[field]]

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


def get_party_field_by_web_code(doctype, web_code, fieldname):
    try:
        if not web_code:
            return None
        return frappe.db.get_value(doctype, {"web_code": str(web_code).strip()}, fieldname)
    except Exception as e:
        frappe.log_error(f"Error resolving {doctype} info: {str(e)}", "get_party_field_by_web_code")
        return None


def resolve_customer_info(web_code):
    return get_party_field_by_web_code("Hns Web Page Customer", web_code, "party_name")


def resolve_employee_info(web_code):
    return get_party_field_by_web_code("Hns Web Page Employee", web_code, "employee_name")


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
    return build_session_user_dict(user_data), token


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


def get_hns_web_page_user_email(username):
    if not username:
        return ""
    user = str(username).strip()
    return (
        frappe.db.get_value("Hns Web Page User", {"user_name": user}, "email")
        or frappe.db.get_value("Hns Web Page User", {"email": user}, "email")
        or (user if "@" in user else "")
    )


def authenticate_party(doctype, display_fields, web_code, username, password):
    if not password or not web_code:
        return None
    fields = ["name", "web_code", "select_portal", *display_fields]
    party = frappe.db.get_value(doctype, {"web_code": web_code}, fields, as_dict=True)
    if not party:
        return None

    pwd = get_decrypted_doc_password(doctype, party.name)
    if not pwd or password != str(pwd).strip():
        return None

    display_name = next((party.get(f) for f in display_fields if party.get(f)), username)
    return frappe._dict(
        user_name=display_name,
        email=get_hns_web_page_user_email(username),
        role=None,
        company=None,
        party_doctype=doctype,
        party_name=party.name,
        web_code=party.web_code or web_code,
        select_portal=party.select_portal,
    )


def authenticate_customer(page_name, web_code, username, password):
    return authenticate_party("Hns Web Page Customer", ("party_name",), web_code, username, password)


def authenticate_employee(page_name, web_code, username, password):
    return authenticate_party("Hns Web Page Employee", ("employee_name", "employee"), web_code, username, password)


def authenticate_page(page_name, username, password):
    if not page_name or not password:
        return None
    pwd = get_decrypted_doc_password("Hns Web Page Creation", page_name)
    if pwd and password == str(pwd).strip():
        return frappe._dict(
            user_name=username or "Portal User",
            email=get_hns_web_page_user_email(username),
            role=None,
            company=None,
        )
    return None


def is_party_session_valid(login_user, protection_type, effective_code):
    expected_doctype = PARTY_PROTECTION_DOCTYPES.get(protection_type)
    if not expected_doctype:
        return True

    session_party_doctype = login_user.get("party_doctype")
    if not session_party_doctype:
        return bool(login_user.get("user_name"))

    if session_party_doctype != expected_doctype:
        return False

    target_name = frappe.db.get_value(expected_doctype, {"web_code": effective_code}, "name")
    return not target_name or login_user.get("party_name") == target_name


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

        if active_token and login_user and not is_expired:
            if is_party_session_valid(login_user, protection_type, effective_code):
                return {
                    "authorized": True,
                    "is_protected": True,
                    "protection_type": protection_type or "user",
                    "login_user": login_user,
                    "session_token": active_token,
                }

        pwd = str(password).strip() if password else ""
        user = str(username).strip() if username else ""

        # 2. If session expired but password provided, allow seamless password auth instead of blocking
        if is_expired and not pwd:
            return build_auth_error(session_expired=True)

        if not pwd:
            return build_auth_error()

        user_data = None
        ptype = protection_type or "user"

        if protection_type == "customer":
            user_data = authenticate_customer(doc.name, effective_code, user, pwd)
        elif protection_type == "employee":
            user_data = authenticate_employee(doc.name, effective_code, user, pwd)
        else:
            if user:
                user_data = authenticate_web_page_user(user, pwd)
                ptype = "user"
            if not user_data:
                user_data = authenticate_page(doc.name, user, pwd)
                ptype = "web_page"

        if user_data:
            if active_token:
                delete_web_page_session(active_token)
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


def resolve_enforced_party_code(page_doc, effective_code, session_token):
    try:
        url_party_doc, url_party_doctype = resolve_party_doc(effective_code) if effective_code else (None, None)
        sess_token, _, sess_login_user, sess_expired = resolve_active_web_session(session_token)
        if not sess_token or not sess_login_user or sess_expired:
            return effective_code, None, url_party_doc, url_party_doctype

        sess_party_doc, sess_party_doctype = resolve_session_party_doc(sess_login_user)
        if not sess_party_doc or not is_party_matching_portal_doc(sess_party_doc, page_doc):
            return effective_code, None, url_party_doc, url_party_doctype

        sess_web_code = (sess_party_doc.web_code or "").strip()
        if not sess_web_code:
            return effective_code, None, url_party_doc, url_party_doctype

        if not effective_code or not url_party_doc:
            return sess_web_code, sess_web_code, sess_party_doc, sess_party_doctype
        if url_party_doc.name == sess_party_doc.name and url_party_doctype == sess_party_doctype:
            return effective_code, sess_web_code, sess_party_doc, sess_party_doctype

        return effective_code, None, url_party_doc, url_party_doctype
    except Exception as e:
        frappe.log_error(f"Error resolving enforced party code: {str(e)}", "resolve_enforced_party_code")
        return effective_code, None, None, None


def apply_party_context(
    page_data,
    page_doc,
    effective_code,
    login_user,
    enforced_web_code,
    doc_party=None,
    doctype_party=None,
):
    try:
        if not doc_party and effective_code:
            doc_party, doctype_party = resolve_party_doc(effective_code)
        is_matching = is_party_matching_portal_doc(doc_party, page_doc) if doc_party else True

        if doc_party and is_matching:
            party_web_code = (doc_party.web_code or effective_code or "").strip()
            append_party_info(page_data, party_web_code, party_web_code)
            if (
                login_user
                and login_user.get("party_doctype") == doctype_party
                and login_user.get("party_name") == doc_party.name
            ):
                login_user["web_code"] = party_web_code
                login_user["select_portal"] = doc_party.select_portal
                enforced_web_code = party_web_code
            page_data["price_list"] = build_price_map(doc_party, doctype_party)
            if not doc_party.show_complete_portal:
                filter_party_portal_items(page_data, doc_party)

        if enforced_web_code:
            page_data["enforced_web_code"] = enforced_web_code
            page_data["web_code"] = enforced_web_code

        page_data["feedback_allow"] = get_effective_feedback_allow(
            page_doc,
            web_code=effective_code if is_matching else None,
            login_user=login_user,
            party_doc=doc_party if is_matching else None,
        )
        apply_party_answer_visibility(page_data, doc_party, is_matching)
    except Exception as e:
        frappe.log_error(f"Error applying party context: {str(e)}", "apply_party_context")


@frappe.whitelist(allow_guest=True)
def get_custom_web_pages(name, password=None, web_code=None, username=None, session_token=None, token=None, pw=None):
    if not name:
        return None

    try:
        doc = fetch_page_doc(name)
        raw_code = (web_code or token or "").strip() or None
        effective_code, enforced_web_code, doc_party, doctype_party = resolve_enforced_party_code(
            doc, raw_code, session_token
        )

        if check_is_deactivated(doc, effective_code):
            return get_base_page_response(
                doc,
                is_deactivated=True,
                deactivation_message=_(
                    "This page is currently inactive. Please contact your administrator."
                ),
            )

        if cint(doc.dynamic_password):
            dynamic_pw = extract_dynamic_password_from_request(pw)
            if not is_valid_dynamic_password(dynamic_pw, doc):
                return get_base_page_response(
                    doc,
                    is_deactivated=True,
                    deactivation_message=_(
                        "Please contact to administrator this page is not accessible"
                    ),
                )
            auth = {"authorized": True, "is_protected": False}
            dyn_user = extract_dynamic_user_email(dynamic_pw)
            if dyn_user:
                auth["login_user"] = {"name": dyn_user, "email": dyn_user, "user_name": dyn_user}
        else:
            auth = check_page_authorization(doc, password, username, session_token, effective_code, effective_code)
            if not auth.get("authorized"):
                return auth.get("error_response")

        page_data = doc.as_dict()
        page_data.pop("password", None)
        if "section" in page_data and "sections" not in page_data:
            page_data["sections"] = page_data["section"]

        if cint(doc.dynamic_password):
            page_data["dynamic"] = 1
            dyn_user = extract_dynamic_user_email(dynamic_pw)
            if dyn_user:
                page_data["dynamic_user_email"] = dyn_user
                page_data["user_email"] = dyn_user

        page_data["is_protected"] = bool(auth.get("is_protected"))
        page_data["is_authorized"] = True
        if auth.get("protection_type"):
            page_data["protection_type"] = auth["protection_type"]

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
        page_data["group_title_color"] = page_data.get("group_title_color") or "#1e3a8a"
        page_data["sub_group_title_color"] = page_data.get("sub_group_title_color") or "#118ab2"

        apply_party_context(
            page_data, doc, effective_code, login_user, enforced_web_code, doc_party, doctype_party
        )
        append_page_settings(page_data)
        return page_data
    except frappe.DoesNotExistError:
        raise
    except Exception as e:
        frappe.log_error(f"Error fetching custom web page: {str(e)}", "get_custom_web_pages")
        frappe.throw(_("Failed to fetch web page"))


def get_code_variants(code):
    variants = set()
    code_val = clean_str(code, lower=True)
    if not code_val:
        return variants
    variants.add(code_val)
    variants.add(code_val.replace(" ", "_"))
    variants.add(code_val.replace("_", " "))
    variants.add(code_val.replace("-", "_"))
    variants.add(code_val.replace(" ", ""))
    return variants


def get_party_child_items(doc_party):
    return (
        doc_party.get("hns_price_list_details")
        or doc_party.get("hns_web_page_employee_details")
        or doc_party.get("customer_details")
        or []
    )


def get_portal_item_identifiers(item, code_field):
    ids = set()
    for key in (code_field, "name", "page_title"):
        if item.get(key):
            ids.update(get_code_variants(item.get(key)))
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

        child_items = get_party_child_items(doc_party)

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
        cust_match, emp_match = resolve_party_by_web_code(web_code)
        if cust_match:
            return frappe.get_doc("Hns Web Page Customer", cust_match), "Hns Web Page Customer"
        if emp_match:
            return frappe.get_doc("Hns Web Page Employee", emp_match), "Hns Web Page Employee"
        return None, None
    except Exception as e:
        frappe.log_error(f"Error fetching party web doc: {str(e)}", "get_party_web_doc")
        return None, None


def build_price_map(doc, doctype):
    try:
        price_map = {}
        for item in get_party_child_items(doc):
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
                sess_party_doctype = sess.get("party_doctype")
                sess_party_name = sess.get("party_name")
                if not sess_party_doctype or (sess_party_doctype == doctype and sess_party_name == doc.name):
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

def is_mcq_option_type(option_type):
    return bool(option_type and "mcq" in str(option_type).strip().lower())


def is_number_rating_option_type(option_type):
    return bool(option_type and ("1-10" in str(option_type).strip().lower() or "number" in str(option_type).strip().lower()))


def parse_feedback_score(option_type, rating, mcq_option, number_rating=None):
    if is_mcq_option_type(option_type):
        raw_option = mcq_option if mcq_option is not None else (rating if isinstance(rating, str) else "")
        selected = str(raw_option or "").strip().upper()
        if selected not in MCQ_OPTION_TO_RATING:
            frappe.throw(_("Please select a valid option (A, B, C, or D)"))
        return MCQ_OPTION_TO_RATING[selected], selected, None

    if is_number_rating_option_type(option_type):
        raw_num = number_rating if number_rating is not None else rating
        try:
            num = int(raw_num)
            if num < 1 or num > 10:
                frappe.throw(_("Please select a valid rating between 1 and 10"))
        except (ValueError, TypeError):
            frappe.throw(_("Please select a valid rating between 1 and 10"))
        return round(num / 10.0, 2), None, num

    if not rating:
        frappe.throw(_("Rating is required"))
    try:
        numeric_rating = float(rating)
    except (ValueError, TypeError):
        frappe.throw(_("Invalid rating"))
    if numeric_rating > 1.0:
        numeric_rating = numeric_rating / 5.0
    return max(0.2, min(1.0, numeric_rating)), None, None


def resolve_feedback_email(email, sess_user):
    if email and email.strip():
        return email.strip()
    if sess_user and sess_user.get("email"):
        return sess_user["email"].strip()
    if frappe.session.user and frappe.session.user != "Guest":
        user_email = frappe.db.get_value("User", frappe.session.user, "email")
        if user_email:
            return user_email.strip()
        return frappe.session.user.strip()
    frappe.throw(_("Email is required"))


def format_mobile_no(mobile_no):
    mobile = clean_str(mobile_no)
    if mobile and not mobile.startswith("+"):
        return f"+91{mobile}"
    return mobile or None


def validate_page_feedback_permission(web_page, web_code, sess_user, doc_party):
    if not web_page:
        return None, None
    try:
        page_doc = fetch_page_doc(web_page)
        if not page_doc:
            return web_page, None
        if not get_effective_feedback_allow(page_doc, web_code=web_code, login_user=sess_user, party_doc=doc_party):
            frappe.throw(_("Feedback is not allowed for this page."))
        return page_doc.title or page_doc.name, page_doc.option_type
    except frappe.ValidationError:
        raise
    except Exception:
        return web_page, None


def apply_feedback_party_fields(feedback_data, doc_party, doctype_party, party_type, party_name):
    party_type_map = {
        "Hns Web Page Customer": "Customer",
        "Hns Web Page Employee": "Employee",
    }
    p_type = party_type_map.get(doctype_party) or party_type
    p_name = doc_party.name if doc_party else party_name

    if p_type in ("Customer", "Employee") and p_name:
        feedback_data["party_type"] = p_type
        feedback_data[f"party_name_{p_type.lower()}"] = p_name


def save_feedback_attachments(doc, attachments_data):
    if not attachments_data:
        return

    if isinstance(attachments_data, str):
        try:
            attachments_data = json.loads(attachments_data)
        except Exception:
            return

    if not isinstance(attachments_data, list):
        return

    from frappe.utils.file_manager import save_file

    has_files = False
    for item in attachments_data:
        if not isinstance(item, dict):
            continue
        fname = item.get("filename") or item.get("name")
        content = item.get("content")
        if not (fname and content):
            continue
        try:
            saved = save_file(
                fname=fname,
                content=content,
                dt="Hns Web Page Feedback",
                dn=doc.name,
                decode=True,
                is_private=0,
            )
            if saved and saved.file_url:
                doc.append("attachments", {
                    "file_name": fname,
                    "attachment": saved.file_url,
                })
                has_files = True
        except Exception as e:
            frappe.log_error(f"Error saving attachment {fname}: {str(e)}", "submit_web_page_feedback")

    if has_files:
        doc.save(ignore_permissions=True)


@frappe.whitelist(allow_guest=True)
def submit_web_page_feedback(
    email=None,
    rating=None,
    number_rating=None,
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
    party_type=None,
    party_name=None,
    option_type=None,
    mcq_option=None,
    attachments_data=None,
):
    try:
        active_token, role, sess_user, is_expired = resolve_active_web_session(session_token)
        user_email = resolve_feedback_email(email, sess_user)
        if not message or not message.strip():
            frappe.throw(_("Message is required"))

        doc_party, doctype_party = resolve_party_doc(web_code)
        resolved_page, page_option_type = validate_page_feedback_permission(
            web_page, web_code, sess_user, doc_party
        )

        resolved_option_type = page_option_type or option_type or "Rating (Star)"
        numeric_rating, selected_mcq, selected_number = parse_feedback_score(
            resolved_option_type, rating, mcq_option, number_rating
        )

        resolved_tab_title = tab_title or resolve_tab_title(tab_code)
        feedback_data = {
            "doctype": "Hns Web Page Feedback",
            "email": user_email,
            "rating": numeric_rating,
            "message": message.strip(),
            "tab_code": tab_code,
            "tab_title": resolved_tab_title,
            "web_page": resolved_page or web_page,
            "mobile_no": format_mobile_no(mobile_no),
            "option_type": resolved_option_type,
            "mcq_option": selected_mcq,
            "number_rating": selected_number,
        }
        apply_feedback_party_fields(feedback_data, doc_party, doctype_party, party_type, party_name)

        doc = frappe.get_doc(feedback_data)
        doc.insert(ignore_permissions=True)

        save_feedback_attachments(doc, attachments_data)

        resolved_section = (section or "").strip()
        resolved_tab = (tab or "").strip() or (resolved_tab_title or tab_code if not resolved_section else "")
        resolved_attachment = (attachment or "").strip()
        resolved_customer = doc_party.name if (doc_party and doctype_party == "Hns Web Page Customer") else customer
        resolved_employee = doc_party.name if (doc_party and doctype_party == "Hns Web Page Employee") else employee

        log_web_page_activity(
            web_page=web_page,
            section=resolved_section or None,
            tab=resolved_tab or None,
            attachment=resolved_attachment or None,
            event_type="Feedback",
            log=log,
            session_token=session_token,
            user=user,
            web_code=web_code,
            customer=resolved_customer,
            employee=resolved_employee,
        )

        return {"status": "success", "message": _("Thank you for your feedback!")}
    except frappe.ValidationError:
        raise
    except Exception as e:
        frappe.log_error(f"Error submitting feedback: {str(e)}", "submit_web_page_feedback")
        return {"status": "error", "message": str(e)}


def fetch_feedback_attachments_map(fb_names):
    if not fb_names:
        return {}

    attachments_map = {}
    try:
        if frappe.db.table_exists("Hns Web Page Feedback Attachment"):
            records = frappe.db.get_all(
                "Hns Web Page Feedback Attachment",
                filters={"parent": ["in", fb_names]},
                fields=["parent", "file_name", "attachment"],
                order_by="idx asc",
            )
            for r in records:
                attachments_map.setdefault(r.parent, []).append({
                    "file_name": r.file_name or (r.attachment.split("/")[-1] if r.attachment else "Attachment"),
                    "file_url": r.attachment,
                })
    except Exception as e:
        frappe.log_error(f"Error fetching child attachments: {str(e)}", "fetch_feedback_attachments_map")

    missing_names = [name for name in fb_names if name not in attachments_map]
    if missing_names:
        try:
            files = frappe.db.get_all(
                "File",
                filters={
                    "attached_to_doctype": "Hns Web Page Feedback",
                    "attached_to_name": ["in", missing_names],
                },
                fields=["attached_to_name", "file_name", "file_url"],
            )
            for f in files:
                attachments_map.setdefault(f.attached_to_name, []).append({
                    "file_name": f.file_name,
                    "file_url": f.file_url,
                })
        except Exception as e:
            frappe.log_error(f"Error fetching file attachments: {str(e)}", "fetch_feedback_attachments_map")

    return attachments_map


def format_feedback_record(fb, attachments_map):
    raw_rating = fb.get("rating") or 0.0
    stars = int(round(float(raw_rating) * 5.0)) if raw_rating <= 1.0 else int(round(float(raw_rating)))
    fb["stars"] = max(1, min(5, stars))
    fb["option_type"] = fb.get("option_type") or "Rating (Star)"

    if is_number_rating_option_type(fb["option_type"]):
        if fb.get("number_rating"):
            fb["number_rating"] = int(fb["number_rating"])
        else:
            fb["number_rating"] = max(1, min(10, int(round(float(raw_rating) * 10.0)))) if raw_rating <= 1.0 else max(1, min(10, int(round(float(raw_rating)))))
    elif is_mcq_option_type(fb["option_type"]):
        if not fb.get("mcq_option"):
            fb["mcq_option"] = RATING_STARS_TO_MCQ.get(fb["stars"], "")
        fb["mcq_option_fallback"] = fb.get("mcq_option") or RATING_STARS_TO_MCQ.get(fb["stars"], "")

    fb["attachments"] = attachments_map.get(fb["name"], [])
    if not fb["attachments"] and fb.get("attachment"):
        fb["attachments"].append({
            "file_name": fb["attachment"].split("/")[-1],
            "file_url": fb["attachment"],
        })

    if fb.get("creation"):
        fb["formatted_date"] = frappe.utils.format_datetime(fb["creation"], "dd MMM yyyy, hh:mm a")
    if fb.get("modified") and fb.get("reply"):
        fb["formatted_reply_date"] = frappe.utils.format_datetime(fb["modified"], "dd MMM yyyy, hh:mm a")

    return fb


@frappe.whitelist(allow_guest=True)
def get_user_feedback_history(email, web_page=None, tab_code=None):
    try:
        user_email = clean_str(email)
        if not user_email:
            return []

        filters = {"email": user_email}
        if web_page:
            filters["web_page"] = web_page

        or_filters = None
        tab = clean_str(tab_code)
        if tab:
            or_filters = [{"tab_code": tab}, {"tab_title": tab}]

        fields = [
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
            "option_type",
            "mcq_option",
            "number_rating",
        ]

        feedbacks = frappe.db.get_all(
            "Hns Web Page Feedback",
            filters=filters,
            or_filters=or_filters,
            fields=fields,
            order_by="creation desc",
            limit=50,
        )

        fb_names = [fb["name"] for fb in feedbacks]
        attachments_map = fetch_feedback_attachments_map(fb_names)

        return [format_feedback_record(fb, attachments_map) for fb in feedbacks]
    except Exception as e:
        frappe.log_error(f"Error fetching user feedback history: {str(e)}", "get_user_feedback_history")
        return []


@frappe.whitelist()
def create_portal_user(doctype, docname):
    try:
        doc = frappe.get_doc(doctype, docname)
        if not doc.user_email:
            frappe.throw(_("Please enter User Email."))

        email = doc.user_email.strip()
        user_type = "Customer" if doctype == "Hns Web Page Customer" else "Employee"

        existing_user = frappe.db.get_value(
            "Hns Web Page User",
            {"email": email, "user_type": user_type},
            "name"
        )
        if existing_user:
            frappe.throw(_("Already this email user created"))

        user = frappe.new_doc("Hns Web Page User")
        user.email = email
        user.user_type = user_type
        user.user_name = email.split("@")[0].strip()
        pwd = get_decrypted_doc_password(doctype, doc.name) or doc.password
        if pwd and not str(pwd).startswith("*"):
            user.password = pwd
        user.insert(ignore_permissions=True)

        doc.db_set("user", user.name)
        return {"user": user.name}
    except Exception as e:
        frappe.log_error(f"Error creating user: {str(e)}", "create_portal_user")
        frappe.throw(str(e))


@frappe.whitelist()
def get_saved_password(doctype, docname, fieldname="password"):
    try:
        if not doctype or not docname:
            frappe.throw(_("Invalid document parameters"))

        if not frappe.has_permission(doctype, "read", docname):
            frappe.throw(_("Not permitted"), frappe.PermissionError)

        pwd = get_decrypted_password(doctype, docname, fieldname, raise_exception=False)
        return {"password": pwd or ""}
    except Exception as e:
        frappe.log_error(f"Error fetching saved password: {str(e)}", "get_saved_password")
        frappe.throw(str(e))


@frappe.whitelist()
def send_portal_access_email(doctype, docname):
    try:
        if not doctype or not docname:
            frappe.throw(_("Invalid document parameters"))

        doc = frappe.get_doc(doctype, docname)
        email = (doc.user_email or "").strip()
        if not email:
            frappe.throw(_("User Email is required."))

        portal_route = ""
        portal_title = doc.select_portal
        if doc.select_portal and frappe.db.exists("Hns Web Page Creation", doc.select_portal):
            portal_doc = frappe.get_doc("Hns Web Page Creation", doc.select_portal)
            portal_route = portal_doc.route or ""
            portal_title = portal_doc.title or portal_doc.name

        base_url = frappe.utils.get_url()
        portal_url = f"{base_url}/#{portal_route}?web_code={doc.web_code}" if portal_route else base_url

        party_label = doc.party_name if doctype == "Hns Web Page Customer" else (doc.employee_name or doc.employee or "User")

        subject = _("Access Details for {0}").format(portal_title)
        message = f"""
        <p>Dear {party_label},</p>
        <p>Here are your access details for <b>{portal_title}</b>:</p>
        <p><b>Portal Link:</b> <a href="{portal_url}">{portal_url}</a></p>
        <p><b>Web Code:</b> {doc.web_code or ''}</p>
        """
        pwd = get_decrypted_doc_password(doctype, doc.name) or doc.password
        if pwd and not str(pwd).startswith("*"):
            message += f"<p><b>Password:</b> {pwd}</p>"
        message += "<p>Thank you!</p>"

        frappe.sendmail(
            recipients=[email],
            subject=subject,
            message=message,
            now=True
        )
        return {"success": True}
    except Exception as e:
        frappe.log_error(f"Error sending portal access email: {str(e)}", "send_portal_access_email")
        frappe.throw(str(e))


@frappe.whitelist()
def get_portal_whatsapp_details(doctype, docname):
    try:
        if not doctype or not docname:
            frappe.throw(_("Invalid document parameters"))

        doc = frappe.get_doc(doctype, docname)
        phone = ""

        # Check Hns Web Page User first
        hw_user_name = doc.user
        if not hw_user_name and doc.user_email:
            hw_user_name = frappe.db.get_value("Hns Web Page User", {"email": doc.user_email.strip()}, "name")

        if hw_user_name:
            hw_user = frappe.get_doc("Hns Web Page User", hw_user_name)
            raw_phone = hw_user.get("whatsapp_no") or hw_user.get("mobile_no") or ""
            for line in str(raw_phone).splitlines():
                if line.strip():
                    phone = line.strip()
                    break

        # Fallback to Frappe User
        if not phone and doc.user_email:
            user_name = frappe.db.get_value("User", {"email": doc.user_email.strip()}, "name")
            if user_name:
                u_doc = frappe.get_doc("User", user_name)
                phone = (
                    u_doc.get("whatsapp_no")
                    or u_doc.get("custom_whatsapp_no")
                    or u_doc.get("mobile_no")
                    or u_doc.get("phone")
                    or ""
                ).strip()

        if not phone:
            user_ref = hw_user_name or doc.user_email or doc.name
            frappe.throw(_("WhatsApp number not found in Hns Web Page User {0}. Please set WhatsApp No in Hns Web Page User.").format(user_ref))

        clean_phone = "".join(filter(str.isdigit, phone))

        portal_route = ""
        portal_title = doc.select_portal
        if doc.select_portal and frappe.db.exists("Hns Web Page Creation", doc.select_portal):
            portal_doc = frappe.get_doc("Hns Web Page Creation", doc.select_portal)
            portal_route = portal_doc.route or ""
            portal_title = portal_doc.title or portal_doc.name

        base_url = frappe.utils.get_url()
        portal_url = f"{base_url}/#{portal_route}?web_code={doc.web_code}" if portal_route else base_url

        party_label = doc.party_name if doctype == "Hns Web Page Customer" else (doc.employee_name or doc.employee or "User")

        msg_lines = [
            f"Hello {party_label},",
            "",
            f"Here are your access details for {portal_title}:",
            f"Portal Link: {portal_url}",
            f"Web Code: {doc.web_code or ''}",
        ]
        pwd = get_decrypted_doc_password(doctype, doc.name) or doc.password
        if pwd and not str(pwd).startswith("*"):
            msg_lines.append(f"Password: {pwd}")
        msg_lines.extend(["", "Thank you!"])

        message_text = "\n".join(msg_lines)
        encoded_message = urllib.parse.quote(message_text)
        whatsapp_url = f"https://api.whatsapp.com/send?phone={clean_phone}&text={encoded_message}"

        return {
            "phone": clean_phone,
            "message": message_text,
            "url": whatsapp_url
        }
    except Exception as e:
        frappe.log_error(f"Error preparing whatsapp details: {str(e)}", "get_portal_whatsapp_details")
        frappe.throw(str(e))


