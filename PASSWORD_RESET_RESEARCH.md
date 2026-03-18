# Password Reset Implementation Research - Frappe Framework

## Research Summary from Official Frappe Apps

### **Frappe Core Implementation**

Frappe has a **built-in password reset system** that we should leverage instead of building custom.

---

## **How Frappe Password Reset Works**

### **1. Backend API (`frappe.core.doctype.user.user`)**

**Forgot Password API:**
```python
@frappe.whitelist(allow_guest=True, methods=["POST"])
@rate_limit(limit=get_password_reset_limit, seconds=60 * 60)
def reset_password(user: str) -> str:
    """
    Sends password reset email to user
    - Whitelisted for guest access
    - Rate limited (default 5 requests per hour)
    - Generates reset key and sends email
    """
    user: User = frappe.get_doc("User", user)
    if user.name == "Administrator":
        return "not allowed"
    if not user.enabled:
        return "disabled"
    
    user.validate_reset_password()
    user.reset_password(send_email=True)
    
    return frappe.msgprint(
        msg=_("Password reset instructions have been sent to your email"),
        title=_("Password Email Sent"),
    )
```

**User.reset_password() Method:**
```python
def reset_password(self, send_email=False, password_expired=False):
    """
    Generates reset key and creates reset link
    - Creates hashed reset key
    - Stores in User.reset_password_key field
    - Generates URL: /update-password?key={key}
    - Optionally sends email
    """
    from frappe.utils import get_url
    
    key = frappe.generate_hash()
    hashed_key = sha256_hash(key)
    self.db_set("reset_password_key", hashed_key)
    self.db_set("last_reset_password_key_generated_on", now_datetime())
    
    url = "/update-password?key=" + key
    if password_expired:
        url = "/update-password?key=" + key + "&password_expired=true"
    
    link = get_url(url, allow_header_override=False)
    if send_email:
        self.password_reset_mail(link)
    
    return link
```

**Update Password API:**
```python
@frappe.whitelist(allow_guest=True)
def update_password(new_password, logout_all_sessions=0, key=None, old_password=None):
    """
    Updates user password
    - Validates reset key or old password
    - Checks password strength
    - Updates password
    - Logs user in automatically
    - Returns redirect URL
    """
    # Validates key expiry (configurable in System Settings)
    # Updates password
    # Clears reset_password_key
    # Logs user in
    # Returns redirect URL (/app for System User, / for Website User)
```

---

### **2. Frontend Pages (Frappe Built-in)**

**A. Forgot Password Page:**
- **URL**: `/login#forgot` (part of login page)
- Shows email input field
- Calls `frappe.core.doctype.user.user.reset_password`
- Displays success message

**B. Update Password Page:**
- **URL**: `/update-password?key={reset_key}`
- **File**: `/apps/frappe/frappe/www/update-password.html`
- **Features**:
  - Old password field (hidden if key present)
  - New password field
  - Confirm password field
  - Real-time password strength indicator
  - Password mismatch validation
  - Calls `frappe.core.doctype.user.user.update_password`
  - Auto-redirects after success

---

### **3. Security Features**

**Rate Limiting:**
- Default: 5 password reset requests per hour per user
- Configurable in System Settings: `password_reset_limit`

**Link Expiry:**
- Configurable in System Settings: `reset_password_link_expiry_duration` (seconds)
- Default: No expiry (but can be set)

**Password Strength:**
- Real-time validation via `frappe.core.doctype.user.user.test_password_strength`
- Configurable password policy

**Key Hashing:**
- Reset keys are SHA256 hashed before storage
- Original key sent via email, hashed version stored in DB

---

## **Implementation Strategy for Shaadi App**

### **Option 1: Use Frappe's Built-in System (RECOMMENDED)**

**Advantages:**
✅ Already implemented and tested
✅ Security features built-in (rate limiting, expiry, hashing)
✅ Email templates included
✅ Password strength validation
✅ No custom code needed

**What We Need:**
1. Add "Forgot Password" link to Signin page
2. Link to Frappe's `/login#forgot` or create custom forgot password page
3. Use Frappe's `/update-password` page (already works)
4. Optionally customize email templates

**Implementation:**
```vue
<!-- In Signin.vue -->
<router-link to="/forgot-password" class="text-sm text-pink-600">
  Forgot Password?
</router-link>
```

