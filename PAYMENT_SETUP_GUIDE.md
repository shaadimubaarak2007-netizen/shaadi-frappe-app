# Shaadi Payment Processing - Complete Setup & Testing Guide

## 🎯 Overview
This guide will help you enable and test the complete payment processing system for subscription purchases on the Shaadi platform.

---

## 📋 Prerequisites Checklist

- [x] Payments app installed
- [x] Payment Transaction DocType created
- [x] Subscription DocType created
- [x] Payment API implemented
- [x] Frontend PaymentModal component created
- [ ] Subscription DocType migrated to database
- [ ] Razorpay Settings configured
- [ ] Test subscription plans created

---

## 🔧 Step 1: Migrate New DocTypes to Database

The Subscription DocType needs to be installed in the database.

```bash
cd /home/erpnext/frappe-bench

# Start bench services if not running
bench start &

# In a new terminal, run migration
bench --site shaadi.localhost migrate

# Clear cache
bench --site shaadi.localhost clear-cache
```

**Expected Output:**
```
Migrating shaadi.localhost
Executing shaadi.shaadi.patches...
Updating DocTypes for shaadi: 100%
```

---

## 🔧 Step 2: Configure Razorpay Settings

### Option A: Using Razorpay Test Mode (Recommended for Development)

1. **Get Razorpay Test Credentials:**
   - Go to https://dashboard.razorpay.com/
   - Sign up or log in
   - Navigate to Settings → API Keys
   - Generate Test Keys (not Live keys)
   - Copy **Key ID** and **Key Secret**

2. **Configure in ERPNext:**
   ```bash
   # Open Razorpay Settings
   # Go to: http://shaadi.localhost:8000/app/razorpay-settings
   ```

   Or via bench console:
   ```bash
   bench --site shaadi.localhost console
   ```

   ```python
   # In console
   settings = frappe.get_single("Razorpay Settings")
   settings.api_key = "rzp_test_XXXXXXXXXXXXXXXX"  # Your test key
   settings.api_secret = "YYYYYYYYYYYYYYYYYYYY"    # Your test secret
   settings.save()
   frappe.db.commit()
   print("✓ Razorpay configured successfully!")
   ```

### Option B: Using ERPNext UI

1. Navigate to: `http://shaadi.localhost:8000/app/razorpay-settings`
2. Enter your Razorpay Test credentials
3. Save

---

## 🔧 Step 3: Create Test Subscription Plans

Run this via bench console to create sample plans:

```bash
bench --site shaadi.localhost console
```

```python
import frappe

# Create Free Plan
free_plan = frappe.get_doc({
    "doctype": "Subscription Plan",
    "plan_name": "Free",
    "plan_type": "Free",
    "price": 0,
    "price_inr": 0,
    "duration_days": 365,
    "contacts_allowed": 0,
    "messages_allowed": 0,
    "can_send_message": 0,
    "can_view_contact": 0,
    "can_see_all_photos": 0,
    "featured_profile": 0
})
free_plan.insert(ignore_if_duplicate=True)

# Create Silver Plan
silver_plan = frappe.get_doc({
    "doctype": "Subscription Plan",
    "plan_name": "Silver",
    "plan_type": "Silver",
    "price": 600,
    "price_inr": 600,
    "duration_days": 30,
    "contacts_allowed": 25,
    "messages_allowed": 50,
    "can_send_message": 1,
    "can_view_contact": 1,
    "can_see_all_photos": 0,
    "featured_profile": 0
})
silver_plan.insert(ignore_if_duplicate=True)

# Create Gold Plan
gold_plan = frappe.get_doc({
    "doctype": "Subscription Plan",
    "plan_name": "Gold",
    "plan_type": "Gold",
    "price": 2499,
    "price_inr": 2499,
    "duration_days": 90,
    "contacts_allowed": 50,
    "messages_allowed": 100,
    "can_send_message": 1,
    "can_view_contact": 1,
    "can_see_all_photos": 1,
    "featured_profile": 1
})
gold_plan.insert(ignore_if_duplicate=True)

frappe.db.commit()
print("✓ Subscription plans created successfully!")
```

---

## 🧪 Step 4: Test Payment Flow

### A. Frontend Testing

1. **Access Subscription Page:**
   ```
   http://localhost:8080/subscription
   ```

2. **Test Flow:**
   - Click on "Choose Gold" or "Choose Silver"
   - Upgrade modal should appear
   - Click "Proceed to Payment"
   - PaymentModal should open
   - Click "Pay ₹2499" (or ₹600 for Silver)
   - You'll be redirected to Razorpay checkout

3. **Test Payment on Razorpay:**
   - Use Razorpay test card: `4111 1111 1111 1111`
   - CVV: Any 3 digits (e.g., `123`)
   - Expiry: Any future date (e.g., `12/25`)
   - Click "Pay"

4. **Verify Success:**
   - You'll be redirected back to `/subscription?payment=success`
   - Success toast should appear
   - Subscription should be activated

### B. Backend Testing via Bench Console

```bash
bench --site shaadi.localhost console
```

