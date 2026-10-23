import json
import re
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint


def sanitize_route(text, default=""):
	if not text:
		return default
	cleaned = re.sub(r"[\s/\\:]+", "_", str(text).strip())
	cleaned = re.sub(r"[^a-zA-Z0-9_-]", "", cleaned)
	cleaned = re.sub(r"_+", "_", cleaned)
	cleaned = re.sub(r"-+", "-", cleaned)
	cleaned = cleaned.strip("_-").lower()
	return cleaned or default


class HnsWebPageCreation(Document):
	def validate(self):
		try:
			if self.is_new() and not self.page_title and self.title:
				self.page_title = self.title
			if self.route:
				self.route = sanitize_route(self.route, default=sanitize_route(self.title, default="web_page"))
			elif self.title:
				self.route = sanitize_route(self.title, default="web_page")

			if self.section:
				for sec in self.section:
					if sec.is_tab_section and sec.is_attachment_section:
						frappe.throw(
							_("Row #{0}: A section cannot be both a Tab Section and an Attachment Section").format(sec.idx)
						)

					if sec.is_tab_section:
						if not sec.tab_group:
							frappe.throw(
								_("Row #{0}: Tab Group is mandatory when Is Tab Section is checked").format(sec.idx)
							)
						sec.section_group = None
						sec.attachment_group = None
					elif sec.is_attachment_section:
						if not sec.attachment_group:
							frappe.throw(
								_("Row #{0}: Attachment Group is mandatory when Is Attachment Section is checked").format(sec.idx)
							)
						sec.section_group = None
						sec.tab_group = None
					else:
						if not sec.section_group:
							frappe.throw(
								_("Row #{0}: Section Group is mandatory when neither Tab Section nor Attachment Section is checked").format(sec.idx)
							)
						sec.tab_group = None
						sec.attachment_group = None

					if sec.section_code:
						sec.section_code = sanitize_route(sec.section_code, default=sanitize_route(sec.page_title))
					elif sec.page_title:
						sec.section_code = sanitize_route(sec.page_title)

			if self.tabs:
				for tab in self.tabs:
					if tab.tab_code:
						tab.tab_code = sanitize_route(tab.tab_code, default=sanitize_route(tab.page_title))
					elif tab.page_title:
						tab.tab_code = sanitize_route(tab.page_title)
		except frappe.ValidationError:
			raise
		except Exception as e:
			frappe.log_error(f"Error validating section details: {str(e)}", "HnsWebPageCreation.validate")
			frappe.throw(str(e))

	def before_save(self):
		try:
			if self.is_new() and not self.page_title and self.title:
				self.page_title = self.title
			if self.route:
				self.route = sanitize_route(self.route, default=sanitize_route(self.title, default="web_page"))
			elif self.title:
				self.route = sanitize_route(self.title, default="web_page")

			if self.section:
				for sec in self.section:
					if sec.is_tab_section and sec.is_attachment_section:
						sec.is_attachment_section = 0
					if sec.is_tab_section:
						sec.section_group = None
						sec.attachment_group = None
					elif sec.is_attachment_section:
						sec.section_group = None
						sec.tab_group = None
					else:
						sec.tab_group = None
						sec.attachment_group = None
					if sec.section_code:
						sec.section_code = sanitize_route(sec.section_code, default=sanitize_route(sec.page_title))
					elif sec.page_title:
						sec.section_code = sanitize_route(sec.page_title)

			if self.tabs:
				for sec in self.tabs:
					if sec.tab_code:
						sec.tab_code = sanitize_route(sec.tab_code, default=sanitize_route(sec.page_title))
					elif sec.page_title:
						sec.tab_code = sanitize_route(sec.page_title)
		except Exception as e:
			frappe.log_error(f"Error in HnsWebPageCreation.before_save: {str(e)}", "HnsWebPageCreation.before_save")


@frappe.whitelist()
def get_web_page_group_query(doctype, txt, searchfield, start, page_len, filters, as_dict=False):
	try:
		if isinstance(filters, str):
			filters = json.loads(filters)

		category = filters.get("category") if filters else None
		web_page = filters.get("web_page") if filters else None

		if isinstance(category, (list, tuple)):
			category = category[-1]

		if isinstance(web_page, (list, tuple)):
			web_page = web_page[-1]

		query_filters = {}
		if category:
			query_filters["category"] = category

		or_filters = [{"is_generic": 1}]
		if web_page:
			or_filters.append({"web_page": web_page})

		if txt:
			query_filters["group_name"] = ["like", f"%{txt}%"]

		return frappe.get_all(
			"Hns Web Page Group",
			filters=query_filters,
			or_filters=or_filters,
			fields=["name", "group_name", "web_page", "category"],
			order_by="is_generic asc, name asc",
			start=cint(start) if start else 0,
			page_length=cint(page_len) if page_len else 20,
			as_list=not as_dict,
		)
	except Exception as e:
		frappe.log_error(f"Error in get_web_page_group_query: {str(e)}", "get_web_page_group_query")
		return []
