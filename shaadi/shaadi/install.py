import frappe
from frappe import _


def after_install():
	"""Run after app installation"""
	create_custom_roles()
	create_default_role_profiles()
	create_default_subscription_plans()
	configure_doctype_permissions()
	setup_existing_user_roles()
	frappe.db.commit()


def create_custom_roles():
	"""Create custom roles for Shaadi app - ERPNext pattern"""
	roles = [
		{
			"role_name": "Matrimonial Member",
			"desk_access": 0,
			"is_custom": 1,
			"home_page": "/frontend"
		},
		{
			"role_name": "Matrimonial Premium Member",
			"desk_access": 0,
			"is_custom": 1,
			"home_page": "/frontend"
		},
		{
			"role_name": "Matrimonial Moderator",
			"desk_access": 1,
			"is_custom": 1
		},
		{
			"role_name": "Matrimonial Admin",
			"desk_access": 1,
			"is_custom": 1
		},
		{
			"role_name": "Matrimonial Support",
			"desk_access": 1,
			"is_custom": 1
		}
	]
	
	for role_data in roles:
		if not frappe.db.exists("Role", role_data["role_name"]):
			role = frappe.get_doc({
				"doctype": "Role",
				**role_data
			})
			role.insert(ignore_permissions=True)
			frappe.logger().info(f"Created role: {role_data['role_name']}")


def create_default_role_profiles():
	"""Create default role profiles - ERPNext pattern"""
	for role_profile_name, roles in DEFAULT_ROLE_PROFILES.items():
		if frappe.db.exists("Role Profile", role_profile_name):
			# Update existing role profile
			role_profile = frappe.get_doc("Role Profile", role_profile_name)
			existing_roles = [row.role for row in role_profile.roles]
			
			# Remove roles not in the new list
			role_profile.roles = [row for row in role_profile.roles if row.role in roles]
			
			# Add new roles
			for role in roles:
				if role not in existing_roles:
					role_profile.append("roles", {"role": role})
			
			role_profile.save(ignore_permissions=True)
			frappe.logger().info(f"Updated role profile: {role_profile_name}")
			continue
		
		# Create new role profile
		role_profile = frappe.new_doc("Role Profile")
		role_profile.role_profile = role_profile_name
		for role in roles:
			role_profile.append("roles", {"role": role})
		
		role_profile.insert(ignore_permissions=True)
		frappe.logger().info(f"Created role profile: {role_profile_name}")


