// Copyright (c) 2026, HNS and contributors
// For license information, please see license.txt

frappe.ui.form.on('VCard', {
	refresh: function(frm) {
		if (frm.doc.vcard_id && !frm.is_new()) {
			// Replace the URL field href with the absolute URL for the frontend
			setTimeout(() => {
				let link = frm.get_field("vcard_id").$wrapper.find("a");
				if(link.length) {
					link.attr("href", frappe.urllib.get_base_url() + "/" + frm.doc.vcard_id);
					link.attr("target", "_blank");
				}
			}, 500);

			// Add custom button to visit VCard
			frm.add_custom_button(__('Visit VCard'), function() {
				window.open(frappe.urllib.get_base_url() + "/" + frm.doc.vcard_id, '_blank');
			});
		}
	},

	employee: function(frm) {
		if (frm.doc.employee) {
			frappe.db.get_value('Employee', frm.doc.employee, 
				['employee_name', 'gender', 'date_of_birth', 'employee_number', 'designation', 'department', 'user_id', 'company'], 
				function(r) {
					if (r) {
						frm.set_value('full_name', r.employee_name);
						frm.set_value('gender', r.gender);
						frm.set_value('date_of_birth', r.date_of_birth);
						frm.set_value('employee_number', r.employee_number);
						frm.set_value('designation', r.designation);
						frm.set_value('department', r.department);
						frm.set_value('company', r.company);
						
						if (r.user_id && r.user_id !== frm.doc.user) {
							frm.set_value('user', r.user_id);
						}
					}
				}
			);
		} else {
			frm.set_value('full_name', '');
			frm.set_value('gender', '');
			frm.set_value('date_of_birth', '');
			frm.set_value('employee_number', '');
			frm.set_value('designation', '');
			frm.set_value('department', '');
			frm.set_value('company', '');
			frm.set_value('user', '');
		}
	},

	user: function(frm) {
		if (frm.doc.user) {
			frappe.db.get_value('User', frm.doc.user, 
				['mobile_no', 'location', 'phone', 'email'], 
				function(r) {
					if (r) {
						frm.set_value('mobile_no', r.mobile_no);
						frm.set_value('location', r.location);
						frm.set_value('phone', r.phone);
						frm.set_value('email', r.email);
					}
				}
			);
		} else {
			frm.set_value('mobile_no', '');
			frm.set_value('location', '');
			frm.set_value('phone', '');
			frm.set_value('email', '');
		}
	}
});