```python
import frappe
from shaadi.shaadi.api import payment

# Test 1: Check if payment API is accessible
print("Testing payment API...")
try:
    gateway = payment.get_payment_gateway()
    print(f"✓ Payment gateway: {gateway}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 2: Check Razorpay configuration
print("\nTesting Razorpay configuration...")
try:
    from payments.utils import get_payment_gateway_controller
    controller = get_payment_gateway_controller("Razorpay")
    controller().validate_transaction_currency("INR")
    print("✓ Razorpay is properly configured")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: Check DocTypes
print("\nChecking DocTypes...")
doctypes = ["Payment Transaction", "Subscription", "Subscription Plan"]
for dt in doctypes:
    if frappe.db.exists("DocType", dt):
        count = frappe.db.count(dt)
        print(f"✓ {dt}: {count} records")
    else:
        print(f"✗ {dt}: NOT FOUND")

# Test 4: Simulate payment initiation (requires logged-in user)
print("\nTo test payment initiation, you need to:")
print("1. Be logged in as a member")
print("2. Have a Member Profile created")
print("3. Call: frappe.call('shaadi.shaadi.api.payment.initiate_payment', subscription_plan_id='PLAN-ID')")
```

---

## 🔍 Step 5: Verify Backend Integration

### Check Payment Transaction Creation

```python
# In bench console
import frappe

# Get latest payment transactions
transactions = frappe.get_all(
    "Payment Transaction",
    fields=["name", "member_profile", "amount", "status", "razorpay_order_id"],
    order_by="creation desc",
    limit=5
)

for txn in transactions:
    print(f"Transaction: {txn.name}")
    print(f"  Member: {txn.member_profile}")
    print(f"  Amount: ₹{txn.amount}")
    print(f"  Status: {txn.status}")
    print(f"  Razorpay Order: {txn.razorpay_order_id}")
    print()
```

### Check Subscription Creation

```python
# In bench console
import frappe

# Get active subscriptions
subscriptions = frappe.get_all(
    "Subscription",
    fields=["name", "member_profile", "subscription_plan", "start_date", "end_date", "status"],
    filters={"status": "Active"},
    order_by="creation desc",
    limit=5
)

for sub in subscriptions:
    print(f"Subscription: {sub.name}")
    print(f"  Member: {sub.member_profile}")
    print(f"  Plan: {sub.subscription_plan}")
    print(f"  Period: {sub.start_date} to {sub.end_date}")
    print(f"  Status: {sub.status}")
    print()
```

---

## 🐛 Troubleshooting

### Issue: "DocType Subscription not found"

**Solution:**
```bash
bench --site shaadi.localhost migrate
bench --site shaadi.localhost clear-cache
```

### Issue: "Razorpay Settings not configured"

**Solution:**
1. Check if payments app is installed: `bench --site shaadi.localhost list-apps`
2. Configure Razorpay Settings as shown in Step 2

### Issue: "Payment modal doesn't open"

**Solution:**
1. Check browser console for errors
2. Ensure PaymentModal.vue is properly imported
3. Rebuild frontend: `cd apps/shaadi/shaadi_ui && npm run build`

### Issue: "Payment callback not working"

**Solution:**
1. Check Integration Request records: `frappe.get_all("Integration Request", limit=5)`
2. Verify `on_payment_authorized` method exists in Payment Transaction
3. Check error logs: `frappe.get_all("Error Log", limit=5)`

---

## 📊 Monitoring Payment Flow

### Check Integration Requests

```python
# In bench console
import frappe

requests = frappe.get_all(
    "Integration Request",
    fields=["name", "reference_doctype", "reference_docname", "status", "data"],
    filters={"reference_doctype": "Payment Transaction"},
    order_by="creation desc",
    limit=3
)

for req in requests:
    print(f"Integration Request: {req.name}")
    print(f"  Reference: {req.reference_docname}")
    print(f"  Status: {req.status}")
    print()
```

### Check Error Logs

```python
# In bench console
import frappe

errors = frappe.get_all(
    "Error Log",
    fields=["name", "error", "creation"],
    filters={"method": ["like", "%payment%"]},
    order_by="creation desc",
    limit=5
)

for error in errors:
    print(f"Error: {error.name}")
    print(f"  Time: {error.creation}")
    print(f"  Message: {error.error[:200]}...")
    print()
```

---

## ✅ Success Criteria

Your payment system is working correctly if:

1. ✓ Razorpay Settings configured with test credentials
2. ✓ Subscription plans visible on frontend
3. ✓ "Proceed to Payment" button opens PaymentModal
4. ✓ Payment Transaction created BEFORE redirect
5. ✓ Razorpay checkout page loads successfully
6. ✓ Test payment completes successfully
7. ✓ User redirected back with success message
8. ✓ Subscription record created with Active status
9. ✓ Payment Transaction updated with payment IDs
10. ✓ Integration Request created and linked

---

## 🚀 Going to Production

When ready for production:

1. **Switch to Live Razorpay Keys:**
   - Get Live API keys from Razorpay dashboard
   - Update Razorpay Settings with live credentials

2. **Update Pricing:**
   - Set actual subscription prices
   - Update plan features as needed

3. **Enable Webhooks:**
   - Configure Razorpay webhook URL
   - Add webhook secret to Razorpay Settings

4. **Test Thoroughly:**
   - Test with real small amounts first
   - Verify refund process
   - Test subscription expiry logic

---

## 📞 Support

If you encounter issues:

1. Check error logs in ERPNext
2. Check browser console for frontend errors
3. Verify all DocTypes are migrated
4. Ensure Razorpay credentials are correct
5. Test with Razorpay test cards first

---

**Last Updated:** March 18, 2024
**Version:** 1.0
