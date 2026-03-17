<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Partner Preferences</h1>
        <p class="text-gray-600 mt-1">Tell us what you're looking for in your ideal partner</p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <LoadingIndicator class="w-8 h-8" />
      </div>

      <!-- Preference Form -->
      <form v-else @submit.prevent="savePreferences" class="space-y-6">
        <!-- Age & Height Section -->
        <Card>
          <template #header>
            <h2 class="text-xl font-semibold text-gray-900">Age & Height</h2>
          </template>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <FormControl
                v-model="preferences.min_age"
                type="number"
                label="Minimum Age"
                placeholder="18"
                :min="18"
                :max="60"
              />
            </div>
            <div>
              <FormControl
                v-model="preferences.max_age"
                type="number"
                label="Maximum Age"
                placeholder="40"
                :min="18"
                :max="60"
              />
            </div>
            <div>
              <FormControl
                v-model="preferences.min_height_cm"
                type="number"
                label="Minimum Height (cm)"
                placeholder="150"
              />
            </div>
            <div>
              <FormControl
                v-model="preferences.max_height_cm"
                type="number"
                label="Maximum Height (cm)"
                placeholder="180"
              />
            </div>
          </div>
        </Card>

        <!-- Marital Status & Religion -->
        <Card>
          <template #header>
            <h2 class="text-xl font-semibold text-gray-900">Marital Status & Religion</h2>
          </template>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <FormControl
                v-model="preferences.marital_status"
                type="select"
                label="Marital Status"
                :options="maritalStatusOptions"
              />
            </div>
            <div>
              <FormControl
                v-model="preferences.religion"
                type="text"
                label="Religion (comma-separated)"
                placeholder="Hindu, Muslim, Christian, Any"
              />
            </div>
            <div>
              <FormControl
                v-model="preferences.caste_bar"
                type="select"
                label="Caste Preference"
                :options="casteBarOptions"
              />
            </div>
            <div>
              <FormControl
                v-model="preferences.caste_preference"
                type="text"
                label="Preferred Castes (comma-separated)"
                placeholder="Optional"
              />
            </div>
          </div>
        </Card>

        <!-- Language & Horoscope -->
        <Card>
          <template #header>
            <h2 class="text-xl font-semibold text-gray-900">Language & Horoscope</h2>
          </template>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <FormControl
                v-model="preferences.mother_tongue"
                type="text"
                label="Mother Tongue (comma-separated)"
                placeholder="Hindi, English, Tamil"
              />
            </div>
            <div>
              <FormControl
                v-model="preferences.manglik_pref"
                type="select"
                label="Manglik Preference"
                :options="manglikOptions"
              />
            </div>
            <div class="md:col-span-2">
              <label class="flex items-center space-x-2">
                <input
                  v-model="preferences.kundali_must"
                  type="checkbox"
                  class="rounded border-gray-300 text-pink-600 focus:ring-pink-500"
                />
                <span class="text-sm text-gray-700">Kundali Match is Must</span>
              </label>
            </div>
          </div>
        </Card>

        <!-- Education & Income -->
        <Card>
          <template #header>
            <h2 class="text-xl font-semibold text-gray-900">Education & Income</h2>
          </template>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <FormControl
                v-model="preferences.education_pref"
                type="select"
                label="Minimum Education"
                :options="educationOptions"
              />
            </div>
            <div>
              <FormControl
                v-model="preferences.income_pref"
                type="select"
                label="Minimum Annual Income"
                :options="incomeOptions"
              />
            </div>
            <div class="md:col-span-2">
              <FormControl
                v-model="preferences.occupation_pref"
                type="text"
                label="Occupation Type (comma-separated)"
                placeholder="Software Engineer, Doctor, Business"
              />
            </div>
          </div>
        </Card>

        <!-- Lifestyle -->
        <Card>
          <template #header>
            <h2 class="text-xl font-semibold text-gray-900">Lifestyle</h2>
          </template>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <FormControl
                v-model="preferences.diet_pref"
                type="select"
                label="Diet"
                :options="dietOptions"
              />
            </div>
            <div>
              <FormControl
                v-model="preferences.smoking_pref"
                type="select"
                label="Smoking"
                :options="smokingOptions"
              />
            </div>
            <div>
              <FormControl
                v-model="preferences.drinking_pref"
                type="select"
                label="Drinking"
                :options="drinkingOptions"
              />
            </div>
          </div>
        </Card>

        <!-- Location -->
        <Card>
          <template #header>
            <h2 class="text-xl font-semibold text-gray-900">Location</h2>
          </template>
          <div class="space-y-4">
            <div>
              <FormControl
                v-model="preferences.country_pref"
                type="select"
                label="Country"
                :options="countryOptions"
              />
            </div>
            <div>
              <FormControl
                v-model="cityInput"
                type="text"
                label="Preferred Cities (comma-separated)"
                placeholder="Mumbai, Delhi, Bangalore"
              />
            </div>
          </div>
        </Card>

        <!-- About Partner -->
        <Card>
          <template #header>
            <h2 class="text-xl font-semibold text-gray-900">About Your Ideal Partner</h2>
          </template>
          <div>
            <Textarea
              v-model="preferences.about_partner"
              rows="4"
              placeholder="Describe your ideal partner..."
            />
          </div>
        </Card>

        <!-- Action Buttons -->
        <div class="flex justify-end space-x-4">
          <Button variant="outline" @click="$router.back()">
            Cancel
          </Button>
          <Button variant="solid" type="submit" :loading="saving">
            {{ isUpdate ? 'Update Preferences' : 'Save Preferences' }}
          </Button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { call, Button, Card, FormControl, Textarea, LoadingIndicator, toast } from 'frappe-ui'

