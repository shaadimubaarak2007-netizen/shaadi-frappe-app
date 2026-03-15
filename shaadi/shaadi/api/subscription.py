import frappe
from frappe import _
from frappe.utils import getdate, add_days, nowdate


@frappe.whitelist(allow_guest=True)
def get_subscription_plans():
	"""Get all active subscription plans"""
	plans = frappe.get_all(
		"Subscription Plan",
		filters={"is_active": 1},
		fields=[
			"name", "plan_name", "plan_type", "duration_days", "price_inr",
			"contacts_allowed", "messages_allowed", "can_view_contact", "can_send_message",
			"can_see_horoscope", "can_see_all_photos", "featured_profile", "priority_support"
		],
		order_by="price_inr asc"
	)
	
	return plans


@frappe.whitelist()
def get_current_subscription(profile_id):
	"""Get member's current active subscription"""
	current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if current_user_profile != profile_id:
		frappe.throw(_("Unauthorized access"))
	
	# First, check for active Member Subscription record
	subscription = frappe.db.get_value(
		"Member Subscription",
		{
			"member_profile": profile_id,
			"status": "Active"
		},
		["name", "plan", "start_date", "end_date", "contacts_used", 
		 "messages_today", "amount_paid"],
		as_dict=True
	)
	
	if subscription:
		# Get plan details from Member Subscription
		plan = frappe.get_doc("Subscription Plan", subscription["plan"])
		subscription["plan_details"] = {
			"plan_name": plan.plan_name,
			"plan_type": plan.plan_type,
			"contacts_allowed": plan.contacts_allowed,
			"messages_allowed": plan.messages_allowed,
			"can_view_contact": plan.can_view_contact,
			"can_send_message": plan.can_send_message,
			"can_see_horoscope": plan.can_see_horoscope,
			"can_see_all_photos": plan.can_see_all_photos,
			"featured_profile": plan.featured_profile,
			"priority_support": plan.priority_support
		}
		
		# Calculate remaining quota
		subscription["contacts_remaining"] = plan.contacts_allowed - subscription["contacts_used"]
		subscription["messages_remaining"] = plan.messages_allowed - subscription["messages_today"]
		subscription["days_remaining"] = (getdate(subscription["end_date"]) - getdate(nowdate())).days
		
		return subscription
	
	# Fallback: Check Member Profile.subscription_plan field
	profile_plan = frappe.db.get_value("Member Profile", profile_id, "subscription_plan")
	
	if profile_plan and profile_plan != "Free":
		# Get plan details from Member Profile field
		plan = frappe.get_doc("Subscription Plan", profile_plan)
		
		return {
			"plan_details": {
				"plan_name": plan.plan_name,
				"plan_type": plan.plan_type,
				"contacts_allowed": plan.contacts_allowed,
				"messages_allowed": plan.messages_allowed,
				"can_view_contact": plan.can_view_contact,
				"can_send_message": plan.can_send_message,
				"can_see_horoscope": plan.can_see_horoscope,
				"can_see_all_photos": plan.can_see_all_photos,
				"featured_profile": plan.featured_profile,
				"priority_support": plan.priority_support
			},
			"contacts_remaining": plan.contacts_allowed,
			"messages_remaining": plan.messages_allowed,
			"days_remaining": 365,  # Default to 1 year for manually assigned plans
			"start_date": nowdate(),
			"end_date": add_days(nowdate(), 365),
			"contacts_used": 0,
			"messages_today": 0
		}
	
	# No subscription found - return free plan
	return {
		"plan_details": {
			"plan_name": "Free Plan",
			"plan_type": "Free",
			"contacts_allowed": 0,
			"messages_allowed": 0,
			"can_view_contact": 0,
			"can_send_message": 0,
			"can_see_horoscope": 0,
			"can_see_all_photos": 0,
			"featured_profile": 0,
			"priority_support": 0
		},
		"contacts_remaining": 0,
		"messages_remaining": 0,
		"days_remaining": 0,
		"start_date": None,
		"end_date": None,
		"contacts_used": 0,
		"messages_today": 0
	}


