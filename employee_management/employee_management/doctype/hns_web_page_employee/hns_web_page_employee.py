# Copyright (c) 2026, HNS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class HnsWebPageEmployee(Document):
	def validate(self):
		self.sync_enable_disable()
		self.validate_unique_user_email()

	def on_update(self):
		if not self.web_code:
			self.db_set('web_code', self.name)

	def validate_unique_user_email(self):
		try:
			if not self.user_email:
				return
			email = self.user_email.strip()
			existing = frappe.db.get_value(
				"Hns Web Page Employee",
				{"user_email": email, "name": ["!=", self.name]},
				"name"
			)
			if existing:
				frappe.throw(frappe._("User Email {0} already exists in Employee {1}.").format(email, existing))
		except Exception as e:
			frappe.log_error(f"Error validating user email: {str(e)}", "HnsWebPageEmployee.validate_unique_user_email")
			raise

	def sync_enable_disable(self):
		try:
			rows = self.hns_web_page_employee_details or []
			if not rows:
				return
			doc_before = self.get_doc_before_save()
			if doc_before and doc_before.enable_disable_all != self.enable_disable_all:
				val = 1 if self.enable_disable_all else 0
				for row in rows:
					row.enable_disable = val
			else:
				all_checked = all(bool(row.enable_disable) for row in rows)
				self.enable_disable_all = 1 if all_checked else 0
		except Exception as e:
			frappe.log_error(f"Error syncing enable_disable: {str(e)}", "sync_enable_disable")
