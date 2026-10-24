frappe.ui.form.on("File", {
	refresh: function (frm) {
		render_google_drive_preview(frm);
	},
	file_url: function (frm) {
		render_google_drive_preview(frm);
	}
});

function get_google_drive_file_id(url) {
	if (!url) return null;
	let match = url.match(/\/d\/([a-zA-Z0-9_-]+)/);
	if (match) return match[1];
	match = url.match(/[?&]id=([a-zA-Z0-9_-]+)/);
	if (match) return match[1];
	return null;
}

function render_google_drive_preview(frm) {
	if (!frm || !frm.doc || frm.doc.is_folder || !frm.doc.file_url) {
		$(".custom-google-drive-preview-wrapper").remove();
		frm._gdrive_preview_id = null;
		return;
	}

	let file_id = get_google_drive_file_id(frm.doc.file_url);
	if (!file_id) {
		$(".custom-google-drive-preview-wrapper").remove();
		frm._gdrive_preview_id = null;
		return;
	}

	if (frm.layout && frm.layout.wrapper) {
		frm.layout.wrapper.find('[data-fieldname="preview"]').hide();
	}
	if (frm.fields_dict && frm.fields_dict["preview_html"] && frm.fields_dict["preview_html"].$wrapper) {
		frm.fields_dict["preview_html"].$wrapper.hide();
	}

	let $existing = $(".custom-google-drive-preview-wrapper");
	if ($existing.length && frm._gdrive_preview_id === file_id) {
		$existing.show();
		return;
	}

	$existing.remove();
	frm._gdrive_preview_id = file_id;

	let preview_html = `
		<div class="google-drive-file-box" style="width: 100%; box-sizing: border-box; border: 1px solid #d1d8dd; border-radius: 8px; overflow: hidden; background: #ffffff; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin: 0;">
			<div style="background: #f8fafc; padding: 12px 16px; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: space-between; gap: 10px; flex-wrap: wrap;">
				<div style="display: flex; align-items: center; gap: 10px;">
					<span style="display: inline-flex; align-items: center; justify-content: center; width: 32px; height: 32px; background: #eff6ff; border-radius: 6px; border: 1px solid #dbeafe;">
						<svg width="20" height="20" viewBox="0 0 87.3 78" xmlns="http://www.w3.org/2000/svg">
							<path d="m6.6 66.85 3.85 6.65c.8 1.4 1.95 2.5 3.3 3.3l13.75-23.8H0c0 1.55.4 3.1 1.2 4.5z" fill="#0066da"/>
							<path d="m43.65 25-13.75-23.8c-1.35.8-2.5 1.9-3.3 3.3l-25.4 44c-.8 1.4-1.2 2.95-1.2 4.5h27.5z" fill="#00ac47"/>
							<path d="m73.55 76.8c1.35-.8 2.5-1.9 3.3-3.3l1.6-2.75 7.65-13.25c.8-1.4 1.2-2.95 1.2-4.5H59.8l5.85 10.15z" fill="#ea4335"/>
							<path d="m43.65 25 13.75-23.8c-1.35-.8-2.9-1.2-4.5-1.2H34.4c-1.6 0-3.15.45-4.5 1.2z" fill="#00832d"/>
							<path d="m59.8 53H32.4L18.65 76.8c1.35.8 2.9 1.2 4.5 1.2h50.4c1.6 0 3.15-.45 4.5-1.2z" fill="#2684fc"/>
							<path d="m73.4 26.5-12.7-22c-.8-1.4-1.95-2.5-3.3-3.3L43.65 25l16.15 28h27.5c0-1.55-.4-3.1-1.2-4.5z" fill="#ffba00"/>
						</svg>
					</span>
					<div>
						<div class="gdrive-preview-title" style="font-weight: 600; font-size: 14px; color: #1e293b;">
							${frappe.utils.escape_html(frm.doc.file_name || "Google Drive File")}
						</div>
						<div style="font-size: 11px; color: #64748b;">
							File ID: <code style="font-size: 11px; color: #0f766e; background: #f0fdfa; padding: 1px 5px; border-radius: 3px; border: 1px solid #ccfbf1;">${file_id}</code>
						</div>
					</div>
				</div>

				<div style="display: flex; align-items: center; gap: 8px;">
					<a href="https://drive.google.com/file/d/${file_id}/view" target="_blank" class="btn btn-default btn-xs" style="display: inline-flex; align-items: center; gap: 5px; font-weight: 500; font-size: 12px; padding: 4px 10px; border-radius: 5px;">
						<i class="fa fa-external-link" style="font-size: 11px;"></i>
						<span>Open in Drive</span>
					</a>
					<a href="https://drive.google.com/uc?id=${file_id}&export=download" target="_blank" class="btn btn-default btn-xs" style="display: inline-flex; align-items: center; gap: 5px; font-weight: 500; font-size: 12px; padding: 4px 10px; border-radius: 5px;">
						<i class="fa fa-download" style="font-size: 11px;"></i>
						<span>Download</span>
					</a>
				</div>
			</div>

			<div style="padding: 16px;">
				<div class="gdrive-preview-content-area" style="position: relative; width: 100%; min-height: 400px; background: #000000; border-radius: 6px; overflow: hidden; border: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: center;">
					<div style="text-align: center; color: #94a3b8; font-size: 13px;">
						<i class="fa fa-spinner fa-spin" style="font-size: 20px; margin-bottom: 8px;"></i>
						<div>${__("Loading preview...")}</div>
					</div>
				</div>
			</div>
		</div>
	`;

	let $preview_section = $(`
		<div class="custom-google-drive-preview-wrapper" style="display: block !important; margin-top: 25px; margin-bottom: 25px; width: 100%; clear: both;">
			<div style="padding: 10px 15px; margin-bottom: 8px; font-weight: 600; font-size: 13px; color: #1e293b; letter-spacing: 0.3px;">
				${__("Preview")}
			</div>
			<div style="width: 100%; padding: 0 15px 15px 15px; box-sizing: border-box;">
				${preview_html}
			</div>
		</div>
	`);

	let $target = null;
	if (frm.fields_dict && frm.fields_dict["file_url"] && frm.fields_dict["file_url"].$wrapper) {
		$target = frm.fields_dict["file_url"].$wrapper.closest(".form-section");
	}
	if ((!$target || !$target.length) && frm.layout && frm.layout.wrapper) {
		$target = frm.layout.wrapper.find('[data-fieldname="section_break_5"]');
	}
	if ((!$target || !$target.length) && frm.$wrapper) {
		$target = frm.$wrapper.find('[data-fieldname="section_break_5"]');
	}

	if ($target && $target.length) {
		$target.after($preview_section);
	} else if (frm.fields_dict && frm.fields_dict["file_url"] && frm.fields_dict["file_url"].$wrapper) {
		frm.fields_dict["file_url"].$wrapper.after($preview_section);
	} else if (frm.layout && frm.layout.page) {
		frm.layout.page.append($preview_section);
	}

	if (frm._gdrive_preview_data && frm._gdrive_preview_data.file_id === file_id) {
		render_content_box($preview_section, frm._gdrive_preview_data, file_id, frm);
		return;
	}

	frappe.call({
		method: "check_google_drive_status",
		args: {
			file_id: file_id,
			docname: frm.doc.name
		},
		callback: function (r) {
			let data = r.message || { status: "fallback" };
			frm._gdrive_preview_data = data;
			render_content_box($preview_section, data, file_id, frm);
		},
		error: function () {
			let fallback_data = { status: "fallback" };
			frm._gdrive_preview_data = fallback_data;
			render_content_box($preview_section, fallback_data, file_id, frm);
		}
	});
}

