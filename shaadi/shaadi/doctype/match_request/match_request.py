import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class MatchRequest(Document):
	def validate(self):
		if self.sender == self.receiver:
			frappe.throw("Cannot send interest to yourself")
		
		existing = frappe.db.exists("Match Request", {
			"sender": self.sender,
			"receiver": self.receiver,
			"status": ["in", ["Pending", "Accepted"]],
			"name": ["!=", self.name]
		})
		
		if existing:
			frappe.throw("An active interest request already exists between these members")
	
	def on_update(self):
		if self.has_value_changed("status") and self.status in ["Accepted", "Declined", "Blocked"]:
			self.responded_on = now_datetime()
			
			if self.status == "Accepted":
				self.create_conversation()
	
	def create_conversation(self):
		if not frappe.db.exists("Conversation", {
			"participant_1": ["in", [self.sender, self.receiver]],
			"participant_2": ["in", [self.sender, self.receiver]]
		}):
			conversation = frappe.get_doc({
				"doctype": "Conversation",
				"participant_1": self.sender,
				"participant_2": self.receiver,
				"match_request": self.name,
				"status": "Active"
			})
			conversation.insert(ignore_permissions=True)
