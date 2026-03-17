<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">Choose Your Perfect Plan</h1>
        <p class="text-lg text-gray-600">Find your life partner with the right subscription</p>
      </div>

      <!-- Current Subscription (if exists) -->
      <Card v-if="currentSubscription" class="mb-8 bg-gradient-to-r from-purple-600 to-pink-600 text-white">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-2xl font-bold mb-2">{{ currentSubscription.plan_details?.plan_name || 'Current Plan' }}</h2>
            <p class="text-purple-100">{{ currentSubscription.days_remaining }} days remaining</p>
          </div>
          <div class="text-right">
            <div class="text-3xl font-bold">{{ currentSubscription.messages_remaining }}/{{ currentSubscription.plan_details?.messages_allowed }}</div>
            <p class="text-purple-100">Messages Left Today</p>
          </div>
        </div>
        <div class="mt-4 grid grid-cols-2 gap-4">
          <div class="bg-white/20 rounded-lg p-3">
            <div class="text-2xl font-bold">{{ currentSubscription.contacts_remaining }}</div>
            <div class="text-sm text-purple-100">Contacts Remaining</div>
          </div>
          <div class="bg-white/20 rounded-lg p-3">
            <div class="text-2xl font-bold">{{ formatDate(currentSubscription.end_date) }}</div>
            <div class="text-sm text-purple-100">Expires On</div>
          </div>
        </div>
      </Card>

      <!-- No Subscription Alert -->
      <Card v-else-if="!loadingSubscription" class="mb-8 bg-yellow-50 border-yellow-200">
        <div class="flex items-start gap-4">
          <div class="flex-shrink-0">
            <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-yellow-900 mb-1">No Active Subscription</h3>
            <p class="text-yellow-700">You're currently on the Free plan with limited access. Upgrade to unlock messaging, contact details, and more!</p>
          </div>
        </div>
      </Card>

      <!-- Plans Grid -->
      <div class="grid md:grid-cols-3 gap-6 mb-8">
        <Card 
          v-for="plan in plans" 
          :key="plan.name"
          :class="[
            'relative overflow-hidden transition-all hover:shadow-xl',
            plan.plan_type === 'Gold' ? 'ring-2 ring-purple-500 transform scale-105' : '',
            isCurrentPlan(plan) ? 'bg-purple-50 border-purple-300' : ''
          ]"
        >
          <!-- Popular Badge -->
          <div v-if="plan.plan_type === 'Gold'" class="absolute top-0 right-0 bg-gradient-to-r from-purple-600 to-pink-600 text-white px-4 py-1 text-sm font-semibold rounded-bl-lg">
            POPULAR
          </div>

          <!-- Current Plan Badge -->
          <div v-if="isCurrentPlan(plan)" class="absolute top-0 left-0 bg-green-500 text-white px-4 py-1 text-sm font-semibold rounded-br-lg">
            CURRENT
          </div>

          <div class="text-center mb-6">
            <h3 class="text-2xl font-bold text-gray-900 mb-2">{{ plan.plan_name }}</h3>
            <div class="flex items-baseline justify-center gap-2">
              <span class="text-4xl font-bold text-purple-600">₹{{ plan.price_inr }}</span>
              <span class="text-gray-500">/ {{ plan.duration_days }} days</span>
            </div>
          </div>

          <!-- Features List -->
          <div class="space-y-3 mb-6">
            <div class="flex items-center gap-2 text-sm">
              <svg class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span>{{ plan.contacts_allowed }} Contact Views</span>
            </div>
            <div class="flex items-center gap-2 text-sm">
              <svg class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span>{{ plan.messages_allowed }} Messages/Day</span>
            </div>
            <div class="flex items-center gap-2 text-sm">
              <svg :class="plan.can_send_message ? 'text-green-500' : 'text-gray-300'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span :class="!plan.can_send_message ? 'text-gray-400 line-through' : ''">Send Messages</span>
            </div>
            <div class="flex items-center gap-2 text-sm">
              <svg :class="plan.can_view_contact ? 'text-green-500' : 'text-gray-300'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span :class="!plan.can_view_contact ? 'text-gray-400 line-through' : ''">View Contact Details</span>
            </div>
            <div class="flex items-center gap-2 text-sm">
              <svg :class="plan.can_see_all_photos ? 'text-green-500' : 'text-gray-300'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span :class="!plan.can_see_all_photos ? 'text-gray-400 line-through' : ''">View All Photos</span>
            </div>
            <div class="flex items-center gap-2 text-sm">
              <svg :class="plan.featured_profile ? 'text-green-500' : 'text-gray-300'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span :class="!plan.featured_profile ? 'text-gray-400 line-through' : ''">Featured Profile</span>
            </div>
          </div>

          <!-- CTA Button -->
          <Button 
            v-if="!isCurrentPlan(plan)"
            :variant="plan.plan_type === 'Gold' ? 'solid' : 'outline'"
            class="w-full"
            :disabled="plan.plan_type === 'Free'"
            @click="selectPlan(plan)"
          >
            <template v-if="plan.plan_type === 'Free'">
              Current Plan
            </template>
            <template v-else>
              Choose {{ plan.plan_name }}
            </template>
          </Button>
          <div v-else class="text-center text-green-600 font-semibold py-2">
            ✓ Active Plan
          </div>
        </Card>
      </div>

      <!-- FAQ Section -->
      <Card class="bg-white">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">Frequently Asked Questions</h2>
        <div class="space-y-4">
          <div>
            <h3 class="font-semibold text-gray-900 mb-2">How does messaging work?</h3>
            <p class="text-gray-600">With a paid subscription, you can send messages to other members. Free users cannot send messages but can receive them.</p>
          </div>
          <div>
            <h3 class="font-semibold text-gray-900 mb-2">What happens when my subscription expires?</h3>
            <p class="text-gray-600">Your account will revert to the Free plan. You'll lose access to premium features but your data remains safe.</p>
          </div>
          <div>
            <h3 class="font-semibold text-gray-900 mb-2">Can I upgrade my plan?</h3>
            <p class="text-gray-600">Yes! You can upgrade to a higher plan at any time. Contact support for assistance.</p>
          </div>
        </div>
      </Card>
    </div>

    <!-- Upgrade Modal -->
    <Dialog 
      v-model="showUpgradeModal" 
      :options="upgradeDialogOptions"
    >
      <template #body-content>
        <div v-if="selectedPlan" class="space-y-4">
          <div class="text-center">
            <h3 class="text-2xl font-bold text-gray-900 mb-2">{{ selectedPlan.plan_name }}</h3>
            <div class="text-4xl font-bold text-purple-600 mb-4">₹{{ selectedPlan.price_inr }}</div>
          </div>
          
          <div class="bg-gray-50 rounded-lg p-4 space-y-2">
            <div class="flex justify-between text-sm">
              <span class="text-gray-600">Duration</span>
              <span class="font-medium">{{ selectedPlan.duration_days }} days</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-600">Messages Allowed</span>
              <span class="font-medium">{{ selectedPlan.messages_allowed }} per day</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-600">Contact Views</span>
              <span class="font-medium">{{ selectedPlan.contacts_allowed }}</span>
            </div>
          </div>
          
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p class="text-sm text-blue-800">
              <strong>Note:</strong> Click "Proceed to Payment" to complete your purchase securely via Razorpay.
            </p>
          </div>
        </div>
      </template>
    </Dialog>

    <!-- Payment Modal -->
    <PaymentModal 
      v-model="showPaymentModal"
      :selected-plan="selectedPlan"
      @payment-complete="handlePaymentComplete"
    />

    <!-- Payment Result Dialog -->
    <Dialog 
      v-model="showPaymentResultModal" 
      :options="paymentResultDialogOptions"
    >
      <template #body-content>
        <div v-if="paymentResult" class="space-y-4">
          <!-- Success State -->
          <div v-if="paymentResult.status === 'success'" class="text-center">
            <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">Payment Successful!</h3>
            <p class="text-gray-600 mb-4">Your subscription has been activated successfully.</p>
            
            <div class="bg-gray-50 rounded-lg p-4 text-left space-y-2">
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Transaction ID</span>
                <span class="font-medium">{{ paymentResult.transactionId }}</span>
              </div>
              <div v-if="paymentResult.transaction" class="flex justify-between text-sm">
                <span class="text-gray-600">Amount Paid</span>
                <span class="font-medium">₹{{ paymentResult.transaction.amount }}</span>
              </div>
              <div v-if="paymentResult.transaction?.razorpay_payment_id" class="flex justify-between text-sm">
                <span class="text-gray-600">Payment ID</span>
                <span class="font-medium text-xs">{{ paymentResult.transaction.razorpay_payment_id }}</span>
              </div>
            </div>
          </div>

          <!-- Failure State -->
          <div v-else class="text-center">
            <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">Payment Failed</h3>
            <p class="text-gray-600 mb-4">
              {{ paymentResult.error || 'Your payment could not be processed. Please try again.' }}
            </p>
            
            <div class="bg-gray-50 rounded-lg p-4 text-left space-y-2">
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Transaction ID</span>
                <span class="font-medium">{{ paymentResult.transactionId }}</span>
              </div>
              <div v-if="paymentResult.transaction?.error_message" class="text-sm">
                <span class="text-gray-600">Error</span>
                <p class="text-red-600 mt-1">{{ paymentResult.transaction.error_message }}</p>
              </div>
            </div>
            
            <div class="mt-4 text-sm text-gray-600">
              Need help? Contact support with the transaction ID above.
            </div>
          </div>
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Card, Button, call, toast } from 'frappe-ui'
import { useRouter, useRoute } from 'vue-router'
import PaymentModal from '../components/PaymentModal.vue'

