import frappe
from frappe import _


@frappe.whitelist()
def typing_indicator(conversation_id, is_typing=True):
	"""Emit typing indicator to other participant"""
	conversation = frappe.get_doc("Conversation", conversation_id)
	
	# Verify user is participant
	current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if current_user_profile not in [conversation.participant_1, conversation.participant_2]:
		frappe.throw(_("Unauthorized access"))
	
	# Get other participant
	other_participant = conversation.participant_2 if conversation.participant_1 == current_user_profile else conversation.participant_1
	
	# Get sender details
	sender_data = frappe.db.get_value(
		"Member Profile", 
		current_user_profile, 
		["full_name"], 
		as_dict=True
	)
	
	# Publish typing event
	frappe.publish_realtime(
		event='typing_indicator',
		message={
			"conversation": conversation_id,
			"sender": current_user_profile,
			"sender_name": sender_data.get("full_name"),
			"is_typing": is_typing
		},
		user=frappe.db.get_value("Member Profile", other_participant, "user")
	)
	
	return {"success": True}


@frappe.whitelist()
def update_online_status(is_online=True):
	"""Update user's online status"""
	current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if not current_user_profile:
		return {"success": False}
	
	# Update last seen
	frappe.db.set_value("Member Profile", current_user_profile, "last_seen", frappe.utils.now())
	
	# Broadcast online status to all conversations
	conversations = frappe.get_all(
		"Conversation",
		or_filters=[
			["participant_1", "=", current_user_profile],
			["participant_2", "=", current_user_profile]
		],
		fields=["name", "participant_1", "participant_2"]
	)
	
	for conv in conversations:
		other_participant = conv["participant_2"] if conv["participant_1"] == current_user_profile else conv["participant_1"]
		
		frappe.publish_realtime(
			event='user_status',
			message={
				"profile": current_user_profile,
				"is_online": is_online,
				"last_seen": frappe.utils.now()
			},
			user=frappe.db.get_value("Member Profile", other_participant, "user")
		)
	
	return {"success": True}
