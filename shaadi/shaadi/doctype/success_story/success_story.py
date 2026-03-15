import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class SuccessStory(Document):
	def validate(self):
		if self.member_1 == self.member_2:
			frappe.throw("Members must be different")
	
	def on_update(self):
		if self.has_value_changed("published") and self.published and not self.published_on:
			self.published_on = getdate()
			self.save()
