# Copyright (c) 2024, Amit Kumar and contributors
# For license information, please see license.txt

"""
Payment Processing API for Shaadi Platform
Integrates with Razorpay via the payments app
Following LMS payment pattern for reliability
"""

import frappe
from frappe import _
from payments.utils import get_payment_gateway_controller


def get_payment_gateway():
	"""Get configured payment gateway from settings"""
	# For now, hardcoded to Razorpay. Can be made configurable later.
	return "Razorpay"


@frappe.whitelist()
def initiate_payment(subscription_plan_id):
	"""
	Initiate payment for a subscription plan purchase
	Following LMS two-step pattern:
	1. Record payment transaction BEFORE redirect
	2. Get payment URL with transaction reference
	3. Redirect user to payment gateway
	
	Args:
		subscription_plan_id: ID of the subscription plan to purchase
	
	Returns:
		dict: Payment URL and transaction details
	"""
	try:
		# Get current member profile
		member_profile = frappe.db.get_value(
			"Member Profile",
			{"email": frappe.session.user},
			"name"
		)
		
		if not member_profile:
			frappe.throw(_("Member profile not found"))
		
		# Get subscription plan details
		plan = frappe.get_doc("Subscription Plan", subscription_plan_id)
		
		if not plan:
			frappe.throw(_("Subscription plan not found"))
		
		# Check if user already has an active subscription to this plan
		active_subscription = frappe.db.get_value(
			"Subscription",
			{
				"member_profile": member_profile,
				"subscription_plan": subscription_plan_id,
				"status": "Active"
			},
			"name"
		)
		
		if active_subscription:
			frappe.throw(_("You are already subscribed to this plan. Please wait for it to expire before purchasing again."))
		
		# Get member details for payment
		member = frappe.get_doc("Member Profile", member_profile)
		
		# STEP 1: Record payment transaction BEFORE redirect (LMS pattern)
		payment_transaction = record_payment_transaction(
			member_profile=member_profile,
			subscription_plan=subscription_plan_id,
			amount=plan.price_inr or plan.price,
			currency="INR"
		)
		
		# Get payment gateway
		payment_gateway = get_payment_gateway()
		controller = get_payment_gateway_controller(payment_gateway)
		
		# Validate currency
		controller.validate_transaction_currency("INR")
		
		# STEP 2: Prepare payment details with transaction reference
		# Redirect to frontend Vue app after payment
		# Detect environment and use appropriate frontend URL
		if frappe.local.conf.developer_mode:
			# Development: Vue dev server
			frontend_url = "http://localhost:8080"
		else:
			# Production: Use site URL with https
			protocol = "https://" if frappe.local.conf.ssl_certificate else "http://"
			frontend_url = f"{protocol}{frappe.local.site}"
		
		payment_details = {
			"amount": float(plan.price_inr or plan.price),
			"title": f"Subscription: {plan.plan_name}",
			"description": f"Purchase {plan.plan_name} subscription plan",
			"reference_doctype": "Payment Transaction",
			"reference_docname": payment_transaction.name,
			"payer_email": member.email,
			"payer_name": member.full_name,
			"order_id": payment_transaction.name,
			"currency": "INR",
			"payment_gateway": payment_gateway,
			"redirect_to": f"{frontend_url}/subscription?transaction={payment_transaction.name}",
			"payment": payment_transaction.name  # LMS pattern: link to payment record
		}
		
		# For Razorpay, create order first (LMS pattern)
		if payment_gateway == "Razorpay":
			order = controller.create_order(**payment_details)
			payment_details.update({"order_id": order.get("id")})
			
			# Update transaction with Razorpay order ID
			payment_transaction.razorpay_order_id = order.get("id")
			payment_transaction.save(ignore_permissions=True)
			frappe.db.commit()
		
		# STEP 3: Get payment URL from gateway
		# The controller returns a relative URL like ./razorpay_checkout?token=xxx
		# We need to convert it to absolute URL using site's backend URL
		payment_url = controller.get_payment_url(**payment_details)
		
		# Get site URL (backend URL, not request URL which could be frontend)
		# Detect protocol based on SSL configuration
		protocol = "https://" if frappe.local.conf.ssl_certificate else "http://"
		
		# Use frappe.local.site which will be:
		# - Development: shaadi.localhost
		# - Production: shaadi.amitkumar.live
		site_url = f"{protocol}{frappe.local.site}"
		
		# Convert relative URL to absolute
		if payment_url and not payment_url.startswith('http'):
			# Remove ./ prefix if present
			if payment_url.startswith('./'):
				payment_url = payment_url[2:]
			elif payment_url.startswith('/'):
				payment_url = payment_url[1:]
			
			payment_url = f"{site_url}/{payment_url}"
		
		frappe.logger().info(f"Payment URL generated: {payment_url} (site: {frappe.local.site}, protocol: {protocol})")
		
		return {
			"success": True,
			"payment_url": payment_url,
			"transaction_id": payment_transaction.name,
			"amount": plan.price_inr or plan.price,
			"plan_name": plan.plan_name
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Payment Initiation Error")
		return {
			"success": False,
			"error": str(e)
		}


def record_payment_transaction(member_profile, subscription_plan, amount, currency):
	"""
	Record payment transaction BEFORE redirecting to gateway
	This follows LMS pattern for better tracking
	
	Args:
		member_profile: Member Profile ID
		subscription_plan: Subscription Plan ID
		amount: Payment amount
		currency: Currency code
	
	Returns:
		Payment Transaction document
	"""
	payment_transaction = frappe.get_doc({
		"doctype": "Payment Transaction",
		"member_profile": member_profile,
		"subscription_plan": subscription_plan,
		"amount": amount,
		"currency": currency,
		"payment_gateway": get_payment_gateway(),
		"status": "Initiated"
	})
	payment_transaction.insert(ignore_permissions=True)
	frappe.db.commit()
	
	return payment_transaction


@frappe.whitelist()
def get_payment_status(transaction_id):
	"""
	Get status of a payment transaction
	
	Args:
		transaction_id: Payment Transaction ID
	
	Returns:
		dict: Transaction status and details
	"""
	try:
		transaction = frappe.get_doc("Payment Transaction", transaction_id)
		
		return {
			"success": True,
			"status": transaction.status,
			"payment_status": transaction.payment_status,
			"amount": transaction.amount,
			"subscription": transaction.subscription,
			"error_message": transaction.error_message
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Payment Status Error")
		return {
			"success": False,
			"error": str(e)
		}


@frappe.whitelist()
def verify_payment(transaction_id, razorpay_payment_id, razorpay_order_id, razorpay_signature):
	"""
	Verify payment signature and update transaction
	This is called from frontend after Razorpay checkout
	
	Args:
		transaction_id: Payment Transaction ID
		razorpay_payment_id: Razorpay payment ID
		razorpay_order_id: Razorpay order ID
		razorpay_signature: Razorpay signature for verification
	
	Returns:
		dict: Verification result
	"""
	try:
		transaction = frappe.get_doc("Payment Transaction", transaction_id)
		
		# Update Razorpay details
		transaction.razorpay_payment_id = razorpay_payment_id
		transaction.razorpay_order_id = razorpay_order_id
		transaction.razorpay_signature = razorpay_signature
		transaction.status = "Pending"
		transaction.save(ignore_permissions=True)
		frappe.db.commit()
		
		return {
			"success": True,
			"message": "Payment verification in progress"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Payment Verification Error")
		return {
			"success": False,
			"error": str(e)
		}


@frappe.whitelist()
def get_razorpay_config():
	"""
	Get Razorpay configuration for frontend
	
	Returns:
		dict: Razorpay API key and configuration
	"""
	try:
		# Get Razorpay settings
		razorpay_settings = frappe.get_doc("Razorpay Settings")
		
		return {
			"success": True,
			"api_key": razorpay_settings.api_key,
			"currency": "INR"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Razorpay Config Error")
		return {
			"success": False,
			"error": str(e)
		}
