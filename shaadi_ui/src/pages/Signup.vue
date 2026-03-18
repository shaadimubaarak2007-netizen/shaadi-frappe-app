<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-blue-50">
    <!-- Background Pattern -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-pink-400 to-purple-500 rounded-full opacity-10 blur-3xl"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-br from-purple-400 to-pink-500 rounded-full opacity-10 blur-3xl"></div>
    </div>

    <div class="flex items-center justify-center min-h-screen py-12 px-4 sm:px-6 lg:px-8">
      <div class="relative max-w-3xl w-full">
        <!-- Header -->
        <div class="text-center mb-8">
          <router-link to="/" class="inline-flex items-center justify-center mb-6">
            <div class="w-16 h-16 bg-gradient-to-r from-pink-600 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg">
              <FeatherIcon name="heart" class="w-8 h-8 text-white" />
            </div>
          </router-link>
          <h2 class="text-3xl font-bold text-gray-900 mb-2">Create Your Profile</h2>
          <p class="text-gray-600">Join thousands of members finding their perfect match</p>
        </div>

        <!-- Registration Form -->
        <Card class="p-8">
          <form class="space-y-8" @submit.prevent="handleSubmit">
            <!-- Personal Information -->
            <div class="space-y-4">
              <div class="flex items-center space-x-2 mb-4">
                <div class="w-8 h-8 bg-pink-100 rounded-lg flex items-center justify-center">
                  <FeatherIcon name="user" class="w-4 h-4 text-pink-600" />
                </div>
                <h3 class="text-lg font-semibold text-gray-900">Personal Information</h3>
              </div>
              <div class="grid md:grid-cols-2 gap-4">
                <FormControl
                  v-model="formData.full_name"
                  :label="'Full Name'"
                  type="text"
                  placeholder="Enter your full name"
                />
                <FormControl
                  type="select"
                  v-model="formData.gender"
                  :options="genderOptions"
                  :label="'Gender'"
                  placeholder="Select gender"
                  :disabled="optionsResource.loading"
                />
                <FormControl
                  v-model="formData.dob"
                  :label="'Date of Birth'"
                  type="date"
                />
                <FormControl
                  v-model="formData.phone"
                  :label="'Phone Number'"
                  type="tel"
                  placeholder="+91 9876543210"
                />
              </div>
            </div>

            <!-- Account Information -->
            <div class="space-y-4">
              <div class="flex items-center space-x-2 mb-4">
                <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                  <FeatherIcon name="mail" class="w-4 h-4 text-purple-600" />
                </div>
                <h3 class="text-lg font-semibold text-gray-900">Account Information</h3>
              </div>
              <FormControl
                v-model="formData.email"
                :label="'Email Address'"
                type="email"
                placeholder="your.email@example.com"
              />
              <div class="text-sm text-gray-600 bg-blue-50 border border-blue-200 rounded-lg p-3">
                <div class="flex items-start">
                  <FeatherIcon name="info" class="w-4 h-4 text-blue-600 mt-0.5 mr-2 flex-shrink-0" />
                  <p>After registration, you'll receive a password reset link via email to set your password.</p>
                </div>
              </div>
            </div>

            <!-- Location -->
            <div class="space-y-4">
              <div class="flex items-center space-x-2 mb-4">
                <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                  <FeatherIcon name="map-pin" class="w-4 h-4 text-blue-600" />
                </div>
                <h3 class="text-lg font-semibold text-gray-900">Location</h3>
              </div>
              <div class="grid md:grid-cols-2 gap-4">
                <FormControl
                  v-model="formData.city"
                  :label="'City'"
                  type="text"
                  placeholder="Enter your city"
                />
                <FormControl
                  type="select"
                  v-model="formData.state"
                  :options="stateOptions"
                  :label="'State'"
                  placeholder="Select state"
                  :disabled="optionsResource.loading"
                />
              </div>
            </div>

            <!-- Basic Details -->
            <div class="space-y-4">
              <div class="flex items-center space-x-2 mb-4">
                <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                  <FeatherIcon name="info" class="w-4 h-4 text-green-600" />
                </div>
                <h3 class="text-lg font-semibold text-gray-900">Basic Details</h3>
              </div>
              <div class="grid md:grid-cols-2 gap-4">
                <FormControl
                  type="select"
                  v-model="formData.religion"
                  :options="religionOptions"
                  :label="'Religion'"
                  placeholder="Select religion"
                  :disabled="optionsResource.loading"
                />
                <FormControl
                  type="select"
                  v-model="formData.marital_status"
                  :options="maritalStatusOptions"
                  :label="'Marital Status'"
                  placeholder="Select marital status"
                  :disabled="optionsResource.loading"
                />
                <FormControl
                  type="select"
                  v-model="formData.education"
                  :options="educationOptions"
                  :label="'Education'"
                  placeholder="Select education"
                  :disabled="optionsResource.loading"
                />
                <FormControl
                  type="select"
                  v-model="formData.occupation"
                  :options="occupationOptions"
                  :label="'Occupation'"
                  placeholder="Select occupation"
                  :disabled="optionsResource.loading"
                />
              </div>
            </div>

            <!-- Terms and Conditions -->
            <div class="flex items-start">
              <div class="flex items-center h-5">
                <input
                  id="terms"
                  v-model="agreedToTerms"
                  type="checkbox"
                  class="h-4 w-4 text-pink-600 focus:ring-pink-500 border-gray-300 rounded"
                  required
                />
              </div>
              <div class="ml-3 text-sm">
                <label for="terms" class="font-medium text-gray-700">
                  I agree to the 
                  <a href="#" class="text-pink-600 hover:text-pink-500">Terms and Conditions</a> and 
                  <a href="#" class="text-pink-600 hover:text-pink-500">Privacy Policy</a>
                </label>
              </div>
            </div>

            <!-- Error Message -->
            <ErrorMessage v-if="error" :message="error" />

            <!-- Success Message -->
            <div v-if="success" class="rounded-lg bg-green-50 border border-green-200 p-4">
              <div class="flex items-start">
                <FeatherIcon name="check-circle" class="h-5 w-5 text-green-500 mt-0.5" />
                <div class="ml-3">
                  <h3 class="text-sm font-semibold text-green-800">Registration Successful!</h3>
                  <p class="mt-1 text-sm text-green-700">{{ successMessage }}</p>
                </div>
              </div>
            </div>

            <!-- Submit Button -->
            <div class="pt-4">
              <Button
                type="submit"
                variant="solid"
                size="lg"
                :loading="registerResource.loading"
                class="w-full !py-3"
              >
                <template #prefix>
                  <FeatherIcon name="user-plus" class="w-5 h-5" />
                </template>
                Create Account
              </Button>
            </div>
          </form>

          <!-- Login Link -->
          <div class="mt-8 pt-6 border-t border-gray-200 text-center">
            <p class="text-sm text-gray-600">
              Already have an account?
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
import { useRouter } from 'vue-router'
import { createResource, FormControl, Button, Card, ErrorMessage, FeatherIcon } from 'frappe-ui'

