import frappe
from frappe import _
from frappe.utils import getdate, nowdate


def has_active_subscription(profile_id):
	"""Check if member has an active subscription"""
	subscription = frappe.db.exists("Member Subscription", {
		"member_profile": profile_id,
		"status": "Active"
	})
	
	return bool(subscription)


def get_subscription_plan(profile_id):
	"""Get member's current subscription plan"""
	subscription = frappe.db.get_value(
		"Member Subscription",
		{
			"member_profile": profile_id,
			"status": "Active"
		},
		"plan"
	)
	
	if subscription:
		return frappe.get_doc("Subscription Plan", subscription)
	
	# Return Free plan
	free_plan = frappe.db.get_value("Subscription Plan", {"plan_type": "Free"})
	if free_plan:
		return frappe.get_doc("Subscription Plan", free_plan)
	
	return None


def can_send_interest(profile_id):
	"""Check if member can send interest (check contact quota)"""
	plan = get_subscription_plan(profile_id)
	
	if not plan:
		return False
	
	# Free plan cannot send interests
	if plan.plan_type == "Free":
		return False
	
	# Check quota
	subscription = frappe.db.get_value(
		"Member Subscription",
		{
			"member_profile": profile_id,
			"status": "Active"
		},
		["contacts_used", "plan"],
		as_dict=True
	)
	
	if not subscription:
		return False
	
	plan_doc = frappe.get_doc("Subscription Plan", subscription["plan"])
	
	# Check if quota exceeded
	if subscription["contacts_used"] >= plan_doc.contacts_allowed:
		return False
	
	return True


def can_send_message(profile_id):
	"""Check if member can send message (check message quota)"""
	plan = get_subscription_plan(profile_id)
	
	if not plan:
		return False
	
	# Free plan cannot send messages
	if plan.plan_type == "Free":
		return False
	
	if not plan.can_send_message:
		return False
	
	# Check daily quota
	subscription = frappe.db.get_value(
		"Member Subscription",
		{
			"member_profile": profile_id,
			"status": "Active"
		},
		["messages_today", "plan"],
		as_dict=True
	)
	
	if not subscription:
		return False
	
	plan_doc = frappe.get_doc("Subscription Plan", subscription["plan"])
	
	# Check if daily quota exceeded
	if subscription["messages_today"] >= plan_doc.messages_allowed:
		return False
	
	return True


def increment_contact_usage(profile_id):
	"""Increment contact usage count"""
	subscription = frappe.db.get_value(
		"Member Subscription",
		{
			"member_profile": profile_id,
			"status": "Active"
		},
		"name"
	)
	
	if subscription:
		frappe.db.sql("""
			UPDATE `tabMember Subscription`
			SET contacts_used = contacts_used + 1
			WHERE name = %s
		""", (subscription,))
		frappe.db.commit()


def increment_message_usage(profile_id):
	"""Increment daily message count"""
	subscription = frappe.db.get_value(
		"Member Subscription",
		{
			"member_profile": profile_id,
			"status": "Active"
		},
		"name"
	)
	
	if subscription:
		frappe.db.sql("""
			UPDATE `tabMember Subscription`
			SET messages_today = messages_today + 1
			WHERE name = %s
		""", (subscription,))
		frappe.db.commit()


def get_remaining_quota(profile_id):
	"""Get remaining quota for contacts and messages"""
	subscription = frappe.db.get_value(
		"Member Subscription",
		{
			"member_profile": profile_id,
			"status": "Active"
		},
		["contacts_used", "messages_today", "plan"],
		as_dict=True
	)
	
	if not subscription:
		return {
			"contacts_remaining": 0,
			"messages_remaining": 0,
			"plan_type": "Free"
		}
	
	plan = frappe.get_doc("Subscription Plan", subscription["plan"])
	
	return {
		"contacts_remaining": max(0, plan.contacts_allowed - subscription["contacts_used"]),
		"messages_remaining": max(0, plan.messages_allowed - subscription["messages_today"]),
		"contacts_used": subscription["contacts_used"],
		"messages_today": subscription["messages_today"],
		"plan_type": plan.plan_type
	}


def has_feature_access(profile_id, feature):
	"""Check if member has access to a specific feature"""
	plan = get_subscription_plan(profile_id)
	
	if not plan:
		return False
	
	feature_map = {
		"view_contact": plan.can_view_contact,
		"send_message": plan.can_send_message,
		"see_horoscope": plan.can_see_horoscope,
		"see_all_photos": plan.can_see_all_photos,
		"featured_profile": plan.featured_profile,
		"priority_support": plan.priority_support
	}
	
	return feature_map.get(feature, False)


def is_subscription_expired(subscription_id):
	"""Check if a subscription has expired"""
	subscription = frappe.get_doc("Member Subscription", subscription_id)
	
	if subscription.status != "Active":
		return True
	
	if getdate(subscription.end_date) < getdate(nowdate()):
		return True
	
	return False


def reset_daily_message_count():
	"""Reset daily message count for all active subscriptions (called by scheduler)"""
	frappe.db.sql("""
		UPDATE `tabMember Subscription`
		SET messages_today = 0
		WHERE status = 'Active'
	""")
	frappe.db.commit()
	
	frappe.logger().info("Reset daily message count for all active subscriptions")


def get_plan_features(plan_type):
	"""Get features for a specific plan type"""
	plan = frappe.db.get_value("Subscription Plan", {"plan_type": plan_type}, "*", as_dict=True)
	
	if not plan:
		return None
	
	return {
		"plan_name": plan["plan_name"],
		"plan_type": plan["plan_type"],
		"duration_days": plan["duration_days"],
		"price_inr": plan["price_inr"],
		"contacts_allowed": plan["contacts_allowed"],
		"messages_allowed": plan["messages_allowed"],
		"can_view_contact": plan["can_view_contact"],
		"can_send_message": plan["can_send_message"],
		"can_see_horoscope": plan["can_see_horoscope"],
		"can_see_all_photos": plan["can_see_all_photos"],
		"featured_profile": plan["featured_profile"],
		"priority_support": plan["priority_support"]
	}
