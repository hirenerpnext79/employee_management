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
	if (!control || !control.$input) return;

	let $input = control.$input;
	let $wrapper = control.$wrapper;

	if (!document.getElementById("hns_password_eye_style")) {
		frappe.dom.set_style(`
			.hns-eye-btn {
				display: flex !important;
				align-items: center;
				justify-content: center;
				cursor: pointer !important;
				position: absolute;
				right: 8px;
				top: 0;
				height: 28px;
				z-index: 10;
				padding: 0 4px;
				color: var(--text-muted);
			}
			.hns-eye-btn:hover {
				color: var(--text-color);
			}
			.frappe-control[data-fieldname="${fieldname}"] .toggle-password {
				display: none !important;
			}
		`, "hns_password_eye_style");
	}

	$wrapper.find(".toggle-password").hide();
	$wrapper.find(".hns-eye-btn").remove();

	let input_height = $input.outerHeight() || 28;
	let $eye = $(`
		<div class="hns-eye-btn" title="${__('Toggle Password Visibility')}" style="height: ${input_height}px; top: 0; right: 8px;">
			${frappe.utils.icon("unhide", "sm")}
		</div>
	`).insertAfter($input);

	let is_revealed = false;

	$input.off("input.hns_pwd keyup.hns_pwd").on("input.hns_pwd keyup.hns_pwd", function() {
		frm._user_typed_password = frm._user_typed_password || {};
		frm._user_typed_password[fieldname] = true;
	});

	$eye.on("click", function(e) {
		e.preventDefault();
		e.stopPropagation();

		is_revealed = !is_revealed;

		if (is_revealed) {
			let user_typed = frm._user_typed_password && frm._user_typed_password[fieldname];

			if (!user_typed && !frm.is_new()) {
				if (frm._decrypted_password && frm._decrypted_password[fieldname]) {
					$input.val(frm._decrypted_password[fieldname]);
					$input.attr("type", "text");
					$eye.html(frappe.utils.icon("hide", "sm"));
				} else {
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
							frm._decrypted_password = frm._decrypted_password || {};
							frm._decrypted_password[fieldname] = pwd;
							$input.val(pwd);
							$input.attr("type", "text");
							$eye.html(frappe.utils.icon("hide", "sm"));
						}
					});
				}
			} else {
				$input.attr("type", "text");
				$eye.html(frappe.utils.icon("hide", "sm"));
			}
		} else {
			$input.attr("type", "password");
			$eye.html(frappe.utils.icon("unhide", "sm"));
			let user_typed = frm._user_typed_password && frm._user_typed_password[fieldname];
			if (!user_typed && !frm.is_new()) {
				$input.val(control.value || "••••••••");
			}
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
		if (window.hns_portal_group && window.hns_portal_group.setup_password_eye) {
			window.hns_portal_group.setup_password_eye(frm, "password");
		}
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
