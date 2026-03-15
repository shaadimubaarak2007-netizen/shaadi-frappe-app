import frappe
from frappe import _


def create_member_role():
	"""Create Member role if it doesn't exist"""
	if not frappe.db.exists("Role", "Member"):
		role_doc = frappe.get_doc({
			"doctype": "Role",
			"role_name": "Member",
			"desk_access": 0,
			"is_custom": 1
		})
		role_doc.insert(ignore_permissions=True)
		frappe.db.commit()
		return role_doc.name
	return "Member"


def assign_member_role_to_user(user_email):
	"""Assign Member role to a user"""
	if not frappe.db.exists("Has Role", {"parent": user_email, "role": "Member"}):
		user_doc = frappe.get_doc("User", user_email)
		user_doc.append("roles", {"role": "Member"})
		user_doc.save(ignore_permissions=True)
		frappe.db.commit()


def setup_member_permissions():
	"""Setup proper permissions for Member role on relevant DocTypes"""
	
	# Create Member role first
	create_member_role()
	
	# DocTypes that Members should have access to
	member_doctypes = [
		{
			"doctype": "Member Profile",
			"permissions": {
				"create": 1,
				"read": 1,
				"write": 1,
				"if_owner": 1
			}
		},
		{
			"doctype": "Partner Preference", 
			"permissions": {
				"create": 1,
				"read": 1,
				"write": 1,
				"if_owner": 1
			}
		},
		{
			"doctype": "Swipe Match",
			"permissions": {
				"create": 1,
				"read": 1,
				"write": 1,
				"if_owner": 1
			}
		},
		{
			"doctype": "Match Request",
			"permissions": {
				"create": 1,
				"read": 1,
				"write": 1,
				"if_owner": 1
			}
		},
		{
			"doctype": "Shortlist",
			"permissions": {
				"create": 1,
				"read": 1,
				"write": 1,
				"if_owner": 1
			}
		}
	]
	
	for doctype_config in member_doctypes:
		# Check if permission already exists
		existing = frappe.db.exists("Custom DocPerm", {
			"parent": doctype_config["doctype"],
			"role": "Member"
		})
		
		if not existing:
			# Create custom permission
			perm_doc = frappe.get_doc({
				"doctype": "Custom DocPerm",
				"parent": doctype_config["doctype"],
				"parenttype": "DocType",
				"parentfield": "permissions",
				"role": "Member",
				**doctype_config["permissions"]
			})
			perm_doc.insert(ignore_permissions=True)
	
	frappe.db.commit()
