// Copyright (c) 2026, HNS and contributors
// For license information, please see license.txt

frappe.ui.form.on("Hns Web Page Group", {
	setup(frm) {
		frm.set_query("disallowed_roles", function () {
			return {
				filters: {
					mode: "Roles",
					is_active: 1,
				},
			};
		});
	},

	refresh(frm) {
		frm.trigger("toggle_web_page_field");
	},

	is_generic(frm) {
		if (frm.doc.is_generic) {
			frm.set_value("web_page", "");
		}
		frm.trigger("toggle_web_page_field");
	},

	toggle_web_page_field(frm) {
		const is_generic = Boolean(frm.doc.is_generic);
		frm.set_df_property("web_page", "reqd", !is_generic);
		frm.set_df_property("web_page", "read_only", is_generic);
	}
});
