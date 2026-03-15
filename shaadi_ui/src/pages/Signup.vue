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
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">Full Name *</label>
                  <Input
                    v-model="formData.full_name"
                    type="text"
                    placeholder="Enter your full name"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">Gender *</label>
                  <FormControl
                    type="select"
                    v-model="formData.gender"
                    :options="[
                      { label: 'Male', value: 'Male' },
                      { label: 'Female', value: 'Female' }
                    ]"
                    placeholder="Select gender"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">Date of Birth *</label>
                  <Input
                    v-model="formData.dob"
                    type="date"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">Phone Number *</label>
                  <Input
                    v-model="formData.phone"
                    type="tel"
                    placeholder="+91 9876543210"
                    required
                  />
                </div>
              </div>
            </div>

            <!-- Account Information -->
            <div class="space-y-4">
              <div class="flex items-center space-x-2 mb-4">
                <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                  <FeatherIcon name="lock" class="w-4 h-4 text-purple-600" />
                </div>
                <h3 class="text-lg font-semibold text-gray-900">Account Information</h3>
              </div>
              <div class="grid md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">Email Address *</label>
                  <Input
                    v-model="formData.email"
                    type="email"
                    placeholder="your.email@example.com"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">Password *</label>
                  <Input
                    v-model="formData.password"
                    type="password"
                    placeholder="Create a strong password"
                    required
                  />
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
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">City *</label>
                  <Input
                    v-model="formData.city"
                    type="text"
                    placeholder="Enter your city"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">State *</label>
                  <Input
                    v-model="formData.state"
                    type="text"
                    placeholder="Enter your state"
                    required
                  />
                </div>
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
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">Religion *</label>
                  <FormControl
                    type="select"
                    v-model="formData.religion"
                    :options="religionOptions"
                    placeholder="Select religion"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">Marital Status *</label>
                  <FormControl
                    type="select"
                    v-model="formData.marital_status"
                    :options="maritalStatusOptions"
                    placeholder="Select marital status"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">Education *</label>
                  <FormControl
                    type="select"
                    v-model="formData.education"
                    :options="educationOptions"
                    placeholder="Select education"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">Occupation *</label>
                  <FormControl
                    type="select"
                    v-model="formData.occupation"
                    :options="occupationOptions"
                    placeholder="Select occupation"
                  />
                </div>
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
                  <p class="mt-1 text-sm text-green-700">Your account has been created. Redirecting to login...</p>
                </div>
              </div>
            </div>

            <!-- Submit Button -->
            <div class="pt-4">
              <Button
                type="submit"
                variant="solid"
                size="lg"
                :loading="loading"
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
import { call, Input, FormControl, Button, Card, ErrorMessage, FeatherIcon } from 'frappe-ui'

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

const agreedToTerms = ref(false)
const loading = ref(false)
const error = ref(null)
const success = ref(false)

const religionOptions = [
  { label: 'Hindu', value: 'Hindu' },
  { label: 'Muslim', value: 'Muslim' },
  { label: 'Christian', value: 'Christian' },
  { label: 'Sikh', value: 'Sikh' },
  { label: 'Jain', value: 'Jain' },
  { label: 'Buddhist', value: 'Buddhist' },
  { label: 'Other', value: 'Other' }
]

const maritalStatusOptions = [
  { label: 'Never Married', value: 'Never Married' },
  { label: 'Divorced', value: 'Divorced' },
  { label: 'Widowed', value: 'Widowed' },
  { label: 'Awaiting Divorce', value: 'Awaiting Divorce' }
]

const educationOptions = [
  { label: 'High School', value: 'High School' },
  { label: 'Diploma', value: 'Diploma' },
  { label: 'Graduation', value: 'Graduation' },
  { label: 'Post Graduation', value: 'Post Graduation' },
  { label: 'Doctorate', value: 'Doctorate' }
]

const occupationOptions = [
  { label: 'Business/Self Employed', value: 'Business/Self Employed' },
  { label: 'Private Job', value: 'Private Job' },
  { label: 'Government Job', value: 'Government Job' },
  { label: 'Defense', value: 'Defense' },
  { label: 'NRI', value: 'NRI' },
  { label: 'Not Working', value: 'Not Working' }
]

async function handleSubmit() {
  if (!agreedToTerms.value) {
    error.value = 'Please agree to the Terms and Conditions'
    return
  }

  loading.value = true
  error.value = null

  try {
    // Create user account
    await call('frappe.core.doctype.user.user.sign_up', {
      email: formData.value.email,
      full_name: formData.value.full_name,
      redirect_to: '/signin'
    })

    // Create member profile
    await call('frappe.client.insert', {
      doc: {
        doctype: 'Member Profile',
        full_name: formData.value.full_name,
        gender: formData.value.gender,
        dob: formData.value.dob,
        phone: formData.value.phone,
        email: formData.value.email,
        city: formData.value.city,
        state: formData.value.state,
        religion: formData.value.religion,
        marital_status: formData.value.marital_status,
        education: formData.value.education,
        occupation: formData.value.occupation,
        is_active: 1
      }
    })

    success.value = true
    
    // Redirect to login after 2 seconds
    setTimeout(() => {
      router.push('/signin')
    }, 2000)
  } catch (err) {
    console.error('Registration error:', err)
    error.value = err.message || 'Failed to create account. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