```vue
<!-- Create ForgotPassword.vue -->
<template>
  <div>
    <FormControl
      v-model="email"
      :label="'Email Address'"
      type="email"
    />
    <Button @click="sendResetLink" :loading="resetResource.loading">
      Send Reset Link
    </Button>
  </div>
</template>

<script setup>
const resetResource = createResource({
  url: 'frappe.core.doctype.user.user.reset_password',
  makeParams(values) {
    return { user: values.email }
  }
})
</script>
```

---

### **Option 2: Custom Implementation (NOT RECOMMENDED)**

Would require:
- Custom reset key generation
- Custom email sending
- Custom password update logic
- Custom security measures
- More code to maintain

**Verdict**: Don't reinvent the wheel. Use Frappe's built-in system.

---

## **Email Templates**

Frappe uses email template: `password_reset`

**Customization:**
- Can override in System Settings: `reset_password_template`
- Default template includes reset link
- Sent via `User.password_reset_mail(link)`

---

## **How LMS/HRMS Handle This**

**Finding**: LMS and HRMS **don't implement custom password reset**. They rely on Frappe's built-in system.

**Evidence:**
- No custom password reset pages in LMS frontend
- No custom password reset APIs in HRMS
- Both use Frappe's standard `/login` and `/update-password` pages

---

## **Recommended Implementation for Shaadi**

### **Step 1: Create Forgot Password Page**
- Simple Vue component with email input
- Calls `frappe.core.doctype.user.user.reset_password`
- Shows success message

### **Step 2: Add Link to Signin Page**
- "Forgot Password?" link below login form
- Routes to `/forgot-password`

### **Step 3: Use Frappe's Update Password Page**
- No custom code needed
- Users click email link → `/update-password?key={key}`
- Frappe handles everything

### **Step 4: Optional Customization**
- Customize email template if needed
- Add branding to update-password page via custom CSS

---

## **Security Checklist**

✅ Rate limiting (built-in)
✅ Key expiry (configurable)
✅ Key hashing (SHA256)
✅ Password strength validation
✅ Email verification
✅ Auto-logout other sessions (optional)
✅ HTTPS required for production

---

## **Code Examples**

### **Forgot Password Component:**
```vue
<template>
  <Card>
    <h2>Forgot Password?</h2>
    <p>Enter your email to receive password reset instructions</p>
    
    <FormControl
      v-model="email"
      :label="'Email Address'"
      type="email"
      placeholder="your.email@example.com"
    />
    
    <ErrorMessage v-if="error" :message="error" />
    
    <div v-if="success" class="success-message">
      Password reset instructions have been sent to your email.
    </div>
    
    <Button
      @click="handleSubmit"
      :loading="resetResource.loading"
      variant="solid"
    >
      Send Reset Link
    </Button>
    
    <router-link to="/signin">Back to Login</router-link>
  </Card>
</template>

<script setup>
import { ref } from 'vue'
import { createResource, FormControl, Button, Card, ErrorMessage } from 'frappe-ui'

const email = ref('')
const error = ref(null)
const success = ref(false)

const resetResource = createResource({
  url: 'frappe.core.doctype.user.user.reset_password',
  makeParams() {
    return { user: email.value }
  }
})

async function handleSubmit() {
  error.value = null
  success.value = false
  
  if (!email.value) {
    error.value = 'Please enter your email address'
    return
  }
  
  try {
    await resetResource.submit({}, {
      onSuccess(data) {
        success.value = true
      },
      onError(err) {
        if (err === 'not found') {
          error.value = 'No account found with this email address'
        } else if (err === 'disabled') {
          error.value = 'This account has been disabled'
        } else {
          error.value = err.messages?.[0] || 'Failed to send reset link'
        }
      }
    })
  } catch (err) {
    error.value = 'An error occurred. Please try again.'
  }
}
</script>
```

### **Add to Router:**
```javascript
{
  path: '/forgot-password',
  name: 'ForgotPassword',
  component: () => import('./pages/ForgotPassword.vue')
}
```

### **Add Link to Signin.vue:**
```vue
<router-link
  to="/forgot-password"
  class="text-sm font-medium text-pink-600 hover:text-pink-500"
>
  Forgot your password?
</router-link>
```

---

## **Summary**

✅ **Use Frappe's built-in password reset system**
✅ **Create simple forgot password page in Vue**
✅ **Use Frappe's /update-password page for actual reset**
✅ **No custom backend code needed**
✅ **All security features included**

This approach is:
- **Secure** (battle-tested by Frappe)
- **Simple** (minimal custom code)
- **Standard** (same as LMS/HRMS)
- **Maintainable** (leverages framework features)
