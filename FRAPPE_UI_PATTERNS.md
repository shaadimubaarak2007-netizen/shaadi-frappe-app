# Frappe UI Best Practices - Based on LMS App Research

## Key Findings from LMS App Analysis

### 1. **TypeScript is NOT Required**
- LMS uses plain JavaScript with Vue 3 `<script setup>`
- Your current setup is correct - no TypeScript needed
- The issue is NOT about TypeScript, it's about using Frappe UI components correctly

### 2. **Critical Pattern: Use `createResource` Instead of `call()`**

**❌ Current Pattern (Not Ideal):**
```javascript
import { call } from 'frappe-ui'

async function handleSubmit() {
  loading.value = true
  try {
    await call('frappe.client.insert', { doc: {...} })
    success.value = true
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
```

**✅ LMS Pattern (Recommended):**
```javascript
import { createResource } from 'frappe-ui'

const signupResource = createResource({
  url: 'frappe.core.doctype.user.user.sign_up',
  makeParams(values) {
    return {
      email: values.email,
      full_name: values.full_name,
      redirect_to: '/signin'
    }
  },
  onSuccess(data) {
    success.value = true
    setTimeout(() => router.push('/signin'), 2000)
  },
  onError(err) {
    error.value = err.messages?.[0] || err
  }
})

// Then call:
function handleSubmit() {
  signupResource.submit(formData.value)
}
```

**Benefits of createResource:**
- Automatic loading state management
- Built-in error handling
- Reactive data binding
- Better integration with Frappe UI components
- Cleaner code structure

### 3. **FormControl Component Usage**

**❌ Current Pattern:**
```vue
<label class="block text-sm font-medium text-gray-700 mb-1.5">Full Name *</label>
<TextInput
  v-model="formData.full_name"
  type="text"
  placeholder="Enter your full name"
  required
/>
```

**✅ LMS Pattern:**
```vue
<FormControl
  v-model="formData.full_name"
  :label="'Full Name'"
  type="text"
  placeholder="Enter your full name"
  class="mb-4"
/>
```

**Key Points:**
- FormControl handles label, input, and validation together
- Use `:label` prop instead of separate `<label>` tags
- FormControl automatically applies Frappe UI styling
- No need for separate TextInput component for simple text fields

### 4. **Select Fields with FormControl**

**✅ Correct Pattern:**
```vue
<FormControl
  type="select"
  v-model="formData.gender"
  :options="genderOptions"
  :label="'Gender'"
  placeholder="Select gender"
  :disabled="loadingOptions"
  class="mb-4"
/>
```

### 5. **Fetching Options with createResource**

**❌ Current Pattern:**
```javascript
onMounted(async () => {
  try {
    const options = await call('shaadi.shaadi.api.form_options.get_member_profile_options')
    genderOptions.value = options.gender || []
    // ...
  } catch (err) {
    error.value = 'Failed to load form options'
  }
})
```

**✅ LMS Pattern:**
```javascript
const optionsResource = createResource({
  url: 'shaadi.shaadi.api.form_options.get_member_profile_options',
  auto: true, // Automatically fetch on mount
  onSuccess(data) {
    genderOptions.value = data.gender || []
    religionOptions.value = data.religion || []
    maritalStatusOptions.value = data.marital_status || []
    educationOptions.value = data.education || []
    occupationOptions.value = data.occupation || []
    stateOptions.value = data.state || []
  },
  onError(err) {
    error.value = 'Failed to load form options. Please refresh the page.'
  }
})

// Access loading state: optionsResource.loading
```

### 6. **Complete Signup.vue Refactored Example**

