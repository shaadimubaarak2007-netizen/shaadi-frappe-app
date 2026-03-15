import frappe
from frappe import _


@frappe.whitelist()
def search_profiles(filters=None, limit=50, offset=0):
	"""Advanced search for member profiles with filters"""
	# First try to find by user field
	current_user_profile = frappe.db.get_value("Member Profile", {"user": frappe.session.user})
	
	# Fallback to email if user field is not set
	if not current_user_profile:
		current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if not current_user_profile:
		frappe.throw(_("Please login to search profiles"))
	
	# Get current user's gender to show opposite gender
	current_user = frappe.get_doc("Member Profile", current_user_profile)
	opposite_gender = "Female" if current_user.gender == "Male" else "Male"
	
	# Base filters
	conditions = {
		"is_active": 1,
		"name": ["!=", current_user_profile],
		"gender": opposite_gender
	}
	
	# Apply additional filters if provided
	if filters:
		if filters.get("min_age"):
			conditions["age"] = [">=", filters.get("min_age")]
		if filters.get("max_age"):
			if "age" in conditions:
				conditions["age"] = ["between", [filters.get("min_age"), filters.get("max_age")]]
			else:
				conditions["age"] = ["<=", filters.get("max_age")]
		
		if filters.get("religion"):
			conditions["religion"] = filters.get("religion")
		
		if filters.get("caste"):
			conditions["caste"] = filters.get("caste")
		
		if filters.get("marital_status"):
			conditions["marital_status"] = filters.get("marital_status")
		
		if filters.get("city"):
			conditions["city"] = filters.get("city")
		
		if filters.get("state"):
			conditions["state"] = filters.get("state")
		
		if filters.get("min_height"):
			conditions["height_cm"] = [">=", filters.get("min_height")]
		
		if filters.get("max_height"):
			if "height_cm" in conditions:
				conditions["height_cm"] = ["between", [filters.get("min_height"), filters.get("max_height")]]
			else:
				conditions["height_cm"] = ["<=", filters.get("max_height")]
		
		if filters.get("education"):
			conditions["education"] = filters.get("education")
		
		if filters.get("occupation"):
			conditions["occupation"] = ["like", f"%{filters.get('occupation')}%"]
	
	# Get profiles
	profiles = frappe.get_all(
		"Member Profile",
		filters=conditions,
		fields=[
			"name", "full_name", "age", "gender", "height_cm", "religion", "caste",
			"marital_status", "education", "occupation", "city", "state", "country_of_residence",
			"profile_photo", "profile_completeness", "verified", "last_active", "last_seen"
		],
		order_by="last_active desc",
		limit=limit,
		start=offset
	)
	
	# Calculate match scores and add online status
	from shaadi.shaadi.utils.match_score import calculate_match_score
	from shaadi.shaadi.utils.privacy import apply_privacy_filters
	
	now = frappe.utils.now_datetime()
	online_threshold = frappe.utils.add_to_date(now, minutes=-5)  # 5 minutes threshold
	
	for profile in profiles:
		profile["match_score"] = calculate_match_score(current_user_profile, profile["name"])
		
		# Add online status
		last_active = profile.get("last_active")
		if last_active:
			last_active_dt = frappe.utils.get_datetime(last_active)
			is_online = last_active_dt > online_threshold
			profile["is_online"] = is_online
			profile["status_text"] = "Online" if is_online else get_last_seen_text(last_active)
		else:
			profile["is_online"] = False
			profile["status_text"] = "Offline"
		
		# Apply privacy filters
		profile = apply_privacy_filters(profile, current_user_profile)
	
	# Sort by match score if no specific order requested
	if not filters or not filters.get("sort_by"):
		profiles.sort(key=lambda x: x.get("match_score", 0), reverse=True)
	
	return profiles


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
def get_daily_recommendations(profile_id, limit=20):
	"""Get cached daily recommendations for a member"""
	current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if current_user_profile != profile_id:
		frappe.throw(_("Unauthorized access"))
	
	# Try to get from cache first
	cache_key = f"top_matches:{profile_id}"
	cached_matches = frappe.cache().get_value(cache_key)
	
	if cached_matches:
		# Get profile details for cached matches
		profile_ids = [m["profile_id"] for m in cached_matches[:limit]]
		profiles = frappe.get_all(
			"Member Profile",
			filters={"name": ["in", profile_ids], "is_active": 1},
			fields=[
				"name", "full_name", "age", "gender", "height_cm", "religion", "caste",
				"marital_status", "education", "occupation", "city", "state",
				"profile_photo", "profile_completeness", "verified"
			]
		)
		
		# Add match scores
		for profile in profiles:
			match_data = next((m for m in cached_matches if m["profile_id"] == profile["name"]), None)
			if match_data:
				profile["match_score"] = match_data["score"]
		
		return profiles
	
	# If not cached, compute on the fly
	from shaadi.shaadi.api.matchmaking import get_recommendations
	return get_recommendations(profile_id, limit)


