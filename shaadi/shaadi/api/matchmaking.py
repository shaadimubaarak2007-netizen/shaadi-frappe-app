import frappe
from frappe import _

# Mutual Matches API - Updated 2026-03-16


@frappe.whitelist()
def get_recommendations(profile_id=None, limit=20):
	"""Get match recommendations for a member"""
	# Get current user's profile if not provided
	if not profile_id:
		profile_id = frappe.db.get_value("Member Profile", {"user": frappe.session.user})
		if not profile_id:
			profile_id = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if not frappe.db.exists("Member Profile", profile_id):
		frappe.throw(_("Profile not found"))
	
	# Get member's partner preference
	preference = frappe.db.get_value("Partner Preference", {"member_profile": profile_id}, "*", as_dict=True)
	
	if not preference:
		return []
	
	# Get member profile
	member = frappe.get_doc("Member Profile", profile_id)
	
	# Build filters based on preferences - ensure we always have valid filters
	filters = {
		"is_active": 1,
		"name": ["!=", profile_id]
	}
	
	# Gender filter - use preferred_gender from Partner Preference
	preferred_gender = preference.get("preferred_gender")
	if preferred_gender and preferred_gender != "Any":
		filters["gender"] = preferred_gender
	elif member.gender:
		# Fallback to opposite gender if preferred_gender not set
		filters["gender"] = "Female" if member.gender == "Male" else "Male"
	else:
		# Last fallback if neither is set
		filters["gender"] = ["!=", ""]
	
	# Age filter - only add if both values are valid
	min_age = preference.get("min_age")
	max_age = preference.get("max_age")
	if min_age and max_age and isinstance(min_age, (int, float)) and isinstance(max_age, (int, float)) and min_age > 0 and max_age > 0:
		filters["age"] = ["between", [int(min_age), int(max_age)]]
	
	# Marital status filter - only add if specified and not "Any"
	marital_status = preference.get("marital_status")
	if marital_status and marital_status != "Any" and marital_status.strip():
		filters["marital_status"] = marital_status
	
	try:
		# Get matching profiles
		profiles = frappe.get_all(
			"Member Profile",
			filters=filters,
			fields=["name", "full_name", "age", "city", "education", "occupation", "profile_photo"],
			limit=limit
		)
	except Exception as e:
		# Fallback with minimal filters if query fails
		profiles = frappe.get_all(
			"Member Profile",
			filters={"is_active": 1, "name": ["!=", profile_id]},
			fields=["name", "full_name", "age", "city", "education", "occupation", "profile_photo"],
			limit=limit
		)
	
	# Calculate match scores
	from shaadi.shaadi.utils.match_score import calculate_match_score
	
	for profile in profiles:
		profile["match_score"] = calculate_match_score(profile_id, profile["name"])
	
	# Sort by match score
	profiles.sort(key=lambda x: x.get("match_score", 0), reverse=True)
	
	return profiles


@frappe.whitelist()
def send_interest(receiver_profile, sender_profile=None, message=""):
	"""Send interest to another member"""
	# Get current user's profile
	if not sender_profile:
		sender_profile = frappe.db.get_value("Member Profile", {"user": frappe.session.user})
		if not sender_profile:
			sender_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if not sender_profile:
		frappe.throw(_("Your profile not found"))
	
	# Check if interest already exists
	existing = frappe.db.exists("Match Request", {
		"sender": sender_profile,
		"receiver": receiver_profile,
		"status": ["in", ["Pending", "Accepted"]]
	})
	
	if existing:
		frappe.throw(_("Interest already sent to this member"))
	
	# Create match request
	match_request = frappe.get_doc({
		"doctype": "Match Request",
		"sender": sender_profile,
		"receiver": receiver_profile,
		"request_type": "Interest",
		"message": message,
		"status": "Pending"
	})
	match_request.insert()
	
	# Publish real-time update
	frappe.publish_realtime("interest_sent", {
		"sender": sender_profile,
		"receiver": receiver_profile,
		"match_request_id": match_request.name,
		"status": "Pending"
	})
	
	# Get updated interaction status
	updated_status = get_profile_interaction_status(receiver_profile)
	
	return {
		"success": True,
		"message": _("Interest sent successfully"),
		"match_request": match_request.name,
		"interaction_status": updated_status
	}


