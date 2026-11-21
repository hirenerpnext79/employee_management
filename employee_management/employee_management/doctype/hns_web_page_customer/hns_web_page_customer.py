import frappe
from frappe.model.document import Document


class HnsWebPageCustomer(Document):
	def validate(self):
		self.sync_enable_disable()
		self.validate_unique_user_email()

	def on_update(self):
		if not self.web_code:
			self.db_set("web_code", self.name)

	def validate_unique_user_email(self):
		try:
			if not self.user_email:
				return
			email = self.user_email.strip()
			existing = frappe.db.get_value(
				"Hns Web Page Customer",
				{"user_email": email, "name": ["!=", self.name]},
				"name"
			)
			if existing:
				frappe.throw(frappe._("User Email {0} already exists in Customer {1}.").format(email, existing))
		except Exception as e:
			frappe.log_error(f"Error validating user email: {str(e)}", "HnsWebPageCustomer.validate_unique_user_email")
			raise

	def sync_enable_disable(self):
		try:
			rows = self.hns_price_list_details or []
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


@frappe.whitelist()
def get_portal_groups_data(portal_name, customer_name=None, parent_doctype=None, parent_name=None):
	try:
		if not portal_name or not frappe.db.exists("Hns Web Page Creation", portal_name):
			return {"error": "Portal not found"}

		portal = frappe.get_doc("Hns Web Page Creation", portal_name)
		group_name_map = _get_group_name_map()

		target_doctype = parent_doctype or "Hns Web Page Customer"
		target_name = parent_name or customer_name
		existing_keys = _get_existing_codes(target_doctype, target_name)

		sections = _process_portal_sections(portal, group_name_map, existing_keys)
		tabs = _process_portal_tabs(portal, group_name_map, existing_keys)
		attachments = _process_portal_attachments(portal, group_name_map, existing_keys)
		return {
			"portal_title": portal.title or portal.name,
			"sections": sections,
			"tabs": tabs,
			"attachments": attachments,
		}
	except Exception as e:
		frappe.log_error(f"Error getting portal groups data: {str(e)}", "get_portal_groups_data")
		return {"error": str(e)}


def _get_group_name_map():
	try:
		groups = frappe.get_all(
			"Hns Web Page Group",
			fields=["name", "group_name", "category"],
		)
		return {g.name: g.group_name for g in groups if g.get("group_name")}
	except Exception as e:
		frappe.log_error(f"Error fetching group name map: {str(e)}", "_get_group_name_map")
		return {}


def _get_existing_codes(doctype, name):
	existing_keys = set()
	try:
		if doctype and name and frappe.db.exists(doctype, name):
			doc = frappe.get_doc(doctype, name)
			child_items = (
				doc.get("hns_price_list_details")
				or doc.get("hns_web_page_employee_details")
				or []
			)
			for row in child_items:
				if row.web_page_code_type and row.web_page_code:
					existing_keys.add(f"{row.web_page_code_type}::{row.web_page_code}")
	except Exception as e:
		frappe.log_error(f"Error fetching existing codes: {str(e)}", "_get_existing_codes")
	return existing_keys


def _process_portal_sections(portal, group_name_map, existing_keys):
	grouped = {}
	try:
		for s in portal.section or []:
			raw_grp = s.section_group or (s.tab_group if s.is_tab_section else None) or (s.attachment_group if s.is_attachment_section else None)
			grp_name = group_name_map.get(raw_grp) or raw_grp or "General Sections"
			code = s.section_code or (frappe.scrub(s.page_title) if s.page_title else "")
			if not code:
				continue

			item_data = {
				"title": s.page_title or code,
				"code": code,
				"type": "Section",
				"description": s.content or "",
				"media_type": s.media_type or "",
				"is_tab_section": bool(s.is_tab_section),
				"is_attachment_section": bool(s.is_attachment_section),
				"already_added": f"Section::{code}" in existing_keys,
			}
			if grp_name not in grouped:
				grouped[grp_name] = []
			grouped[grp_name].append(item_data)
	except Exception as e:
		frappe.log_error(f"Error processing portal sections: {str(e)}", "_process_portal_sections")
	return grouped


def _process_portal_tabs(portal, group_name_map, existing_keys):
	grouped = {}
	try:
		for t in portal.tabs or []:
			grp_name = group_name_map.get(t.group_name) or t.group_name or "General Tabs"
			code = t.tab_code or (frappe.scrub(t.page_title) if t.page_title else "")
			if not code:
				continue

			item_data = {
				"title": t.page_title or code,
				"code": code,
				"type": "Tab",
				"tab_type": t.tab_type or "Horizontal",
				"description": t.content or "",
				"already_added": f"Tab::{code}" in existing_keys,
			}
			if grp_name not in grouped:
				grouped[grp_name] = []
			grouped[grp_name].append(item_data)
	except Exception as e:
		frappe.log_error(f"Error processing portal tabs: {str(e)}", "_process_portal_tabs")
	return grouped


def _process_portal_attachments(portal, group_name_map, existing_keys):
	grouped = {}
	try:
		for a in portal.attachment or []:
			grp_name = group_name_map.get(a.group_title) or a.group_title or "General Attachments"
			sub_grp = a.group_sub_title or "General Files"
			label = a.group_sub_title or a.drive_label or a.pdf_label or a.image_text or (a.attachment.split("/")[-1] if a.attachment else "") or a.name
			code = label
			if not code:
				continue

			item_data = {
				"title": label,
				"code": code,
				"type": "Attachment",
				"media_type": a.type or "",
				"attachment_url": a.attachment or "",
				"description": a.image_text or a.attachment or "",
				"sub_group": sub_grp,
				"already_added": f"Attachment::{code}" in existing_keys,
			}
			if grp_name not in grouped:
				grouped[grp_name] = {}
			if sub_grp not in grouped[grp_name]:
				grouped[grp_name][sub_grp] = []
			grouped[grp_name][sub_grp].append(item_data)
	except Exception as e:
		frappe.log_error(f"Error processing portal attachments: {str(e)}", "_process_portal_attachments")
	return grouped



