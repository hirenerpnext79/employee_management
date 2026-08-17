// Copyright (c) 2026, HNS and contributors
// For license information, please see license.txt

frappe.ui.form.on('VCard', {
	refresh: function(frm) {
		if (frm.doc.vcard_id && !frm.is_new()) {
			// Replace the URL field href with the absolute URL for the frontend
			setTimeout(() => {
				let link = frm.get_field("vcard_id").$wrapper.find("a");
				if(link.length) {
					link.attr("href", frappe.urllib.get_base_url() + "/" + frm.doc.vcard_id);
					link.attr("target", "_blank");
				}
			}, 500);

			// Add custom button to visit VCard
			frm.add_custom_button(__('Visit VCard'), function() {
				window.open(frappe.urllib.get_base_url() + "/" + frm.doc.vcard_id, '_blank');
			});
		}
	}
});

