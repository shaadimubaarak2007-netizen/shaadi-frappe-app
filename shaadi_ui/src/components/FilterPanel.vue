<template>
  <div class="filter-panel bg-shaadi-surface rounded-xl shadow-sm border border-shaadi p-4">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Filters</h3>
      <Button variant="ghost" size="sm" @click="clearFilters">
        Clear All
      </Button>
    </div>

    <div class="space-y-6">
      <!-- Religion -->
      <div class="filter-section">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Religion</label>
        <select 
          v-model="localFilters.religion" 
          class="w-full px-3 py-2 border border-shaadi-mid rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-pink-500 bg-shaadi-surface text-shaadi-primary"
        >
          <option value="">Any</option>
          <option value="Hindu">Hindu</option>
          <option value="Muslim">Muslim</option>
          <option value="Christian">Christian</option>
          <option value="Sikh">Sikh</option>
          <option value="Jain">Jain</option>
          <option value="Buddhist">Buddhist</option>
          <option value="Other">Other</option>
        </select>
      </div>

      <!-- Marital Status -->
      <div class="filter-section">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Marital Status</label>
        <select 
          v-model="localFilters.marital_status" 
          class="w-full px-3 py-2 border border-shaadi-mid rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-pink-500 bg-shaadi-surface text-shaadi-primary"
        >
          <option value="">Any</option>
          <option value="Never Married">Never Married</option>
          <option value="Divorced">Divorced</option>
          <option value="Widowed">Widowed</option>
          <option value="Awaiting Divorce">Awaiting Divorce</option>
        </select>
      </div>

      <!-- Education -->
      <div class="filter-section">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Education</label>
        <select 
          v-model="localFilters.education" 
          class="w-full px-3 py-2 border border-shaadi-mid rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-pink-500 bg-shaadi-surface text-shaadi-primary"
        >
          <option value="">Any</option>
          <option value="Below 10th">Below 10th</option>
          <option value="10th Pass">10th Pass</option>
          <option value="12th Pass">12th Pass</option>
          <option value="Diploma">Diploma</option>
          <option value="Graduation">Graduation</option>
          <option value="Post Graduation">Post Graduation</option>
          <option value="Doctorate">Doctorate</option>
        </select>
      </div>

      <!-- State -->
      <div class="filter-section">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">State</label>
        <select 
          v-model="localFilters.state" 
          class="w-full px-3 py-2 border border-shaadi-mid rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-pink-500 bg-shaadi-surface text-shaadi-primary"
        >
          <option value="">Any</option>
          <option value="Delhi">Delhi</option>
          <option value="Maharashtra">Maharashtra</option>
          <option value="Karnataka">Karnataka</option>
          <option value="Tamil Nadu">Tamil Nadu</option>
          <option value="Gujarat">Gujarat</option>
          <option value="Uttar Pradesh">Uttar Pradesh</option>
          <option value="West Bengal">West Bengal</option>
          <option value="Rajasthan">Rajasthan</option>
          <option value="Punjab">Punjab</option>
          <option value="Haryana">Haryana</option>
        </select>
      </div>

      <!-- Apply Button -->
      <Button 
        variant="solid" 
        theme="blue" 
        class="w-full"
        @click="applyFilters"
      >
        Apply Filters
      </Button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue', 'apply'])

const localFilters = ref({
  religion: props.modelValue.religion || '',
  marital_status: props.modelValue.marital_status || '',
  education: props.modelValue.education || '',
  state: props.modelValue.state || ''
})

function clearFilters() {
  localFilters.value = {
    religion: '',
    marital_status: '',
    education: '',
    state: ''
  }
  applyFilters()
}

function applyFilters() {
  // Remove empty values
  const cleanFilters = Object.fromEntries(
    Object.entries(localFilters.value).filter(([_, v]) => v !== '' && v !== null && v !== undefined)
  )
  emit('update:modelValue', cleanFilters)
  emit('apply', cleanFilters)
}

watch(() => props.modelValue, (newVal) => {
  localFilters.value = { ...localFilters.value, ...newVal }
}, { deep: true })
</script>

<style scoped>
.filter-section {
  @apply pb-4 border-b border-gray-100 last:border-0 last:pb-0;
}
</style>
