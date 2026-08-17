# Copyright (c) 2026, HNS and contributors
# For license information, please see license.txt

import frappe
import random
from frappe.model.document import Document

class VCard(Document):
	def before_save(self):
		if not self.vcard_id:
			self.vcard_id = self.generate_unique_vcard_id()

	def generate_unique_vcard_id(self):
		while True:
			new_id = str(random.randint(10000, 99999))
			if not frappe.db.exists("VCard", {"vcard_id": new_id}):
				return new_id
