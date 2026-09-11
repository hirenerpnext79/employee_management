// Copyright (c) 2026, HNS and contributors
// For license information, please see license.txt

frappe.ui.form.on("VCard Analytics Log", {
	refresh(frm) {
        setTimeout(() => {
            frm.page.clear_primary_action();
            frm.disable_save();
        }, 10);
	},
});
