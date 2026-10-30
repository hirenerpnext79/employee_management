// Copyright (c) 2026, HNS and contributors
// For license information, please see license.txt

function ensure_portal_group_helper(callback) {
	if (window.hns_portal_group) {
		callback(window.hns_portal_group);
	} else {
		frappe.require("/assets/employee_management/js/portal_group_selector.js", function() {
			callback(window.hns_portal_group);
		});
	}
}

frappe.ui.form.on("Hns Web Page Customer", {
	refresh: async function(frm) {
		ensure_portal_group_helper(helper => {
			helper.setup_portal_codes(frm, "hns_price_list_details", "Hns Web Page Customer Details");
		});
		if (!frm.is_new() && frm.doc.select_portal && frm.doc.web_code) {
			let response = await frappe.db.get_value("Hns Web Page Creation", frm.doc.select_portal, "route");
			if (response && response.message && response.message.route) {
				frm.add_web_link("/#" + response.message.route + "?web_code=" + frm.doc.web_code);
			}
		}
	},

	select_portal(frm) {
		ensure_portal_group_helper(helper => {
			helper.setup_portal_codes(frm, "hns_price_list_details", "Hns Web Page Customer Details", true);
		});
	},

	fetch_portal_group(frm) {
		if (!frm.doc.select_portal) {
			frappe.msgprint(__("Please select a Portal first."));
			return;
		}
		ensure_portal_group_helper(helper => {
			helper.show_dialog(frm, {
				parent_doctype: "Hns Web Page Customer",
				child_table: "hns_price_list_details",
				child_doctype: "Hns Web Page Customer Details",
				has_item: true
			});
		});
	},

	hns_price_list_details_add(frm, cdt, cdn) {
		ensure_portal_group_helper(helper => {
			helper.set_row_code_options(frm, cdt, cdn, "hns_price_list_details", "Hns Web Page Customer Details");
		});
	}
});

frappe.ui.form.on("Hns Web Page Customer Details", {
	web_page_code_type(frm, cdt, cdn) {
		ensure_portal_group_helper(helper => {
			helper.on_code_type_change(frm, cdt, cdn, "hns_price_list_details", "Hns Web Page Customer Details");
		});
	},

	form_render(frm, cdt, cdn) {
		ensure_portal_group_helper(helper => {
			helper.set_row_code_options(frm, cdt, cdn, "hns_price_list_details", "Hns Web Page Customer Details");
		});
	}
});
