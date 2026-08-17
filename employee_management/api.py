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
	employee_name = None
	
	if len(token) == 5 and token.isdigit():
		vcard = frappe.get_all("VCard", filters={"vcard_id": token}, fields=["name", "employee", "theme", "vcard_id"], limit=1, ignore_permissions=True)
		if vcard:
			employee_name = vcard[0].employee

	if not employee_name:
		employees = frappe.get_all(
			"Employee",
			filters={"v_card_url": ["like", f"%token={token}%"]},
			fields=["name"],
			ignore_permissions=True
		)
		if not employees:
			frappe.throw(_("Employee not found or invalid token"), frappe.PermissionError)
		employee_name = employees[0].name
		vcard = frappe.get_all("VCard", filters={"employee": employee_name}, fields=["name", "employee", "theme", "vcard_id"], limit=1, ignore_permissions=True)

	employee = frappe.get_all("Employee", filters={"name": employee_name}, fields=["*"], ignore_permissions=True)[0]
	employee['display_name'] = ' '.join(filter(None, [employee.first_name, employee.middle_name, employee.last_name]))
	employee['email'] = employee.prefered_email or employee.company_email or employee.personal_email

	if vcard:
		theme_name = vcard[0].theme
		theme_path = None
		if theme_name:
			theme_path = frappe.db.get_value("VCard Theme", theme_name, "path")
		
		employee['theme'] = theme_path if theme_path else theme_name
		employee['vcard_id'] = vcard[0].vcard_id
		attachments = frappe.get_all("VCard Attachment", filters={"parent": vcard[0].name}, fields=["*"], ignore_permissions=True)
		employee['attachments'] = attachments
	else:
		employee['theme'] = None
		employee['vcard_id'] = None
		employee['attachments'] = []

	return employee

@frappe.whitelist(allow_guest=True)
def get_csrf_token():
	return frappe.sessions.get_csrf_token()