@frappe.whitelist()
def respond_to_interest(match_request_id, action):
	"""Accept or decline interest"""
	if action not in ["Accepted", "Declined"]:
		frappe.throw(_("Invalid action"))
	
	match_request = frappe.get_doc("Match Request", match_request_id)
	
	# Verify current user is the receiver
	current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if current_user_profile != match_request.receiver:
		frappe.throw(_("You can only respond to interests sent to you"))
	
	match_request.status = action
	match_request.save()
	
	return {
		"success": True,
		"message": _("Interest {0}").format(action.lower()),
		"status": action
	}


@frappe.whitelist()
def get_sent_interests(profile_id=None):
	"""Get interests sent by member"""
	# Get current user's profile if not provided
	if not profile_id:
		profile_id = frappe.db.get_value("Member Profile", {"user": frappe.session.user})
		if not profile_id:
			profile_id = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if not profile_id:
		frappe.throw(_("Profile not found"))
	
	interests = frappe.get_all(
		"Match Request",
		filters={"sender": profile_id},
		fields=["name", "receiver", "status", "sent_on", "message"],
		order_by="sent_on desc"
	)
	
	# Get receiver details
	for interest in interests:
		receiver = frappe.db.get_value("Member Profile", interest["receiver"], 
			["full_name", "age", "city", "profile_photo"], as_dict=True)
		interest.update(receiver)
	
	return interests


@frappe.whitelist()
def get_received_interests(profile_id=None):
	"""Get interests received by member"""
	# Get current user's profile if not provided
	if not profile_id:
		profile_id = frappe.db.get_value("Member Profile", {"user": frappe.session.user})
		if not profile_id:
			profile_id = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if not profile_id:
		frappe.throw(_("Profile not found"))
	
	interests = frappe.get_all(
		"Match Request",
		filters={"receiver": profile_id},
		fields=["name", "sender", "status", "sent_on", "message"],
		order_by="sent_on desc"
	)
	
	# Get sender details
	for interest in interests:
		sender = frappe.db.get_value("Member Profile", interest["sender"], 
			["full_name", "age", "city", "profile_photo"], as_dict=True)
		interest.update(sender)
	
	return interests


@frappe.whitelist()
def get_profile_interaction_status(profile_id):
	"""Get comprehensive interaction status between current user and target profile"""
	# Get current user's profile
	current_user_profile = frappe.db.get_value("Member Profile", {"user": frappe.session.user})
	if not current_user_profile:
		current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if not current_user_profile:
		frappe.throw(_("Your profile not found"))
	
	# Get interest status (both directions)
	sent_interest = frappe.db.get_value(
		"Match Request",
		{
			"sender": current_user_profile,
			"receiver": profile_id,
			"request_type": "Interest"
		},
		["name", "status", "sent_on"],
		as_dict=True,
		order_by="sent_on desc"
	)
	
	received_interest = frappe.db.get_value(
		"Match Request", 
		{
			"sender": profile_id,
			"receiver": current_user_profile,
			"request_type": "Interest"
		},
		["name", "status", "sent_on"],
		as_dict=True,
		order_by="sent_on desc"
	)
	
	# Get shortlist status
	shortlist_status = frappe.db.get_value(
		"Shortlist",
		{
			"member": current_user_profile,
			"shortlisted_profile": profile_id
		},
		["name", "category", "shortlisted_on"],
		as_dict=True
	)
	
	# Check if user is blocked (will implement Blocked User DocType later)
	is_blocked = False  # TODO: Implement blocking system
	
	# Determine overall relationship status
	relationship_status = "none"
	can_message = False
	
	if is_blocked:
		relationship_status = "blocked"
	elif sent_interest and sent_interest.status == "Accepted" and received_interest and received_interest.status == "Accepted":
		relationship_status = "mutual_interest"
		can_message = True
	elif sent_interest and sent_interest.status == "Accepted":
		relationship_status = "interest_accepted"
		can_message = True
	elif received_interest and received_interest.status == "Accepted":
		relationship_status = "accepted_their_interest"
		can_message = True
	
	return {
		"profile_id": profile_id,
		"current_user_profile": current_user_profile,
		"sent_interest": sent_interest,
		"received_interest": received_interest,
		"shortlist_status": shortlist_status,
		"is_blocked": bool(is_blocked),
		"relationship_status": relationship_status,
		"can_message": can_message,
		"can_send_interest": not bool(sent_interest and sent_interest.status in ["Pending", "Accepted"]) and not is_blocked,
		"can_shortlist": not bool(shortlist_status) and not is_blocked
	}


