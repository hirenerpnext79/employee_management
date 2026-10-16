// Copyright (c) 2026, HNS and contributors
// For license information, please see license.txt

frappe.ui.form.on("Hns Web Page Activity", {
	refresh(frm) {
		frm.page.clear_primary_action();
		frm.disable_save();
	},
});