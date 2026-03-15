import frappe
from frappe.model.document import Document
from frappe.utils import getdate, now_datetime
from datetime import datetime
from frappe import _


class MemberProfile(Document):
	def validate(self):
		"""Validate profile changes"""
		# Prevent manual subscription_plan changes if managed by Member Subscription
		if self.has_value_changed("subscription_plan") and not frappe.flags.in_patch:
			# Check if change is coming from Member Subscription sync
			if not frappe.flags.ignore_subscription_validation:
				# Allow only System Manager to manually change subscription_plan
				if "System Manager" not in frappe.get_roles():
					# Check if there's an active Member Subscription
					active_sub = frappe.db.exists(
						"Member Subscription",
						{
							"member_profile": self.name,
							"status": "Active"
						}
					)
					if active_sub:
						frappe.throw(_("Subscription plan is managed by Member Subscription. Please update the subscription record instead."))
	
	def before_save(self):
		self.calculate_age()
		self.calculate_profile_completeness()
	
	def calculate_age(self):
		if self.dob:
			today = getdate()
			dob = getdate(self.dob)
			age = today.year - dob.year
			if today.month < dob.month or (today.month == dob.month and today.day < dob.day):
				age -= 1
			self.age = age
	
	def after_insert(self):
		"""Create default Partner Preference and assign role after Member Profile is created"""
		from shaadi.shaadi.api.partner_preference import create_default_partner_preference
		try:
			create_default_partner_preference(self.name)
		except Exception as e:
			frappe.log_error(f"Failed to create Partner Preference for {self.name}: {str(e)}")
		
		# Assign Matrimonial Member role to user
		try:
			self.assign_matrimonial_role()
		except Exception as e:
			frappe.log_error(f"Failed to assign role for {self.email}: {str(e)}")
	
	def assign_matrimonial_role(self):
		"""Assign Matrimonial Member role to the user"""
		if not self.email:
			return
		
		# Check if user exists
		if not frappe.db.exists("User", self.email):
			return
		
		# Check if role already assigned
		if frappe.db.exists("Has Role", {"parent": self.email, "role": "Matrimonial Member"}):
			return
		
		# Assign role
		user_doc = frappe.get_doc("User", self.email)
		user_doc.append("roles", {"role": "Matrimonial Member"})
		user_doc.save(ignore_permissions=True)
		frappe.db.commit()
	
	def calculate_profile_completeness(self):
		total_fields = 0
		filled_fields = 0
		
		basic_fields = ['full_name', 'dob', 'gender', 'email', 'phone', 'religion', 'caste', 
		                'mother_tongue', 'height_cm', 'marital_status', 'education', 'occupation',
		                'city', 'state', 'profile_bio']
		
		for field in basic_fields:
			total_fields += 1
			if self.get(field):
				filled_fields += 1
		
		if self.profile_photo:
			filled_fields += 1
		total_fields += 1
		
		if self.profile_photos and len(self.profile_photos) > 0:
			filled_fields += 1
		total_fields += 1
		
		horoscope = frappe.db.exists("Horoscope Detail", {"member_profile": self.name})
		if horoscope:
			filled_fields += 1
		total_fields += 1
		
		family = frappe.db.exists("Family Detail", {"member_profile": self.name})
		if family:
			filled_fields += 1
		total_fields += 1
		
		preference = frappe.db.exists("Partner Preference", {"member_profile": self.name})
		if preference:
			filled_fields += 1
		total_fields += 1
		
		self.profile_completeness = (filled_fields / total_fields) * 100 if total_fields > 0 else 0
	
	def on_update(self):
		self.last_active = now_datetime()
