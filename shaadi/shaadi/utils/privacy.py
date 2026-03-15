import frappe
from frappe import _


def can_view_contact(profile_id, viewer_profile_id):
	"""Check if viewer can see contact details of a profile"""
	if profile_id == viewer_profile_id:
		return True
	
	# Get privacy settings
	privacy = frappe.db.get_value(
		"Privacy Setting",
		{"member_profile": profile_id},
		["hide_contact_until_accepted"],
		as_dict=True
	)
	
	if not privacy or not privacy.get("hide_contact_until_accepted"):
		return True
	
	# Check if there's an accepted interest between them
	accepted_interest = frappe.db.exists("Match Request", {
		"sender": ["in", [profile_id, viewer_profile_id]],
		"receiver": ["in", [profile_id, viewer_profile_id]],
		"status": "Accepted"
	})
	
	return bool(accepted_interest)


def can_view_photos(profile_id, viewer_profile_id):
	"""Check if viewer can see all photos of a profile"""
	if profile_id == viewer_profile_id:
		return True
	
	# Get privacy settings
	privacy = frappe.db.get_value(
		"Privacy Setting",
		{"member_profile": profile_id},
		["hide_photo_until_interest"],
		as_dict=True
	)
	
	if not privacy or not privacy.get("hide_photo_until_interest"):
		return True
	
	# Check if there's any interest (sent or received) between them
	any_interest = frappe.db.exists("Match Request", {
		"sender": ["in", [profile_id, viewer_profile_id]],
		"receiver": ["in", [profile_id, viewer_profile_id]]
	})
	
	return bool(any_interest)


def is_blocked(profile_id, viewer_profile_id):
	"""Check if viewer is blocked by the profile owner"""
	if profile_id == viewer_profile_id:
		return False
	
	# Check if viewer is in blocked list
	blocked = frappe.db.exists("Privacy Blocked Member", {
		"parent": profile_id,
		"blocked_member": viewer_profile_id
	})
	
	return bool(blocked)


def can_view_profile(profile_id, viewer_profile_id):
	"""Check if viewer can view the profile at all"""
	if profile_id == viewer_profile_id:
		return True
	
	# Check if blocked
	if is_blocked(profile_id, viewer_profile_id):
		return False
	
	# Get privacy settings
	privacy = frappe.db.get_value(
		"Privacy Setting",
		{"member_profile": profile_id},
		["profile_visible_to"],
		as_dict=True
	)
	
	if not privacy:
		return True
	
	visibility = privacy.get("profile_visible_to", "Everyone")
	
	if visibility == "Everyone":
		return True
	elif visibility == "Premium Members Only":
		# Check if viewer has premium subscription
		has_premium = frappe.db.exists("Member Subscription", {
			"member_profile": viewer_profile_id,
			"status": "Active"
		})
		return bool(has_premium)
	elif visibility == "No One":
		return False
	
	return True


def apply_privacy_filters(profile_data, viewer_profile_id):
	"""Apply privacy filters to profile data based on viewer permissions"""
	if not profile_data:
		return profile_data
	
	profile_id = profile_data.get("name")
	
	# Check if viewer can see the profile at all
	if not can_view_profile(profile_id, viewer_profile_id):
		return None
	
	# Check if blocked
	if is_blocked(profile_id, viewer_profile_id):
		return None
	
	# Hide contact details if not allowed
	if not can_view_contact(profile_id, viewer_profile_id):
		profile_data["phone"] = None
		profile_data["whatsapp_number"] = None
		profile_data["email"] = None
	
	# Hide photos if not allowed
	if not can_view_photos(profile_id, viewer_profile_id):
		profile_data["profile_photo"] = None
		if "profile_photos" in profile_data:
			profile_data["profile_photos"] = []
	
	return profile_data


def block_member(profile_id, member_to_block):
	"""Block a member"""
	# Check if already blocked
	existing = frappe.db.exists("Privacy Blocked Member", {
		"parent": profile_id,
		"blocked_member": member_to_block
	})
	
	if existing:
		return {
			"success": False,
			"message": _("Member is already blocked")
		}
	
	# Get or create privacy setting
	privacy = frappe.db.get_value("Privacy Setting", {"member_profile": profile_id})
	
	if not privacy:
		privacy_doc = frappe.get_doc({
			"doctype": "Privacy Setting",
			"member_profile": profile_id
		})
		privacy_doc.insert(ignore_permissions=True)
		privacy = privacy_doc.name
	else:
		privacy_doc = frappe.get_doc("Privacy Setting", privacy)
	
	# Add to blocked list
	privacy_doc.append("blocked_members", {
		"blocked_member": member_to_block
	})
	privacy_doc.save(ignore_permissions=True)
	
	return {
		"success": True,
		"message": _("Member blocked successfully")
	}


def unblock_member(profile_id, member_to_unblock):
	"""Unblock a member"""
	# Get privacy setting
	privacy = frappe.db.get_value("Privacy Setting", {"member_profile": profile_id})
	
	if not privacy:
		return {
			"success": False,
			"message": _("No blocked members found")
		}
	
	privacy_doc = frappe.get_doc("Privacy Setting", privacy)
	
	# Find and remove from blocked list
	for row in privacy_doc.blocked_members:
		if row.blocked_member == member_to_unblock:
			privacy_doc.blocked_members.remove(row)
			privacy_doc.save(ignore_permissions=True)
			return {
				"success": True,
				"message": _("Member unblocked successfully")
			}
	
	return {
		"success": False,
		"message": _("Member was not blocked")
	}


def get_blocked_members(profile_id):
	"""Get list of blocked members"""
	privacy = frappe.db.get_value("Privacy Setting", {"member_profile": profile_id})
	
	if not privacy:
		return []
	
	blocked = frappe.get_all(
		"Privacy Blocked Member",
		filters={"parent": privacy},
		fields=["blocked_member", "blocked_on"],
		order_by="blocked_on desc"
	)
	
	# Get member details
	for item in blocked:
		member_data = frappe.db.get_value(
			"Member Profile",
			item["blocked_member"],
			["full_name", "age", "city", "profile_photo"],
			as_dict=True
		)
		item.update(member_data)
	
	return blocked


def update_privacy_settings(profile_id, settings):
	"""Update privacy settings for a member"""
	# Get or create privacy setting
	privacy = frappe.db.get_value("Privacy Setting", {"member_profile": profile_id})
	
	if not privacy:
		privacy_doc = frappe.get_doc({
			"doctype": "Privacy Setting",
			"member_profile": profile_id
		})
		privacy_doc.insert(ignore_permissions=True)
	else:
		privacy_doc = frappe.get_doc("Privacy Setting", privacy)
	
	# Update settings
	if "hide_contact_until_accepted" in settings:
		privacy_doc.hide_contact_until_accepted = settings["hide_contact_until_accepted"]
	
	if "hide_photo_until_interest" in settings:
		privacy_doc.hide_photo_until_interest = settings["hide_photo_until_interest"]
	
	if "show_last_seen" in settings:
		privacy_doc.show_last_seen = settings["show_last_seen"]
	
	if "profile_visible_to" in settings:
		privacy_doc.profile_visible_to = settings["profile_visible_to"]
	
	privacy_doc.save(ignore_permissions=True)
	
	return {
		"success": True,
		"message": _("Privacy settings updated successfully")
	}