def configure_doctype_permissions():
	"""Configure permissions for all Shaadi DocTypes"""
	
	# Member Profile - All roles can read, members can create/update their own
	set_doctype_permissions("Member Profile", [
		{"role": "Matrimonial Member", "read": 1, "write": 1, "create": 1},
		{"role": "Matrimonial Premium Member", "read": 1, "write": 1, "create": 1},
		{"role": "Matrimonial Moderator", "read": 1, "write": 1, "create": 1, "delete": 1},
		{"role": "Matrimonial Admin", "read": 1, "write": 1, "create": 1, "delete": 1},
		{"role": "Matrimonial Support", "read": 1, "write": 1}
	])
	
	# Horoscope Detail - Members can manage their own
	set_doctype_permissions("Horoscope Detail", [
		{"role": "Matrimonial Member", "read": 1, "write": 1, "create": 1},
		{"role": "Matrimonial Moderator", "read": 1, "write": 1, "delete": 1},
		{"role": "Matrimonial Admin", "read": 1, "write": 1, "delete": 1}
	])
	
	# Family Detail - Members can manage their own
	set_doctype_permissions("Family Detail", [
		{"role": "Matrimonial Member", "read": 1, "write": 1, "create": 1},
		{"role": "Matrimonial Moderator", "read": 1, "write": 1, "delete": 1},
		{"role": "Matrimonial Admin", "read": 1, "write": 1, "delete": 1}
	])
	
	# Partner Preference - Members can manage their own
	set_doctype_permissions("Partner Preference", [
		{"role": "Matrimonial Member", "read": 1, "write": 1, "create": 1},
		{"role": "Matrimonial Admin", "read": 1, "write": 1, "delete": 1}
	])
	
	# Match Request - Members can send/respond
	set_doctype_permissions("Match Request", [
		{"role": "Matrimonial Member", "read": 1, "write": 1, "create": 1},
		{"role": "Matrimonial Moderator", "read": 1, "write": 1, "delete": 1},
		{"role": "Matrimonial Admin", "read": 1, "write": 1, "delete": 1}
	])
	
	# Conversation - Members can access their conversations
	set_doctype_permissions("Conversation", [
		{"role": "Matrimonial Member", "read": 1, "write": 1, "create": 1},
		{"role": "Matrimonial Moderator", "read": 1, "delete": 1},
		{"role": "Matrimonial Admin", "read": 1, "delete": 1}
	])
	
	# Conversation Message - Members can send messages
	set_doctype_permissions("Conversation Message", [
		{"role": "Matrimonial Member", "read": 1, "write": 1, "create": 1},
		{"role": "Matrimonial Moderator", "read": 1, "delete": 1},
		{"role": "Matrimonial Admin", "read": 1, "delete": 1}
	])
	
	# Shortlist - Members only
	set_doctype_permissions("Shortlist", [
		{"role": "Matrimonial Member", "read": 1, "write": 1, "create": 1, "delete": 1},
		{"role": "Matrimonial Admin", "read": 1}
	])
	
	# Subscription Plan - Read for all, manage for admin
	set_doctype_permissions("Subscription Plan", [
		{"role": "Matrimonial Member", "read": 1},
		{"role": "Matrimonial Admin", "read": 1, "write": 1, "create": 1, "delete": 1}
	])
	
	# Member Subscription - Members can view their own, admin manages
	set_doctype_permissions("Member Subscription", [
		{"role": "Matrimonial Member", "read": 1},
		{"role": "Matrimonial Admin", "read": 1, "write": 1, "create": 1, "delete": 1},
		{"role": "Matrimonial Support", "read": 1, "write": 1}
	])
	
	# Privacy Setting - Members manage their own
	set_doctype_permissions("Privacy Setting", [
		{"role": "Matrimonial Member", "read": 1, "write": 1, "create": 1},
		{"role": "Matrimonial Admin", "read": 1, "write": 1}
	])
	
	# Success Story - Members create, moderators approve, admin manages
	set_doctype_permissions("Success Story", [
		{"role": "Matrimonial Member", "read": 1, "write": 1, "create": 1},
		{"role": "Matrimonial Moderator", "read": 1, "write": 1},
		{"role": "Matrimonial Admin", "read": 1, "write": 1, "create": 1, "delete": 1}
	])
	
	# Child Tables - Members can manage their own
	set_doctype_permissions("Member Profile Photo", [
		{"role": "Matrimonial Member", "read": 1, "write": 1, "create": 1, "delete": 1},
		{"role": "Matrimonial Moderator", "read": 1, "write": 1, "delete": 1},
		{"role": "Matrimonial Admin", "read": 1, "write": 1, "delete": 1}
	])
	
	set_doctype_permissions("Partner Preference City", [
		{"role": "Matrimonial Member", "read": 1, "write": 1, "create": 1, "delete": 1},
		{"role": "Matrimonial Admin", "read": 1, "write": 1, "delete": 1}
	])
	
	set_doctype_permissions("Privacy Blocked Member", [
		{"role": "Matrimonial Member", "read": 1, "write": 1, "create": 1, "delete": 1},
		{"role": "Matrimonial Admin", "read": 1, "write": 1, "delete": 1}
	])
	
	# Swipe Match - Members can create and view their own swipes
	set_doctype_permissions("Swipe Match", [
		{"role": "Matrimonial Member", "read": 1, "write": 1, "create": 1},
		{"role": "Matrimonial Premium Member", "read": 1, "write": 1, "create": 1},
		{"role": "Matrimonial Moderator", "read": 1, "write": 1, "delete": 1},
		{"role": "Matrimonial Admin", "read": 1, "write": 1, "create": 1, "delete": 1}
	])


def set_doctype_permissions(doctype, permissions):
	"""Helper function to set permissions for a DocType"""
	try:
		# Clear existing custom permissions
		frappe.db.delete("Custom DocPerm", {"parent": doctype})
		
		# Add new permissions
		for perm in permissions:
			if not frappe.db.exists("Custom DocPerm", {"parent": doctype, "role": perm["role"]}):
				doc_perm = frappe.get_doc({
					"doctype": "Custom DocPerm",
					"parent": doctype,
					"parenttype": "DocType",
					"parentfield": "permissions",
					"role": perm["role"],
					"read": perm.get("read", 0),
					"write": perm.get("write", 0),
					"create": perm.get("create", 0),
					"delete": perm.get("delete", 0),
					"submit": perm.get("submit", 0),
					"cancel": perm.get("cancel", 0),
					"amend": perm.get("amend", 0),
					"report": perm.get("report", 1) if perm.get("read", 0) else 0,
					"export": perm.get("export", 1) if perm.get("read", 0) else 0,
					"print": perm.get("print", 1) if perm.get("read", 0) else 0,
					"email": perm.get("email", 1) if perm.get("read", 0) else 0,
					"share": perm.get("share", 1) if perm.get("write", 0) else 0
				})
				doc_perm.insert(ignore_permissions=True)
		
		frappe.logger().info(f"Configured permissions for {doctype}")
	except Exception as e:
		frappe.logger().error(f"Error configuring permissions for {doctype}: {str(e)}")