const router = useRouter()
const loading = ref(true)
const saving = ref(false)
const isUpdate = ref(false)
const cityInput = ref('')

const preferences = ref({
  min_age: 18,
  max_age: 40,
  min_height_cm: null,
  max_height_cm: null,
  marital_status: 'Never Married',
  religion: 'Any',
  caste_bar: 'Any',
  caste_preference: '',
  mother_tongue: '',
  manglik_pref: 'Doesnt Matter',
  kundali_must: 0,
  education_pref: '',
  income_pref: '',
  occupation_pref: '',
  diet_pref: 'Any',
  smoking_pref: 'Doesnt Matter',
  drinking_pref: 'Doesnt Matter',
  country_pref: 'India',
  about_partner: ''
})

// Options
const maritalStatusOptions = ['Never Married', 'Divorced', 'Widowed', 'Any']
const casteBarOptions = ['Same Caste', 'Same Religion Any Caste', 'Any']
const manglikOptions = ['Manglik', 'Non Manglik', 'Partial', 'Doesnt Matter']
const educationOptions = ['Below 10th', '10th Pass', '12th Pass', 'Diploma', 'Graduation', 'Post Graduation', 'Doctorate']
const incomeOptions = ['No Income', 'Below 2 Lakh', '2-5 Lakh', '5-10 Lakh', '10-20 Lakh', '20-50 Lakh', 'Above 50 Lakh']
const dietOptions = ['Vegetarian', 'Any', 'Non-Vegetarian']
const smokingOptions = ['Non Smoker Only', 'OK with Smoking', 'Doesnt Matter']
const drinkingOptions = ['Non Drinker Only', 'OK with Drinking', 'Doesnt Matter']
const countryOptions = ['India', 'NRI', 'Any']

async function loadPreferences() {
  loading.value = true
  try {
    const response = await call('shaadi.shaadi.api.partner_preference.get_partner_preference')
    
    if (response) {
      isUpdate.value = true
      Object.assign(preferences.value, response)
      
      // Convert cities array to comma-separated string
      if (response.cities && response.cities.length > 0) {
        cityInput.value = response.cities.join(', ')
      }
    }
  } catch (error) {
    console.error('Error loading preferences:', error)
  } finally {
    loading.value = false
  }
}

async function savePreferences() {
  saving.value = true
  try {
    // Parse cities from comma-separated input
    const cities = cityInput.value
      .split(',')
      .map(city => city.trim())
      .filter(city => city.length > 0)
    
    const data = {
      ...preferences.value,
      cities: cities,
      kundali_must: preferences.value.kundali_must ? 1 : 0
    }
    
    const response = await call('shaadi.shaadi.api.partner_preference.create_or_update_partner_preference', {
      preferences: data
    })
    
    toast({
      title: 'Success!',
      text: response.message || 'Preferences saved successfully!',
      icon: 'check-circle',
      iconClasses: 'text-green-500'
    })
    
    // Redirect to matches page
    setTimeout(() => {
      router.push('/matches')
    }, 1000)
    
  } catch (error) {
    console.error('Error saving preferences:', error)
    toast({
      title: 'Error',
      text: error.message || 'Failed to save preferences',
      icon: 'alert-circle',
      iconClasses: 'text-red-500'
    })
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  loadPreferences()
})
</script>

<style scoped>
/* Additional custom styles if needed */
</style>
