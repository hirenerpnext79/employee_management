// Copyright (c) 2026, HNS and contributors
// For license information, please see license.txt

frappe.ui.form.on("Hns Web Page Creation", {
	refresh(frm) {
		if (!frm.is_new() && frm.doc.route) {
			frm.add_web_link("/#" + frm.doc.route);
		}
	},
});
