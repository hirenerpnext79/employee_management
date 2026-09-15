import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    custom_fields = {
        'Company': [
            {
                'fieldname': 'physical_card_tab',
                'label': 'Physical Card',
                'fieldtype': 'Tab Break',
                'insert_after': 'old_parent'
            },
            {
                'fieldname': 'company_logo_1',
                'label': 'Company Logo 1',
                'fieldtype': 'Attach Image',
                'insert_after': 'physical_card_tab'
            },
            {
                'fieldname': 'company_logo_2',
                'label': 'Company Logo 2',
                'fieldtype': 'Attach Image',
                'insert_after': 'company_logo_1'
            },
            {
                'fieldname': 'company_logo_3',
                'label': 'Company Logo 3',
                'fieldtype': 'Attach Image',
                'insert_after': 'company_logo_2'
            },
            {
                'fieldname': 'company_name_line_1',
                'label': 'Company Name Line 1',
                'fieldtype': 'Data',
                'insert_after': 'company_logo_3'
            },
            {
                'fieldname': 'company_name_line_2',
                'label': 'Company Name Line 2',
                'fieldtype': 'Data',
                'insert_after': 'company_name_line_1'
            },
            {
                'fieldname': 'company_address_1',
                'label': 'Company Address 1',
                'fieldtype': 'Long Text',
                'insert_after': 'company_name_line_2'
            },
            {
                'fieldname': 'company_address_2',
                'label': 'Company Address 2',
                'fieldtype': 'Long Text',
                'insert_after': 'company_address_1'
            }
        ]
    }
    
    create_custom_fields(custom_fields, update=True)
    frappe.db.commit()
    print('Custom fields created/updated successfully on Company DocType under the new Tab.')
