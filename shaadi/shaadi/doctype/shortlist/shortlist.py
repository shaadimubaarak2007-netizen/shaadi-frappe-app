import frappe
from frappe.model.document import Document


class Shortlist(Document):
	def validate(self):
		if self.member == self.shortlisted_profile:
			frappe.throw("Cannot shortlist yourself")
