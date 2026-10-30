import frappe
from frappe import _
from frappe.model.document import Document


class HnsWebPageSectionDetails(Document):
	def validate(self):
		try:
			if self.is_tab_section and self.is_attachment_section:
				frappe.throw(
					_("Row #{0}: A section cannot be both a Tab Section and an Attachment Section").format(self.idx)
				)

			if self.is_tab_section:
				if not self.tab_group:
					frappe.throw(
						_("Row #{0}: Tab Group is mandatory when Is Tab Section is checked").format(self.idx)
					)
				self.section_group = None
				self.attachment_group = None
			elif self.is_attachment_section:
				if not self.attachment_group:
					frappe.throw(
						_("Row #{0}: Attachment Group is mandatory when Is Attachment Section is checked").format(self.idx)
					)
				self.section_group = None
				self.tab_group = None
			else:
				if not self.section_group:
					frappe.throw(
						_("Row #{0}: Section Group is mandatory when neither Tab Section nor Attachment Section is checked").format(self.idx)
					)
				self.tab_group = None
				self.attachment_group = None
		except frappe.ValidationError:
			raise
		except Exception as e:
			frappe.log_error(f"Error in HnsWebPageSectionDetails.validate: {str(e)}", "HnsWebPageSectionDetails.validate")
			frappe.throw(str(e))
