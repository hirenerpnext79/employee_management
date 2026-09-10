# Copyright (c) 2026, HNS and contributors
# For license information, please see license.txt

import frappe
import random
import requests
from frappe.model.document import Document
from frappe.utils import strip_html, getdate

class VCard(Document):
	def validate(self):
		if self.is_new() and not self.vcard_id:
			self.vcard_id = self.generate_unique_vcard_id()
		self.set_default_about_us()
		self.fetch_employee_image()

	def set_default_about_us(self):
		print("self.about_us",self.about_us)
		is_empty = not self.about_us
		if self.about_us:
			if not strip_html(self.about_us).strip():
				is_empty = True
		if is_empty:
			bio_template = frappe.db.get_single_value("VCard Setting", "employee_bio")
			if bio_template:
				pronoun = "he" if self.gender == "Male" else "she" if self.gender == "Female" else "they"
				
				dob = ""
				if self.date_of_birth:
					if isinstance(self.date_of_birth, str):
						dob = getdate(self.date_of_birth).strftime("%d-%m-%Y")
					else:
						dob = self.date_of_birth.strftime("%d-%m-%Y")
				
				try:
					self.about_us = bio_template.format(
						full_name=self.full_name or "",
						designation=self.designation or "",
						department=self.department or "",
						company=self.company or "",
						pronoun=pronoun,
						date_of_birth=dob
					)
				except Exception as e:
					frappe.log_error(title="VCard Bio Formatting Error", message=str(e))

	def fetch_employee_image(self):
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
