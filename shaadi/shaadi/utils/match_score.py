import frappe


def calculate_match_score(profile1_id, profile2_id):
	"""
	Calculate compatibility score between two profiles (0-100)
	Based on 7 dimensions with configurable weights
	"""
	
	profile1 = frappe.get_doc("Member Profile", profile1_id)
	profile2 = frappe.get_doc("Member Profile", profile2_id)
	
	# Get partner preferences
	pref1 = frappe.db.get_value("Partner Preference", {"member_profile": profile1_id}, "*", as_dict=True)
	pref2 = frappe.db.get_value("Partner Preference", {"member_profile": profile2_id}, "*", as_dict=True)
	
	if not pref1 or not pref2:
		return 0
	
	# Default weights (can be made configurable)
	weights = {
		"religion": 20,
		"caste": 15,
		"age": 15,
		"location": 10,
		"education": 15,
		"income": 10,
		"manglik": 15
	}
	
	score = 0
	total_weight = sum(weights.values())
	
	# 1. Religion match
	if profile1.religion == profile2.religion:
		score += weights["religion"]
	
	# 2. Caste match
	if profile1.caste == profile2.caste:
		score += weights["caste"]
	
	# 3. Age compatibility
	age_diff = abs(profile1.age - profile2.age)
	if age_diff <= 3:
		score += weights["age"]
	elif age_diff <= 5:
		score += weights["age"] * 0.7
	elif age_diff <= 7:
		score += weights["age"] * 0.4
	
	# 4. Location match
	if profile1.city == profile2.city:
		score += weights["location"]
	elif profile1.state == profile2.state:
		score += weights["location"] * 0.6
	elif profile1.country_of_residence == profile2.country_of_residence:
		score += weights["location"] * 0.3
	
	# 5. Education compatibility
	education_levels = {
		"Below 10th": 1,
		"10th Pass": 2,
		"12th Pass": 3,
		"Diploma": 4,
		"Graduation": 5,
		"Post Graduation": 6,
		"Doctorate": 7
	}
	
	edu1_level = education_levels.get(profile1.education, 0)
	edu2_level = education_levels.get(profile2.education, 0)
	
	if edu1_level and edu2_level:
		edu_diff = abs(edu1_level - edu2_level)
		if edu_diff == 0:
			score += weights["education"]
		elif edu_diff == 1:
			score += weights["education"] * 0.7
		elif edu_diff == 2:
			score += weights["education"] * 0.4
	
	# 6. Income compatibility
	income_levels = {
		"No Income": 0,
		"Below 2 Lakh": 1,
		"2-5 Lakh": 2,
		"5-10 Lakh": 3,
		"10-20 Lakh": 4,
		"20-50 Lakh": 5,
		"Above 50 Lakh": 6
	}
	
	inc1_level = income_levels.get(profile1.annual_income_band, 0)
	inc2_level = income_levels.get(profile2.annual_income_band, 0)
	
	if inc1_level and inc2_level:
		inc_diff = abs(inc1_level - inc2_level)
		if inc_diff <= 1:
			score += weights["income"]
		elif inc_diff == 2:
			score += weights["income"] * 0.6
	
	# 7. Manglik compatibility
	if profile1.manglik_status == profile2.manglik_status:
		score += weights["manglik"]
	elif profile1.manglik_status == "Not Known" or profile2.manglik_status == "Not Known":
		score += weights["manglik"] * 0.5
	
	# Normalize to 0-100
	final_score = (score / total_weight) * 100
	
	return round(final_score, 2)


def get_top_matches(profile_id, limit=50):
	"""
	Get top matches for a profile based on compatibility score
	Used for daily precomputation
	"""
	
	member = frappe.get_doc("Member Profile", profile_id)
	
	# Get all active profiles of opposite gender
	filters = {
		"is_active": 1,
		"name": ["!=", profile_id],
		"gender": "Female" if member.gender == "Male" else "Male"
	}
	
	profiles = frappe.get_all("Member Profile", filters=filters, pluck="name")
	
	# Calculate scores for all profiles
	matches = []
	for profile in profiles:
		score = calculate_match_score(profile_id, profile)
		if score > 0:
			matches.append({
				"profile_id": profile,
				"score": score
			})
	
	# Sort by score and return top matches
	matches.sort(key=lambda x: x["score"], reverse=True)
	
	return matches[:limit]
