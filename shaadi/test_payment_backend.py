#!/usr/bin/env python3
"""
Test script to verify Shaadi payment backend compatibility
Run with: bench --site shaadi.localhost execute shaadi.test_payment_backend.test_payment_integration
"""

import frappe
import json


def test_payment_integration():
    """Test all payment integration components"""
    
    print("\n" + "="*80)
    print("SHAADI PAYMENT BACKEND COMPATIBILITY TEST")
    print("="*80 + "\n")
    
    results = {
        "passed": [],
        "failed": [],
        "warnings": []
    }
    
    # Test 1: Check Payment Transaction DocType
    print("1. Checking Payment Transaction DocType...")
    try:
        if frappe.db.exists("DocType", "Payment Transaction"):
            doc = frappe.get_meta("Payment Transaction")
            print("   ✓ Payment Transaction DocType exists")
            
            # Check required fields
            required_fields = [
                "member_profile", "subscription_plan", "amount", "currency",
                "payment_gateway", "status", "razorpay_order_id", 
                "razorpay_payment_id", "integration_request"
            ]
            
            existing_fields = [f.fieldname for f in doc.fields]
            missing_fields = [f for f in required_fields if f not in existing_fields]
            
            if missing_fields:
                results["warnings"].append(f"Missing fields in Payment Transaction: {missing_fields}")
                print(f"   ⚠ Missing fields: {missing_fields}")
            else:
                results["passed"].append("Payment Transaction DocType has all required fields")
                print("   ✓ All required fields present")
        else:
            results["failed"].append("Payment Transaction DocType not found")
            print("   ✗ Payment Transaction DocType NOT FOUND")
    except Exception as e:
        results["failed"].append(f"Payment Transaction check failed: {str(e)}")
        print(f"   ✗ Error: {str(e)}")
    
    # Test 2: Check payments app installation
    print("\n2. Checking payments app installation...")
    try:
        installed_apps = frappe.get_installed_apps()
        if "payments" in installed_apps:
            results["passed"].append("Payments app is installed")
            print("   ✓ Payments app is installed")
            
            # Check Razorpay Settings
            if frappe.db.exists("DocType", "Razorpay Settings"):
                print("   ✓ Razorpay Settings DocType exists")
                
                # Check if Razorpay is configured
                try:
                    settings = frappe.get_doc("Razorpay Settings")
                    if settings.api_key:
                        results["passed"].append("Razorpay is configured")
                        print("   ✓ Razorpay API key is configured")
                    else:
                        results["warnings"].append("Razorpay API key not configured")
                        print("   ⚠ Razorpay API key NOT configured (required for payments)")
                except Exception as e:
                    results["warnings"].append(f"Could not check Razorpay settings: {str(e)}")
                    print(f"   ⚠ Could not check Razorpay settings: {str(e)}")
            else:
                results["failed"].append("Razorpay Settings DocType not found")
                print("   ✗ Razorpay Settings DocType NOT FOUND")
        else:
            results["failed"].append("Payments app is NOT installed")
            print("   ✗ Payments app is NOT installed")
    except Exception as e:
        results["failed"].append(f"Payments app check failed: {str(e)}")
        print(f"   ✗ Error: {str(e)}")
    
    # Test 3: Check payment API endpoints
    print("\n3. Checking payment API endpoints...")
    try:
        # Check if payment.py exists and has required functions
        from shaadi.shaadi.api import payment
        
        required_functions = ["initiate_payment", "get_payment_status", "get_razorpay_config"]
        existing_functions = [f for f in dir(payment) if not f.startswith("_")]
        
        missing_functions = [f for f in required_functions if f not in existing_functions]
        
        if missing_functions:
            results["failed"].append(f"Missing API functions: {missing_functions}")
            print(f"   ✗ Missing functions: {missing_functions}")
        else:
            results["passed"].append("All payment API endpoints exist")
            print("   ✓ All required API functions exist")
            
            # Check if functions are whitelisted
            for func_name in required_functions:
                func = getattr(payment, func_name)
                if hasattr(func, "_is_whitelisted"):
                    print(f"   ✓ {func_name} is whitelisted")
                else:
                    results["warnings"].append(f"{func_name} may not be whitelisted")
                    print(f"   ⚠ {func_name} may not be whitelisted")
    except ImportError as e:
        results["failed"].append(f"Payment API module not found: {str(e)}")
        print(f"   ✗ Payment API module not found: {str(e)}")
    except Exception as e:
        results["failed"].append(f"Payment API check failed: {str(e)}")
        print(f"   ✗ Error: {str(e)}")
    
    # Test 4: Check Payment Transaction controller
    print("\n4. Checking Payment Transaction controller...")
    try:
        from shaadi.shaadi.doctype.payment_transaction import payment_transaction
        
        # Check if on_payment_authorized method exists
        if hasattr(payment_transaction.PaymentTransaction, "on_payment_authorized"):
            results["passed"].append("on_payment_authorized callback exists")
            print("   ✓ on_payment_authorized callback exists")
        else:
            results["failed"].append("on_payment_authorized callback NOT found")
            print("   ✗ on_payment_authorized callback NOT found")
        
        # Check if update_payment_record function exists
        if hasattr(payment_transaction, "update_payment_record"):
            results["passed"].append("update_payment_record function exists")
            print("   ✓ update_payment_record function exists")
        else:
            results["failed"].append("update_payment_record function NOT found")
            print("   ✗ update_payment_record function NOT found")
    except ImportError as e:
        results["failed"].append(f"Payment Transaction controller not found: {str(e)}")
        print(f"   ✗ Payment Transaction controller not found: {str(e)}")
    except Exception as e:
        results["failed"].append(f"Payment Transaction controller check failed: {str(e)}")
        print(f"   ✗ Error: {str(e)}")
    
    # Test 5: Check Subscription Plan DocType
    print("\n5. Checking Subscription Plan DocType...")
    try:
        if frappe.db.exists("DocType", "Subscription Plan"):
            print("   ✓ Subscription Plan DocType exists")
            
            # Check if any plans exist
            plan_count = frappe.db.count("Subscription Plan")
            if plan_count > 0:
                results["passed"].append(f"Found {plan_count} subscription plans")
                print(f"   ✓ Found {plan_count} subscription plan(s)")
                
                # Get a sample plan
                sample_plan = frappe.get_all("Subscription Plan", 
                                            fields=["name", "plan_name", "price"],
                                            limit=1)
                if sample_plan:
                    print(f"   ℹ Sample plan: {sample_plan[0].plan_name} - ₹{sample_plan[0].price}")
            else:
                results["warnings"].append("No subscription plans found")
                print("   ⚠ No subscription plans found (create plans to test payments)")
        else:
            results["failed"].append("Subscription Plan DocType not found")
            print("   ✗ Subscription Plan DocType NOT FOUND")
    except Exception as e:
        results["failed"].append(f"Subscription Plan check failed: {str(e)}")
        print(f"   ✗ Error: {str(e)}")
    
    # Test 6: Check Integration Request DocType (from payments app)
    print("\n6. Checking Integration Request DocType...")
    try:
        if frappe.db.exists("DocType", "Integration Request"):
            results["passed"].append("Integration Request DocType exists")
            print("   ✓ Integration Request DocType exists (from payments app)")
        else:
            results["failed"].append("Integration Request DocType not found")
            print("   ✗ Integration Request DocType NOT FOUND")
    except Exception as e:
        results["failed"].append(f"Integration Request check failed: {str(e)}")
        print(f"   ✗ Error: {str(e)}")
    
    # Print Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"\n✓ Passed: {len(results['passed'])}")
    for item in results['passed']:
        print(f"  • {item}")
    
    if results['warnings']:
        print(f"\n⚠ Warnings: {len(results['warnings'])}")
        for item in results['warnings']:
            print(f"  • {item}")
    
    if results['failed']:
        print(f"\n✗ Failed: {len(results['failed'])}")
        for item in results['failed']:
            print(f"  • {item}")
    
    # Overall status
    print("\n" + "="*80)
    if not results['failed']:
        if not results['warnings']:
            print("✓ ALL TESTS PASSED - Backend is fully compatible!")
        else:
            print("⚠ TESTS PASSED WITH WARNINGS - Backend is compatible but needs configuration")
    else:
        print("✗ SOME TESTS FAILED - Backend needs fixes")
    print("="*80 + "\n")
    
    return results


if __name__ == "__main__":
    test_payment_integration()
