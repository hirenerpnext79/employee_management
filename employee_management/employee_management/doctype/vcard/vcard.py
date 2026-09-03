# Copyright (c) 2026, HNS and contributors
# For license information, please see license.txt

import frappe
import random
import requests
from frappe.model.document import Document

class VCard(Document):
	def before_save(self):
		if not self.vcard_id:
			self.vcard_id = self.generate_unique_vcard_id()
			
		if self.employee:
			image_url = frappe.db.get_value("Employee", self.employee, "image")
			if image_url:
				if "/file/d/" in image_url:
					try:
						file_id = image_url.split("/file/d/")[1].split("/")[0]
						download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
						
						response = requests.get(download_url, timeout=30)
						response.raise_for_status()
						
						file_doc = frappe.get_doc({
							"doctype": "File",
							"file_name": f"{file_id}.jpg",
							"content": response.content,
							"is_private": 0
						})
						file_doc.insert(ignore_permissions=True)
						self.user_photo = file_doc.file_url
					except Exception as e:
						frappe.log_error(title="VCard Image Fetch Error", message=str(e))
						self.user_photo = f"https://drive.google.com/uc?export=view&id={file_id}" if 'file_id' in locals() else image_url
				else:
					self.user_photo = image_url

	def generate_unique_vcard_id(self):
		while True:
			new_id = str(random.randint(10000, 99999))
			if not frappe.db.exists("VCard", {"vcard_id": new_id}):
				return new_id
