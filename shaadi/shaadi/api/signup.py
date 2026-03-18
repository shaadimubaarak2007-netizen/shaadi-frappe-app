"""
Custom signup API for Shaadi app
Handles user registration and member profile creation
"""
import frappe
from frappe import _
from frappe.utils import validate_email_address

@frappe.whitelist(allow_guest=True)
def register_member(full_name, email, gender, dob, phone, city, state, religion, marital_status, education, occupation):
	"""
	Register a new member with user account and profile
	This combines user creation and member profile creation in one API call
	Uses Frappe's built-in sign_up() which sends password reset email
	"""
	try:
		# Validate email
		validate_email_address(email, True)
		
		# Check if user already exists
		if frappe.db.exists("User", email):
			frappe.throw(_("User {0} already exists").format(email))
		
		# Create user account using Frappe's built-in signup
		# This will send a password reset email automatically
		from frappe.core.doctype.user.user import sign_up
		sign_up(email=email, full_name=full_name, redirect_to="/signin")
		
		# Get the created user and add Matrimonial Member role
		# Using the same pattern as HRMS for adding roles
		user = frappe.get_doc("User", email)
		user.flags.ignore_permissions = True
		user.add_roles("Matrimonial Member")
		frappe.db.commit()
		
		# Create member profile linked to the user
		member_profile = frappe.get_doc({
			"doctype": "Member Profile",
			"user": email,  # Link to the User document
			"full_name": full_name,
			"email": email,
			"gender": gender,
			"dob": dob,
			"phone": phone,
			"city": city,
			"state": state,
			"religion": religion,
			"marital_status": marital_status,
			"education": education,
			"occupation": occupation,
			"is_active": 1
		})
		
		# Insert with ignore_permissions since this is guest access
		member_profile.insert(ignore_permissions=True)
		frappe.db.commit()
		
		return {
			"success": True,
			"message": _("Registration successful! A password reset link has been sent to your email. Please check your inbox and set your password to login."),
			"user": email,
			"member_profile": member_profile.name
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Member Registration Error")
		frappe.throw(str(e))
