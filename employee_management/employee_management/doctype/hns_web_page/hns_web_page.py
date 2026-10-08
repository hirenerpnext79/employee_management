# Copyright (c) 2026, HNS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class HNSWebPage(Document):
	def before_save(self):
		if self.section:
			for sec in self.section:
				if not sec.section_code and sec.page_title:
					sec.section_code = frappe.scrub(sec.page_title)
