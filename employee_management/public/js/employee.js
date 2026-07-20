frappe.ui.form.on('Employee', {
	refresh: function (frm) {
		if (!frm.is_new() && !frm.doc.v_card_url) {
			frm.add_custom_button(__('Generate V Card'), function () {
				frappe.call({
					method: 'employee_management.api.generate_v_card',
					args: {
						employee: frm.doc.name
					},
					callback: function (r) {
						if (r.message) {
							frm.reload_doc();
							frappe.show_alert({
								message: __('V-Card URL generated successfully!'),
								indicator: 'green'
							});
						}
					}
				});
			});
		}
	}
});