@frappe.whitelist()
def create_subscription(profile_id, plan_id, payment_method="Razorpay", payment_id=None):
	"""Create a new subscription for a member"""
	current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if current_user_profile != profile_id:
		frappe.throw(_("Unauthorized access"))
	
	# Get plan details
	plan = frappe.get_doc("Subscription Plan", plan_id)
	
	if not plan.is_active:
		frappe.throw(_("This subscription plan is not available"))
	
	# Check for existing active subscription
	existing = frappe.db.exists("Member Subscription", {
		"member_profile": profile_id,
		"status": "Active"
	})
	
	if existing:
		frappe.throw(_("You already have an active subscription. Please wait for it to expire or contact support."))
	
	# Create subscription
	subscription = frappe.get_doc({
		"doctype": "Member Subscription",
		"member_profile": profile_id,
		"plan": plan_id,
		"amount_paid": plan.price_inr,
		"payment_method": payment_method,
		"payment_id": payment_id,
		"payment_status": "Pending" if not payment_id else "Paid",
		"status": "Pending" if not payment_id else "Active"
	})
	subscription.insert()
	
	return {
		"success": True,
		"message": _("Subscription created successfully"),
		"subscription_id": subscription.name,
		"payment_required": not payment_id
	}


@frappe.whitelist()
def check_feature_access(profile_id, feature):
	"""Check if member has access to a specific feature"""
	current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if current_user_profile != profile_id:
		frappe.throw(_("Unauthorized access"))
	
	# Get active subscription
	subscription = frappe.db.get_value(
		"Member Subscription",
		{
			"member_profile": profile_id,
			"status": "Active"
		},
		"plan"
	)
	
	if not subscription:
		# Free plan - no access to premium features
		return {
			"has_access": False,
			"message": _("This feature requires a subscription. Please upgrade your plan.")
		}
	
	# Get plan details
	plan = frappe.get_doc("Subscription Plan", subscription)
	
	feature_map = {
		"view_contact": plan.can_view_contact,
		"send_message": plan.can_send_message,
		"see_horoscope": plan.can_see_horoscope,
		"see_all_photos": plan.can_see_all_photos,
		"featured_profile": plan.featured_profile,
		"priority_support": plan.priority_support
	}
	
	has_access = feature_map.get(feature, False)
	
	return {
		"has_access": has_access,
		"plan_type": plan.plan_type,
		"message": _("Access granted") if has_access else _("Upgrade your plan to access this feature")
	}


@frappe.whitelist()
def get_usage_stats(profile_id):
	"""Get subscription usage statistics"""
	current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if current_user_profile != profile_id:
		frappe.throw(_("Unauthorized access"))
	
	# Get active subscription
	subscription = frappe.db.get_value(
		"Member Subscription",
		{
			"member_profile": profile_id,
			"status": "Active"
		},
		["name", "plan", "contacts_used", "messages_today", "start_date", "end_date"],
		as_dict=True
	)
	
	if not subscription:
		return {
			"plan_type": "Free",
			"contacts_used": 0,
			"contacts_allowed": 0,
			"messages_today": 0,
			"messages_allowed": 0,
			"days_remaining": 0
		}
	
	# Get plan limits
	plan = frappe.get_doc("Subscription Plan", subscription["plan"])
	
	return {
		"plan_type": plan.plan_type,
		"contacts_used": subscription["contacts_used"],
		"contacts_allowed": plan.contacts_allowed,
		"contacts_remaining": plan.contacts_allowed - subscription["contacts_used"],
		"messages_today": subscription["messages_today"],
		"messages_allowed": plan.messages_allowed,
		"messages_remaining": plan.messages_allowed - subscription["messages_today"],
		"days_remaining": (getdate(subscription["end_date"]) - getdate(nowdate())).days,
		"start_date": subscription["start_date"],
		"end_date": subscription["end_date"]
	}


@frappe.whitelist()
def cancel_subscription(subscription_id, reason=""):
	"""Cancel an active subscription"""
	subscription = frappe.get_doc("Member Subscription", subscription_id)
	
	current_user_profile = frappe.db.get_value("Member Profile", {"email": frappe.session.user})
	
	if current_user_profile != subscription.member_profile:
		frappe.throw(_("Unauthorized access"))
	
	if subscription.status != "Active":
		frappe.throw(_("Only active subscriptions can be cancelled"))
	
	subscription.status = "Cancelled"
	subscription.add_comment("Comment", f"Subscription cancelled. Reason: {reason}")
	subscription.save(ignore_permissions=True)
	
	# Update member profile
	frappe.db.set_value("Member Profile", subscription.member_profile, "subscription_plan", "Free")
	
	return {
		"success": True,
		"message": _("Subscription cancelled successfully")
	}
