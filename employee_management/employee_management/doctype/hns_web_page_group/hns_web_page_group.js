frappe.ui.form.on("Hns Web Page Group", {
	setup(frm) {
		frm.set_query("disallowed_roles", function () {
			return {
				filters: {
					mode: "Roles",
					is_active: 1,
				},
			};
		});
	}
});
