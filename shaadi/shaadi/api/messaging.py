import frappe
from frappe import _
from frappe.utils import now


@frappe.whitelist()
def get_or_create_conversation(other_profile_id):
	"""Get existing conversation or create new one with another member"""
	current_user_profile = frappe.db.get_value("Member Profile", {"user": frappe.session.user})
	if not current_user_profile:
		current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if not current_user_profile:
		frappe.throw(_("Your profile not found"))
	
	# Check if conversation already exists
	existing = frappe.db.exists("Conversation", {
		"participant_1": ["in", [current_user_profile, other_profile_id]],
		"participant_2": ["in", [current_user_profile, other_profile_id]]
	})
	
	if existing:
		conversation = frappe.get_doc("Conversation", existing)
	else:
		# Create new conversation
		conversation = frappe.get_doc({
			"doctype": "Conversation",
			"participant_1": current_user_profile,
			"participant_2": other_profile_id,
			"status": "Active"
		})
		conversation.insert(ignore_permissions=True)
	
	# Get other participant details
	participant_data = frappe.db.get_value(
		"Member Profile", 
		other_profile_id, 
		["full_name", "age", "city", "profile_photo"], 
		as_dict=True
	)
	
	return {
		"name": conversation.name,
		"participant_1": conversation.participant_1,
		"participant_2": conversation.participant_2,
		"status": conversation.status,
		"last_message_on": conversation.last_message_on,
		"other_profile_id": other_profile_id,
		"other_profile_name": participant_data.get("full_name"),
		"other_profile_city": participant_data.get("city"),
		"other_profile_age": participant_data.get("age"),
		"other_profile_photo": participant_data.get("profile_photo"),
		"unread_count": 0
	}


@frappe.whitelist()
def get_current_user_profile():
	"""Get current user's profile data for navigation"""
	# Get current user's profile
	profile = frappe.db.get_value(
		"Member Profile", 
		{"user": frappe.session.user},
		["name", "full_name", "profile_photo", "email"],
		as_dict=True
	)
	
	if not profile:
		profile = frappe.db.get_value(
			"Member Profile", 
			{"email": frappe.session.user},
			["name", "full_name", "profile_photo", "email"],
			as_dict=True
		)
	
	if not profile:
		return {
			"profile_id": None,
			"full_name": frappe.session.user,
			"profile_photo": None,
			"email": frappe.session.user
		}
	
	return {
		"profile_id": profile.get("name"),
		"full_name": profile.get("full_name") or frappe.session.user,
		"profile_photo": profile.get("profile_photo"),
		"email": profile.get("email") or frappe.session.user
	}


@frappe.whitelist()
def get_unread_count():
	"""Get total unread message count for current user"""
	# Get current user's profile
	profile_id = frappe.db.get_value("Member Profile", {"user": frappe.session.user})
	if not profile_id:
		profile_id = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if not profile_id:
		return {"unread_count": 0}
	
	# Get all conversations where user is a participant
	conversations = frappe.get_all(
		"Conversation",
		filters={"status": "Active"},
		or_filters=[
			["participant_1", "=", profile_id],
			["participant_2", "=", profile_id]
		],
		fields=["name", "participant_1", "unread_count_p1", "unread_count_p2"]
	)
	
	# Sum up unread counts
	total_unread = 0
	for conv in conversations:
		if conv["participant_1"] == profile_id:
			total_unread += conv.get("unread_count_p1", 0)
		else:
			total_unread += conv.get("unread_count_p2", 0)
	
	return {"unread_count": total_unread}


