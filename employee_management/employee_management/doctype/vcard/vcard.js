// Copyright (c) 2026, HNS and contributors
// For license information, please see license.txt

frappe.ui.form.on('VCard', {
	render_qr_codes: function(frm) {
		if (frm.doc.vcard_id && !frm.is_new()) {
			let vcard_url = frappe.urllib.get_base_url() + "/" + frm.doc.vcard_id;
			let qr_api_url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=" + encodeURIComponent(vcard_url);
			
			if (!window.download_qr_code) {
				window.download_qr_code = function(url, filename) {
					frappe.dom.freeze(); frappe.show_alert({message: __("Downloading..."), indicator: "orange"});
					fetch(url)
						.then(r => r.blob())
						.then(b => {
							let reader = new FileReader();
							reader.onload = () => {
								let a = document.createElement("a");
								a.href = reader.result;
								a.download = filename;
								a.click();
								frappe.dom.unfreeze();
								frappe.show_alert({message: __("Download successful"), indicator: "green"});
							};
							reader.readAsDataURL(b);
						})
						.catch(e => {
							console.error(e);
							frappe.dom.unfreeze();
							frappe.msgprint(__("Error downloading QR Code"));
						});
				};
			}

			if (!window.download_card_image) {
				window.download_card_image = function(id, filename) {
					frappe.dom.freeze(__("Preparing..."));
					frappe.require("https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js", function() {
						let el = document.getElementById(id);
						if (el) {
							// Temporarily remove card background, border, and shadow for a clean transparent print
							let originalBackground = el.style.background;
							let originalBorder = el.style.border;
							let originalBoxShadow = el.style.boxShadow;
							
							el.style.background = 'transparent';
							el.style.border = 'none';
							el.style.boxShadow = 'none';

							window.html2canvas(el, {
								useCORS: true, 
								scale: 4, 
								allowTaint: true,
								backgroundColor: null // Force transparent canvas
							}).then(canvas => {
								let a = document.createElement('a');
								a.href = canvas.toDataURL('image/png');
								a.download = filename;
								a.click();
								
								// Restore original styles
								el.style.background = originalBackground;
								el.style.border = originalBorder;
								el.style.boxShadow = originalBoxShadow;
								
								frappe.dom.unfreeze();
								frappe.show_alert({message: __("Download successful"), indicator: "green"});
							}).catch(e => {
								console.error(e);
								el.style.background = originalBackground;
								el.style.border = originalBorder;
								el.style.boxShadow = originalBoxShadow;
								
								frappe.dom.unfreeze();
								frappe.msgprint(__("Error generating image"));
							});
						} else {
							frappe.dom.unfreeze();
						}
					});
				};
			}

			let html = `
				<style>
				.physical-card-preview {
					display: flex;
					gap: 30px;
					justify-content: center;
					margin: 20px 0 40px 0;
					flex-wrap: wrap;
				}
				.visiting-card {
					width: 400px;
					height: 220px;
					background: #fff;
					border: 1px solid #d1d8dd;
					border-radius: 8px;
					box-shadow: 0 4px 12px rgba(0,0,0,0.05);
					padding: 20px;
					box-sizing: border-box;
					display: flex;
					flex-direction: column;
					justify-content: center;
					position: relative;
				}
				.visiting-card-front {
					text-align: center;
				}
				.visiting-card-back {
					display: flex;
					flex-direction: row;
					justify-content: space-around;
					align-items: center;
				}
				.logos-container {
					display: flex;
					justify-content: space-between;
					align-items: flex-start;
					width: 100%;
					position: absolute;
					top: 20px;
					left: 0;
					padding: 0 20px;
					box-sizing: border-box;
				}
				.logos-container .logo-wrapper {
					flex: 1;
					display: flex;
				}
				.logos-container .logo-left { justify-content: flex-start; }
				.logos-container .logo-center { justify-content: center; }
				.logos-container .logo-right { justify-content: flex-end; }
				.logos-container img {
					max-height: 40px;
					max-width: 90px;
					object-fit: contain;
				}
				.company-name-card {
					font-size: 22px;
					font-weight: bold;
					color: #333;
					text-align: center;
				}
				.company-address-card-container {
					display: flex;
					justify-content: space-between;
					align-items: flex-end;
					width: 100%;
					position: absolute;
					bottom: 20px;
					left: 0;
					padding: 0 20px;
					box-sizing: border-box;
					font-size: 8px;
					color: #000;
					line-height: 1.4;
				}
				.address-left {
					max-width: 48%;
					text-align: left;
				}
				.address-right {
					max-width: 48%;
					text-align: right;
				}
				.qr-container-card {
					text-align: center;
				}
				.qr-container-card img {
					width: 140px;
					height: 140px;
					border: 1px solid #eaeaea;
					padding: 5px;
					border-radius: 4px;
					background: #fff;
				}
				.qr-label-card {
					font-size: 11px;
					margin-top: 8px;
					color: #555;
					font-weight: 600;
				}
				.card-title {
					text-align: center;
					font-weight: bold;
					margin-bottom: 15px;
					color: #36414c;
					font-size: 14px;
				}
				</style>
			`;

			let logo1 = frm.doc.company_logo_1 ? `<img src="${frm.doc.company_logo_1}" />` : '';
			let logo2 = frm.doc.company_logo_2 ? `<img src="${frm.doc.company_logo_2}" />` : '';
			let logo3 = frm.doc.company_logo_3 ? `<img src="${frm.doc.company_logo_3}" />` : '';
			let company_name = frm.doc.company_name || frm.doc.company || '';
			let address1 = frm.doc.company_address_1 ? frm.doc.company_address_1.replace(/\n/g, '<br>') : '';
			let address2 = frm.doc.company_address_2 ? frm.doc.company_address_2.replace(/\n/g, '<br>') : '';
			
			let wa_qr_api_url = "";
			if (frm.doc.mobile_no) {
				let wa_url = "https://wa.me/" + frm.doc.mobile_no.replace(/\D/g, '');
				wa_qr_api_url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=" + encodeURIComponent(wa_url);
			}

			let back_wa_qr_html = wa_qr_api_url ? `
				<div class="qr-container-card">
					<img src="${wa_qr_api_url}" alt="WhatsApp QR"/>
					<div class="qr-label-card">WhatsApp QR</div>
				</div>
			` : '';

			// 1. INDIVIDUAL QR CODES (Moved to Top)
			html += `<div style="display: flex; gap: 40px; justify-content: center; margin: 20px 0; flex-wrap: wrap;">`;
			
			// Profile QR
			html += `
				<div style="text-align: center;">
					<div style="display: flex; justify-content: center; align-items: center; gap: 8px; margin-bottom: 10px;">
						<span style="font-weight: bold; color: #36414c; font-size: 14px;">Profile QR Code</span>
						<button type="button" class="btn btn-xs btn-default" onclick="window.download_qr_code(&quot;${qr_api_url}&quot;, &quot;${frm.doc.vcard_id}_profile_qr.png&quot;)">Download</button>
					</div>
					<img src="${qr_api_url}" style="display: none; border: 1px solid #d1d8dd; border-radius: 4px; padding: 10px; background: white;" alt="VCard QR"/>
				</div>
			`;
			
			// WhatsApp QR
			if (wa_qr_api_url) {
				html += `
				<div style="text-align: center;">
					<div style="display: flex; justify-content: center; align-items: center; gap: 8px; margin-bottom: 10px;">
						<span style="font-weight: bold; color: #36414c; font-size: 14px;">WhatsApp QR</span>
						<button type="button" class="btn btn-xs btn-default" onclick="window.download_qr_code(&quot;${wa_qr_api_url}&quot;, &quot;${frm.doc.vcard_id}_whatsapp_qr.png&quot;)">Download</button>
					</div>
					<img src="${wa_qr_api_url}" style="display: none; border: 1px solid #d1d8dd; border-radius: 4px; padding: 10px; background: white;" alt="WhatsApp QR"/>
				</div>
				`;
			}
			
			html += `</div>`;

			html += `<hr style="margin: 30px 0; border-color: #d1d8dd;">`;

			// 2. PHYSICAL CARD PREVIEW (Moved to Bottom)
			html += `
				<div class="physical-card-preview">
					<!-- Front Side -->
					<div style="text-align: center;">
						<div class="card-title" style="display: flex; justify-content: center; align-items: center; gap: 8px;">
							Front Side
							<button type="button" class="btn btn-xs btn-default" onclick="window.download_card_image(&quot;front-card-preview&quot;, &quot;${frm.doc.vcard_id}_front_card.png&quot;)">Download</button>
						</div>
						<div class="visiting-card visiting-card-front" id="front-card-preview">
							<div class="logos-container">
								<div class="logo-wrapper logo-left">${logo1}</div>
								<div class="logo-wrapper logo-center">${logo2}</div>
								<div class="logo-wrapper logo-right">${logo3}</div>
							</div>
							<div class="company-name-card">${company_name}</div>
							<div class="company-address-card-container">
								<div class="address-left">${address1}</div>
								<div class="address-right">${address2}</div>
							</div>
						</div>
					</div>
					
					<!-- Back Side -->
					<div style="text-align: center;">
						<div class="card-title" style="display: flex; justify-content: center; align-items: center; gap: 8px;">
							Back Side
							<button type="button" class="btn btn-xs btn-default" onclick="window.download_card_image(&quot;back-card-preview&quot;, &quot;${frm.doc.vcard_id}_back_card.png&quot;)">Download</button>
						</div>
						<div class="visiting-card visiting-card-back" id="back-card-preview">
							<div class="qr-container-card">
								<img src="${qr_api_url}" alt="Profile QR"/>
								<div class="qr-label-card">Profile QR Code</div>
							</div>
							${back_wa_qr_html}
						</div>
					</div>
				</div>
			`;
						frm.set_df_property('qr_code_html', 'options', html);

			if (!frm.custom_buttons || !frm.custom_buttons['Visit VCard']) {
				frm.add_custom_button(__('Visit VCard'), function() {
					window.open(vcard_url, '_blank');
				});
			}
		} else {
			frm.set_df_property('qr_code_html', 'options', `<div style="text-align: center; margin: 20px 0;"></div>`);
		}
	},
		refresh: function(frm) {
		frm.events.render_qr_codes(frm);
	},
	
	company_name: function(frm) { frm.events.render_qr_codes(frm); },
	company_address_1: function(frm) { frm.events.render_qr_codes(frm); },
	company_address_2: function(frm) { frm.events.render_qr_codes(frm); },
	company_logo_1: function(frm) { frm.events.render_qr_codes(frm); },
	company_logo_2: function(frm) { frm.events.render_qr_codes(frm); },
	company_logo_3: function(frm) { frm.events.render_qr_codes(frm); },
	mobile_no: function(frm) { frm.events.render_qr_codes(frm); },

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
