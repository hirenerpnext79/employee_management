// Copyright (c) 2026, HNS and contributors
// For license information, please see license.txt

frappe.provide("hns_portal_group");

hns_portal_group = {
	setup_portal_codes: function(frm, child_table_field, child_doctype, portal_changed = false) {
		if (!frm.doc.select_portal) {
			frm._portal_section_codes = [];
			frm._portal_tab_codes = [];
			frm._portal_attachment_codes = [];
			frm._current_portal = null;
			this.set_global_code_options(frm, child_table_field, child_doctype, "");
			this.update_all_rows_code_options(frm, child_table_field, child_doctype);
			return;
		}

		if (!portal_changed && frm._current_portal === frm.doc.select_portal && frm._portal_section_codes) {
			this.update_all_rows_code_options(frm, child_table_field, child_doctype);
			return;
		}

		let me = this;
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

					let attachment_codes = (r.message.attachment || [])
						.map(a => a.drive_label || a.pdf_label || a.image_text || (a.attachment ? a.attachment.split("/").pop() : "") || a.name)
						.filter(Boolean);

					frm._portal_section_codes = [...new Set(section_codes)];
					frm._portal_tab_codes = [...new Set(tab_codes)];
					frm._portal_attachment_codes = [...new Set(attachment_codes)];

					let all_codes = ["", ...frm._portal_section_codes, ...frm._portal_tab_codes, ...frm._portal_attachment_codes];
					me.set_global_code_options(frm, child_table_field, child_doctype, all_codes.join("\n"));
					me.update_all_rows_code_options(frm, child_table_field, child_doctype);
				}
			}
		});
	},

	get_valid_code_options: function(frm, code_type) {
		if (code_type === "Section") {
			return frm._portal_section_codes || [];
		}
		if (code_type === "Tab") {
			return frm._portal_tab_codes || [];
		}
		if (code_type === "Attachment") {
			return frm._portal_attachment_codes || [];
		}
		return [];
	},

	set_global_code_options: function(frm, child_table_field, child_doctype, options_str) {
		let df = frappe.meta.get_docfield(child_doctype, "web_page_code", frm.doc.name);
		if (df) {
			df.options = options_str;
		}

		let grid = frm.fields_dict[child_table_field] && frm.fields_dict[child_table_field].grid;
		if (grid && grid.docfields) {
			let grid_df = grid.docfields.find(d => d.fieldname === "web_page_code");
			if (grid_df) {
				grid_df.options = options_str;
			}
		}
	},

	set_row_code_options: function(frm, cdt, cdn, child_table_field, child_doctype) {
		let row = locals[cdt] && locals[cdt][cdn];
		if (!row) return;

		let valid_codes = this.get_valid_code_options(frm, row.web_page_code_type);
		let options = ["", ...valid_codes];
		let options_str = options.join("\n");

		let row_df = frappe.meta.get_docfield(child_doctype, "web_page_code", cdn);
		if (row_df) {
			row_df.options = options_str;
		}

		frm.set_df_property(child_table_field, "options", options_str, frm.doc.name, "web_page_code", cdn);

		let grid = frm.fields_dict[child_table_field] && frm.fields_dict[child_table_field].grid;
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
	},

	on_code_type_change: function(frm, cdt, cdn, child_table_field, child_doctype) {
		let row = locals[cdt][cdn];
		if (!frm.doc.select_portal) {
			frappe.msgprint(__("Please select a Portal first."));
			frappe.model.set_value(cdt, cdn, "web_page_code_type", "");
			return;
		}

		this.set_row_code_options(frm, cdt, cdn, child_table_field, child_doctype);

		let valid_options = this.get_valid_code_options(frm, row.web_page_code_type);
		if (row.web_page_code && !valid_options.includes(row.web_page_code)) {
			frappe.model.set_value(cdt, cdn, "web_page_code", "");
		}
	},

	update_all_rows_code_options: function(frm, child_table_field, child_doctype) {
		let rows = frm.doc[child_table_field] || [];
		for (let row of rows) {
			this.set_row_code_options(frm, row.doctype, row.name, child_table_field, child_doctype);
			let valid_options = this.get_valid_code_options(frm, row.web_page_code_type);
			if (row.web_page_code && !valid_options.includes(row.web_page_code)) {
				frappe.model.set_value(row.doctype, row.name, "web_page_code", "");
			}
		}
	},

	show_dialog: function(frm, opts) {
		let me = this;
		frappe.call({
			method: "employee_management.employee_management.doctype.hns_web_page_customer.hns_web_page_customer.get_portal_groups_data",
			args: {
				portal_name: frm.doc.select_portal,
				parent_doctype: opts.parent_doctype,
				parent_name: frm.doc.name || null
			},
			freeze: true,
			freeze_message: __("Fetching portal group data..."),
			callback: function(r) {
				if (!r.message || r.message.error) {
					frappe.msgprint(r.message?.error || __("Failed to fetch portal groups."));
					return;
				}
				me.render_dialog(frm, r.message, opts);
			}
		});
	},

	render_dialog: function(frm, data, opts) {
		let me = this;

		// Clean up any previous dialog to prevent duplicate DOM IDs
		if (frm._portal_group_dialog) {
			try {
				frm._portal_group_dialog.$wrapper.remove();
			} catch (e) {}
			frm._portal_group_dialog = null;
		}

		let current_keys = new Set();
		(frm.doc[opts.child_table] || []).forEach(row => {
			if (row.web_page_code_type && row.web_page_code) {
				current_keys.add(`${row.web_page_code_type}::${row.web_page_code}`);
			}
		});



		let sections_html = this.build_sections_html(data.sections || {}, current_keys);
		let tabs_html = this.build_tabs_html(data.tabs || {}, current_keys);
		let attachments_html = this.build_attachments_html(data.attachments || {}, current_keys);

		let dialog_content = `
			<div class="pg-dialog-wrapper">
				<style>
					.pg-dialog-wrapper { font-size: 13px; color: #1e293b; width: 100%; box-sizing: border-box; }
					.pg-toolbar {
						background: #ffffff;
						border: 1px solid #e2e8f0;
						border-radius: 8px;
						padding: 10px 14px;
						margin-bottom: 12px;
						box-shadow: 0 1px 3px rgba(0,0,0,0.04);
						width: 100%;
						box-sizing: border-box;
					}
					.pg-toolbar-top { margin-bottom: 8px; width: 100%; }
					.pg-search-input {
						width: 100% !important;
						height: 36px !important;
						border-radius: 6px !important;
						border: 1px solid #cbd5e1 !important;
						font-size: 13px !important;
						padding: 6px 12px !important;
						box-shadow: none !important;
						box-sizing: border-box !important;
					}
					.pg-search-input:focus {
						border-color: #3b82f6 !important;
						box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15) !important;
					}
					.pg-toolbar-bottom {
						display: flex;
						align-items: center;
						justify-content: space-between;
						flex-wrap: wrap;
						gap: 8px;
						padding-top: 6px;
						border-top: 1px solid #f1f5f9;
					}
					.pg-btn-group { display: flex; align-items: center; gap: 6px; }
					.pg-btn-pill {
						font-size: 11px;
						font-weight: 500;
						padding: 4px 10px;
						border-radius: 4px;
						border: 1px solid #e2e8f0;
						background: #f8fafc;
						color: #334155;
						cursor: pointer;
						transition: all 0.15s ease;
					}
					.pg-btn-pill:hover { background: #e2e8f0; color: #0f172a; border-color: #cbd5e1; }
					.pg-badge-counter {
						display: inline-block;
						background: #1e40af;
						color: #ffffff;
						font-weight: 600;
						font-size: 12px;
						padding: 4px 12px;
						border-radius: 12px;
						box-shadow: 0 1px 2px rgba(0,0,0,0.1);
					}
					.pg-tree-scroll {
						max-height: 500px;
						overflow-y: auto;
						padding-right: 4px;
						width: 100%;
						box-sizing: border-box;
					}
					.pg-category-container {
						margin-bottom: 12px;
						border: 1px solid #e2e8f0;
						border-radius: 8px;
						overflow: hidden;
						background: #ffffff;
						box-shadow: 0 1px 2px rgba(0,0,0,0.03);
						width: 100%;
						box-sizing: border-box;
					}
					.pg-cat-header {
						display: flex;
						align-items: center;
						padding: 10px 14px;
						background: #f1f5f9;
						border-bottom: 1px solid #e2e8f0;
						cursor: pointer;
						user-select: none;
						gap: 10px;
						transition: background 0.15s ease;
						width: 100%;
						box-sizing: border-box;
					}
					.pg-cat-header:hover { background: #e2e8f0; }
					.pg-cat-title-text { font-size: 14px; font-weight: 700; color: #0f172a; }
					.pg-group-container {
						margin: 6px 0 8px 0;
						border: 1px solid #e2e8f0;
						border-left: 4px solid #3b82f6;
						border-radius: 6px;
						background: #ffffff;
						overflow: hidden;
						width: 100%;
						box-sizing: border-box;
					}
					.pg-category-container[data-cat="Tab"] .pg-group-container { border-left-color: #8b5cf6; }
					.pg-category-container[data-cat="Attachment"] .pg-group-container { border-left-color: #10b981; }
					.pg-group-header {
						display: flex;
						align-items: center;
						padding: 8px 12px;
						background: #f8fafc;
						cursor: pointer;
						user-select: none;
						gap: 8px;
						border-bottom: 1px solid #f1f5f9;
						transition: background 0.15s ease;
						width: 100%;
						box-sizing: border-box;
					}
					.pg-group-header:hover { background: #f1f5f9; }
					.pg-group-title-text { font-size: 13px; font-weight: 600; color: #1e293b; }
					.pg-group-body { display: none; padding: 4px 6px; width: 100%; box-sizing: border-box; }
					.pg-count-badge {
						margin-left: auto;
						font-size: 12px;
						font-weight: 700;
						color: #000000 !important;
						background: #f1f5f9;
						border: 1px solid #cbd5e1;
						border-radius: 12px;
						padding: 2px 10px;
						white-space: nowrap;
						min-width: 52px;
						text-align: center;
						display: inline-block;
					}
					.pg-subgroup-container {
						margin: 4px 0 4px 12px;
						border-left: 2px solid #cbd5e1;
						box-sizing: border-box;
					}
					.pg-subgroup-header {
						display: flex;
						align-items: center;
						padding: 6px 10px;
						background: #fafafa;
						border-radius: 4px;
						cursor: pointer;
						user-select: none;
						gap: 6px;
						font-size: 12px;
						font-weight: 600;
						color: #334155;
						box-sizing: border-box;
					}
					.pg-subgroup-header:hover { background: #f1f5f9; }
					.pg-subgroup-body { display: none; padding-left: 12px; box-sizing: border-box; }
					.pg-item-row {
						display: flex;
						align-items: center;
						padding: 6px 10px 6px 20px;
						border-radius: 4px;
						margin: 2px 0;
						gap: 8px;
						font-size: 13px;
						transition: background 0.15s ease;
						width: 100%;
						box-sizing: border-box;
					}
					.pg-item-row:hover { background: #f8fafc; }
					.pg-item-name { font-weight: 500; color: #1e293b; }
					.pg-item-code {
						color: #64748b;
						font-size: 12px;
						background: #f1f5f9;
						padding: 1px 6px;
						border-radius: 4px;
						font-family: monospace;
					}
					.pg-badge-added {
						background-color: #fef3c7;
						color: #92400e;
						border: 1px solid #fde68a;
						font-size: 11px;
						padding: 2px 8px;
						border-radius: 4px;
						margin-left: auto;
						font-weight: 600;
					}
					.pg-chevron {
						display: inline-block;
						width: 14px;
						text-align: center;
						color: #64748b;
						font-size: 10px;
						transition: transform 0.15s ease;
						transform: rotate(0deg);
					}
					.pg-collapsed .pg-chevron, .pg-collapsed > .pg-chevron { transform: rotate(-90deg); }
					.pg-item-check, .pg-group-check, .pg-subgroup-check, .pg-cat-check {
						margin: 0;
						cursor: pointer;
						width: 15px;
						height: 15px;
						flex-shrink: 0;
					}
				</style>

				<div class="pg-toolbar">
					<div class="pg-toolbar-top">
						<input type="text" id="pg-search-box" class="form-control pg-search-input" placeholder="${__("Search sections, tabs, attachments, codes...")}">
					</div>
					<div class="pg-toolbar-bottom">
						<div class="pg-btn-group">
							<button type="button" class="pg-btn-pill" id="pg-btn-select-all">&#9745; ${__("Select All")}</button>
							<button type="button" class="pg-btn-pill" id="pg-btn-deselect-all">&#9744; ${__("Deselect All")}</button>
						</div>
						<div>
							<span id="pg-selected-count" class="pg-badge-counter">0 Selected</span>
						</div>
					</div>
				</div>

				<div class="pg-tree-scroll">
					${sections_html}
					${tabs_html}
					${attachments_html}
				</div>
			</div>
		`;

		let d = new frappe.ui.Dialog({
			title: __("Fetch Portal Group - {0}", [data.portal_title || frm.doc.select_portal]),
			size: "large",
			fields: [
				{
					fieldtype: "HTML",
					fieldname: "tree_html",
					options: dialog_content
				}
			],
			primary_action_label: __("Push"),
			primary_action: function() {
				me.execute_push(frm, d, opts);
			},
			secondary_action_label: __("Cancel"),
			secondary_action: function() {
				d.hide();
			}
		});

		frm._portal_group_dialog = d;
		d.$wrapper.on("hidden.bs.modal", function() {
			try {
				d.$wrapper.remove();
			} catch (e) {}
			frm._portal_group_dialog = null;
		});

		d.show();
		d.$wrapper.find(".modal-dialog").css("max-width", "820px");

		this.attach_events(d);
	},

	build_sections_html: function(sections_map, current_keys) {
		let groups = Object.keys(sections_map);
		if (!groups.length) return "";

		let total_items = groups.reduce((acc, g) => acc + (sections_map[g] || []).length, 0);
		let assigned_total = 0;

		let groups_html = "";
		groups.forEach(grp => {
			let items = sections_map[grp] || [];
			let grp_assigned = items.filter(it => current_keys.has(`Section::${it.code}`)).length;
			assigned_total += grp_assigned;

			let items_html = "";
			items.forEach(item => {
				let is_already = current_keys.has(`Section::${item.code}`);
				let already_badge = is_already ? `<span class="pg-badge-added">${__("Already Added")}</span>` : "";
				let checked_attr = is_already ? "checked" : "";

				items_html += `
					<div class="pg-item-row" data-search="${frappe.utils.escape_html((item.title + ' ' + item.code + ' ' + grp).toLowerCase())}">
						<input type="checkbox" class="pg-item-check" ${checked_attr} data-cat="Section" data-code="${frappe.utils.escape_html(item.code)}">
						<span class="pg-item-name">${frappe.utils.escape_html(item.title)}</span>
						<span class="pg-item-code">(${frappe.utils.escape_html(item.code)})</span>
						${already_badge}
					</div>
				`;
			});

			groups_html += `
				<div class="pg-group-container" data-group-name="${frappe.utils.escape_html(grp.toLowerCase())}">
					<div class="pg-group-header pg-toggle-trigger pg-collapsed" data-target="pg-body-sec-${frappe.scrub(grp)}">
						<span class="pg-chevron">&#9660;</span>
						<input type="checkbox" class="pg-group-check">
						<span class="pg-group-title-text">${frappe.utils.escape_html(grp)}</span>
						<span class="pg-count-badge">(${grp_assigned}/${items.length})</span>
					</div>
					<div class="pg-group-body" id="pg-body-sec-${frappe.scrub(grp)}" style="display: none;">
						${items_html}
					</div>
				</div>
			`;
		});

		return `
			<div class="pg-category-container" data-cat="Section">
				<div class="pg-cat-header pg-toggle-trigger pg-collapsed" data-target="pg-cat-body-sec">
					<span class="pg-chevron">&#9660;</span>
					<input type="checkbox" class="pg-cat-check">
					<span class="pg-cat-title-text">${__("Sections")}</span>
					<span class="pg-count-badge">(${assigned_total}/${total_items})</span>
				</div>
				<div class="pg-cat-body" id="pg-cat-body-sec" style="display: none;">
					${groups_html}
				</div>
			</div>
		`;
	},

	build_tabs_html: function(tabs_map, current_keys) {
		let groups = Object.keys(tabs_map);
		if (!groups.length) return "";

		let total_items = groups.reduce((acc, g) => acc + (tabs_map[g] || []).length, 0);
		let assigned_total = 0;

		let groups_html = "";
		groups.forEach(grp => {
			let items = tabs_map[grp] || [];
			let grp_assigned = items.filter(it => current_keys.has(`Tab::${it.code}`)).length;
			assigned_total += grp_assigned;

			let items_html = "";
			items.forEach(item => {
				let is_already = current_keys.has(`Tab::${item.code}`);
				let already_badge = is_already ? `<span class="pg-badge-added">${__("Already Added")}</span>` : "";
				let checked_attr = is_already ? "checked" : "";

				items_html += `
					<div class="pg-item-row" data-search="${frappe.utils.escape_html((item.title + ' ' + item.code + ' ' + grp).toLowerCase())}">
						<input type="checkbox" class="pg-item-check" ${checked_attr} data-cat="Tab" data-code="${frappe.utils.escape_html(item.code)}">
						<span class="pg-item-name">${frappe.utils.escape_html(item.title)}</span>
						<span class="pg-item-code">(${frappe.utils.escape_html(item.code)})</span>
						${already_badge}
					</div>
				`;
			});

			groups_html += `
				<div class="pg-group-container" data-group-name="${frappe.utils.escape_html(grp.toLowerCase())}">
					<div class="pg-group-header pg-toggle-trigger pg-collapsed" data-target="pg-body-tab-${frappe.scrub(grp)}">
						<span class="pg-chevron">&#9660;</span>
						<input type="checkbox" class="pg-group-check">
						<span class="pg-group-title-text">${frappe.utils.escape_html(grp)}</span>
						<span class="pg-count-badge">(${grp_assigned}/${items.length})</span>
					</div>
					<div class="pg-group-body" id="pg-body-tab-${frappe.scrub(grp)}" style="display: none;">
						${items_html}
					</div>
				</div>
			`;
		});

		return `
			<div class="pg-category-container" data-cat="Tab">
				<div class="pg-cat-header pg-toggle-trigger pg-collapsed" data-target="pg-cat-body-tab">
					<span class="pg-chevron">&#9660;</span>
					<input type="checkbox" class="pg-cat-check">
					<span class="pg-cat-title-text">${__("Tabs")}</span>
					<span class="pg-count-badge">(${assigned_total}/${total_items})</span>
				</div>
				<div class="pg-cat-body" id="pg-cat-body-tab" style="display: none;">
					${groups_html}
				</div>
			</div>
		`;
	},

	build_attachments_html: function(attachments_map, current_keys) {
		let groups = Object.keys(attachments_map);
		if (!groups.length) return "";

		let total_items = 0;
		let assigned_total = 0;

		let groups_html = "";
		groups.forEach(grp => {
			let sub_groups = attachments_map[grp] || {};
			let sub_group_keys = Object.keys(sub_groups);
			let group_items_count = 0;
			let group_assigned_count = 0;
			let subgroups_html = "";

			sub_group_keys.forEach(sub_grp => {
				let items = sub_groups[sub_grp] || [];
				group_items_count += items.length;
				let sub_assigned = items.filter(it => current_keys.has(`Attachment::${it.code}`)).length;
				group_assigned_count += sub_assigned;

				let items_html = "";
				items.forEach(item => {
					let is_already = current_keys.has(`Attachment::${item.code}`);
					let already_badge = is_already ? `<span class="pg-badge-added">${__("Already Added")}</span>` : "";
					let checked_attr = is_already ? "checked" : "";

					items_html += `
						<div class="pg-item-row" data-search="${frappe.utils.escape_html((item.title + ' ' + item.code + ' ' + sub_grp + ' ' + grp).toLowerCase())}">
							<input type="checkbox" class="pg-item-check" ${checked_attr} data-cat="Attachment" data-code="${frappe.utils.escape_html(item.code)}">
							<span class="pg-item-name">${frappe.utils.escape_html(item.title)}</span>
							${already_badge}
						</div>
					`;
				});

				subgroups_html += `
					<div class="pg-subgroup-container" data-subgroup-name="${frappe.utils.escape_html(sub_grp.toLowerCase())}">
						<div class="pg-subgroup-header pg-toggle-trigger pg-collapsed" data-target="pg-body-att-${frappe.scrub(grp)}-${frappe.scrub(sub_grp)}">
							<span class="pg-chevron">&#9660;</span>
							<input type="checkbox" class="pg-subgroup-check">
							<span>&#128193; ${frappe.utils.escape_html(sub_grp)}</span>
							<span class="pg-count-badge">(${sub_assigned}/${items.length})</span>
						</div>
						<div class="pg-subgroup-body" id="pg-body-att-${frappe.scrub(grp)}-${frappe.scrub(sub_grp)}" style="display: none;">
							${items_html}
						</div>
					</div>
				`;
			});

			total_items += group_items_count;
			assigned_total += group_assigned_count;

			groups_html += `
				<div class="pg-group-container" data-group-name="${frappe.utils.escape_html(grp.toLowerCase())}">
					<div class="pg-group-header pg-toggle-trigger pg-collapsed" data-target="pg-body-att-${frappe.scrub(grp)}">
						<span class="pg-chevron">&#9660;</span>
						<input type="checkbox" class="pg-group-check">
						<span class="pg-group-title-text">${frappe.utils.escape_html(grp)}</span>
						<span class="pg-count-badge">(${group_assigned_count}/${group_items_count})</span>
					</div>
					<div class="pg-group-body" id="pg-body-att-${frappe.scrub(grp)}" style="display: none;">
						${subgroups_html}
					</div>
				</div>
			`;
		});

		return `
			<div class="pg-category-container" data-cat="Attachment">
				<div class="pg-cat-header pg-toggle-trigger pg-collapsed" data-target="pg-cat-body-att">
					<span class="pg-chevron">&#9660;</span>
					<input type="checkbox" class="pg-cat-check">
					<span class="pg-cat-title-text">${__("Attachments")}</span>
					<span class="pg-count-badge">(${assigned_total}/${total_items})</span>
				</div>
				<div class="pg-cat-body" id="pg-cat-body-att" style="display: none;">
					${groups_html}
				</div>
			</div>
		`;
	},

	attach_events: function(d) {
		let $wrapper = d.$wrapper;
		let me = this;

		$wrapper.find(".pg-category-container").each(function() {
			let $cat = $(this);
			$cat.find(".pg-group-container").each(function() {
				let $grp = $(this);
				$grp.find(".pg-subgroup-container").each(function() {
					me.sync_checkboxes($(this));
				});
				me.sync_checkboxes($grp);
			});
			me.sync_checkboxes($cat);
		});
		this.update_counts_and_counter(d);

		$wrapper.on("click", ".pg-toggle-trigger", function(e) {
			if ($(e.target).is("input[type='checkbox']")) {
				return;
			}
			let $body = $(this).next(".pg-cat-body, .pg-group-body, .pg-subgroup-body");
			if (!$body.length) {
				let target_id = $(this).attr("data-target");
				$body = $wrapper.find("#" + target_id);
			}
			$(this).toggleClass("pg-collapsed");
			$body.slideToggle(120);
		});

		$wrapper.on("change", ".pg-cat-check", function(e) {
			e.stopPropagation();
			let checked = $(this).prop("checked");
			let $cat = $(this).closest(".pg-category-container");
			$cat.find(".pg-group-check, .pg-subgroup-check, .pg-item-check").prop("checked", checked);
			me.update_counts_and_counter(d);
		});

		$wrapper.on("change", ".pg-group-check", function(e) {
			e.stopPropagation();
			let checked = $(this).prop("checked");
			let $group = $(this).closest(".pg-group-container");
			$group.find(".pg-subgroup-check, .pg-item-check").prop("checked", checked);
			me.sync_checkboxes($group.closest(".pg-category-container"));
			me.update_counts_and_counter(d);
		});

		$wrapper.on("change", ".pg-subgroup-check", function(e) {
			e.stopPropagation();
			let checked = $(this).prop("checked");
			let $subgroup = $(this).closest(".pg-subgroup-container");
			$subgroup.find(".pg-item-check").prop("checked", checked);
			me.sync_checkboxes($subgroup.closest(".pg-group-container"));
			me.sync_checkboxes($subgroup.closest(".pg-category-container"));
			me.update_counts_and_counter(d);
		});

		$wrapper.on("change", ".pg-item-check", function(e) {
			e.stopPropagation();
			let $subgroup = $(this).closest(".pg-subgroup-container");
			if ($subgroup.length) {
				me.sync_checkboxes($subgroup);
			}
			let $group = $(this).closest(".pg-group-container");
			if ($group.length) {
				me.sync_checkboxes($group);
			}
			let $cat = $(this).closest(".pg-category-container");
			if ($cat.length) {
				me.sync_checkboxes($cat);
			}
			me.update_counts_and_counter(d);
		});

		$wrapper.find("#pg-btn-select-all").on("click", function() {
			$wrapper.find("input[type='checkbox']").prop("checked", true).prop("indeterminate", false);
			me.update_counts_and_counter(d);
		});

		$wrapper.find("#pg-btn-deselect-all").on("click", function() {
			$wrapper.find("input[type='checkbox']").prop("checked", false).prop("indeterminate", false);
			me.update_counts_and_counter(d);
		});

		$wrapper.find("#pg-search-box").on("input", function() {
			let term = ($(this).val() || "").trim().toLowerCase();
			if (!term) {
				$wrapper.find(".pg-item-row, .pg-subgroup-container, .pg-group-container, .pg-category-container").show();
				$wrapper.find(".pg-cat-body, .pg-group-body, .pg-subgroup-body").hide();
				$wrapper.find(".pg-toggle-trigger").addClass("pg-collapsed");
				return;
			}

			$wrapper.find(".pg-category-container").each(function() {
				let cat_match = false;
				let cat_name = ($(this).attr("data-cat") || "").toLowerCase();

				$(this).find(".pg-group-container").each(function() {
					let grp_match = false;
					let grp_name = ($(this).attr("data-group-name") || "").toLowerCase();

					let $subgroups = $(this).find(".pg-subgroup-container");
					if ($subgroups.length) {
						$subgroups.each(function() {
							let sub_match = false;
							let sub_name = ($(this).attr("data-subgroup-name") || "").toLowerCase();

							$(this).find(".pg-item-row").each(function() {
								let text = $(this).attr("data-search") || "";
								if (text.includes(term) || sub_name.includes(term) || grp_name.includes(term) || cat_name.includes(term)) {
									$(this).show();
									sub_match = true;
								} else {
									$(this).hide();
								}
							});
							if (sub_match || sub_name.includes(term)) {
								$(this).show();
								$(this).find(".pg-subgroup-body").show();
								$(this).find(".pg-subgroup-header").removeClass("pg-collapsed");
								grp_match = true;
							} else {
								$(this).hide();
							}
						});
					} else {
						$(this).find(".pg-item-row").each(function() {
							let text = $(this).attr("data-search") || "";
							if (text.includes(term) || grp_name.includes(term) || cat_name.includes(term)) {
								$(this).show();
								grp_match = true;
							} else {
								$(this).hide();
							}
						});
					}

					if (grp_match || grp_name.includes(term)) {
						$(this).show();
						$(this).find(".pg-group-body").show();
						$(this).find(".pg-group-header").removeClass("pg-collapsed");
						cat_match = true;
					} else {
						$(this).hide();
					}
				});

				if (cat_match || cat_name.includes(term)) {
					$(this).show();
					$(this).find(".pg-cat-body").show();
					$(this).find(".pg-cat-header").removeClass("pg-collapsed");
				} else {
					$(this).hide();
				}
			});
		});
	},

	sync_checkboxes: function($container) {
		let $items = $container.find(".pg-item-check");
		if (!$items.length) return;

		let total = $items.length;
		let checked = $items.filter(":checked").length;

		let $header_check = $container.children(".pg-cat-header, .pg-group-header, .pg-subgroup-header").find("input[type='checkbox']");
		if (checked === 0) {
			$header_check.prop("checked", false).prop("indeterminate", false);
		} else if (checked === total) {
			$header_check.prop("checked", true).prop("indeterminate", false);
		} else {
			$header_check.prop("checked", false).prop("indeterminate", true);
		}
	},

	update_counts_and_counter: function(d) {
		d.$wrapper.find(".pg-category-container").each(function() {
			let $cat = $(this);
			let cat_total = $cat.find(".pg-item-check").length;
			let cat_checked = $cat.find(".pg-item-check:checked").length;
			$cat.find(".pg-cat-header .pg-count-badge").text(`(${cat_checked}/${cat_total})`);

			$cat.find(".pg-group-container").each(function() {
				let $grp = $(this);
				let grp_total = $grp.find(".pg-item-check").length;
				let grp_checked = $grp.find(".pg-item-check:checked").length;
				$grp.find(".pg-group-header .pg-count-badge").text(`(${grp_checked}/${grp_total})`);

				$grp.find(".pg-subgroup-container").each(function() {
					let $sub = $(this);
					let sub_total = $sub.find(".pg-item-check").length;
					let sub_checked = $sub.find(".pg-item-check:checked").length;
					$sub.find(".pg-subgroup-header .pg-count-badge").text(`(${sub_checked}/${sub_total})`);
				});
			});
		});

		let total_checked = d.$wrapper.find(".pg-item-check:checked").length;
		let new_checked = 0;
		d.$wrapper.find(".pg-item-check:checked").each(function() {
			if (!$(this).closest(".pg-item-row").find(".pg-badge-added").length) {
				new_checked++;
			}
		});

		let badge_text = `${total_checked} ${__("Selected")}`;
		if (new_checked > 0) {
			badge_text += ` (${new_checked} ${__("new")})`;
		}
		d.$wrapper.find("#pg-selected-count").text(badge_text);

		let btn_label = new_checked > 0 ? `${__("Push")} (${new_checked} ${__("New")})` : `${__("Push")} (${total_checked})`;
		d.set_primary_action(btn_label, d.primary_action);
	},

	execute_push: function(frm, d, opts) {
		let selected_boxes = d.$wrapper.find(".pg-item-check:checked");
		if (!selected_boxes.length) {
			frappe.msgprint(__("Please select at least one item to push."));
			return;
		}

		let existing_set = new Set();
		(frm.doc[opts.child_table] || []).forEach(row => {
			if (row.web_page_code_type && row.web_page_code) {
				existing_set.add(`${row.web_page_code_type}::${row.web_page_code}`);
			}
		});

		let added_count = 0;
		let already_count = 0;

		selected_boxes.each(function() {
			let type = $(this).attr("data-cat");
			let code = $(this).attr("data-code");

			let key = `${type}::${code}`;
			if (existing_set.has(key)) {
				already_count++;
				return;
			}

			let child = frm.add_child(opts.child_table);
			child.web_page_code_type = type;
			child.web_page_code = code;

			existing_set.add(key);
			added_count++;
		});

		if (added_count > 0) {
			frm.refresh_field(opts.child_table);
			this.setup_portal_codes(frm, opts.child_table, opts.child_doctype, false);
			frm.dirty();
			d.hide();
			let target_label = opts.parent_doctype.includes("Employee") ? __("Employee Details") : __("Customer Details");
			let msg = __("Pushed {0} new item(s) to {1}.", [added_count, target_label]);
			if (already_count > 0) {
				msg += ` ${__("({0} already existed)", [already_count])}`;
			}
			frappe.show_alert({ message: msg, indicator: "green" });
		} else {
			d.hide();
			frappe.show_alert({
				message: __("All {0} selected item(s) are already added.", [already_count]),
				indicator: "blue"
			});
		}
	}
};
