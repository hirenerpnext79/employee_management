frappe.ui.form.on("Hns Web Page Creation", {
	refresh(frm) {
		if (!frm.is_new() && frm.doc.route) {
			frm.add_web_link("/#" + frm.doc.route);
		}
	},
});

frappe.ui.form.on("Hns Web Page Section Details", {
	page_title(frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		if (row && row.page_title) {
			frappe.model.set_value(cdt, cdn, "section_code", frappe.scrub(row.page_title));
		}
	},
});

frappe.ui.form.on("Hns Web Page Tab Details", {
	page_title(frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		if (row && row.page_title) {
			frappe.model.set_value(cdt, cdn, "tab_code", frappe.scrub(row.page_title));
		}
	},
});