@frappe.whitelist()
def swipe_profile(profile_id, action):
	"""Handle swipe action (like/pass) on a profile"""
	if action not in ["like", "pass"]:
		frappe.throw(_("Invalid action. Must be 'like' or 'pass'"))
	
	# Get current user's profile
	current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	if not current_user_profile:
		frappe.throw(_("Profile not found"))
	
	# Check if already swiped on this profile
	existing_swipe = frappe.db.exists("Swipe Match", {
		"swiper": current_user_profile,
		"swiped_profile": profile_id
	})
	
	if existing_swipe:
		frappe.throw(_("You have already swiped on this profile"))
	
	# Create swipe record
	swipe_doc = frappe.get_doc({
		"doctype": "Swipe Match",
		"swiper": current_user_profile,
		"swiped_profile": profile_id,
		"action": action.title()
	})
	swipe_doc.insert()
	
	result = {
		"success": True,
		"action": action,
		"swipe_id": swipe_doc.name
	}
	
	# If it's a like, check for mutual match
	if action == "like":
		is_mutual = swipe_doc.check_mutual_match()
		if is_mutual:
			result["mutual_match"] = True
			result["matched_profile"] = frappe.get_doc("Member Profile", profile_id).as_dict()
	
	# Get next profile for swiping
	next_profile = get_next_swipe_profile(current_user_profile)
	if next_profile:
		result["next_profile"] = next_profile
	
	return result


@frappe.whitelist()
def get_swipe_queue(limit=10):
	"""Get profiles for swiping based on matching algorithm"""
	# Get current user's profile
	current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	if not current_user_profile:
		frappe.throw(_("Profile not found"))
	
	# Get profiles already swiped on
	swiped_profiles = frappe.get_all("Swipe Match", 
		filters={"swiper": current_user_profile},
		pluck="swiped_profile"
	)
	
	# Get recommendations excluding already swiped profiles
	recommendations = get_recommendations(current_user_profile, limit=limit*2)
	
	# Filter out already swiped profiles
	available_profiles = []
	for profile in recommendations:
		if profile["name"] not in swiped_profiles:
			available_profiles.append(profile)
		
		if len(available_profiles) >= limit:
			break
	
	return {
		"profiles": available_profiles[:limit],
		"total": len(available_profiles)
	}


