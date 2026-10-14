// Copyright (c) 2026, HNS and contributors
// For license information, please see license.txt

frappe.ui.form.on("Hns Web Page Customer", {
	refresh: async function(frm) {
		load_portal_codes(frm);
		if (!frm.is_new() && frm.doc.select_portal && frm.doc.web_code) {
			let response = await frappe.db.get_value("Hns Web Page Creation", frm.doc.select_portal, "route");
			if (response && response.message && response.message.route) {
				frm.add_web_link("/#" + response.message.route + "?web_code=" + frm.doc.web_code);
			}
		}
	},

	select_portal(frm) {
		load_portal_codes(frm, true);
	},

	hns_price_list_details_add(frm, cdt, cdn) {
		set_row_code_options(frm, cdt, cdn);
	}
});

frappe.ui.form.on("Hns Web Page Customer Details", {
	web_page_code_type(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		if (!frm.doc.select_portal) {
			frappe.msgprint(__("Please select a Portal first."));
			frappe.model.set_value(cdt, cdn, "web_page_code_type", "");
			return;
		}

		set_row_code_options(frm, cdt, cdn);

		let valid_options = get_valid_code_options(frm, row.web_page_code_type);
		if (row.web_page_code && !valid_options.includes(row.web_page_code)) {
			frappe.model.set_value(cdt, cdn, "web_page_code", "");
		}
	},

	form_render(frm, cdt, cdn) {
		set_row_code_options(frm, cdt, cdn);
	}
});

function load_portal_codes(frm, portal_changed = false) {
	if (!frm.doc.select_portal) {
		frm._portal_section_codes = [];
		frm._portal_tab_codes = [];
		frm._current_portal = null;
		set_global_code_options(frm, "");
		update_all_rows_code_options(frm);
		return;
	}

	if (!portal_changed && frm._current_portal === frm.doc.select_portal && frm._portal_section_codes) {
		update_all_rows_code_options(frm);
		return;
	}

	frappe.call({
		method: "frappe.client.get",
		args: {
			doctype: "Hns Web Page Creation",
			name: frm.doc.select_portal
		},
		callback: function(r) {
			if (r.message) {
				frm._current_portal = frm.doc.select_portal;

				let section_codes = (r.message.section || [])
					.map(s => s.section_code || (s.page_title ? frappe.scrub(s.page_title) : ""))
					.filter(Boolean);

				let tab_codes = (r.message.tabs || [])
					.map(t => t.tab_code || (t.page_title ? frappe.scrub(t.page_title) : ""))
					.filter(Boolean);

				frm._portal_section_codes = [...new Set(section_codes)];
				frm._portal_tab_codes = [...new Set(tab_codes)];

				let all_codes = ["", ...frm._portal_section_codes, ...frm._portal_tab_codes];
				set_global_code_options(frm, all_codes.join("\n"));

				update_all_rows_code_options(frm);
			}
		}
	});
}

function get_valid_code_options(frm, code_type) {
	if (code_type === "Section") {
		return frm._portal_section_codes || [];
	}
	if (code_type === "Tab") {
		return frm._portal_tab_codes || [];
	}
	return [];
}

function set_global_code_options(frm, options_str) {
	let df = frappe.meta.get_docfield("Hns Web Page Customer Details", "web_page_code", frm.doc.name);
	if (df) {
		df.options = options_str;
	}

	let grid = frm.fields_dict.hns_price_list_details && frm.fields_dict.hns_price_list_details.grid;
	if (grid && grid.docfields) {
		let grid_df = grid.docfields.find(d => d.fieldname === "web_page_code");
		if (grid_df) {
			grid_df.options = options_str;
		}
	}
}

function set_row_code_options(frm, cdt, cdn) {
	let row = locals[cdt] && locals[cdt][cdn];
	if (!row) return;

	let valid_codes = get_valid_code_options(frm, row.web_page_code_type);
	let options = ["", ...valid_codes];
	let options_str = options.join("\n");

	let row_df = frappe.meta.get_docfield("Hns Web Page Customer Details", "web_page_code", cdn);
	if (row_df) {
		row_df.options = options_str;
	}

	frm.set_df_property("hns_price_list_details", "options", options_str, frm.doc.name, "web_page_code", cdn);

	let grid = frm.fields_dict.hns_price_list_details && frm.fields_dict.hns_price_list_details.grid;
	if (grid && grid.grid_rows_by_docname && grid.grid_rows_by_docname[cdn]) {
		let grid_row = grid.grid_rows_by_docname[cdn];

		let col_df = grid_row.docfields && grid_row.docfields.find(d => d.fieldname === "web_page_code");
		if (col_df) {
			col_df.options = options_str;
		}

		if (grid_row.columns && grid_row.columns.web_page_code && grid_row.columns.web_page_code.df) {
			grid_row.columns.web_page_code.df.options = options_str;
		}

		if (grid_row.on_grid_fields_dict && grid_row.on_grid_fields_dict.web_page_code) {
			let control = grid_row.on_grid_fields_dict.web_page_code;
			control.df.options = options_str;
			control.refresh();
		}

		if (grid_row.grid_form && grid_row.grid_form.fields_dict && grid_row.grid_form.fields_dict.web_page_code) {
			let control = grid_row.grid_form.fields_dict.web_page_code;
			control.df.options = options_str;
			control.refresh();
		}
	}
}

function update_all_rows_code_options(frm) {
	let rows = frm.doc.hns_price_list_details || [];
	for (let row of rows) {
		set_row_code_options(frm, row.doctype, row.name);
		let valid_options = get_valid_code_options(frm, row.web_page_code_type);
		if (row.web_page_code && !valid_options.includes(row.web_page_code)) {
			frappe.model.set_value(row.doctype, row.name, "web_page_code", "");
		}
	}
}
