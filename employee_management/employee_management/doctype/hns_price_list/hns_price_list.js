// Copyright (c) 2026, HNS and contributors
// For license information, please see license.txt

frappe.ui.form.on("HNS Price List", {
	refresh(frm) {
		frm.trigger("set_web_section_code_options");
	},
	select_portal(frm) {
		frm.trigger("set_web_section_code_options");
	},
	set_web_section_code_options(frm) {
		if (frm.doc.select_portal) {
			frappe.call({
				method: "frappe.client.get",
				args: {
					doctype: "HNS Web Page",
					name: frm.doc.select_portal
				},
				callback: function(r) {
					if (r.message && r.message.section) {
						let options = r.message.section.map(s => s.section_code).filter(Boolean);
						options.unshift(""); // Add blank option
						
						let options_str = options.join("\n");
						frappe.meta.get_docfield("HNS Price List Details", "web_section_code", frm.doc.name).options = options_str;
						
						if (frm.fields_dict.hns_price_list_details && frm.fields_dict.hns_price_list_details.grid) {
							frm.fields_dict.hns_price_list_details.grid.update_docfield_property("web_section_code", "options", options_str);
						}
					}
				}
			});
		} else {
			frappe.meta.get_docfield("HNS Price List Details", "web_section_code", frm.doc.name).options = "";
			if (frm.fields_dict.hns_price_list_details && frm.fields_dict.hns_price_list_details.grid) {
				frm.fields_dict.hns_price_list_details.grid.update_docfield_property("web_section_code", "options", "");
			}
		}
	}
});
