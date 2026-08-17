import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_vcard_details(token):
	if not token:
		frappe.throw(_("Token is required"), frappe.ValidationError)

	vcard = None
	
	if len(token) == 5 and token.isdigit():
		vcard_records = frappe.get_all("VCard", filters={"vcard_id": token}, fields=["*"], limit=1, ignore_permissions=True)
		if vcard_records:
			vcard = vcard_records[0]

	if not vcard:
		frappe.throw(_("VCard not found or invalid token"), frappe.PermissionError)

	theme_name = vcard.theme
	theme_path = None
	if theme_name:
		theme_path = frappe.db.get_value("VCard Theme", theme_name, "path")
	
	vcard['theme'] = theme_path if theme_path else theme_name
	
	attachments = frappe.get_all("VCard Attachment", filters={"parent": vcard.name}, fields=["*"], ignore_permissions=True)
	vcard['attachments'] = attachments

	social_media = frappe.get_all("VCard Social Media", filters={"parent": vcard.name}, fields=["*"], ignore_permissions=True)
	vcard['social_media'] = social_media

	# We return vcard as the main object. The frontend still refers to it as 'employee' in props.
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


