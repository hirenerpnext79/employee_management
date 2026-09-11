// Copyright (c) 2026, HNS and contributors
// For license information, please see license.txt

frappe.ui.form.on('VCard', {
	refresh: function(frm) {
		if (frm.doc.vcard_id && !frm.is_new()) {
			let vcard_url = frappe.urllib.get_base_url() + "/" + frm.doc.vcard_id;
			let qr_api_url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=" + encodeURIComponent(vcard_url);
			
			let html = `<div style="display: flex; gap: 40px; justify-content: center; margin: 20px 0; flex-wrap: wrap;">`;
			
			// VCard QR
			html += `
				<div style="text-align: center;">
					<img src="${qr_api_url}" style="border: 1px solid #d1d8dd; border-radius: 4px; padding: 10px; background: white;" alt="VCard QR"/>
					<div style="margin-top: 10px; font-weight: bold; color: #36414c;">Profile QR Code</div>
					<button type="button" class="btn btn-xs btn-default" onclick="fetch(&quot;${qr_api_url}&quot;).then(r=>r.blob()).then(b=>{let reader=new FileReader();reader.onload=()=>{let a=document.createElement(&quot;a&quot;);a.href=reader.result;a.download=&quot;${frm.doc.vcard_id}_profile_qr.png&quot;;a.click();};reader.readAsDataURL(b);})" style="margin-top: 5px;">Download</button>
				</div>
			`;
			
			// WhatsApp QR
			if (frm.doc.mobile_no) {
				let wa_url = "https://wa.me/" + frm.doc.mobile_no.replace(/\D/g, '');
				let wa_qr_api_url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=" + encodeURIComponent(wa_url);
				html += `
				<div style="text-align: center;">
					<img src="${wa_qr_api_url}" style="border: 1px solid #d1d8dd; border-radius: 4px; padding: 10px; background: white;" alt="WhatsApp QR"/>
					<div style="margin-top: 10px; font-weight: bold; color: #36414c;">WhatsApp QR</div>
					<button type="button" class="btn btn-xs btn-default" onclick="fetch(&quot;${wa_qr_api_url}&quot;).then(r=>r.blob()).then(b=>{let reader=new FileReader();reader.onload=()=>{let a=document.createElement(&quot;a&quot;);a.href=reader.result;a.download=&quot;${frm.doc.vcard_id}_whatsapp_qr.png&quot;;a.click();};reader.readAsDataURL(b);})" style="margin-top: 5px;">Download</button>
				</div>
				`;
			}
			
			html += `</div>`;
			
			frm.set_df_property('qr_code_html', 'options', html);

			// Add custom button to visit VCard
			frm.add_custom_button(__('Visit VCard'), function() {
				window.open(vcard_url, '_blank');
			});
		} else {
			frm.set_df_property('qr_code_html', 'options', `<div style="text-align: center; margin: 20px 0;"></div>`);
		}
	},

	employee: function(frm) {
		if (frm.doc.employee) {
			frappe.db.get_value('Employee', frm.doc.employee, 
				['employee_name', 'gender', 'date_of_birth', 'designation', 'department', 'user_id', 'company'], 
				function(r) {
					if (r) {
						frm.set_value('full_name', r.employee_name);
						frm.set_value('gender', r.gender);
						frm.set_value('date_of_birth', r.date_of_birth);
						frm.set_value('designation', r.designation);
						frm.set_value('department', r.department);
						frm.set_value('company', r.company);
						
						if (r.user_id && r.user_id !== frm.doc.user) {
							frm.set_value('user', r.user_id);
						}
					}
				}
			);
		} else {
			frm.set_value('full_name', '');
			frm.set_value('gender', '');
			frm.set_value('date_of_birth', '');
			frm.set_value('designation', '');
			frm.set_value('department', '');
			frm.set_value('company', '');
			frm.set_value('user', '');
		}
	},

	user: function(frm) {
		if (frm.doc.user) {
			frappe.db.get_value('User', frm.doc.user, 
				['mobile_no', 'location', 'phone', 'email'], 
				function(r) {
					if (r) {
						frm.set_value('mobile_no', r.mobile_no);
						frm.set_value('location', r.location);
						frm.set_value('phone', r.phone);
						frm.set_value('email', r.email);
					}
				}
			);
		} else {
			frm.set_value('mobile_no', '');
			frm.set_value('location', '');
			frm.set_value('phone', '');
			frm.set_value('email', '');
		}
	}
});
