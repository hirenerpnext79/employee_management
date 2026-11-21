// Copyright (c) 2026, HNS and contributors
// For license information, please see license.txt

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
