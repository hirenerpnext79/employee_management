app_name = "employee_management"
app_title = "Employee Management"
app_publisher = "HNS"
app_description = "Employee Management"
app_email = "hiren@hns.com"
app_license = "mit"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_js = "/assets/employee_management/js/portal_group_selector.js"

website_route_rules = [
	{"from_route": "/<int:vcard_id>", "to_route": "frontend"}
]

after_migrate = "employee_management.setup_company_fields.execute"