const router = useRouter()
const route = useRoute()
const plans = ref([])
const currentSubscription = ref(null)
const loadingPlans = ref(false)
const loadingSubscription = ref(false)
const showUpgradeModal = ref(false)
const showPaymentModal = ref(false)
const showPaymentResultModal = ref(false)
const paymentResult = ref(null)
const selectedPlan = ref(null)

const upgradeDialogOptions = computed(() => ({
  title: 'Upgrade Subscription',
  disableOutsideClickToClose: true,
  actions: [
    {
      label: 'Proceed to Payment',
      variant: 'solid',
      onClick: () => {
        proceedToPayment()
      }
    },
    {
      label: 'Cancel',
      variant: 'outline',
      onClick: () => {
        showUpgradeModal.value = false
      }
    }
  ]
}))

onMounted(async () => {
  // Check for payment status in URL (LMS pattern)
  handlePaymentRedirect()
  
  await Promise.all([loadPlans(), loadCurrentSubscription()])
})

async function handlePaymentRedirect() {
  // Handle payment success/failure from redirect
  const paymentStatus = route.query.payment
  const transactionId = route.query.transaction
  
  if (paymentStatus && transactionId) {
    // Fetch transaction details
    try {
      const transaction = await call('frappe.client.get', {
        doctype: 'Payment Transaction',
        name: transactionId
      })
      
      paymentResult.value = {
        status: paymentStatus,
        transaction: transaction,
        transactionId: transactionId
      }
      
      showPaymentResultModal.value = true
      
      // Reload subscription if payment was successful
      if (paymentStatus === 'success') {
        setTimeout(() => {
          loadCurrentSubscription()
        }, 1000)
      }
      
    } catch (error) {
      console.error('Error fetching transaction:', error)
      paymentResult.value = {
        status: paymentStatus,
        transactionId: transactionId,
        error: 'Could not fetch transaction details'
      }
      showPaymentResultModal.value = true
    }
    
    // Clean URL
    router.replace('/subscription')
  }
}