@frappe.whitelist()
def get_notifications():
	"""Get notification details for unread messages"""
	# Get current user's profile
	profile_id = frappe.db.get_value("Member Profile", {"user": frappe.session.user})
	if not profile_id:
		profile_id = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if not profile_id:
		return {"notifications": [], "unread_count": 0}
	
	# Get conversations with unread messages
	conversations = frappe.get_all(
		"Conversation",
		filters={"status": "Active"},
		or_filters=[
			["participant_1", "=", profile_id],
			["participant_2", "=", profile_id]
		],
		fields=["name", "participant_1", "participant_2", "unread_count_p1", "unread_count_p2", "last_message_on"]
	)
	
	notifications = []
	total_unread = 0
	
	for conv in conversations:
		# Get unread count for current user
		if conv["participant_1"] == profile_id:
			unread_count = conv.get("unread_count_p1", 0)
			other_participant = conv["participant_2"]
		else:
			unread_count = conv.get("unread_count_p2", 0)
			other_participant = conv["participant_1"]
		
		if unread_count > 0:
			# Get sender details
			sender_data = frappe.db.get_value(
				"Member Profile", 
				other_participant, 
				["full_name", "profile_photo"], 
				as_dict=True
			)
			
			# Get last message preview
			last_message = frappe.db.get_value(
				"Conversation Message",
				{"conversation": conv["name"], "is_deleted": 0},
				["message_text", "sent_on"],
				order_by="sent_on desc",
				as_dict=True
			)
			
			notifications.append({
				"type": "message",
				"title": f"New message from {sender_data.get('full_name', 'Unknown')}",
				"message": (last_message.get("message_text") or "")[:100] + ("..." if len(last_message.get("message_text", "")) > 100 else ""),
				"sender_name": sender_data.get("full_name"),
				"sender_photo": sender_data.get("profile_photo"),
				"conversation_id": conv["name"],
				"unread_count": unread_count,
				"timestamp": last_message.get("sent_on") if last_message else conv.get("last_message_on"),
				"link": f"/messages?profile={other_participant}",
				"icon": "message-circle"
			})
			
			total_unread += unread_count
	
	# Sort by timestamp (newest first)
	notifications.sort(key=lambda x: x.get("timestamp") or "", reverse=True)
	
	return {
		"notifications": notifications,
		"unread_count": total_unread
	}


@frappe.whitelist()
def update_online_status(is_online=True):
	"""Update current user's online status"""
	# Get current user's profile
	profile_id = frappe.db.get_value("Member Profile", {"user": frappe.session.user})
	if not profile_id:
		profile_id = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if not profile_id:
		return {"success": False, "message": "Profile not found"}
	
	now = frappe.utils.now()
	
	# Update last_active always, and last_seen when going offline
	if is_online:
		frappe.db.set_value("Member Profile", profile_id, {
			"last_active": now
		}, update_modified=False)
	else:
		frappe.db.set_value("Member Profile", profile_id, {
			"last_active": now,
			"last_seen": now
		}, update_modified=False)
	
	frappe.db.commit()
	
	# Publish real-time update to other users
	frappe.publish_realtime("user_status_update", {
		"profile_id": profile_id,
		"is_online": is_online,
		"last_active": now
	})
	
	return {"success": True}


@frappe.whitelist()
def get_online_status(profile_ids):
	"""Get online status for multiple users"""
	if isinstance(profile_ids, str):
		profile_ids = frappe.parse_json(profile_ids)
	
	if not profile_ids:
		return {}
	
	# Get last_active times for all profiles
	profiles = frappe.get_all(
		"Member Profile",
		filters={"name": ("in", profile_ids)},
		fields=["name", "last_active", "last_seen"]
	)
	
	now = frappe.utils.now_datetime()
	online_threshold = frappe.utils.add_to_date(now, minutes=-5)  # 5 minutes threshold
	
	status_map = {}
	for profile in profiles:
		last_active = profile.get("last_active")
		if last_active:
			last_active_dt = frappe.utils.get_datetime(last_active)
			is_online = last_active_dt > online_threshold
			
			status_map[profile["name"]] = {
				"is_online": is_online,
				"last_active": last_active,
				"last_seen": profile.get("last_seen"),
				"status_text": "Online" if is_online else get_last_seen_text(last_active)
			}
		else:
			status_map[profile["name"]] = {
				"is_online": False,
				"last_active": None,
				"last_seen": profile.get("last_seen"),
				"status_text": "Offline"
			}
	
	return status_map


def get_last_seen_text(last_active):
	"""Convert last_active datetime to human readable text"""
	if not last_active:
		return "Offline"
	
	now = frappe.utils.now_datetime()
	last_active_dt = frappe.utils.get_datetime(last_active)
	diff = now - last_active_dt
	
	if diff.days > 0:
		if diff.days == 1:
			return "Last seen yesterday"
		elif diff.days < 7:
			return f"Last seen {diff.days} days ago"
		else:
			return "Last seen a week ago"
	elif diff.seconds > 3600:  # More than 1 hour
		hours = diff.seconds // 3600
		return f"Last seen {hours}h ago"
	elif diff.seconds > 60:  # More than 1 minute
		minutes = diff.seconds // 60
		return f"Last seen {minutes}m ago"
	else:
		return "Last seen just now"


