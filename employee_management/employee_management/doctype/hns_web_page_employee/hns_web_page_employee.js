// Copyright (c) 2026, HNS and contributors
// For license information, please see license.txt

function ensure_portal_group_helper(callback) {
	if (window.hns_portal_group) {
		callback(window.hns_portal_group);
	} else {
		frappe.require("/assets/employee_management/js/portal_group_selector.js", function() {
			callback(window.hns_portal_group);
		});
	}
}

function set_child_enable_disable(frm, table_field, val) {
	let rows = frm.doc[table_field] || [];
	rows.forEach(row => {
		frappe.model.set_value(row.doctype, row.name, "enable_disable", val);
	});
	frm.refresh_field(table_field);
}

function sync_parent_enable_disable_all(frm, table_field) {
	let rows = frm.doc[table_field] || [];
	let all_enabled = rows.length > 0 && rows.every(r => Boolean(r.enable_disable));
	let current_val = frm.doc.enable_disable_all ? 1 : 0;
	let target_val = all_enabled ? 1 : 0;
	if (current_val !== target_val) {
		frm.set_value("enable_disable_all", target_val);
	}
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

frappe.ui.form.on("Hns Web Page Employee", {
	refresh: async function(frm) {
		setup_password_eye(frm, "password");
		ensure_portal_group_helper(helper => {
			helper.setup_portal_codes(frm, "hns_web_page_employee_details", "Hns Web Page Employee Details");
		});
		if (!frm.is_new() && frm.doc.select_portal && frm.doc.web_code) {
			let response = await frappe.db.get_value("Hns Web Page Creation", frm.doc.select_portal, "route");
			if (response && response.message && response.message.route) {
				frm.add_web_link("/#" + response.message.route + "?web_code=" + frm.doc.web_code);
			}
		}
		if (!frm.is_new() && !frm.doc.user) {
			frm.add_custom_button(__("Create User"), () => frm.trigger("create_user"));
		}
		if (!frm.is_new()) {
			frm.add_custom_button(__("Send Email"), () => frm.trigger("send_email"));
			frm.add_custom_button(__("Send WhatsApp"), () => frm.trigger("send_whatsapp"));
		}
	},

	user(frm) {
		if (frm.doc.user) {
			frm.remove_custom_button(__("Create User"));
			frappe.db.get_value("Hns Web Page User", frm.doc.user, "email").then(r => {
				if (r && r.message && r.message.email && !frm.doc.user_email) {
					frm.set_value("user_email", r.message.email);
				}
			});
		} else if (!frm.is_new()) {
			frm.add_custom_button(__("Create User"), () => frm.trigger("create_user"));
		}
	},

	employee(frm) {
		if (frm.doc.employee && !frm.doc.user_email) {
			frappe.db.get_value("Employee", frm.doc.employee, ["prefered_email", "company_email", "personal_email", "user_id"]).then(r => {
				if (r && r.message) {
					let email = r.message.prefered_email || r.message.company_email || r.message.personal_email;
					if (email) {
						frm.set_value("user_email", email);
					}
					if (r.message.user_id && !frm.doc.user) {
						frm.set_value("user", r.message.user_id);
					}
				}
			});
		}
	},

	create_user(frm) {
		if (!frm.doc.user_email) {
			frappe.msgprint(__("Please enter User Email first."));
			return;
		}
		frappe.call({
			method: "employee_management.api.create_portal_user",
			args: {
				doctype: frm.doc.doctype,
				docname: frm.doc.name
			},
			freeze: true,
			freeze_message: __("Creating User..."),
			callback: function(r) {
				if (r.message && r.message.user) {
					frm.set_value("user", r.message.user);
					frm.remove_custom_button(__("Create User"));
					frm.refresh_fields(["user", "user_email"]);
				}
			}
		});
	},

	send_email(frm) {
		if (!frm.doc.user_email) {
			frappe.msgprint(__("Please enter User Email first."));
			return;
		}
		frappe.confirm(
			__("Are you sure you want to send portal access email to {0}?", [frm.doc.user_email]),
			function() {
				frappe.call({
					method: "employee_management.api.send_portal_access_email",
					args: {
						doctype: frm.doc.doctype,
						docname: frm.doc.name
					},
					freeze: true,
					freeze_message: __("Sending Email..."),
					callback: function(r) {
						if (r.message && r.message.success) {
							frappe.show_alert({
								message: __("Email sent successfully to {0}", [frm.doc.user_email]),
								indicator: "green"
							});
						}
					}
				});
			}
		);
	},

	send_whatsapp(frm) {
		frappe.call({
			method: "employee_management.api.get_portal_whatsapp_details",
			args: {
				doctype: frm.doc.doctype,
				docname: frm.doc.name
			},
			freeze: true,
			freeze_message: __("Preparing WhatsApp message..."),
			callback: function(r) {
				if (r.message && r.message.url) {
					window.open(r.message.url, "_blank");
				}
			}
		});
	},

	enable_disable_all(frm) {
		set_child_enable_disable(frm, "hns_web_page_employee_details", frm.doc.enable_disable_all ? 1 : 0);
	},

	select_portal(frm) {
		ensure_portal_group_helper(helper => {
			helper.setup_portal_codes(frm, "hns_web_page_employee_details", "Hns Web Page Employee Details", true);
		});
	},

	fetch_portal_group(frm) {
		if (!frm.doc.select_portal) {
			frappe.msgprint(__("Please select a Portal first."));
			return;
		}
		ensure_portal_group_helper(helper => {
			helper.show_dialog(frm, {
				parent_doctype: "Hns Web Page Employee",
				child_table: "hns_web_page_employee_details",
				child_doctype: "Hns Web Page Employee Details",
				has_item: false
			});
		});
	},

	hns_web_page_employee_details_add(frm, cdt, cdn) {
		ensure_portal_group_helper(helper => {
			helper.set_row_code_options(frm, cdt, cdn, "hns_web_page_employee_details", "Hns Web Page Employee Details");
		});
		if (frm.doc.enable_disable_all) {
			frappe.model.set_value(cdt, cdn, "enable_disable", 1);
		}
	}
});

frappe.ui.form.on("Hns Web Page Employee Details", {
	web_page_code_type(frm, cdt, cdn) {
		ensure_portal_group_helper(helper => {
			helper.on_code_type_change(frm, cdt, cdn, "hns_web_page_employee_details", "Hns Web Page Employee Details");
		});
	},

	form_render(frm, cdt, cdn) {
		ensure_portal_group_helper(helper => {
			helper.set_row_code_options(frm, cdt, cdn, "hns_web_page_employee_details", "Hns Web Page Employee Details");
		});
	},

	enable_disable(frm, cdt, cdn) {
		sync_parent_enable_disable_all(frm, "hns_web_page_employee_details");
	}
});
