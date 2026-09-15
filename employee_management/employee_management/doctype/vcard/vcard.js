// Copyright (c) 2026, HNS and contributors
// For license information, please see license.txt

frappe.ui.form.on('VCard', {
	render_qr_codes: function(frm) {
		if (frm.doc.vcard_id && !frm.is_new()) {
			let vcard_url = frappe.urllib.get_base_url() + "/" + frm.doc.vcard_id;
			let qr_api_url = "https://quickchart.io/qr?size=150&margin=0&light=0000&text=" + encodeURIComponent(vcard_url);
			
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
							window.html2canvas(el, {
								useCORS: true, 
								scale: 4, 
								allowTaint: true
							}).then(canvas => {
								let a = document.createElement('a');
								a.href = canvas.toDataURL('image/png');
								a.download = filename;
								a.click();
								
								frappe.dom.unfreeze();
								frappe.show_alert({message: __("Download successful"), indicator: "green"});
							}).catch(e => {
								console.error(e);
								
								frappe.dom.unfreeze();
								frappe.msgprint(__("Error generating image"));
							});
						} else {
							frappe.dom.unfreeze();
						}
					});
				};
			}

			if (!window.download_both_cards) {
				window.download_both_cards = function(front_id, back_id, filename) {
					frappe.dom.freeze(__("Preparing..."));
					frappe.require("https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js", function() {
						let front_el = document.getElementById(front_id);
						let back_el = document.getElementById(back_id);
						if (front_el && back_el) {
							let container = document.createElement('div');
							container.style.position = 'absolute';
							container.style.left = '-9999px';
							container.style.display = 'flex';
							container.style.flexDirection = 'column';
							container.style.gap = '30px';
							container.style.padding = '30px';
							container.style.background = '#ffffff';
							
							container.appendChild(front_el.cloneNode(true));
							container.appendChild(back_el.cloneNode(true));
							document.body.appendChild(container);
							
							window.html2canvas(container, {
								useCORS: true, 
								scale: 4, 
								allowTaint: true
							}).then(canvas => {
								let a = document.createElement('a');
								a.href = canvas.toDataURL('image/png');
								a.download = filename;
								a.click();
								document.body.removeChild(container);
								frappe.dom.unfreeze();
								frappe.show_alert({message: __("Download successful"), indicator: "green"});
							}).catch(e => {
								console.error(e);
								if (container.parentNode) document.body.removeChild(container);
								frappe.dom.unfreeze();
								frappe.msgprint(__("Error generating image"));
							});
						} else {
							frappe.dom.unfreeze();
						}
					});
				};
			}

			let fetch_theme_promise = Promise.resolve({});
			if (frm.doc.physical_card_theme) {
				fetch_theme_promise = new Promise(resolve => {
					frappe.db.get_value('Physical Card Theme', frm.doc.physical_card_theme, 
						['physical_card_bg', 'font_color', 'profile_qr_size', 'profile_qr_font_size', 'whatsapp_qr_size', 'whatsapp_qr_font_size', 'company_font_size', 'tag_line_font_size', 'tag_line_font_color', 'address_font_size', 'user_details_font_size', 'user_designation_font_size', 'user_whatsapp_font_size', 'user_mobile_font_size', 'user_email_font_size', 'logo_1_size', 'logo_2_size', 'logo_3_size', 'tag_line_position'], 
						(r) => { resolve((r && r.message) ? r.message : (r || {})); }
					);
				});
			}

			fetch_theme_promise.then(theme => {
				function get_absolute_url(url) {
					if (!url) return '';
					if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) return url;
					return frappe.urllib.get_base_url() + (url.startsWith('/') ? '' : '/') + url;
				}

				let bg_url = get_absolute_url(theme.physical_card_bg);
				let bg_css = theme.physical_card_bg ? (theme.physical_card_bg.startsWith('#') ? `background: ${theme.physical_card_bg};` : `background: url("${bg_url}") center center / cover no-repeat;`) : 'background: #fff;';
				let font_color = theme.font_color || '#333';
				
				let wa_icon = `<svg width="1.2em" height="1.2em" viewBox="0 0 24 24" fill="${font_color}" xmlns="http://www.w3.org/2000/svg" style="flex-shrink: 0;"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>`;
				let phone_icon = `<svg width="1.2em" height="1.2em" viewBox="0 0 24 24" fill="${font_color}" xmlns="http://www.w3.org/2000/svg" style="flex-shrink: 0;"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>`;
				let email_icon = `<svg width="1.2em" height="1.2em" viewBox="0 0 24 24" fill="${font_color}" xmlns="http://www.w3.org/2000/svg" style="flex-shrink: 0;"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>`;

				let physical_card_html_str = `
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
					${bg_css}
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
					flex-direction: column;
					justify-content: center;
					align-items: center;
				}
				.back-qr-wrapper {
					display: flex;
					flex-direction: row;
					justify-content: space-around;
					align-items: flex-start;
					width: 100%;
				}
				.back-side-text-container {
					width: 90%;
					text-align: center;
					margin-top: 15px;
					border-top: 1px solid ${font_color};
					padding-top: 10px;
					color: ${font_color};
					font-size: 12px;
				}
				.logos-container {
					display: flex;
					justify-content: space-between;
					align-items: center;
					width: 100%;
					position: absolute;
					top: 5px;
					left: 0;
					padding: 0 20px;
					box-sizing: border-box;
				}
				.logos-container .logo-wrapper {
					flex: 1;
					display: flex;
					align-items: center;
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
					font-size: ${frm.doc.company_font_size || theme.company_font_size || 20}px;
					font-weight: bold;
					color: ${font_color};
					word-wrap: break-word;
					word-break: break-word;
					overflow-wrap: break-word;
				}
				.bottom-section-wrapper {
					position: absolute;
					bottom: 5px;
					left: 20px;
					width: calc(100% - 40px);
					display: flex;
					flex-direction: column;
				}
				.contact-row {
					display: flex;
					align-items: center;
					gap: 6px;
					margin-bottom: 2px;
				}
				.company-address-card-container {
					width: 100%;
					border-top: 1px solid ${font_color};
					padding-top: 4px;
					box-sizing: border-box;
					font-size: ${theme.address_font_size || 8}px;
					color: ${font_color};
					line-height: 1.4;
				}
				.company-address-card-container::after {
					content: "";
					clear: both;
					display: table;
				}
				.middle-info-container {
					width: 100%;
					padding-bottom: 4px;
					box-sizing: border-box;
					color: ${font_color};
				}
				.middle-info-container::after {
					content: "";
					clear: both;
					display: table;
				}
				.info-left {
					float: left;
					text-align: left;
					width: 175px;
					line-height: 1.2;
					word-wrap: break-word;
					word-break: break-word;
					overflow-wrap: break-word;
				}
				.info-right {
					float: right;
					text-align: right;
					width: 175px;
					word-wrap: break-word;
					word-break: break-word;
					overflow-wrap: break-word;
					white-space: normal;
				}
				.address-left {
					float: left;
					width: 175px;
					text-align: left;
					word-wrap: break-word;
					word-break: break-word;
					overflow-wrap: break-word;
					white-space: normal;
				}
				.address-right {
					float: right;
					width: 175px;
					text-align: left;
					word-wrap: break-word;
					word-break: break-word;
					overflow-wrap: break-word;
					white-space: normal;
				}
				.qr-container-card {
					text-align: center;
				}
				.qr-container-card img {
					width: 140px;
					height: 140px;
					}
				.qr-label-card {
					font-size: 11px;
					margin-top: 8px;
					color: ${font_color};
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

			let logo_1_size = frm.doc.logo_1_size || theme.logo_1_size || 40;
			let logo_2_size = frm.doc.logo_2_size || theme.logo_2_size || 40;
			let logo_3_size = frm.doc.logo_3_size || theme.logo_3_size || 40;

			let logo1 = frm.doc.company_logo_1 ? `<img src="${get_absolute_url(frm.doc.company_logo_1)}" style="max-height: ${logo_1_size}px;" />` : '';
			let logo2 = frm.doc.company_logo_2 ? `<img src="${get_absolute_url(frm.doc.company_logo_2)}" style="max-height: ${logo_2_size}px;" />` : '';
			let logo3 = frm.doc.company_logo_3 ? `<img src="${get_absolute_url(frm.doc.company_logo_3)}" style="max-height: ${logo_3_size}px;" />` : '';
			
			let line1 = frm.doc.company_name_line_1;
			let line2 = frm.doc.company_name_line_2;
			let company_name = '';
			if (line1 && line2) {
				company_name = line1 + '<br>' + line2;
			} else if (line1 || line2) {
				company_name = line1 || line2;
			} else {
				company_name = frm.doc.company_name || frm.doc.company || '';
			}
			
			let address1 = frm.doc.company_address_1 ? frm.doc.company_address_1.replace(/\n/g, '<br>') : '';
			let address2 = frm.doc.company_address_2 ? frm.doc.company_address_2.replace(/\n/g, '<br>') : '';
			
			let full_name = frm.doc.full_name || '';
			let designation = frm.doc.designation || '';
			let phone = frm.doc.phone || '';
			let email = frm.doc.email || '';
			let tag_line = frm.doc.tag_line || '';
			let tag_line_position = (frm.doc.tag_line_position || theme.tag_line_position || 'Left').toLowerCase();
			let raw_back = frm.doc.back_side_text ? String(frm.doc.back_side_text) : '';
			let stripped_back = raw_back.replace(/<[^>]*>?/gm, '').replace(/&nbsp;/g, '').trim();
			let back_side_text = stripped_back ? raw_back : '';
			
			let wa_qr_api_url = "";
			if (frm.doc.mobile_no) {
				let wa_url = "https://wa.me/" + frm.doc.mobile_no.replace(/\D/g, '');
				wa_qr_api_url = "https://quickchart.io/qr?size=150&margin=0&light=0000&text=" + encodeURIComponent(wa_url);
			}

			let back_wa_qr_html = wa_qr_api_url ? `
				<div class="qr-container-card">
					<img src="${wa_qr_api_url}" style="width: ${frm.doc.whatsapp_qr_size || theme.whatsapp_qr_size || 100}%; height: ${frm.doc.whatsapp_qr_size || theme.whatsapp_qr_size || 100}%;" alt="WhatsApp QR" crossorigin="anonymous"/>
					<div class="qr-label-card" style="font-size: ${frm.doc.whatsapp_qr_font_size || theme.whatsapp_qr_font_size || 11}px;">WhatsApp QR</div>
				</div>
			` : '';

			// 1. INDIVIDUAL QR CODES (Moved to Top)
			let qr_code_html_str = `<div style="display: flex; gap: 40px; justify-content: center; margin: 20px 0; flex-wrap: wrap;">`;
			
			// Profile QR
			qr_code_html_str += `
				<div style="text-align: center;">
					<div style="display: flex; justify-content: center; align-items: center; gap: 8px; margin-bottom: 10px;">
						<span style="font-weight: bold; color: #36414c; font-size: 14px;">Profile QR Code</span>
						<button type="button" class="btn btn-xs btn-default" onclick="window.download_qr_code(&quot;${qr_api_url}&quot;, &quot;${frm.doc.vcard_id}_profile_qr.png&quot;)">Download</button>
					</div>
					<img src="${qr_api_url}" style="display: block; margin: 0 auto; width: 150px; height: 150px;" alt="VCard QR"/>
				</div>
			`;
			
			// WhatsApp QR
			if (wa_qr_api_url) {
				qr_code_html_str += `
				<div style="text-align: center;">
					<div style="display: flex; justify-content: center; align-items: center; gap: 8px; margin-bottom: 10px;">
						<span style="font-weight: bold; color: #36414c; font-size: 14px;">WhatsApp QR</span>
						<button type="button" class="btn btn-xs btn-default" onclick="window.download_qr_code(&quot;${wa_qr_api_url}&quot;, &quot;${frm.doc.vcard_id}_whatsapp_qr.png&quot;)">Download</button>
					</div>
					<img src="${wa_qr_api_url}" style="display: block; margin: 0 auto; width: 150px; height: 150px;" alt="WhatsApp QR"/>
				</div>
				`;
			}
			
			qr_code_html_str += `</div>`;



			// 2. PHYSICAL CARD PREVIEW (Moved to Bottom)
			physical_card_html_str += `
				<div style="text-align: center; margin-bottom: 20px;">
					<button type="button" class="btn btn-sm btn-primary" onclick="window.download_both_cards(&quot;front-card-preview&quot;, &quot;back-card-preview&quot;, &quot;${frm.doc.vcard_id}_full_card.png&quot;)">Download Full VCard (Front + Back)</button>
				</div>
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
							<div class="bottom-section-wrapper">
								${tag_line ? `<div style="font-size: ${frm.doc.tag_line_font_size || theme.tag_line_font_size || 14}px; font-weight: bold; margin-bottom: 15px; width: 100%; line-height: 1.2; text-align: ${tag_line_position}; color: ${frm.doc.tag_line_font_color || theme.tag_line_font_color || '#000000'};">${tag_line}</div>` : ''}
								<div class="middle-info-container">
									<div class="info-left">
										<div style="font-size: ${theme.user_details_font_size || 14}px; font-weight: bold;">${full_name}</div>
										<div style="font-size: ${theme.user_designation_font_size || 10}px; margin-bottom: 4px;">${designation}</div>
										<div style="margin-top: 6px; line-height: 1.2;">
											${frm.doc.mobile_no ? `<div class="contact-row" style="font-size: ${theme.user_whatsapp_font_size || 9}px;">${wa_icon}${frm.doc.mobile_no}</div>` : ''}
											${phone ? `<div class="contact-row" style="font-size: ${theme.user_mobile_font_size || 9}px;">${phone_icon}${phone}</div>` : ''}
											${email ? `<div class="contact-row" style="font-size: ${theme.user_email_font_size || 9}px;">${email_icon}${email}</div>` : ''}
										</div>
									</div>
									<div class="info-right">
										<div class="company-name-card">${company_name}</div>
									</div>
								</div>
								<div class="company-address-card-container">
									<div class="address-left">${address1}</div>
									<div class="address-right">${address2}</div>
								</div>
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
							<div class="back-qr-wrapper">
								<div class="qr-container-card">
									<img src="${qr_api_url}" style="width: ${frm.doc.profile_qr_size || theme.profile_qr_size || 50}%; height: ${frm.doc.profile_qr_size || theme.profile_qr_size || 50}%;" alt="Profile QR" crossorigin="anonymous"/>
									<div class="qr-label-card" style="font-size: ${frm.doc.profile_qr_font_size || theme.profile_qr_font_size || 11}px;">Profile QR Code</div>
								</div>
								${back_wa_qr_html}
							</div>
							${back_side_text ? `<div class="back-side-text-container">${back_side_text.replace(/\n/g, '<br>')}</div>` : ''}
						</div>
					</div>
				</div>
			`;
			
			frm.set_df_property('qr_code_html', 'options', qr_code_html_str);
				frm.refresh_field('qr_code_html');
				frm.set_df_property('physical_card_preview', 'options', physical_card_html_str);
				frm.refresh_field('physical_card_preview');
				
				if (frm.doc.physical_card_html !== physical_card_html_str) {
					frm.set_value('physical_card_html', physical_card_html_str);
				}

				if (!frm.custom_buttons || !frm.custom_buttons['Visit VCard']) {
					frm.add_custom_button(__('Visit VCard'), function() {
						window.open(vcard_url, '_blank');
					});
				}
			});
		} else {
			frm.set_df_property('qr_code_html', 'options', `<div style="text-align: center; margin: 20px 0;"></div>`);
			frm.set_df_property('physical_card_preview', 'options', `<div style="text-align: center; margin: 20px 0;"></div>`);
		}
	},
		refresh: function(frm) {
		frm.events.render_qr_codes(frm);
	},
	
	company_name: function(frm) { frm.events.render_qr_codes(frm); },
	company_name_line_1: function(frm) { frm.events.render_qr_codes(frm); },
	company_name_line_2: function(frm) { frm.events.render_qr_codes(frm); },
	company_address_1: function(frm) { frm.events.render_qr_codes(frm); },
	company_address_2: function(frm) { frm.events.render_qr_codes(frm); },
	company_logo_1: function(frm) { frm.events.render_qr_codes(frm); },
	company_logo_2: function(frm) { frm.events.render_qr_codes(frm); },
	company_logo_3: function(frm) { frm.events.render_qr_codes(frm); },
	mobile_no: function(frm) { frm.events.render_qr_codes(frm); },
	physical_card_theme: function(frm) { frm.events.render_qr_codes(frm); },
	profile_qr_size: function(frm) { frm.events.render_qr_codes(frm); },
	profile_qr_font_size: function(frm) { frm.events.render_qr_codes(frm); },
	whatsapp_qr_size: function(frm) { frm.events.render_qr_codes(frm); },
	whatsapp_qr_font_size: function(frm) { frm.events.render_qr_codes(frm); },
	company_font_size: function(frm) { frm.events.render_qr_codes(frm); },
	tag_line: function(frm) { frm.events.render_qr_codes(frm); },
	tag_line_font_size: function(frm) { frm.events.render_qr_codes(frm); },
	tag_line_font_color: function(frm) { frm.events.render_qr_codes(frm); },
	back_side_text: function(frm) { frm.events.render_qr_codes(frm); },

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
