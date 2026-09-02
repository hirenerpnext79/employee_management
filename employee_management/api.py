import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_vcard_details(token):
	if not token:
		frappe.throw(_("Token is required"), frappe.ValidationError)

	vcard = None
	vcard_doc = None
	
	if len(token) == 5 and token.isdigit():
		vcard_records = frappe.get_all("VCard", filters={"vcard_id": token}, fields=["*"], limit=1, ignore_permissions=True)
		if vcard_records:
			vcard = vcard_records[0]
			try:
				vcard_doc = frappe.get_doc("VCard", vcard.name)
			except Exception:
				pass

	if not vcard:
		frappe.throw(_("VCard not found or invalid token"), frappe.PermissionError)

	theme_name = vcard.theme
	theme_path = None
	if theme_name:
		theme_path = frappe.db.get_value("VCard Theme", theme_name, "path")
	
	vcard['theme'] = theme_path if theme_path else theme_name
	
	if vcard_doc:
		# Use the doc to get child tables to avoid returning deleted/orphaned rows
		attachments = vcard_doc.get("attachment") or []
		vcard['attachments'] = [a.as_dict() for a in attachments]

		# Fetch personal social media using the likely field names
		personal_social = vcard_doc.get("table_shmz") or vcard_doc.get("personal_social_media") or vcard_doc.get("social_media") or []
		vcard['personal_social_media'] = [s.as_dict() for s in personal_social]
	
		# Fetch company and product page routes
		if vcard.get('company_page'):
			try:
				vcard['company_page_route'] = frappe.db.get_value('HNS Web Page', vcard.get('company_page'), 'route')
			except Exception:
				pass
		if vcard.get('product_page'):
			try:
				vcard['product_page_route'] = frappe.db.get_value('HNS Web Page', vcard.get('product_page'), 'route')
			except Exception:
				pass

	else:
		vcard['attachments'] = []
		vcard['personal_social_media'] = []

	# Fetch VCard Setting (Single DocType)
	try:
		# Use get_doc to ensure child tables are fetched for Single doctypes!
		try:
			vcard_setting = frappe.get_doc("VCard Setting")
		except Exception:
			# Fallback if case sensitive
			vcard_setting = frappe.get_doc("Vcard Setting")
			
		vcard['global_company_name'] = vcard_setting.get("company_name")
		
		# The user might have renamed the company social media child table field
		company_social = vcard_setting.get("company_social_media") or vcard_setting.get("table_fypv") or []
		vcard['company_social_media'] = [s.as_dict() for s in company_social]
	except Exception as e:
		print("ERROR loading VCard Setting:", e)
		vcard['global_company_name'] = None
		vcard['company_social_media'] = []
		
	return vcard

@frappe.whitelist(allow_guest=True)
def get_csrf_token():
	return frappe.sessions.get_csrf_token()

@frappe.whitelist(allow_guest=True)
def track_vcard_event(vcard, event_type, action_details=None):
	# Add validation
	if not vcard or not event_type:
		frappe.throw(_('Missing required parameters'))
		
	# Check if vcard exists
	if not frappe.db.exists('VCard', vcard):
		return
		
	ip_address = frappe.local.request_ip
	session_id = frappe.session.sid
	
	# Prevent duplicate logging for the same IP/session and event within 1 hour
	cache_key = f"vcard_track_{vcard}_{event_type}_{ip_address}_{session_id}"
	if action_details:
		cache_key += f"_{action_details}"
		
	if frappe.cache().get_value(cache_key):
		return {'status': 'success', 'message': 'Duplicate event ignored'}
		
	frappe.cache().set_value(cache_key, True, expires_in_sec=3600)

	doc = frappe.get_doc({
		'doctype': 'VCard Analytics Log',
		'vcard': vcard,
		'event_type': event_type,
		'action_details': action_details,
		'user_agent': frappe.request.environ.get('HTTP_USER_AGENT', ''),
		'ip_address': frappe.local.request_ip
	})
	doc.insert(ignore_permissions=True)
	
	vcard_doc = frappe.get_doc('VCard', vcard)
	if event_type == 'View':
		vcard_doc.total_views = (vcard_doc.total_views or 0) + 1
	elif event_type == 'Click':
		vcard_doc.total_clicks = (vcard_doc.total_clicks or 0) + 1
	
	vcard_doc.save(ignore_permissions=True)
	
	return {'status': 'success'}

@frappe.whitelist(allow_guest=True)
def download_vcard(employee):
	if not employee:
		frappe.throw(_("Employee is required"))
		
	if not frappe.db.exists("VCard", employee):
		frappe.throw(_("VCard not found"), frappe.NotFoundError)
		
	vcard = frappe.get_doc("VCard", employee)
	
	# Generate VCF content
	vcf = []
	vcf.append("BEGIN:VCARD")
	vcf.append("VERSION:3.0")
	
	# Name
	first_name = vcard.get("first_name") or vcard.get("full_name") or "Contact"
	last_name = vcard.get("last_name") or ""
	vcf.append(f"N:{last_name};{first_name};;;")
	vcf.append(f"FN:{vcard.get('full_name') or first_name}")
	
	# Org
	if vcard.get("company"):
		vcf.append(f"ORG:{vcard.company}")
	
	# Title
	if vcard.get("designation"):
		vcf.append(f"TITLE:{vcard.designation}")
		
	# Phones
	if vcard.get("mobile_no"):
		vcf.append(f"TEL;TYPE=CELL,VOICE:{vcard.mobile_no}")
	if vcard.get("phone"):
		vcf.append(f"TEL;TYPE=WORK,VOICE:{vcard.phone}")
		
	# Emails
	if vcard.get("email"):
		vcf.append(f"EMAIL;TYPE=WORK,INTERNET:{vcard.email}")
	if vcard.get("personal_email"):
		vcf.append(f"EMAIL;TYPE=HOME,INTERNET:{vcard.personal_email}")
		
	# URLs
	if vcard.get("company_website"):
		vcf.append(f"URL:{vcard.company_website}")
		
	vcf.append("END:VCARD")
	
	vcf_data = "\n".join(vcf)
	
	# Return as downloadable file
	frappe.local.response.filename = f"{vcard.get('full_name') or 'contact'}.vcf"
	frappe.local.response.filecontent = vcf_data.encode('utf-8')
	frappe.local.response.type = 'download'

@frappe.whitelist(allow_guest=True)
def get_custom_web_pages(name):
	if not name:
		return None
	try:
		doc = frappe.get_doc("HNS Web Page", {"route": name})
		return doc.as_dict()
	except frappe.DoesNotExistError:
		frappe.throw(_("Page not found"), frappe.NotFoundError)






