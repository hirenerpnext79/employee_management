// Copyright (c) 2026, HNS and contributors
// For license information, please see license.txt

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

frappe.ui.form.on("Hns Web Page User", {
	refresh(frm) {
		setup_password_eye(frm, "password");
	},

	email(frm) {
		if (frm.doc.email && (!frm.doc.user_name || frm.doc.user_name.includes("@"))) {
			frm.set_value("user_name", frm.doc.email.split("@")[0].trim());
		}
	}
});
