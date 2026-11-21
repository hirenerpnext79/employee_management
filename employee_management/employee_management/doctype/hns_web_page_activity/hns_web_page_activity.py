# Copyright (c) 2026, HNS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class HnsWebPageActivity(Document):
	@property
	def dynamic_flag(self):
		return self.dynamic

	@dynamic_flag.setter
	def dynamic_flag(self, value):
		self.dynamic = value
