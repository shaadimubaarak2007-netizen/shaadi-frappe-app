"""
Backend compatibility test for Shaadi payment integration
Can be run via bench console
"""

import frappe
import json


def run_backend_tests():
    """Run comprehensive backend compatibility tests"""
    
    print("\n" + "="*80)
    print("SHAADI PAYMENT BACKEND COMPATIBILITY TEST")
    print("="*80 + "\n")
    
    tests_passed = 0
    tests_failed = 0
    warnings = 0
    
    # Test 1: DocTypes existence
    print("1. Checking Required DocTypes...")
    required_doctypes = {
        "Payment Transaction": "Tracks payment transactions",
        "Subscription": "Tracks user subscription instances",
        "Subscription Plan": "Defines subscription pricing tiers",
        "Member Profile": "User profiles",
        "Integration Request": "Payment gateway integration (from payments app)"
    }
    
    for doctype, description in required_doctypes.items():
        if frappe.db.exists("DocType", doctype):
            print(f"   ✓ {doctype} - {description}")
            tests_passed += 1
        else:
            print(f"   ✗ {doctype} NOT FOUND - {description}")
            tests_failed += 1
    
    # Test 2: Payment Transaction fields
    print("\n2. Checking Payment Transaction Fields...")
    try:
        meta = frappe.get_meta("Payment Transaction")
        required_fields = [
            "member_profile", "subscription_plan", "amount", "currency",
            "payment_gateway", "status", "razorpay_order_id",
            "razorpay_payment_id", "integration_request", "subscription"
        ]
        
        existing_fields = [f.fieldname for f in meta.fields]
        
        for field in required_fields:
            if field in existing_fields:
                print(f"   ✓ {field}")
                tests_passed += 1
            else:
                print(f"   ✗ {field} MISSING")
                tests_failed += 1
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
        tests_failed += 1
    
    # Test 3: Subscription fields
    print("\n3. Checking Subscription Fields...")
    try:
        meta = frappe.get_meta("Subscription")
        required_fields = [
            "member_profile", "subscription_plan", "start_date",
            "end_date", "status", "payment_transaction"
        ]
        
        existing_fields = [f.fieldname for f in meta.fields]
        
        for field in required_fields:
            if field in existing_fields:
                print(f"   ✓ {field}")
                tests_passed += 1
            else:
                print(f"   ✗ {field} MISSING")
                tests_failed += 1
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
        tests_failed += 1
    
    # Test 4: Payments app
    print("\n4. Checking Payments App...")
    try:
        apps = frappe.get_installed_apps()
        if "payments" in apps:
            print("   ✓ Payments app installed")
            tests_passed += 1
            
            # Check Razorpay Settings
            if frappe.db.exists("DocType", "Razorpay Settings"):
                print("   ✓ Razorpay Settings DocType exists")
                tests_passed += 1
                
                try:
                    settings = frappe.get_single("Razorpay Settings")
                    if settings.api_key:
                        print(f"   ✓ Razorpay configured (Key: {settings.api_key[:10]}...)")
                        tests_passed += 1
                    else:
                        print("   ⚠ Razorpay API key NOT configured")
                        warnings += 1
                except Exception as e:
                    print(f"   ⚠ Could not check Razorpay config: {e}")
                    warnings += 1
            else:
                print("   ✗ Razorpay Settings NOT FOUND")
                tests_failed += 1
        else:
            print("   ✗ Payments app NOT installed")
            tests_failed += 1
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
        tests_failed += 1
    
    # Test 5: Payment API
    print("\n5. Checking Payment API...")
    try:
        from shaadi.shaadi.api import payment
        
        functions = [
            "initiate_payment",
            "get_payment_status",
            "get_razorpay_config",
            "get_payment_gateway",
            "record_payment_transaction"
        ]
        
        for func in functions:
            if hasattr(payment, func):
                print(f"   ✓ {func}()")
                tests_passed += 1
            else:
                print(f"   ✗ {func}() MISSING")
                tests_failed += 1
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
        tests_failed += 1
    
    # Test 6: Payment Transaction controller
    print("\n6. Checking Payment Transaction Controller...")
    try:
        from shaadi.shaadi.doctype.payment_transaction import payment_transaction
        
        # Check class methods
        if hasattr(payment_transaction.PaymentTransaction, "on_payment_authorized"):
            print("   ✓ on_payment_authorized() callback")
            tests_passed += 1
        else:
            print("   ✗ on_payment_authorized() MISSING")
            tests_failed += 1
        
        if hasattr(payment_transaction.PaymentTransaction, "create_subscription"):
            print("   ✓ create_subscription() method")
            tests_passed += 1
        else:
            print("   ✗ create_subscription() MISSING")
            tests_failed += 1
        
        # Check module-level function
        if hasattr(payment_transaction, "update_payment_record"):
            print("   ✓ update_payment_record() function")
            tests_passed += 1
        else:
            print("   ✗ update_payment_record() MISSING")
            tests_failed += 1
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
        tests_failed += 1
    
    # Test 7: Subscription controller
    print("\n7. Checking Subscription Controller...")
    try:
        from shaadi.shaadi.doctype.subscription import subscription
        
        if hasattr(subscription.Subscription, "validate"):
            print("   ✓ validate() method")
            tests_passed += 1
        else:
            print("   ⚠ validate() method not found")
            warnings += 1
        
        if hasattr(subscription.Subscription, "update_status"):
            print("   ✓ update_status() method")
            tests_passed += 1
        else:
            print("   ⚠ update_status() method not found")
            warnings += 1
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
        tests_failed += 1
    
    # Test 8: Payment gateway controller
    print("\n8. Testing Payment Gateway Controller...")
    try:
        from payments.utils import get_payment_gateway_controller
        
        controller = get_payment_gateway_controller("Razorpay")
        print("   ✓ Can get Razorpay controller")
        tests_passed += 1
        
        # Test currency validation
        try:
            controller().validate_transaction_currency("INR")
            print("   ✓ Currency validation works (INR)")
            tests_passed += 1
        except Exception as e:
            print(f"   ⚠ Currency validation issue: {e}")
            warnings += 1
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
        tests_failed += 1
    
    # Test 9: Sample data check
    print("\n9. Checking Sample Data...")
    try:
        plan_count = frappe.db.count("Subscription Plan")
        if plan_count > 0:
            print(f"   ✓ Found {plan_count} subscription plan(s)")
            tests_passed += 1
            
            # Show sample plans
            plans = frappe.get_all(
                "Subscription Plan",
                fields=["name", "plan_name", "price", "duration_days"],
                limit=3
            )
            for plan in plans:
                print(f"      • {plan.plan_name}: ₹{plan.price} for {plan.duration_days} days")
        else:
            print("   ⚠ No subscription plans found (create plans to test)")
            warnings += 1
        
        member_count = frappe.db.count("Member Profile")
        print(f"   ℹ Found {member_count} member profile(s)")
        
        subscription_count = frappe.db.count("Subscription")
        print(f"   ℹ Found {subscription_count} active subscription(s)")
        
        transaction_count = frappe.db.count("Payment Transaction")
        print(f"   ℹ Found {transaction_count} payment transaction(s)")
        
    except Exception as e:
        print(f"   ⚠ Could not check sample data: {e}")
        warnings += 1
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"✓ Passed:   {tests_passed}")
    print(f"✗ Failed:   {tests_failed}")
    print(f"⚠ Warnings: {warnings}")
    
    if tests_failed == 0:
        if warnings == 0:
            print("\n✓ ALL TESTS PASSED - Backend is fully compatible!")
        else:
            print("\n⚠ TESTS PASSED WITH WARNINGS - Backend is compatible but needs configuration")
    else:
        print("\n✗ SOME TESTS FAILED - Backend needs fixes")
    
    print("="*80 + "\n")
    
    return {
        "passed": tests_passed,
        "failed": tests_failed,
        "warnings": warnings
    }
