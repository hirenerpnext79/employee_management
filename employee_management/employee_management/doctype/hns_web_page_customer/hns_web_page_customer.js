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

frappe.ui.form.on("Hns Web Page Customer", {
	refresh: async function(frm) {
		setup_password_eye(frm, "password");
		ensure_portal_group_helper(helper => {
			helper.setup_portal_codes(frm, "hns_price_list_details", "Hns Web Page Customer Details");
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

	party_name(frm) {
		if (frm.doc.party_type === "Customer" && frm.doc.party_name && !frm.doc.user_email) {
			frappe.db.get_value("Customer", frm.doc.party_name, ["email_id", "custom_hns_email"]).then(r => {
				if (r && r.message) {
					let email = r.message.email_id || r.message.custom_hns_email;
					if (email) {
						frm.set_value("user_email", email);
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
					frappe.show_alert({
						message: __("User {0} created successfully.", [r.message.user]),
						indicator: "green"
					});
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
		set_child_enable_disable(frm, "hns_price_list_details", frm.doc.enable_disable_all ? 1 : 0);
	},

	select_portal(frm) {
		ensure_portal_group_helper(helper => {
			helper.setup_portal_codes(frm, "hns_price_list_details", "Hns Web Page Customer Details", true);
		});
	},

	fetch_portal_group(frm) {
		if (!frm.doc.select_portal) {
			frappe.msgprint(__("Please select a Portal first."));
			return;
		}
		ensure_portal_group_helper(helper => {
			helper.show_dialog(frm, {
				parent_doctype: "Hns Web Page Customer",
				child_table: "hns_price_list_details",
				child_doctype: "Hns Web Page Customer Details",
				has_item: true
			});
		});
	},

	hns_price_list_details_add(frm, cdt, cdn) {
		ensure_portal_group_helper(helper => {
			helper.set_row_code_options(frm, cdt, cdn, "hns_price_list_details", "Hns Web Page Customer Details");
		});
		if (frm.doc.enable_disable_all) {
			frappe.model.set_value(cdt, cdn, "enable_disable", 1);
		}
	}
});

frappe.ui.form.on("Hns Web Page Customer Details", {
	web_page_code_type(frm, cdt, cdn) {
		ensure_portal_group_helper(helper => {
			helper.on_code_type_change(frm, cdt, cdn, "hns_price_list_details", "Hns Web Page Customer Details");
		});
	},

	form_render(frm, cdt, cdn) {
		ensure_portal_group_helper(helper => {
			helper.set_row_code_options(frm, cdt, cdn, "hns_price_list_details", "Hns Web Page Customer Details");
		});
	},

	enable_disable(frm, cdt, cdn) {
		sync_parent_enable_disable_all(frm, "hns_price_list_details");
	}
});