```vue
<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-blue-50">
    <div class="flex items-center justify-center min-h-screen py-12 px-4">
      <div class="relative max-w-3xl w-full">
        <Card class="p-8">
          <form class="space-y-6" @submit.prevent="handleSubmit">
            <!-- Personal Information -->
            <div class="space-y-4">
              <h3 class="text-lg font-semibold">Personal Information</h3>
              
              <FormControl
                v-model="formData.full_name"
                :label="'Full Name'"
                type="text"
                placeholder="Enter your full name"
                class="mb-4"
              />
              
              <FormControl
                type="select"
                v-model="formData.gender"
                :options="genderOptions"
                :label="'Gender'"
                placeholder="Select gender"
                :disabled="optionsResource.loading"
                class="mb-4"
              />
              
              <FormControl
                v-model="formData.dob"
                :label="'Date of Birth'"
                type="date"
                class="mb-4"
              />
              
              <FormControl
                v-model="formData.phone"
                :label="'Phone Number'"
                type="tel"
                placeholder="+91 9876543210"
                class="mb-4"
              />
            </div>

            <!-- Account Information -->
            <div class="space-y-4">
              <h3 class="text-lg font-semibold">Account Information</h3>
              
              <FormControl
                v-model="formData.email"
                :label="'Email Address'"
                type="email"
                placeholder="your.email@example.com"
                class="mb-4"
              />
              
              <FormControl
                v-model="formData.password"
                :label="'Password'"
                type="password"
                placeholder="Create a strong password"
                class="mb-4"
              />
            </div>

            <!-- Error/Success Messages -->
            <ErrorMessage v-if="error" :message="error" />
            
            <div v-if="success" class="rounded-lg bg-green-50 border border-green-200 p-4">
              <p class="text-sm text-green-700">Registration successful! Redirecting...</p>
            </div>

            <!-- Submit Button -->
            <Button
              type="submit"
              variant="solid"
              :loading="signupResource.loading"
              class="w-full"
            >
              Create Account
            </Button>
          </form>
        </Card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { createResource, FormControl, Button, Card, ErrorMessage } from 'frappe-ui'

const router = useRouter()

const formData = ref({
  full_name: '',
  gender: '',
  dob: '',
  phone: '',
  email: '',
  password: '',
  city: '',
  state: '',
  religion: '',
  marital_status: '',
  education: '',
  occupation: ''
})

const error = ref(null)
const success = ref(false)

// Dynamic options from Frappe
const genderOptions = ref([])
const religionOptions = ref([])
const maritalStatusOptions = ref([])
const educationOptions = ref([])
const occupationOptions = ref([])
const stateOptions = ref([])

// Fetch field options using createResource
const optionsResource = createResource({
  url: 'shaadi.shaadi.api.form_options.get_member_profile_options',
  auto: true,
  onSuccess(data) {
    genderOptions.value = data.gender || []
    religionOptions.value = data.religion || []
    maritalStatusOptions.value = data.marital_status || []
    educationOptions.value = data.education || []
    occupationOptions.value = data.occupation || []
    stateOptions.value = data.state || []
  },
  onError(err) {
    error.value = 'Failed to load form options. Please refresh the page.'
  }
})

// User signup using createResource
const signupResource = createResource({
  url: 'frappe.core.doctype.user.user.sign_up',
  makeParams(values) {
    return {
      email: values.email,
      full_name: values.full_name,
      redirect_to: '/signin'
    }
  }
})

// Member profile creation using createResource
const profileResource = createResource({
  url: 'frappe.client.insert',
  makeParams(values) {
    return {
      doc: {
        doctype: 'Member Profile',
        full_name: values.full_name,
        gender: values.gender,
        dob: values.dob,
        phone: values.phone,
        email: values.email,
        city: values.city,
        state: values.state,
        religion: values.religion,
        marital_status: values.marital_status,
        education: values.education,
        occupation: values.occupation,
        is_active: 1
      }
    }
  }
})

async function handleSubmit() {
  error.value = null
  
  try {
    // Create user account
    await signupResource.submit(formData.value, {
      onError(err) {
        throw new Error(err.messages?.[0] || err)
      }
    })
    
    // Create member profile
    await profileResource.submit(formData.value, {
      onError(err) {
        throw new Error(err.messages?.[0] || err)
      }
    })
    
    success.value = true
    setTimeout(() => router.push('/signin'), 2000)
    
  } catch (err) {
    error.value = err.message || 'Failed to create account. Please try again.'
  }
}
</script>
```

## Summary of Changes Needed

1. **Replace `call()` with `createResource()`** for all API calls
2. **Use FormControl's `:label` prop** instead of separate label tags
3. **Remove TextInput** - use FormControl for all input types
4. **Use `auto: true`** in createResource for automatic data fetching on mount
5. **Access loading states** from resource objects (e.g., `signupResource.loading`)
6. **Simplify error handling** using createResource's built-in callbacks

## Why This Matters

- **Better UX**: Automatic loading states and error handling
- **Cleaner Code**: Less boilerplate, more declarative
- **Frappe UI Integration**: Components work together seamlessly
- **Maintainability**: Follows established patterns from official Frappe apps
- **Reactivity**: Better Vue 3 reactivity integration

## References

- LMS App: `/apps/lms/frontend/src/components/Modals/EditProfile.vue`
- Frappe UI Docs: Uses createResource pattern throughout
- HRMS App: Similar patterns for form handling
