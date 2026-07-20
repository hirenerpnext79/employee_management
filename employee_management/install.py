import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def after_migrate():
	create_custom_fields({
		"Employee": [
			{
				"fieldname": "v_card_url",
				"label": "V Card Url",
				"fieldtype": "Data",
				"insert_after": "status",
				"read_only": 1,
				"options": "URL",
				"no_copy": 1
			}
		]
	})
