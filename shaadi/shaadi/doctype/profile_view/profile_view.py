import frappe
from frappe.model.document import Document


class ProfileView(Document):
	def after_insert(self):
		"""Increment view count on viewed profile"""
		frappe.db.set_value("Member Profile", self.viewed_profile, "view_count", 
			frappe.db.get_value("Member Profile", self.viewed_profile, "view_count") + 1)
