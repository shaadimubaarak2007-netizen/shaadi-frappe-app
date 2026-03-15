import frappe
from frappe import _


@frappe.whitelist()
def get_partner_preference(profile_id=None):
	"""Get Partner Preference for a member profile"""
	if not profile_id:
		profile_id = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
		if not profile_id:
			profile_id = frappe.db.get_value("Member Profile", {"user": frappe.session.user})
	
	if not profile_id:
		frappe.throw(_("Member Profile not found"))
	
	# Get existing preference
	preference = frappe.db.get_value("Partner Preference", {"member_profile": profile_id}, "*", as_dict=True)
	
	if preference:
		# Get city preferences
		cities = frappe.get_all("Partner Preference City", 
			filters={"parent": preference.name},
			fields=["city"],
			pluck="city"
		)
		preference["cities"] = cities
		return preference
	
	return None


@frappe.whitelist()
def create_or_update_partner_preference(profile_id=None, preferences=None):
	"""Create or update Partner Preference for a member"""
	if not profile_id:
		profile_id = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
		if not profile_id:
			profile_id = frappe.db.get_value("Member Profile", {"user": frappe.session.user})
	
	if not profile_id:
		frappe.throw(_("Member Profile not found"))
	
	if not preferences:
		frappe.throw(_("Preferences data is required"))
	
	# Parse preferences if it's a string
	if isinstance(preferences, str):
		import json
		preferences = json.loads(preferences)
	
	# Check if preference already exists
	existing = frappe.db.get_value("Partner Preference", {"member_profile": profile_id})
	
	if existing:
		# Update existing preference
		doc = frappe.get_doc("Partner Preference", existing)
		doc.update(preferences)
		
		# Update cities if provided
		if "cities" in preferences:
			doc.city_preferences = []
			for city in preferences.get("cities", []):
				doc.append("city_preferences", {"city": city})
		
		doc.save(ignore_permissions=True)
		frappe.db.commit()
		
		return {
			"success": True,
			"message": _("Partner Preference updated successfully"),
			"preference": doc.as_dict()
		}
	else:
		# Create new preference
		doc = frappe.get_doc({
			"doctype": "Partner Preference",
			"member_profile": profile_id,
			**preferences
		})
		
		# Add cities if provided
		if "cities" in preferences:
			for city in preferences.get("cities", []):
				doc.append("city_preferences", {"city": city})
		
		doc.insert(ignore_permissions=True)
		frappe.db.commit()
		
		return {
			"success": True,
			"message": _("Partner Preference created successfully"),
			"preference": doc.as_dict()
		}


@frappe.whitelist()
def check_preference_exists(profile_id=None):
	"""Check if Partner Preference exists for a member"""
	if not profile_id:
		profile_id = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
		if not profile_id:
			profile_id = frappe.db.get_value("Member Profile", {"user": frappe.session.user})
	
	if not profile_id:
		return {"exists": False, "profile_id": None}
	
	exists = frappe.db.exists("Partner Preference", {"member_profile": profile_id})
	
	return {
		"exists": bool(exists),
		"profile_id": profile_id,
		"preference_name": exists if exists else None
	}


def create_default_partner_preference(member_profile_id):
	"""Create default Partner Preference when Member Profile is created"""
	# Check if preference already exists
	if frappe.db.exists("Partner Preference", {"member_profile": member_profile_id}):
		return
	
	# Get member profile to determine defaults
	member = frappe.get_doc("Member Profile", member_profile_id)
	
	# Set default age range based on member's age
	member_age = member.age or 25
	min_age = max(18, member_age - 5)
	max_age = min(60, member_age + 5)
	
	# Set default height range based on gender
	if member.gender == "Male":
		min_height = 150
		max_height = 175
		preferred_gender = "Female"
	else:
		min_height = 165
		max_height = 185
		preferred_gender = "Male"
	
	# Create default preference
	doc = frappe.get_doc({
		"doctype": "Partner Preference",
		"member_profile": member_profile_id,
		"preferred_gender": preferred_gender,
		"min_age": min_age,
		"max_age": max_age,
		"min_height_cm": min_height,
		"max_height_cm": max_height,
		"marital_status": "Never Married",
		"religion": "Any",
		"caste_bar": "Any",
		"manglik_pref": "Doesnt Matter",
		"kundali_must": 0,
		"diet_pref": "Any",
		"smoking_pref": "Doesnt Matter",
		"drinking_pref": "Doesnt Matter",
		"country_pref": "India",
		"about_partner": "Looking for a compatible life partner"
	})
	
	doc.insert(ignore_permissions=True)
	frappe.db.commit()
	
	return doc.name
