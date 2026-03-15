import frappe
from frappe.model.document import Document
from frappe import _


class PartnerPreference(Document):
	def validate(self):
		"""Validate that only one Partner Preference exists per member"""
		self.validate_unique_member_profile()
	
	def validate_unique_member_profile(self):
		"""Ensure only one Partner Preference per Member Profile"""
		if self.is_new():
			existing = frappe.db.exists("Partner Preference", {
				"member_profile": self.member_profile,
				"name": ["!=", self.name]
			})
			if existing:
				frappe.throw(_(f"Partner Preference already exists for {self.member_profile}. Please update the existing preference instead."))
	
	def before_save(self):
		"""Set default values if not provided"""
		if not self.min_age:
			self.min_age = 18
		if not self.max_age:
			self.max_age = 40
		if not self.marital_status:
			self.marital_status = "Any"
		if not self.caste_bar:
			self.caste_bar = "Any"
