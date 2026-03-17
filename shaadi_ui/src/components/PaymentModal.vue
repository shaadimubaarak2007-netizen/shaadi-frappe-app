<template>
  <Dialog v-model="show" :options="{ title: 'Complete Payment', size: 'lg' }">
    <template #body-content>
      <div class="space-y-6">
        <!-- Plan Summary -->
        <div class="bg-gradient-to-r from-pink-50 to-purple-50 rounded-lg p-6">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="text-xl font-bold text-gray-900">{{ selectedPlan?.plan_name }}</h3>
              <p class="text-sm text-gray-600 mt-1">{{ selectedPlan?.description }}</p>
            </div>
            <div class="text-right">
              <div class="text-3xl font-bold text-pink-600">₹{{ selectedPlan?.price_inr || selectedPlan?.price }}</div>
              <div class="text-sm text-gray-500">{{ selectedPlan?.duration_days }} days</div>
            </div>
          </div>
          
          <!-- Features -->
          <div class="grid grid-cols-2 gap-4 mt-4 pt-4 border-t border-pink-200">
            <div class="flex items-center gap-2">
              <FeatherIcon name="message-circle" class="w-4 h-4 text-pink-600" />
              <span class="text-sm">{{ selectedPlan?.messages_allowed || selectedPlan?.messages_limit }} Messages</span>
            </div>
            <div class="flex items-center gap-2">
              <FeatherIcon name="phone" class="w-4 h-4 text-pink-600" />
              <span class="text-sm">{{ selectedPlan?.contacts_allowed || selectedPlan?.contacts_limit }} Contacts</span>
            </div>
          </div>
        </div>

        <!-- Payment Processing Status -->
        <div v-if="processing" class="text-center py-8">
          <Spinner class="w-8 h-8 mx-auto mb-4" />
          <p class="text-gray-600">{{ processingMessage }}</p>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4">
          <div class="flex items-start gap-3">
            <FeatherIcon name="alert-circle" class="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
            <div>
              <h4 class="font-semibold text-red-900">Payment Failed</h4>
              <p class="text-sm text-red-700 mt-1">{{ error }}</p>
            </div>
          </div>
        </div>

        <!-- Payment Information -->
        <div v-if="!processing && !error" class="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div class="flex items-start gap-3">
            <FeatherIcon name="info" class="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
            <div class="text-sm text-blue-900">
              <p class="font-semibold mb-1">Secure Payment via Razorpay</p>
              <p>You will be redirected to Razorpay's secure payment gateway to complete your purchase.</p>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex gap-3 pt-4">
          <Button
            variant="outline"
            class="flex-1"
            @click="closeModal"
            :disabled="processing"
          >
            Cancel
          </Button>
          <Button
            variant="solid"
            class="flex-1"
            @click="initiatePayment"
            :loading="processing"
            :disabled="processing"
          >
            <template #prefix>
              <FeatherIcon name="credit-card" class="w-4 h-4" />
            </template>
            Pay ₹{{ selectedPlan?.price_inr || selectedPlan?.price }}
          </Button>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Dialog, Button, FeatherIcon, Spinner, call, toast } from 'frappe-ui'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  selectedPlan: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'payment-success'])

const show = ref(props.modelValue)
const processing = ref(false)
const processingMessage = ref('Initializing payment...')
const error = ref(null)

watch(() => props.modelValue, (newVal) => {
  show.value = newVal
  if (newVal) {
    error.value = null
  }
})

watch(show, (newVal) => {
  emit('update:modelValue', newVal)
})

async function initiatePayment() {
  if (!props.selectedPlan) return
  
  // Validate before initiating payment (LMS pattern)
  if (!validatePayment()) {
    return
  }
  
  processing.value = true
  processingMessage.value = 'Initializing payment...'
  error.value = null
  
  try {
    // Call backend API to initiate payment (LMS pattern)
    const response = await call('shaadi.shaadi.api.payment.initiate_payment', {
      subscription_plan_id: props.selectedPlan.name
    })
    
    if (response.success) {
      processingMessage.value = 'Redirecting to payment gateway...'
      
      // LMS pattern: Redirect to payment URL
      console.log('Payment URL received:', response.payment_url)
      
      // Use window.location.replace to force full page reload and bypass Vue Router
      window.location.replace(response.payment_url)
    } else {
      error.value = response.error || 'Failed to initiate payment'
      processing.value = false
    }
  } catch (err) {
    console.error('Payment initiation error:', err)
    error.value = err.message || 'Failed to initiate payment. Please try again.'
    processing.value = false
    
    toast({
      title: 'Payment Error',
      text: 'Failed to initiate payment. Please try again.',
      icon: 'alert-circle',
      iconClasses: 'text-red-500'
    })
  }
}

function validatePayment() {
  // Basic validation before payment
  if (!props.selectedPlan) {
    error.value = 'Please select a subscription plan'
    return false
  }
  
  const price = props.selectedPlan.price_inr || props.selectedPlan.price
  if (!price || price <= 0) {
    error.value = 'Invalid plan amount'
    return false
  }
  
  return true
}

function closeModal() {
  show.value = false
  error.value = null
  processing.value = false
}
</script>
