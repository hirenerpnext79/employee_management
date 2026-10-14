// Copyright (c) 2026, HNS and contributors
// For license information, please see license.txt

frappe.ui.form.on("Hns Web Page Customer", {
	refresh: async function(frm) {
		frm.trigger("set_tab_code_options");
		if (!frm.is_new() && frm.doc.select_portal && frm.doc.web_code) {
			let response = await frappe.db.get_value("Hns Web Page Creation", frm.doc.select_portal, "route");
			if (response && response.message && response.message.route) {
				frm.add_web_link("/#" + response.message.route + "?web_code=" + frm.doc.web_code);
			}
		}
	},
	select_portal(frm) {
		frm.trigger("set_tab_code_options");
	},
	set_tab_code_options(frm) {
		if (frm.doc.select_portal) {
			frappe.call({
				method: "frappe.client.get",
				args: {
					doctype: "Hns Web Page Creation",
					name: frm.doc.select_portal
				},
				callback: function(r) {
					if (r.message && r.message.tabs) {
						let options = r.message.tabs.map(s => s.tab_code).filter(Boolean);
						options.unshift(""); // Add blank option
						
						let options_str = options.join("\n");
						frappe.meta.get_docfield("Hns Web Page Customer Details", "tab_code", frm.doc.name).options = options_str;
						
						if (frm.fields_dict.hns_price_list_details && frm.fields_dict.hns_price_list_details.grid) {
							frm.fields_dict.hns_price_list_details.grid.update_docfield_property("tab_code", "options", options_str);
						}
					}
				}
			});
		} else {
			frappe.meta.get_docfield("Hns Web Page Customer Details", "tab_code", frm.doc.name).options = "";
			if (frm.fields_dict.hns_price_list_details && frm.fields_dict.hns_price_list_details.grid) {
				frm.fields_dict.hns_price_list_details.grid.update_docfield_property("tab_code", "options", "");
			}
		}
	}
});
