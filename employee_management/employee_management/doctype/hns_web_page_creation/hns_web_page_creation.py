# Copyright (c) 2026, HNS and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document
from frappe.utils import cint


class HnsWebPageCreation(Document):
	def before_save(self):
		if self.section:
			for sec in self.section:
				if not sec.section_code and sec.page_title:
					sec.section_code = frappe.scrub(sec.page_title)

		if self.tabs:
			for sec in self.tabs:
				if not sec.tab_code and sec.page_title:
					sec.tab_code = frappe.scrub(sec.page_title)


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