@frappe.whitelist()
def get_mutual_matches(limit=50):
	"""Get profiles where both users have liked each other (mutual matches)"""
	# Get current user's profile
	current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	if not current_user_profile:
		frappe.throw(_("Profile not found"))
	
	# Get all profiles current user has liked
	my_likes = frappe.get_all("Swipe Match",
		filters={
			"swiper": current_user_profile,
			"action": "Like"
		},
		pluck="swiped_profile"
	)
	
	if not my_likes:
		return []
	
	# Get profiles who have also liked current user back (mutual matches)
	mutual_matches = frappe.get_all("Swipe Match",
		filters={
			"swiper": ["in", my_likes],
			"swiped_profile": current_user_profile,
			"action": "Like"
		},
		fields=["swiper", "created_on", "is_mutual"],
		limit=limit
	)
	
	# Get full profile details for mutual matches
	result = []
	for match in mutual_matches:
		profile = frappe.get_doc("Member Profile", match.swiper)
		
		profile_data = {
			"name": profile.name,
			"full_name": profile.full_name,
			"age": profile.age,
			"gender": profile.gender,
			"city": profile.city,
			"state": profile.state,
			"education": profile.education,
			"occupation": profile.occupation,
			"religion": profile.religion,
			"marital_status": profile.marital_status,
			"profile_photo": profile.profile_photo,
			"profile_bio": profile.profile_bio,
			"height_cm": profile.height_cm,
			"matched_on": match.created_on,
			"is_mutual": match.is_mutual
		}
		
		# Calculate match score
		from shaadi.shaadi.utils.match_score import calculate_match_score
		profile_data["match_score"] = calculate_match_score(current_user_profile, profile.name)
		
		result.append(profile_data)
	
	# Sort by match score
	result.sort(key=lambda x: x.get("match_score", 0), reverse=True)
	
	return result


@frappe.whitelist()
def get_swipe_statistics():
	"""Get swipe statistics for current user"""
	current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	if not current_user_profile:
		return {"passed": 0, "liked": 0, "matches": 0}
	
	# Count passes
	pass_count = frappe.db.count("Swipe Match", {
		"swiper": current_user_profile,
		"action": "Pass"
	})
	
	# Count likes
	like_count = frappe.db.count("Swipe Match", {
		"swiper": current_user_profile,
		"action": "Like"
	})
	
	# Count mutual matches
	match_count = frappe.db.count("Swipe Match", {
		"swiper": current_user_profile,
		"is_mutual": 1
	})
	
	return {
		"passed": pass_count,
		"liked": like_count,
		"matches": match_count
	}


@frappe.whitelist()
def get_mutual_matches_count():
	"""Get count of mutual matches for current user"""
	current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	if not current_user_profile:
		return 0
	
	# Get all profiles current user has liked
	my_likes = frappe.get_all("Swipe Match",
		filters={
			"swiper": current_user_profile,
			"action": "Like"
		},
		pluck="swiped_profile"
	)
	
	if not my_likes:
		return 0
	
	# Count profiles who have also liked current user back
	count = frappe.db.count("Swipe Match",
		filters={
			"swiper": ["in", my_likes],
			"swiped_profile": current_user_profile,
			"action": "Like"
		}
	)
	
	return count


def get_next_swipe_profile(current_user_profile):
	"""Get the next profile for swiping"""
	queue = get_swipe_queue(limit=1)
	return queue[0] if queue else None


@frappe.whitelist()
def get_interest_status(profile_id):
	"""Get interest status between current user and target profile"""
	status_data = get_profile_interaction_status(profile_id)
	return {
		"sent_interest": status_data["sent_interest"],
		"received_interest": status_data["received_interest"],
		"can_send_interest": status_data["can_send_interest"]
	}


@frappe.whitelist()
def get_shortlist_status(profile_id):
	"""Get shortlist status for target profile"""
	status_data = get_profile_interaction_status(profile_id)
	return {
		"shortlist_status": status_data["shortlist_status"],
		"can_shortlist": status_data["can_shortlist"]
	}


@frappe.whitelist()
def withdraw_interest(match_request_id):
	"""Withdraw a sent interest"""
	match_request = frappe.get_doc("Match Request", match_request_id)
	
	# Get current user's profile
	current_user_profile = frappe.db.get_value("Member Profile", {"user": frappe.session.user})
	if not current_user_profile:
		current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	# Verify current user is the sender
	if current_user_profile != match_request.sender:
		frappe.throw(_("Unauthorized access"))
	
	# Can only withdraw pending interests
	if match_request.status != "Pending":
		frappe.throw(_("Can only withdraw pending interests"))
	
	# Update status to withdrawn
	match_request.status = "Withdrawn"
	match_request.responded_on = frappe.utils.now()
	match_request.save()
	
	return {
		"success": True,
		"message": _("Interest withdrawn successfully")
	}