function render_content_box($container, data, file_id, frm) {
	let $box = $container.find(".gdrive-preview-content-area");
	if (!$box.length) return;

	let preview_url = (data && data.preview_url) || `https://drive.google.com/file/d/${file_id}/preview`;
	let view_url = (data && data.view_url) || `https://drive.google.com/file/d/${file_id}/view`;
	
	let file_name = "";
	if (frm && frm.doc && frm.doc.file_name && !frm.doc.file_name.startsWith("view")) {
		file_name = frm.doc.file_name;
	} else if (data && data.filename && data.filename !== file_id && !data.filename.startsWith("view")) {
		file_name = data.filename;
	} else if (frm && frm.doc && frm.doc.file_name) {
		file_name = frm.doc.file_name;
	} else if (data && data.filename) {
		file_name = data.filename;
	}

	if (file_name) {
		$container.find(".gdrive-preview-title").text(file_name);
	}

	let mime = (data && data.mime_type) || "";
	let lower_name = file_name.toLowerCase();

	let is_video = (data && data.is_video) 
		|| /\.(webm|mp4|mov|avi|mkv|m4v|3gp|flv|wmv)$/i.test(lower_name) 
		|| lower_name.startsWith("vid-") 
		|| lower_name.startsWith("aud-")
		|| mime.startsWith("video/");

	let is_audio = (data && data.is_audio) 
		|| /\.(mp3|wav|ogg|aac|m4a|flac|opus)$/i.test(lower_name) 
		|| mime.startsWith("audio/");

	// 1. Videos & Audio Recordings (like AUD-*.webm, .mp4, etc.): Full Google Drive Video Player
	if (is_video) {
		$box.html(`
			<div style="position: relative; width: 100%; height: 560px; background: #000000; border-radius: 6px; overflow: hidden; display: flex; flex-direction: column;">
				<iframe 
					src="${preview_url}" 
					style="width: 100%; height: 100%; border: none; background: #000000;" 
					allow="autoplay; encrypted-media; fullscreen" 
					allowfullscreen>
				</iframe>
			</div>
		`);
		return;
	}

	// 2. Audio files (.mp3, .wav)
	if (is_audio) {
		$box.html(`
			<div style="position: relative; width: 100%; height: 260px; background: #000000; border-radius: 6px; overflow: hidden; display: flex; align-items: center; justify-content: center;">
				<iframe 
					src="${preview_url}" 
					style="width: 100%; height: 100%; border: none; background: #000000;" 
					allow="autoplay; encrypted-media">
				</iframe>
			</div>
		`);
		return;
	}

	// 3. Images: Direct high-res CDN render
	if (data && data.image_url) {
		$box.html(`
			<div style="width: 100%; text-align: center; background: #0f172a; padding: 24px; border-radius: 6px; min-height: 450px; display: flex; align-items: center; justify-content: center;">
				<img src="${data.image_url}" onerror="this.onerror=null; this.parentElement.innerHTML='<iframe src=\\'${preview_url}\\' style=\\'width:100%;height:600px;border:none;background:#ffffff;\\' allow=\\'autoplay; encrypted-media; fullscreen\\' allowfullscreen></iframe>';" style="max-width: 100%; max-height: 600px; object-fit: contain; border-radius: 4px; box-shadow: 0 4px 14px rgba(0,0,0,0.4);" />
			</div>
		`);
		return;
	}

	// 4. PDFs and all other documents
	$box.html(`
		<div style="position: relative; width: 100%; height: 650px; background: #f8fafc; border-radius: 6px; overflow: hidden;">
			<iframe 
				src="${preview_url}" 
				style="width: 100%; height: 100%; border: none; background: #ffffff;" 
				allow="autoplay; encrypted-media; fullscreen" 
				allowfullscreen>
			</iframe>
		</div>
	`);
}
