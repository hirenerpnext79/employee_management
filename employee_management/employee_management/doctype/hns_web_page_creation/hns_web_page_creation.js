function sanitize_route(text) {
	if (!text) return "";
	return String(text)
		.trim()
		.replace(/[\s/\\:]+/g, "_")
		.replace(/[^a-zA-Z0-9_-]/g, "")
		.replace(/_+/g, "_")
		.replace(/-+/g, "-")
		.replace(/^[-_]+|[-_]+$/g, "")
		.toLowerCase();
}

function setup_password_eye(frm, fieldname) {
	fieldname = fieldname || "password";
	let control = frm.get_field(fieldname);
	if (!control || !control.$wrapper) return;

	let $wrapper = control.$wrapper;

	// Restore default text box completely
	$wrapper.find(".hns-eye-btn").remove();
	$wrapper.find(".toggle-password").show();
	if (control.$input) {
		control.$input.off(".hns_pwd").on("focus.hns_pwd", function() {
			let v = control.$input.val();
			if (v && /^\*+$/.test(v)) {
				control.$input.select();
			}
		});
	}

	let $label = $wrapper.find(".control-label");
	if (!$label.length) {
		$label = $wrapper.find("label");
	}
	if (!$label.length) return;

	$wrapper.find(".hns-pwd-label-action").remove();

	// Only show after save if a password exists
	let has_saved_pwd = !frm.is_new() && Boolean(frm.doc[fieldname] || control.value);
	if (!has_saved_pwd) return;

	let $action = $(`
		<span class="hns-pwd-label-action" style="display: inline-flex; align-items: center; gap: 6px; margin-left: 10px; font-weight: normal; vertical-align: middle;">
			<span class="hns-pwd-val" style="display: none; font-family: monospace; font-size: 11px; padding: 1px 7px; background: var(--bg-light-gray, #f4f5f7); border: 1px solid var(--border-color, #d1d8dd); border-radius: 4px; color: var(--text-color, #1f272e); font-weight: 600; user-select: all; cursor: text;" title="${__('Click to select')}"></span>
			<button type="button" class="btn btn-xs btn-default hns-pwd-copy-btn" style="display: none; padding: 1px 6px; font-size: 11px; line-height: 1.4;" title="${__('Copy Password')}">
				<i class="fa fa-copy"></i>
			</button>
			<button type="button" class="btn btn-xs btn-default hns-pwd-toggle-btn" style="padding: 1px 7px; font-size: 11px; line-height: 1.4; display: inline-flex; align-items: center; gap: 4px; cursor: pointer;">
				<span class="hns-pwd-icon">${frappe.utils.icon("unhide", "xs")}</span>
				<span class="hns-pwd-text">${__("Show Password")}</span>
			</button>
		</span>
	`).appendTo($label);

	let $val = $action.find(".hns-pwd-val");
	let $copy_btn = $action.find(".hns-pwd-copy-btn");
	let $toggle_btn = $action.find(".hns-pwd-toggle-btn");
	let $icon = $action.find(".hns-pwd-icon");
	let $text = $action.find(".hns-pwd-text");

	let is_shown = false;

	$val.on("click", function(e) {
		e.stopPropagation();
	});

	$toggle_btn.on("click", function(e) {
		e.preventDefault();
		e.stopPropagation();

		if (is_shown) {
			is_shown = false;
			$val.hide().text("");
			$copy_btn.hide();
			$icon.html(frappe.utils.icon("unhide", "xs"));
			$text.text(__("Show Password"));
			return;
		}

		let show_pwd = function(pwd) {
			if (!pwd) {
				$action.remove();
				frappe.show_alert({ message: __("No password saved yet."), indicator: "orange" });
				return;
			}
			is_shown = true;
			$val.text(pwd).show();
			$copy_btn.show();
			$icon.html(frappe.utils.icon("hide", "xs"));
			$text.text(__("Hide Password"));
		};

		$text.text(__("Loading..."));
		frappe.call({
			method: "employee_management.api.get_saved_password",
			args: {
				doctype: frm.doc.doctype,
				docname: frm.doc.name,
				fieldname: fieldname
			},
			freeze: false,
			callback: function(r) {
				let pwd = (r.message && r.message.password) || "";
				show_pwd(pwd);
			},
			error: function() {
				$text.text(__("Show Password"));
			}
		});
	});

	$copy_btn.on("click", function(e) {
		e.preventDefault();
		e.stopPropagation();
		let pwd = $val.text();
		if (pwd) {
			frappe.utils.copy_to_clipboard(pwd);
			frappe.show_alert({ message: __("Password copied to clipboard"), indicator: "green" }, 3);
		}
	});
}

frappe.ui.form.on("Hns Web Page Creation", {
	refresh(frm) {
		setup_password_eye(frm, "password");
		if (!frm.is_new() && frm.doc.route) {
			if (cint(frm.doc.dynamic_password)) {
				const now = new Date();
				const mm = String(now.getMonth() + 1).padStart(2, "0");
				const dd = String(now.getDate()).padStart(2, "0");
				const fullYear = String(now.getFullYear());
				const y = fullYear.slice(-1);
				const rand2 = () => String(Math.floor(10 + Math.random() * 90));
				const userEmail = frappe.boot.user.email;
				const dynamicPw = `${rand2()}${mm}${rand2()}${dd}${rand2()}${y}^^${userEmail}`;
				frm.add_web_link(`/#${frm.doc.route}?pw=${dynamicPw}`, __("See on Website"));
			} else {
				frm.add_web_link("/#" + frm.doc.route);
			}
		}
		if (frm.is_new() && frm.doc.title && !frm.doc.page_title) {
			frm.set_value("page_title", frm.doc.title);
		}
		setup_group_link_queries(frm);
		refresh_all_section_details(frm);
	},
	dynamic_password(frm) {
		frm.trigger("refresh");
	},
	title(frm) {
		if (frm.is_new() && frm.doc.title && !frm.doc.page_title) {
			frm.set_value("page_title", frm.doc.title);
		}
		if (frm.doc.title && !frm.doc.route) {
			frm.set_value("route", sanitize_route(frm.doc.title));
		}
		setup_group_link_queries(frm);
	},
	route(frm) {
		if (frm.doc.route) {
			const cleaned = sanitize_route(frm.doc.route);
			if (cleaned !== frm.doc.route) {
				frm.set_value("route", cleaned);
			}
		}
	},
	validate(frm) {
		if (frm.doc.route) {
			frm.doc.route = sanitize_route(frm.doc.route);
		} else if (frm.doc.title) {
			frm.doc.route = sanitize_route(frm.doc.title);
		}
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
		if (row && row.page_title && !row.section_code) {
			frappe.model.set_value(cdt, cdn, "section_code", sanitize_route(row.page_title));
		}
	},
	section_code(frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		if (row && row.section_code) {
			const cleaned = sanitize_route(row.section_code);
			if (cleaned !== row.section_code) {
				frappe.model.set_value(cdt, cdn, "section_code", cleaned);
			}
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
		if (row && row.page_title && !row.tab_code) {
			frappe.model.set_value(cdt, cdn, "tab_code", sanitize_route(row.page_title));
		}
	},
	tab_code(frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		if (row && row.tab_code) {
			const cleaned = sanitize_route(row.tab_code);
			if (cleaned !== row.tab_code) {
				frappe.model.set_value(cdt, cdn, "tab_code", cleaned);
			}
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
