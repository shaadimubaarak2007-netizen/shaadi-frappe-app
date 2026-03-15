import frappe
from frappe.model.document import Document


class Conversation(Document):
	def validate(self):
		if self.participant_1 == self.participant_2:
			frappe.throw("Participants must be different")
		
		existing = frappe.db.exists("Conversation", {
			"participant_1": ["in", [self.participant_1, self.participant_2]],
			"participant_2": ["in", [self.participant_1, self.participant_2]],
			"name": ["!=", self.name]
		})
		
		if existing:
			frappe.throw("A conversation already exists between these members")
