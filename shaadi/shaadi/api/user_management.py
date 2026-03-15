import frappe
from frappe import _


@frappe.whitelist()
def assign_matrimonial_role_to_existing_users():
	"""Assign Matrimonial Member role to existing users who have Member Profiles"""
	
	# Get all Member Profiles with email addresses
	member_profiles = frappe.get_all("Member Profile", 
		filters={"email": ["!=", ""]},
		fields=["name", "email"]
	)
	
	assigned_count = 0
	
	for profile in member_profiles:
		try:
			# Check if user exists
			if not frappe.db.exists("User", profile.email):
				continue
			
			# Check if role already assigned
			if frappe.db.exists("Has Role", {"parent": profile.email, "role": "Matrimonial Member"}):
				continue
			
			# Assign role
			user_doc = frappe.get_doc("User", profile.email)
			user_doc.append("roles", {"role": "Matrimonial Member"})
			user_doc.save(ignore_permissions=True)
			assigned_count += 1
			
		except Exception as e:
			frappe.log_error(f"Failed to assign role to {profile.email}: {str(e)}")
	
	frappe.db.commit()
	
	return {
		"success": True,
		"message": f"Assigned Matrimonial Member role to {assigned_count} users",
		"assigned_count": assigned_count
	}


def setup_existing_user_roles():
	"""Setup roles for existing users - called during installation"""
	try:
		result = assign_matrimonial_role_to_existing_users()
		frappe.logger().info(f"Role assignment completed: {result['message']}")
		return result
	except Exception as e:
		frappe.logger().error(f"Error in role assignment: {str(e)}")
		return {"success": False, "error": str(e)}
