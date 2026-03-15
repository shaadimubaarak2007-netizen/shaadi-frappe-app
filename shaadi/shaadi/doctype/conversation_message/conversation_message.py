import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class ConversationMessage(Document):
	def after_insert(self):
		conversation = frappe.get_doc("Conversation", self.conversation)
		conversation.last_message_on = now_datetime()
		
		if self.sender == conversation.participant_1:
			conversation.unread_count_p2 += 1
		else:
			conversation.unread_count_p1 += 1
		
		conversation.save(ignore_permissions=True)
