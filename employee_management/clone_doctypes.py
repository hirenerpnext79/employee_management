import frappe

def clone_doctype(source_name, target_name, module):
    if frappe.db.exists("DocType", target_name):
        print(f"{target_name} already exists. Skipping clone.")
        return frappe.get_doc("DocType", target_name)
        
    source = frappe.get_doc("DocType", source_name)
    
    # Create new doctype based on source
    new_doc = frappe.new_doc("DocType")
    new_doc.update(source.as_dict())
    
    # Clean up standard fields
    for field in ["name", "creation", "modified", "owner", "modified_by", "idx"]:
        if field in new_doc:
            del new_doc.flags
            del new_doc[field]
            
    new_doc.name = target_name
    new_doc.module = module
    new_doc.custom = 0 # Since it's going into an app, it should be custom=0 to write JSON
    
    # Clean fields standard fields
    for f in new_doc.fields:
        for key in ["name", "creation", "modified", "owner", "modified_by", "idx", "parent", "parentfield", "parenttype"]:
            if key in f:
                del f[key]
                
    new_doc.insert(ignore_permissions=True)
    print(f"Created {target_name}")
    return new_doc

def update_hns_web_page():
    if not frappe.db.exists("DocType", "HNS Web Page"):
        print("HNS Web Page does not exist.")
        return
        
    hns_doc = frappe.get_doc("DocType", "HNS Web Page")
    source = frappe.get_doc("DocType", "Custom Web Page")
    
    # Clear existing fields
    hns_doc.set("fields", [])
    
    # Copy fields
    for field in source.fields:
        new_field = field.as_dict().copy()
        
        # Clean up
        for key in ["name", "creation", "modified", "owner", "modified_by", "idx", "parent", "parentfield", "parenttype"]:
            if key in new_field:
                del new_field[key]
                
        # Link to new tables
        if new_field.get("fieldname") == "tabs":
            new_field["options"] = "HNS Tab Details"
        elif new_field.get("fieldname") == "section":
            new_field["options"] = "HNS Section Details"
            
        hns_doc.append("fields", new_field)
        
    # Copy other attributes
    hns_doc.autoname = source.autoname
    hns_doc.naming_rule = source.naming_rule
    
    hns_doc.save(ignore_permissions=True)
    print("Updated HNS Web Page")

def execute():
    frappe.flags.in_import = True # Skip some validations if needed
    
    # Clone Child Tables
    clone_doctype("Web Page Detail", "HNS Tab Details", "Employee Management")
    clone_doctype("Web Page Section", "HNS Section Details", "Employee Management")
    
    # Update Parent
    update_hns_web_page()
    
    print("All DocTypes processed.")

# If running directly inside a Frappe environment without bench execute, uncomment:
# if __name__ == "__main__":
#     frappe.init(site="erpnext.local")
#     frappe.connect()
#     execute()
#     frappe.db.commit()
