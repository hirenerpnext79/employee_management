# Copyright (c) 2026, HNS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class HNSPriceList(Document):
	def on_update(self):
		if not self.web_code:
			self.web_code = self.name