@frappe.whitelist()
def get_profile_visitors(profile_id, limit=50):
	"""Get list of members who viewed this profile"""
	current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if current_user_profile != profile_id:
		frappe.throw(_("Unauthorized access"))
	
	# This would require a Profile View tracking DocType
	# For now, return empty list with TODO
	# TODO: Create Profile View DocType to track profile visits
	
	return {
		"visitors": [],
		"message": _("Profile visitor tracking will be implemented soon")
	}


@frappe.whitelist()
def get_shortlisted_profiles(profile_id, category=None):
	"""Get member's shortlisted profiles"""
	current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if current_user_profile != profile_id:
		frappe.throw(_("Unauthorized access"))
	
	filters = {"member": profile_id}
	if category:
		filters["category"] = category
	
	shortlists = frappe.get_all(
		"Shortlist",
		filters=filters,
		fields=["name", "shortlisted_profile", "category", "shortlisted_on", "note"],
		order_by="shortlisted_on desc"
	)
	
	# Get profile details
	for item in shortlists:
		profile_data = frappe.db.get_value(
			"Member Profile",
			item["shortlisted_profile"],
			["full_name", "age", "city", "education", "occupation", "profile_photo"],
			as_dict=True
		)
		item.update(profile_data)
	
	return shortlists


@frappe.whitelist()
def add_to_shortlist(profile_id, shortlisted_profile_id, category="Liked", note=""):
	"""Add a profile to shortlist"""
	current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if current_user_profile != profile_id:
		frappe.throw(_("Unauthorized access"))
	
	# Check if already shortlisted
	existing = frappe.db.exists("Shortlist", {
		"member": profile_id,
		"shortlisted_profile": shortlisted_profile_id
	})
	
	if existing:
		# Update category
		frappe.db.set_value("Shortlist", existing, {
			"category": category,
			"note": note
		})
		return {
			"success": True,
			"message": _("Shortlist updated"),
			"shortlist_id": existing
		}
	
	# Create new shortlist entry
	shortlist = frappe.get_doc({
		"doctype": "Shortlist",
		"member": profile_id,
		"shortlisted_profile": shortlisted_profile_id,
		"category": category,
		"note": note
	})
	shortlist.insert()
	
	# Publish real-time update
	frappe.publish_realtime("profile_shortlisted", {
		"member": profile_id,
		"shortlisted_profile": shortlisted_profile_id,
		"category": category,
		"shortlist_id": shortlist.name
	})
	
	# Get updated interaction status
	from shaadi.shaadi.api.matchmaking import get_profile_interaction_status
	updated_status = get_profile_interaction_status(shortlisted_profile_id)
	
	return {
		"success": True,
		"message": _("Profile added to shortlist"),
		"shortlist_id": shortlist.name,
		"interaction_status": updated_status
	}


@frappe.whitelist()
def remove_from_shortlist(profile_id, shortlisted_profile_id=None):
	"""Remove a profile from shortlist"""
	current_user_profile = frappe.db.get_value("Member Profile", {"user": frappe.session.user})
	if not current_user_profile:
		current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if current_user_profile != profile_id:
		frappe.throw(_("Unauthorized access"))
	
	# If shortlisted_profile_id is provided, find by member and shortlisted_profile
	if shortlisted_profile_id:
		shortlist_name = frappe.db.get_value("Shortlist", {
			"member": profile_id,
			"shortlisted_profile": shortlisted_profile_id
		})
		if not shortlist_name:
			frappe.throw(_("Shortlist entry not found"))
	else:
		# Assume profile_id is actually the shortlist_id for backward compatibility
		shortlist_name = profile_id
	
	shortlist = frappe.get_doc("Shortlist", shortlist_name)
	
	if current_user_profile != shortlist.member:
		frappe.throw(_("Unauthorized access"))
	
	shortlist.delete()
	
	return {
		"success": True,
		"message": _("Profile removed from shortlist")
	}
