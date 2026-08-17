import frappe
from frappe import _

@frappe.whitelist()
def generate_v_card(employee):
	if not employee:
		frappe.throw(_("Employee ID is required"))

	if not frappe.has_permission("Employee", "write", doc=employee):
		frappe.throw(_("Not permitted to update Employee {0}").format(employee))

	token = frappe.generate_hash(length=32)
	v_card_url = f"/?token={token}"
	frappe.db.set_value("Employee", employee, "v_card_url", v_card_url)
	
	return v_card_url

@frappe.whitelist(allow_guest=True)
def get_vcard_details(token):
	if not token:
		frappe.throw(_("Token is required"), frappe.ValidationError)

	vcard = None
	
	if len(token) == 5 and token.isdigit():
		vcard_records = frappe.get_all("VCard", filters={"vcard_id": token}, fields=["*"], limit=1, ignore_permissions=True)
		if vcard_records:
			vcard = vcard_records[0]

	# Fallback if token is an old hash or just to be safe
	if not vcard:
		employees = frappe.get_all(
			"Employee",
			filters={"v_card_url": ["like", f"%token={token}%"]},
			fields=["name"],
			ignore_permissions=True
		)
		if employees:
			vcard_records = frappe.get_all("VCard", filters={"employee": employees[0].name}, fields=["*"], limit=1, ignore_permissions=True)
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