@frappe.whitelist()
def get_conversations(profile_id=None, limit=50):
	"""Get all conversations for a member"""
	# Get current user's profile if not provided
	if not profile_id:
		profile_id = frappe.db.get_value("Member Profile", {"user": frappe.session.user})
		if not profile_id:
			profile_id = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if not profile_id:
		frappe.throw(_("Profile not found"))
	
	conversations = frappe.get_all(
		"Conversation",
		filters={
			"status": "Active"
		},
		or_filters=[
			["participant_1", "=", profile_id],
			["participant_2", "=", profile_id]
		],
		fields=[
			"name", "participant_1", "participant_2", "status", 
			"last_message_on", "unread_count_p1", "unread_count_p2"
		],
		order_by="last_message_on desc",
		limit=limit
	)
	
	# Get participant details and last message
	for conv in conversations:
		other_participant = conv["participant_2"] if conv["participant_1"] == profile_id else conv["participant_1"]
		participant_data = frappe.db.get_value(
			"Member Profile", 
			other_participant, 
			["full_name", "age", "city", "profile_photo", "last_active", "last_seen"], 
			as_dict=True
		)
		
		conv["other_participant"] = other_participant
		conv["other_participant_name"] = participant_data.get("full_name")
		conv["other_participant_photo"] = participant_data.get("profile_photo")
		conv["other_participant_age"] = participant_data.get("age")
		conv["other_participant_city"] = participant_data.get("city")
		
		# Add online status
		last_active = participant_data.get("last_active")
		if last_active:
			now = frappe.utils.now_datetime()
			online_threshold = frappe.utils.add_to_date(now, minutes=-5)
			last_active_dt = frappe.utils.get_datetime(last_active)
			is_online = last_active_dt > online_threshold
			
			conv["other_participant_online"] = is_online
			conv["other_participant_status"] = "Online" if is_online else get_last_seen_text(last_active)
		else:
			conv["other_participant_online"] = False
			conv["other_participant_status"] = "Offline"
		
		# Get last message text
		last_message = frappe.db.get_value(
			"Conversation Message",
			{"conversation": conv["name"], "is_deleted": 0},
			["message_text", "sender"],
			order_by="sent_on desc",
			as_dict=True
		)
		
		if last_message:
			# Prefix with "You: " if current user sent it
			prefix = "You: " if last_message.get("sender") == profile_id else ""
			conv["last_message_text"] = prefix + (last_message.get("message_text") or "")[:50]
		else:
			conv["last_message_text"] = "No messages yet"
		
		# Get unread count for current user
		conv["unread_count"] = conv["unread_count_p2"] if conv["participant_1"] == profile_id else conv["unread_count_p1"]
	
	return conversations


@frappe.whitelist()
def get_messages(conversation_id, limit=100, offset=0):
	"""Get messages from a conversation"""
	conversation = frappe.get_doc("Conversation", conversation_id)
	
	# Verify user is participant
	current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if current_user_profile not in [conversation.participant_1, conversation.participant_2]:
		frappe.throw(_("Unauthorized access"))
	
	messages = frappe.get_all(
		"Conversation Message",
		filters={"conversation": conversation_id, "is_deleted": 0},
		fields=["name", "sender", "message_type", "message_text", "attachment", "sent_on", "read_on"],
		order_by="sent_on asc",
		limit=limit,
		start=offset
	)
	
	# Get sender details
	for msg in messages:
		sender_data = frappe.db.get_value(
			"Member Profile", 
			msg["sender"], 
			["full_name", "profile_photo"], 
			as_dict=True
		)
		msg["sender_name"] = sender_data.get("full_name")
		msg["sender_photo"] = sender_data.get("profile_photo")
		msg["is_own_message"] = msg["sender"] == current_user_profile
	
	return messages


@frappe.whitelist()
def mark_conversation_read(conversation_id):
	"""Mark conversation as read for current user"""
	conversation = frappe.get_doc("Conversation", conversation_id)
	
	# Verify user is participant
	current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if current_user_profile not in [conversation.participant_1, conversation.participant_2]:
		frappe.throw(_("Unauthorized access"))
	
	# Reset unread count for current user
	if conversation.participant_1 == current_user_profile:
		conversation.unread_count_p1 = 0
	else:
		conversation.unread_count_p2 = 0
	
	conversation.save(ignore_permissions=True)
	
	return {"success": True}


