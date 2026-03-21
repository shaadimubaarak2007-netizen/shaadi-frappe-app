<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-blue-50 dark:from-shaadi-dk-base dark:via-shaadi-dk-surface dark:to-shaadi-dk-base">
    <!-- Background Pattern -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-pink-400 to-purple-500 rounded-full opacity-10 blur-3xl"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-br from-purple-400 to-pink-500 rounded-full opacity-10 blur-3xl"></div>
    </div>

    <div class="flex items-center justify-center min-h-screen py-12 px-4 sm:px-6 lg:px-8">
      <div class="relative max-w-md w-full">
        <!-- Header -->
        <div class="text-center mb-8">
          <router-link to="/" class="inline-flex items-center justify-center mb-6">
            <div class="w-16 h-16 bg-gradient-to-r from-pink-600 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg">
              <FeatherIcon name="heart" class="w-8 h-8 text-white" />
            </div>
          </router-link>
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">Forgot Password?</h2>
          <p class="text-gray-600 dark:text-gray-400">Enter your email address and we'll send you instructions to reset your password</p>
        </div>

        <!-- Reset Form -->
        <Card class="p-8 bg-shaadi-surface border-shaadi">
          <form class="space-y-6" @submit.prevent="handleSubmit">
            <FormControl
              v-model="email"
              :label="'Email Address'"
              type="email"
              placeholder="your.email@example.com"
            />

            <!-- Error Message -->
            <ErrorMessage v-if="error" :message="error" />

            <!-- Success Message -->
            <div v-if="success" class="rounded-lg bg-green-50 border border-green-200 p-4">
              <div class="flex items-start">
                <FeatherIcon name="check-circle" class="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
                <div class="ml-3">
                  <h3 class="text-sm font-semibold text-green-800">Email Sent!</h3>
                  <p class="mt-1 text-sm text-green-700">
                    Password reset instructions have been sent to your email address. Please check your inbox and follow the link to reset your password.
                  </p>
                </div>
              </div>
            </div>

            <!-- Submit Button -->
            <div class="pt-2">
              <Button
                type="submit"
                variant="solid"
                size="lg"
                :loading="resetResource.loading"
                class="w-full !py-3"
              >
                <template #prefix>
                  <FeatherIcon name="mail" class="w-5 h-5" />
                </template>
                Send Reset Link
              </Button>
            </div>
          </form>

          <!-- Back to Login Link -->
          <div class="mt-6 pt-6 border-t border-shaadi text-center">
            <p class="text-sm text-gray-600 dark:text-gray-400">
              Remember your password?
              <router-link to="/signin" class="font-semibold text-pink-600 hover:text-pink-500 transition-colors">
                Sign in
              </router-link>
            </p>
          </div>
        </Card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { createResource, FormControl, Button, Card, ErrorMessage, FeatherIcon } from 'frappe-ui'

const email = ref('')
const error = ref(null)
const success = ref(false)

// Use Frappe's built-in password reset API
const resetResource = createResource({
  url: 'frappe.core.doctype.user.user.reset_password',
  makeParams() {
    return {
      user: email.value
    }
  }
})

async function handleSubmit() {
  error.value = null
  success.value = false
  
  // Validate email
  if (!email.value) {
    error.value = 'Please enter your email address'
    return
  }
  
  // Basic email format validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(email.value)) {
    error.value = 'Please enter a valid email address'
    return
  }
  
  try {
    await resetResource.submit({}, {
      onSuccess(data) {
        success.value = true
        // Clear email field
        email.value = ''
      },
      onError(err) {
        // Handle different error responses
        if (err === 'not found') {
          error.value = 'No account found with this email address'
        } else if (err === 'disabled') {
          error.value = 'This account has been disabled. Please contact support.'
        } else if (err === 'not allowed') {
          error.value = 'Password reset is not allowed for this account'
        } else {
          error.value = err.messages?.[0] || 'Failed to send reset link. Please try again.'
        }
      }
    })
  } catch (err) {
    console.error('Password reset error:', err)
    error.value = 'An unexpected error occurred. Please try again later.'
  }
}
</script>