def create_default_subscription_plans():
	"""Create default subscription plans"""
	plans = [
		{
			"plan_name": "Free",
			"plan_type": "Free",
			"duration_days": 0,
			"price_inr": 0,
			"contacts_allowed": 0,
			"messages_allowed": 0,
			"can_view_contact": 0,
			"can_send_message": 0,
			"can_see_horoscope": 0,
			"can_see_all_photos": 0,
			"featured_profile": 0,
			"priority_support": 0,
			"is_active": 1
		},
		{
			"plan_name": "Silver",
			"plan_type": "Silver",
			"duration_days": 30,
			"price_inr": 999,
			"contacts_allowed": 10,
			"messages_allowed": 20,
			"can_view_contact": 1,
			"can_send_message": 1,
			"can_see_horoscope": 0,
			"can_see_all_photos": 0,
			"featured_profile": 0,
			"priority_support": 0,
			"is_active": 1
		},
		{
			"plan_name": "Gold",
			"plan_type": "Gold",
			"duration_days": 90,
			"price_inr": 2499,
			"contacts_allowed": 50,
			"messages_allowed": 100,
			"can_view_contact": 1,
			"can_send_message": 1,
			"can_see_horoscope": 1,
			"can_see_all_photos": 1,
			"featured_profile": 0,
			"priority_support": 0,
			"is_active": 1
		},
		{
			"plan_name": "Platinum",
			"plan_type": "Platinum",
			"duration_days": 180,
			"price_inr": 4999,
			"contacts_allowed": 150,
			"messages_allowed": 500,
			"can_view_contact": 1,
			"can_send_message": 1,
			"can_see_horoscope": 1,
			"can_see_all_photos": 1,
			"featured_profile": 1,
			"priority_support": 1,
			"is_active": 1
		},
		{
			"plan_name": "Diamond",
			"plan_type": "Diamond",
			"duration_days": 365,
			"price_inr": 8999,
			"contacts_allowed": 999999,
			"messages_allowed": 999999,
			"can_view_contact": 1,
			"can_send_message": 1,
			"can_see_horoscope": 1,
			"can_see_all_photos": 1,
			"featured_profile": 1,
			"priority_support": 1,
			"is_active": 1
		}
	]
	
	for plan_data in plans:
		if not frappe.db.exists("Subscription Plan", plan_data["plan_name"]):
			plan = frappe.get_doc({
				"doctype": "Subscription Plan",
				**plan_data
			})
			plan.insert(ignore_permissions=True)
			frappe.logger().info(f"Created subscription plan: {plan_data['plan_name']}")


# Role Profile Configuration - ERPNext Pattern
DEFAULT_ROLE_PROFILES = {
	"Matrimonial Free Member": [
		"Matrimonial Member"
	],
	"Matrimonial Silver Member": [
		"Matrimonial Member",
		"Matrimonial Premium Member"
	],
	"Matrimonial Gold Member": [
		"Matrimonial Member",
		"Matrimonial Premium Member"
	],
	"Matrimonial Platinum Member": [
		"Matrimonial Member",
		"Matrimonial Premium Member"
	],
	"Matrimonial Diamond Member": [
		"Matrimonial Member",
		"Matrimonial Premium Member"
	],
	"Matrimonial Content Moderator": [
		"Matrimonial Moderator",
		"Matrimonial Support"
	],
	"Matrimonial Platform Admin": [
		"Matrimonial Admin",
		"Matrimonial Moderator",
		"Matrimonial Support",
		"Matrimonial Member"
	]
}


def setup_existing_user_roles():
	"""Setup roles for existing users - called during installation"""
	from shaadi.shaadi.api.user_management import setup_existing_user_roles as setup_roles
	try:
		result = setup_roles()
		frappe.logger().info(f"Role assignment completed: {result.get('message', 'Success')}")
		return result
	except Exception as e:
		frappe.logger().error(f"Error in role assignment: {str(e)}")
		return {"success": False, "error": str(e)}