@frappe.whitelist()
def send_message(conversation_id, message_text=None, message_type="Text", attachment=None):
	"""Send a message in a conversation"""
	conversation = frappe.get_doc("Conversation", conversation_id)
	
	# Verify user is participant
	current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if current_user_profile not in [conversation.participant_1, conversation.participant_2]:
		frappe.throw(_("Unauthorized access"))
	
	# Check subscription limits
	from shaadi.shaadi.utils.subscription import can_send_message
	if not can_send_message(current_user_profile):
		frappe.throw(_("Message limit reached. Please upgrade your subscription."))
	
	# Create message
	message = frappe.get_doc({
		"doctype": "Conversation Message",
		"conversation": conversation_id,
		"sender": current_user_profile,
		"message_type": message_type,
		"message_text": message_text,
		"attachment": attachment
	})
	message.insert()
	
	# Update conversation last message time
	# Reload conversation to avoid timestamp mismatch
	conversation.reload()
	conversation.last_message_on = now()
	
	# Increment unread count for other participant
	other_participant = conversation.participant_2 if conversation.participant_1 == current_user_profile else conversation.participant_1
	if conversation.participant_1 == current_user_profile:
		conversation.unread_count_p2 = (conversation.unread_count_p2 or 0) + 1
	else:
		conversation.unread_count_p1 = (conversation.unread_count_p1 or 0) + 1
	
	conversation.save(ignore_permissions=True)
	
	# Get sender details for real-time event
	sender_data = frappe.db.get_value(
		"Member Profile", 
		current_user_profile, 
		["full_name", "profile_photo"], 
		as_dict=True
	)
	
	# Emit real-time event to other participant
	message_data = {
		"name": message.name,
		"conversation": conversation_id,
		"sender": current_user_profile,
		"sender_name": sender_data.get("full_name"),
		"sender_photo": sender_data.get("profile_photo"),
		"message_type": message_type,
		"message_text": message_text,
		"attachment": attachment,
		"sent_on": message.sent_on,
		"is_own_message": False
	}
	
	# Publish real-time event
	recipient_user = frappe.db.get_value("Member Profile", other_participant, "user")
	
	frappe.logger().info(f"Publishing new_message event to user: {recipient_user}")
	frappe.logger().info(f"Message data: {message_data}")
	
	frappe.publish_realtime(
		event='new_message',
		message=message_data,
		user=recipient_user,
		after_commit=True
	)
	
	frappe.logger().info(f"Real-time event published successfully")
	
	return {
		"success": True,
		"message": _("Message sent successfully"),
		"message_id": message.name,
		"message_data": {
			**message_data,
			"is_own_message": True
		}
	}


@frappe.whitelist()
def mark_as_read(conversation_id):
	"""Mark all messages in conversation as read"""
	conversation = frappe.get_doc("Conversation", conversation_id)
	
	# Verify user is participant
	current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if current_user_profile not in [conversation.participant_1, conversation.participant_2]:
		frappe.throw(_("Unauthorized access"))
	
	# Mark unread messages as read
	messages = frappe.get_all(
		"Conversation Message",
		filters={
			"conversation": conversation_id,
			"sender": ["!=", current_user_profile],
			"read_on": ["is", "not set"]
		},
		pluck="name"
	)
	
	for msg_id in messages:
		frappe.db.set_value("Conversation Message", msg_id, "read_on", now())
	
	# Reset unread count
	if conversation.participant_1 == current_user_profile:
		conversation.unread_count_p1 = 0
	else:
		conversation.unread_count_p2 = 0
	
	conversation.save(ignore_permissions=True)
	
	return {
		"success": True,
		"message": _("Messages marked as read"),
		"count": len(messages)
	}


@frappe.whitelist()
def delete_message(message_id):
	"""Soft delete a message"""
	message = frappe.get_doc("Conversation Message", message_id)
	
	# Verify user is sender
	current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if current_user_profile != message.sender:
		frappe.throw(_("You can only delete your own messages"))
	
	message.is_deleted = 1
	message.save(ignore_permissions=True)
	
	return {
		"success": True,
		"message": _("Message deleted successfully")
	}


