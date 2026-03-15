import frappe
from frappe import _


@frappe.whitelist()
def get_profile(profile_id):
	"""Get member profile with privacy filtering"""
	if not frappe.db.exists("Member Profile", profile_id):
		frappe.throw(_("Profile not found"))
	
	profile = frappe.get_doc("Member Profile", profile_id)
	
	# Check privacy settings
	privacy = frappe.db.get_value("Privacy Setting", {"member_profile": profile_id}, "*", as_dict=True)
	
	current_user_profile = get_current_user_profile()
	
	# Apply privacy filters
	if privacy:
		# Check if current user is blocked
		if is_blocked(profile_id, current_user_profile):
			frappe.throw(_("You cannot view this profile"))
		
		# Hide contact details if not accepted
		if privacy.get("hide_contact_until_accepted"):
			if not has_accepted_interest(profile_id, current_user_profile):
				profile.phone = None
				profile.whatsapp_number = None
				profile.email = None
		
		# Hide photos until interest
		if privacy.get("hide_photo_until_interest"):
			if not has_sent_or_received_interest(profile_id, current_user_profile):
				profile.profile_photo = None
				profile.profile_photos = []
	
	# Increment view count
	frappe.db.set_value("Member Profile", profile_id, "view_count", profile.view_count + 1, update_modified=False)
	
	return profile


@frappe.whitelist()
def update_profile(profile_id, data):
	"""Update member profile"""
	current_user_profile = get_current_user_profile()
	
	if current_user_profile != profile_id:
		frappe.throw(_("You can only update your own profile"))
	
	profile = frappe.get_doc("Member Profile", profile_id)
	profile.update(data)
	profile.save()
	
	return profile


@frappe.whitelist()
def upload_photo(profile_id, file_url, is_primary=0):
	"""Add photo to member profile"""
	current_user_profile = get_current_user_profile()
	
	if current_user_profile != profile_id:
		frappe.throw(_("You can only upload to your own profile"))
	
	profile = frappe.get_doc("Member Profile", profile_id)
	
	# Add to photos table
	profile.append("profile_photos", {
		"photo": file_url,
		"is_primary": is_primary,
		"approved": 0
	})
	
	profile.save()
	
	return {"success": True, "message": _("Photo uploaded successfully")}


def get_current_user_profile():
	"""Helper to get current user's profile"""
	user = frappe.session.user
	if user == "Guest":
		return None
	
	return frappe.db.get_value("Member Profile", {"email": user})


def is_blocked(profile_id, current_user_profile):
	"""Check if current user is blocked by profile"""
	if not current_user_profile:
		return False
	
	blocked = frappe.db.exists("Privacy Blocked Member", {
		"parent": profile_id,
		"blocked_member": current_user_profile
	})
	
	return bool(blocked)


def has_accepted_interest(profile_id, current_user_profile):
	"""Check if there's an accepted interest between profiles"""
	if not current_user_profile:
		return False
	
	accepted = frappe.db.exists("Match Request", {
		"sender": ["in", [profile_id, current_user_profile]],
		"receiver": ["in", [profile_id, current_user_profile]],
		"status": "Accepted"
	})
	
	return bool(accepted)


def has_sent_or_received_interest(profile_id, current_user_profile):
	"""Check if there's any interest between profiles"""
	if not current_user_profile:
		return False
	
	interest = frappe.db.exists("Match Request", {
		"sender": ["in", [profile_id, current_user_profile]],
		"receiver": ["in", [profile_id, current_user_profile]]
	})
	
	return bool(interest)
