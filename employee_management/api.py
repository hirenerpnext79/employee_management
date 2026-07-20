import frappe
from frappe import _

@frappe.whitelist()
def generate_v_card(employee):
	if not employee:
		frappe.throw(_("Employee ID is required"))

	# Check permission
	if not frappe.has_permission("Employee", "write", doc=employee):
		frappe.throw(_("Not permitted to update Employee {0}").format(employee))

	# Generate a secure unique token
	token = frappe.generate_hash(length=32)
	
	# Build unique link pointing to the Vue frontend
	v_card_url = f"/?token={token}"

	# Save to the employee document
	frappe.db.set_value("Employee", employee, "v_card_url", v_card_url)
	
	# Return the generated URL
	return v_card_url

@frappe.whitelist(allow_guest=True)
def get_vcard_details(token):
	if not token:
		frappe.throw(_("Token is required"), frappe.ValidationError)

	employees = frappe.get_all(
		"Employee",
		filters={"v_card_url": ["like", f"%token={token}%"]},
		fields=["*"],
		ignore_permissions=True
	)

	if not employees:
		frappe.throw(_("Employee not found or invalid token"), frappe.PermissionError)

	employee = employees[0]
	employee['display_name'] = ' '.join(filter(None, [employee.first_name, employee.middle_name, employee.last_name]))
	employee['email'] = employee.prefered_email or employee.company_email or employee.personal_email

	return employee