const router = useRouter()

const formData = ref({
  full_name: '',
  gender: '',
  dob: '',
  phone: '',
  email: '',
  city: '',
  state: '',
  religion: '',
  marital_status: '',
  education: '',
  occupation: ''
})

const agreedToTerms = ref(false)
const error = ref(null)
const success = ref(false)
const successMessage = ref('')

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
    if (data.error) {
      error.value = 'Failed to load form options. Please refresh the page.'
      return
    }
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

// Combined signup and profile creation using custom API
const registerResource = createResource({
  url: 'shaadi.shaadi.api.signup.register_member',
  makeParams(values) {
    return {
      full_name: values.full_name,
      email: values.email,
      gender: values.gender,
      dob: values.dob,
      phone: values.phone,
      city: values.city,
      state: values.state,
      religion: values.religion,
      marital_status: values.marital_status,
      education: values.education,
      occupation: values.occupation
    }
  }
})

async function handleSubmit() {
  if (!agreedToTerms.value) {
    error.value = 'Please agree to the Terms and Conditions'
    return
  }

  error.value = null
  
  try {
    // Register user and create member profile in one call
    await registerResource.submit(formData.value, {
      onSuccess(data) {
        success.value = true
        successMessage.value = data.message || 'Registration successful! A password reset link has been sent to your email.'
        // Redirect to login after 5 seconds to give user time to read the message
        setTimeout(() => {
          router.push('/signin')
        }, 5000)
      },
      onError(err) {
        throw new Error(err.messages?.[0] || err)
      }
    })
  } catch (err) {
    console.error('Registration error:', err)
    error.value = err.message || 'Failed to create account. Please try again.'
  }
}
</script>
