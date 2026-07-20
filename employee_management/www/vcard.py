import frappe

def get_context(context):
	# Disable page caching to ensure latest information is shown
	context.no_cache = 1
	
	token = frappe.form_dict.get('token')
	if token:
		frappe.redirect(f"/?token={token}")
	else:
		frappe.redirect("/")
