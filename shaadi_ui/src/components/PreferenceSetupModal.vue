<template>
  <Dialog v-model="show" :options="{ title: 'Complete Your Profile', size: 'xl' }">
    <template #body-content>
      <div class="space-y-6">
        <!-- Header -->
        <div class="text-center">
          <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-pink-100 mb-4">
            <FeatherIcon name="heart" class="h-6 w-6 text-pink-600" />
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">
            Set Your Partner Preferences
          </h3>
          <p class="text-sm text-gray-500">
            Help us find your perfect match by setting your preferences
          </p>
        </div>

        <!-- Quick Setup Form -->
        <div class="space-y-4">
          <!-- Age Range -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Age Range</label>
            <div class="grid grid-cols-2 gap-4">
              <FormControl
                v-model="quickPrefs.min_age"
                type="number"
                placeholder="Min Age"
                :min="18"
                :max="60"
              />
              <FormControl
                v-model="quickPrefs.max_age"
                type="number"
                placeholder="Max Age"
                :min="18"
                :max="60"
              />
            </div>
          </div>

          <!-- Marital Status -->
          <div>
            <FormControl
              v-model="quickPrefs.marital_status"
              type="select"
              label="Marital Status"
              :options="['Never Married', 'Divorced', 'Widowed', 'Any']"
            />
          </div>

          <!-- Religion -->
          <div>
            <FormControl
              v-model="quickPrefs.religion"
              type="text"
              label="Religion Preference"
              placeholder="Any, Hindu, Muslim, Christian, etc."
            />
          </div>

          <!-- Location -->
          <div>
            <FormControl
              v-model="quickPrefs.country_pref"
              type="select"
              label="Location"
              :options="['India', 'NRI', 'Any']"
            />
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex flex-col sm:flex-row gap-3 pt-4">
          <Button
            variant="solid"
            class="flex-1"
            @click="saveQuickPreferences"
            :loading="saving"
          >
            Save & Continue
          </Button>
          <Button
            variant="outline"
            class="flex-1"
            @click="goToFullPreferences"
          >
            Set Detailed Preferences
          </Button>
        </div>

        <!-- Skip Option -->
        <div class="text-center">
          <button
            @click="skipForNow"
            class="text-sm text-gray-500 hover:text-gray-700 underline"
          >
            Skip for now
          </button>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Dialog, Button, FormControl, FeatherIcon, call, toast } from 'frappe-ui'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'saved', 'skipped'])

const router = useRouter()
const show = ref(props.modelValue)
const saving = ref(false)

const quickPrefs = ref({
  min_age: 24,
  max_age: 32,
  marital_status: 'Never Married',
  religion: 'Any',
  country_pref: 'India'
})

watch(() => props.modelValue, (newVal) => {
  show.value = newVal
})

watch(show, (newVal) => {
  emit('update:modelValue', newVal)
})

async function saveQuickPreferences() {
  saving.value = true
  try {
    const preferences = {
      ...quickPrefs.value,
      min_height_cm: 150,
      max_height_cm: 180,
      caste_bar: 'Any',
      manglik_pref: 'Doesnt Matter',
      kundali_must: 0,
      diet_pref: 'Any',
      smoking_pref: 'Doesnt Matter',
      drinking_pref: 'Doesnt Matter',
      about_partner: 'Looking for a compatible life partner'
    }

    await call('shaadi.shaadi.api.partner_preference.create_or_update_partner_preference', {
      preferences: preferences
    })

    toast({
      title: 'Success!',
      text: 'Preferences saved successfully!',
      icon: 'check-circle',
      iconClasses: 'text-green-500'
    })
    show.value = false
    emit('saved')
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

function goToFullPreferences() {
  show.value = false
  router.push('/preferences')
}

function skipForNow() {
  show.value = false
  emit('skipped')
}
</script>

<style scoped>
/* Additional styles if needed */
</style>
