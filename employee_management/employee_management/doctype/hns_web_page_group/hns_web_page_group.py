# Copyright (c) 2026, HNS and contributors
# For license information, please see license.txt

import re
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


def clean_naming_part(text, default=""):
	cleaned = re.sub(r"[^a-zA-Z0-9\s_-]", "", str(text or ""))
	cleaned = re.sub(r"\s+", " ", cleaned).strip()
	return cleaned or default


class HnsWebPageGroup(Document):
	def autoname(self):
		try:
			category = clean_naming_part(self.category, "Group")
			if self.is_generic:
				self.name = make_autoname(f"Generic.-.{category}.-.####")
			elif self.web_page:
				web_page = clean_naming_part(self.web_page, "Web Page")
				self.name = make_autoname(f"{web_page}.-.{category}.-.####")
			else:
				frappe.throw(frappe._("Value missing for {0}: {1}").format(self.doctype, frappe._("Web Page")))
		except Exception as e:
			frappe.log_error(f"Error naming Hns Web Page Group: {str(e)}", "autoname_hns_web_page_group")
			raise

	def validate(self):
		try:
			if self.is_generic:
				self.web_page = None
			elif not self.web_page:
				frappe.throw(frappe._("Value missing for {0}: {1}").format(self.doctype, frappe._("Web Page")))
		except Exception as e:
			frappe.log_error(f"Error validating Hns Web Page Group: {str(e)}", "validate_hns_web_page_group")
			raise
