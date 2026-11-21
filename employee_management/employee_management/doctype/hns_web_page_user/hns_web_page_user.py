import frappe
from frappe import _
from frappe.model.document import Document


class HnsWebPageUser(Document):
	def validate(self):
		self.set_user_name_from_email()
		self.validate_unique_email_and_group()

	def set_user_name_from_email(self):
		try:
			if self.email and (not self.user_name or "@" in self.user_name):
				self.user_name = self.email.split("@")[0].strip()
		except Exception as e:
			frappe.log_error(f"Error setting user name: {str(e)}", "HnsWebPageUser.set_user_name_from_email")

	def validate_unique_email_and_group(self):
		try:
			if not self.email or not self.user_type:
				return

			filters = {
				"email": self.email.strip(),
				"user_type": self.user_type,
				"name": ["!=", self.name],
			}
			existing = frappe.db.get_value("Hns Web Page User", filters, "name")
			if existing:
				frappe.throw(_("User with Email {0} already exists for {1} ({2}).").format(self.email, self.user_type, existing))
		except Exception as e:
			frappe.log_error(f"Error validating user: {str(e)}", "HnsWebPageUser.validate")
			raise