async function loadPlans() {
  loadingPlans.value = true
  try {
    const response = await call('shaadi.shaadi.api.subscription.get_subscription_plans')
    plans.value = response || []
  } catch (error) {
    console.error('Error loading plans:', error)
    toast({
      title: 'Error',
      text: 'Failed to load subscription plans',
      icon: 'alert-circle',
      iconClasses: 'text-red-500'
    })
  } finally {
    loadingPlans.value = false
  }
}

async function loadCurrentSubscription() {
  loadingSubscription.value = true
  try {
    const profileResponse = await call('shaadi.shaadi.api.auth.get_current_member_profile')
    if (profileResponse?.name) {
      const subscription = await call('shaadi.shaadi.api.subscription.get_current_subscription', {
        profile_id: profileResponse.name
      })
      currentSubscription.value = subscription
    }
  } catch (error) {
    console.error('Error loading subscription:', error)
  } finally {
    loadingSubscription.value = false
  }
}

function isCurrentPlan(plan) {
  // Check if this plan is the user's current active subscription
  if (!currentSubscription.value) return false
  return currentSubscription.value.subscription_plan === plan.name
}

function selectPlan(plan) {
  if (plan.plan_type === 'Free') return
  
  // Prevent selecting current plan
  if (isCurrentPlan(plan)) {
    toast({
      title: 'Already Subscribed',
      text: 'You are already subscribed to this plan.',
      icon: 'info',
      iconClasses: 'text-blue-500'
    })
    return
  }
  
  selectedPlan.value = plan
  showUpgradeModal.value = true
}

function proceedToPayment() {
  // Close upgrade modal and open payment modal
  showUpgradeModal.value = false
  showPaymentModal.value = true
}

function handlePaymentComplete() {
  // Close payment modal and reload subscription
  showPaymentModal.value = false
  selectedPlan.value = null
  
  // Reload subscription data after successful payment
  setTimeout(() => {
    loadCurrentSubscription()
  }, 1000)
}

function closePaymentResultModal() {
  showPaymentResultModal.value = false
  paymentResult.value = null
}

const paymentResultDialogOptions = computed(() => {
  if (!paymentResult.value) return {}
  
  const isSuccess = paymentResult.value.status === 'success'
  
  return {
    title: isSuccess ? 'Payment Successful!' : 'Payment Failed',
    actions: [
      {
        label: 'Close',
        variant: 'solid',
        onClick: closePaymentResultModal
      }
    ]
  }
})

function formatDate(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
}
</script>
