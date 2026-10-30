frappe.ui.form.on("Hns Web Page Section Details", {
	page_title(frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		if (row && row.page_title) {
			frappe.model.set_value(cdt, cdn, "section_code", frappe.scrub(row.page_title));
		}
	},
	is_tab_section(frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		if (!row) return;
		if (cint(row.is_tab_section)) {
			frappe.model.set_value(cdt, cdn, "is_attachment_section", 0);
			frappe.model.set_value(cdt, cdn, "attachment_group", null);
			frappe.model.set_value(cdt, cdn, "section_group", null);
		} else {
			frappe.model.set_value(cdt, cdn, "tab_group", null);
		}
		set_section_details_mandatory(frm, cdt, cdn);
	},
	is_attachment_section(frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		if (!row) return;
		if (cint(row.is_attachment_section)) {
			frappe.model.set_value(cdt, cdn, "is_tab_section", 0);
			frappe.model.set_value(cdt, cdn, "tab_group", null);
			frappe.model.set_value(cdt, cdn, "section_group", null);
		} else {
			frappe.model.set_value(cdt, cdn, "attachment_group", null);
		}
		set_section_details_mandatory(frm, cdt, cdn);
	},
	form_render(frm, cdt, cdn) {
		set_section_details_mandatory(frm, cdt, cdn);
	},
});

function set_section_details_mandatory(frm, cdt, cdn) {
	const row = locals[cdt] && locals[cdt][cdn] ? locals[cdt][cdn] : null;
	if (!row) return;
	const is_tab = Boolean(cint(row.is_tab_section));
	const is_att = Boolean(cint(row.is_attachment_section));
	const is_sec = !is_tab && !is_att;

	if (frm.fields_dict && frm.fields_dict.section && frm.fields_dict.section.grid) {
		const grid = frm.fields_dict.section.grid;
		if (grid.grid_rows_by_docname && grid.grid_rows_by_docname[cdn]) {
			const grid_row = grid.grid_rows_by_docname[cdn];
			if (grid_row.toggle_reqd) {
				grid_row.toggle_reqd("tab_group", is_tab);
				grid_row.toggle_reqd("attachment_group", is_att);
				grid_row.toggle_reqd("section_group", is_sec);
			}
			if (grid_row.toggle_display) {
				grid_row.toggle_display("tab_group", is_tab);
				grid_row.toggle_display("attachment_group", is_att);
				grid_row.toggle_display("section_group", is_sec);
			}
		}
	} else if (frm.toggle_reqd && frm.toggle_display) {
		frm.toggle_reqd("tab_group", is_tab);
		frm.toggle_reqd("attachment_group", is_att);
		frm.toggle_reqd("section_group", is_sec);

		frm.toggle_display("tab_group", is_tab);
		frm.toggle_display("attachment_group", is_att);
		frm.toggle_display("section_group", is_sec);
	}
}
