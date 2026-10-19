frappe.ui.form.on("Hns Web Page Creation", {
	refresh(frm) {
		if (!frm.is_new() && frm.doc.route) {
			frm.add_web_link("/#" + frm.doc.route);
		}
		setup_group_link_queries(frm);
	},
	title(frm) {
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
});

frappe.ui.form.on("Hns Web Page Tab Details", {
	page_title(frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		if (row && row.page_title) {
			frappe.model.set_value(cdt, cdn, "tab_code", frappe.scrub(row.page_title));
		}
	},
});
