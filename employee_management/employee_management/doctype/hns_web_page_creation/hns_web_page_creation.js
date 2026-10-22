frappe.ui.form.on("Hns Web Page Creation", {
	refresh(frm) {
		if (!frm.is_new() && frm.doc.route) {
			frm.add_web_link("/#" + frm.doc.route);
		}
		if (frm.doc.title && !frm.doc.page_title) {
			frm.set_value("page_title", frm.doc.title);
		}
		setup_group_link_queries(frm);
		refresh_all_section_details(frm);
	},
	title(frm) {
		if (frm.doc.title) {
			frm.set_value("page_title", frm.doc.title);
			frm.set_value("route", frappe.scrub(frm.doc.title));
		}
		setup_group_link_queries(frm);
	},
});

function setup_group_link_queries(frm) {
	const get_group_query = (category) => {
		const page_name = frm.doc.name || frm.doc.title || "";
		return {
			query: "employee_management.employee_management.doctype.hns_web_page_creation.hns_web_page_creation.get_web_page_group_query",
			filters: {
				category: category,
				web_page: page_name,
			},
		};
	};

	frm.set_query("section_group", "section", () => get_group_query("Section"));
	frm.set_query("tab_group", "section", () => get_group_query("Tab"));
	frm.set_query("attachment_group", "section", () => get_group_query("Attachment"));
	frm.set_query("group_name", "tabs", () => get_group_query("Tab"));
	frm.set_query("group_title", "attachment", () => get_group_query("Attachment"));
}

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
	section_add(frm, cdt, cdn) {
		set_section_details_mandatory(frm, cdt, cdn);
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

function refresh_all_section_details(frm) {
	if (frm.doc.section && Array.isArray(frm.doc.section)) {
		frm.doc.section.forEach((row) => {
			set_section_details_mandatory(frm, row.doctype, row.name);
		});
	}
}

function set_section_details_mandatory(frm, cdt, cdn) {
	const row = locals[cdt] && locals[cdt][cdn] ? locals[cdt][cdn] : null;
	if (!row || !frm.fields_dict.section) return;
	const is_tab = Boolean(cint(row.is_tab_section));
	const is_att = Boolean(cint(row.is_attachment_section));
	const is_sec = !is_tab && !is_att;

	const grid = frm.fields_dict.section.grid;
	if (grid && grid.grid_rows_by_docname && grid.grid_rows_by_docname[cdn]) {
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
}
