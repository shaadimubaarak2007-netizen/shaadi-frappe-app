import frappe
from frappe import _
from frappe.utils import random_string, now_datetime
import re


@frappe.whitelist(allow_guest=True)
def send_otp(phone):
	"""Send OTP to phone number for registration/login"""
	if not phone:
		frappe.throw(_("Phone number is required"))
	
	# Validate phone format
	if not re.match(r'^\+?[1-9]\d{9,14}$', phone):
		frappe.throw(_("Invalid phone number format"))
	
	# Generate 6-digit OTP
	otp = random_string(6, digits_only=True)
	
	# Store OTP in cache with 10-minute expiry
	cache_key = f"otp:{phone}"
	frappe.cache().set_value(cache_key, otp, expires_in_sec=600)
	
	# Send OTP via SMS
	from shaadi.shaadi.utils.notifications import send_otp_sms
	send_otp_sms(phone, otp)
	
	return {
		"success": True,
		"message": _("OTP sent successfully"),
		"otp": otp if frappe.conf.developer_mode else None  # Only in dev mode
	}


@frappe.whitelist(allow_guest=True)
def verify_otp(phone, otp):
	"""Verify OTP and create/login user"""
	if not phone or not otp:
		frappe.throw(_("Phone and OTP are required"))
	
	# Get stored OTP from cache
	cache_key = f"otp:{phone}"
	stored_otp = frappe.cache().get_value(cache_key)
	
	if not stored_otp:
		frappe.throw(_("OTP expired or invalid"))
	
	if stored_otp != otp:
		frappe.throw(_("Invalid OTP"))
	
	# Clear OTP from cache
	frappe.cache().delete_value(cache_key)
	
	# Check if user exists
	user = frappe.db.get_value("User", {"phone": phone})
	
	if user:
		# Login existing user
		frappe.local.login_manager.login_as(user)
		frappe.local.login_manager.user = user
		
		return {
			"success": True,
			"message": _("Login successful"),
			"user": user
		}
	else:
		# Return success but indicate registration needed
		return {
			"success": True,
			"message": _("OTP verified. Please complete registration"),
			"phone": phone,
			"registration_required": True
		}


@frappe.whitelist(allow_guest=True)
def register(phone, full_name, email, gender, dob):
	"""Register new member"""
	if not all([phone, full_name, email, gender, dob]):
		frappe.throw(_("All fields are required"))
	
	# Validate email
	from frappe.utils import validate_email_address
	if not validate_email_address(email):
		frappe.throw(_("Invalid email address"))
	
	# Check if user already exists
	if frappe.db.exists("User", {"phone": phone}):
		frappe.throw(_("User with this phone already exists"))
	
	if frappe.db.exists("User", {"email": email}):
		frappe.throw(_("User with this email already exists"))
	
	# Create User
	user = frappe.get_doc({
		"doctype": "User",
		"email": email,
		"first_name": full_name,
		"phone": phone,
		"enabled": 1,
		"send_welcome_email": 0,
		"user_type": "Website User"
	})
	user.insert(ignore_permissions=True)
	
	# Add Matrimonial Member role
	user.add_roles("Matrimonial Member")
	
	# Create Member Profile
	profile = frappe.get_doc({
		"doctype": "Member Profile",
		"full_name": full_name,
		"email": email,
		"phone": phone,
		"gender": gender,
		"dob": dob,
		"is_active": 1
	})
	profile.insert(ignore_permissions=True)
	
	# Create default Privacy Setting
	privacy = frappe.get_doc({
		"doctype": "Privacy Setting",
		"member_profile": profile.name,
		"hide_contact_until_accepted": 1,
		"profile_visible_to": "Everyone"
	})
	privacy.insert(ignore_permissions=True)
	
	# Login user
	frappe.local.login_manager.login_as(user.name)
	frappe.local.login_manager.user = user.name
	
	return {
		"success": True,
		"message": _("Registration successful"),
		"user": user.name,
		"profile": profile.name
	}


@frappe.whitelist()
def get_current_member_profile():
	"""Get current logged in user's member profile"""
	if frappe.session.user == "Guest":
		frappe.throw(_("Please login to continue"))
	
	# First try to find by user field
	profile = frappe.db.get_value("Member Profile", {"user": frappe.session.user}, "name")
	
	# Fallback to email if user field is not set
	if not profile:
		profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user}, "name")
	
	if not profile:
		frappe.throw(_("Member profile not found for this user"))
	
	return frappe.get_doc("Member Profile", profile)
