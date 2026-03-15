<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Back Button -->
      <Button variant="ghost" class="mb-4" @click="$router.back()">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
        Back
      </Button>

      <div v-if="loading" class="animate-pulse">
        <div class="h-64 bg-gray-200 rounded-lg mb-6"></div>
        <div class="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
        <div class="h-4 bg-gray-200 rounded w-1/2"></div>
      </div>

      <div v-else-if="profile" class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Main Content -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Photo Gallery -->
          <Card>
            <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
              <div v-if="profile.profile_photo" class="col-span-2 md:col-span-3">
                <img :src="profile.profile_photo" :alt="profile.full_name" class="w-full h-96 object-cover rounded-lg" />
              </div>
              <div v-else class="col-span-2 md:col-span-3 h-96 bg-gradient-to-br from-purple-100 to-pink-100 rounded-lg flex items-center justify-center">
                <span class="text-9xl font-bold text-purple-600">{{ getInitials(profile.full_name) }}</span>
              </div>
              <div v-for="(photo, index) in profile.profile_photos" :key="index" class="h-32 bg-gray-200 rounded-lg overflow-hidden">
                <img v-if="photo.photo" :src="photo.photo" :alt="`Photo ${index + 1}`" class="w-full h-full object-cover" />
              </div>
            </div>
          </Card>

          <!-- About Section -->
          <Card>
            <h2 class="text-2xl font-bold text-gray-900 mb-4">About {{ profile.full_name }}</h2>
            <div class="flex items-center gap-2 mb-4">
              <MatchPercentage v-if="profile.match_score" :score="profile.match_score" size="md" />
              <Badge v-if="profile.verified" variant="success">
                <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                </svg>
                Verified
              </Badge>
            </div>
            <p v-if="profile.profile_bio" class="text-gray-700 leading-relaxed">{{ profile.profile_bio }}</p>
            <p v-else class="text-gray-500 italic">No bio available</p>
          </Card>

          <!-- Basic Details -->
          <Card>
            <h3 class="text-xl font-semibold text-gray-900 mb-4">Basic Details</h3>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <p class="text-sm text-gray-500">Age</p>
                <p class="font-medium">{{ profile.age }} years</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">Height</p>
                <p class="font-medium">{{ formatHeight(profile.height_cm) }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">Religion</p>
                <p class="font-medium">{{ profile.religion || 'Not specified' }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">Caste</p>
                <p class="font-medium">{{ profile.caste || 'Not specified' }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">Mother Tongue</p>
                <p class="font-medium">{{ profile.mother_tongue || 'Not specified' }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">Marital Status</p>
                <p class="font-medium">{{ profile.marital_status || 'Not specified' }}</p>
              </div>
            </div>
          </Card>

          <!-- Education & Career -->
          <Card>
            <h3 class="text-xl font-semibold text-gray-900 mb-4">Education & Career</h3>
            <div class="space-y-4">
              <div>
                <p class="text-sm text-gray-500">Education</p>
                <p class="font-medium">{{ profile.education || 'Not specified' }}</p>
                <p v-if="profile.education_detail" class="text-sm text-gray-600">{{ profile.education_detail }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">Occupation</p>
                <p class="font-medium">{{ profile.occupation || 'Not specified' }}</p>
                <p v-if="profile.occupation_detail" class="text-sm text-gray-600">{{ profile.occupation_detail }}</p>
              </div>
              <div v-if="profile.annual_income_band">
                <p class="text-sm text-gray-500">Annual Income</p>
                <p class="font-medium">{{ profile.annual_income_band }}</p>
              </div>
            </div>
          </Card>

          <!-- Lifestyle -->
          <Card>
            <h3 class="text-xl font-semibold text-gray-900 mb-4">Lifestyle</h3>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <p class="text-sm text-gray-500">Diet</p>
                <p class="font-medium">{{ profile.diet || 'Not specified' }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">Smoking</p>
                <p class="font-medium">{{ profile.smoking || 'Not specified' }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">Drinking</p>
                <p class="font-medium">{{ profile.drinking || 'Not specified' }}</p>
              </div>
            </div>
          </Card>

          <!-- Location -->
          <Card>
            <h3 class="text-xl font-semibold text-gray-900 mb-4">Location</h3>
            <div class="flex items-start gap-2">
              <svg class="w-5 h-5 text-gray-400 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
              <div>
                <p class="font-medium">{{ profile.city }}, {{ profile.state }}</p>
                <p class="text-sm text-gray-600">{{ profile.country_of_residence }}</p>
              </div>
            </div>
          </Card>
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Action Buttons -->
          <Card>
            <div class="space-y-2">
              <!-- Dynamic Interest Button -->
              <Button 
                v-if="canSendInterest()"
                variant="solid" 
                size="md" 
                class="w-full" 
                @click="sendInterest"
              >
                <template #prefix>
                  <FeatherIcon name="heart" class="w-4 h-4" />
                </template>
                {{ getInterestButtonText() }}
              </Button>
              <Button 
                v-else-if="canWithdrawInterest()"
                variant="outline" 
                theme="red"
                size="md" 
                class="w-full" 
                @click="withdrawInterest"
              >
                <template #prefix>
                  <FeatherIcon name="x-circle" class="w-4 h-4" />
                </template>
                Withdraw Interest
              </Button>
              <Button 
                v-else
                variant="ghost" 
                size="md" 
                class="w-full" 
                :disabled="true"
              >
                <template #prefix>
                  <FeatherIcon name="heart" class="w-4 h-4" />
                </template>
                {{ getInterestButtonText() }}
              </Button>
              
              <!-- Dynamic Shortlist Button -->
              <Button 
                v-if="!isShortlisted() && canShortlist()"
                variant="outline" 
                size="md" 
                class="w-full" 
                @click="addToShortlist"
              >
                <template #prefix>
                  <FeatherIcon name="star" class="w-4 h-4" />
                </template>
                {{ getShortlistButtonText() }}
              </Button>
              <Button 
                v-else-if="isShortlisted()"
                variant="outline" 
                theme="red"
                size="md" 
                class="w-full" 
                @click="removeFromShortlist"
              >
                <template #prefix>
                  <FeatherIcon name="minus" class="w-4 h-4" />
                </template>
                {{ getShortlistButtonText() }}
              </Button>
              <Button 
                v-else
                variant="ghost" 
                size="md" 
                class="w-full" 
                :disabled="true"
              >
                <template #prefix>
                  <FeatherIcon name="star" class="w-4 h-4" />
                </template>
                {{ getShortlistButtonText() }}
              </Button>
              <Button variant="subtle" size="md" class="w-full" @click="sendMessage">
                <template #prefix>
                  <FeatherIcon name="message-circle" class="w-4 h-4" />
                </template>
                Send Message
              </Button>
              <Button variant="ghost" size="md" class="w-full text-red-600 hover:bg-red-50" @click="reportProfile">
                <template #prefix>
                  <FeatherIcon name="alert-triangle" class="w-4 h-4" />
                </template>
                Report Profile
              </Button>
            </div>
          </Card>

          <!-- Profile Stats -->
          <Card>
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Profile Stats</h3>
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Profile Views</span>
                <span class="font-semibold">{{ profile.view_count || 0 }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Profile Completeness</span>
                <span class="font-semibold">{{ profile.profile_completeness || 0 }}%</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Last Active</span>
                <span class="text-sm">{{ formatDate(profile.last_active) }}</span>
              </div>
            </div>
          </Card>

          <!-- Contact Info (Premium) -->
          <Card v-if="canViewContact" class="bg-green-50 border-green-200">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Contact Information</h3>
            <div class="space-y-3">
              <div v-if="profile.phone">
                <p class="text-sm text-gray-600">Phone</p>
                <p class="font-medium">{{ profile.phone }}</p>
              </div>
              <div v-if="profile.email">
                <p class="text-sm text-gray-600">Email</p>
                <p class="font-medium">{{ profile.email }}</p>
              </div>
              <div v-if="profile.whatsapp_number">
                <p class="text-sm text-gray-600">WhatsApp</p>
                <p class="font-medium">{{ profile.whatsapp_number }}</p>
              </div>
            </div>
          </Card>
          <Card v-else class="bg-yellow-50 border-yellow-200">
            <div class="text-center">
              <svg class="w-12 h-12 mx-auto text-yellow-600 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
              <h3 class="text-lg font-semibold text-gray-900 mb-2">Contact Hidden</h3>
              <p class="text-sm text-gray-600 mb-4">Upgrade to premium to view contact details</p>
              <Button variant="solid" size="sm" @click="$router.push('/subscription')">
                <template #prefix>
                  <FeatherIcon name="zap" class="w-4 h-4" />
                </template>
                Upgrade Now
              </Button>
            </div>
          </Card>
        </div>
      </div>

      <div v-else class="text-center py-12">
        <p class="text-gray-500">Profile not found</p>
      </div>
    </div>

    <!-- Subscription Required Dialog -->
    <Dialog 
      v-model="showUpgradeDialog"
      :options="dialogOptions"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { call, Button, Card, FeatherIcon, Dialog, toast } from 'frappe-ui'
import MatchPercentage from '@/components/MatchPercentage.vue'

const route = useRoute()
const router = useRouter()

const profile = ref(null)
const loading = ref(true)
const currentUserProfile = ref(null)
const profileStatus = ref(null)
const showUpgradeDialog = ref(false)

const dialogOptions = computed(() => ({
  title: 'Subscription Required',
  message: 'To send messages and connect with other members, you need an active subscription plan. Upgrade now to unlock unlimited messaging and connect with potential matches!',
  disableOutsideClickToClose: true,
  actions: [
    {
      label: 'Upgrade Now',
      variant: 'solid',
      onClick: () => {
        router.push('/subscription')
        showUpgradeDialog.value = false
      }
    },
    {
      label: 'Cancel',
      variant: 'outline',
      onClick: () => {
        showUpgradeDialog.value = false
      }
    }
  ]
}))

const canViewContact = computed(() => {
  // Check if user has premium subscription or interest accepted
  return currentUserProfile.value?.plan !== 'Free'
})

onMounted(async () => {
  await loadProfile()
  await loadCurrentUser()
  await loadProfileStatus()
  await trackView()
})

async function loadCurrentUser() {
  try {
    currentUserProfile.value = await call('shaadi.shaadi.api.auth.get_current_member_profile')
  } catch (error) {
    console.error('Error loading current user:', error)
  }
}

async function loadProfile() {
  try {
    loading.value = true
    profile.value = await call('frappe.client.get', {
      doctype: 'Member Profile',
      name: route.params.id
    })
  } catch (error) {
    console.error('Error loading profile:', error)
  } finally {
    loading.value = false
  }
}

async function loadProfileStatus() {
  if (!profile.value) return
  
  try {
    const status = await call('shaadi.shaadi.api.matchmaking.get_profile_interaction_status', {
      profile_id: profile.value.name
    })
    profileStatus.value = status
  } catch (error) {
    console.error('Error loading profile status:', error)
    profileStatus.value = {
      can_send_interest: true,
      can_shortlist: true,
      sent_interest: null,
      shortlist_status: null
    }
  }
}

async function trackView() {
  if (!currentUserProfile.value || !profile.value) return
  
  try {
    await call('frappe.client.insert', {
      doc: {
        doctype: 'Profile View',
        viewer: currentUserProfile.value.name,
        viewed_profile: profile.value.name
      }
    })
  } catch (error) {
    console.error('Error tracking view:', error)
  }
}

async function sendInterest() {
  if (!currentUserProfile.value) return
  
  try {
    const response = await call('shaadi.shaadi.api.matchmaking.send_interest', {
      sender_profile: currentUserProfile.value.name,
      receiver_profile: profile.value.name,
      message: 'I am interested in your profile'
    })
    
    // Update local status
    if (response.interaction_status) {
      profileStatus.value = response.interaction_status
    }
    
    toast.success('Interest sent successfully!')
  } catch (error) {
    console.error('Error sending interest:', error)
    toast.error(error.message || 'Failed to send interest')
  }
}

async function sendMessage() {
  // Check subscription before allowing messaging
  try {
    console.log('Checking subscription for messaging...')
    const profileResponse = await call('shaadi.shaadi.api.auth.get_current_member_profile')
    console.log('Profile response:', profileResponse)
    
    if (profileResponse?.name) {
      const response = await call('shaadi.shaadi.api.subscription.check_feature_access', {
        profile_id: profileResponse.name,
        feature: 'send_message'
      })
      console.log('Subscription check response:', response)
      
      if (response?.has_access) {
        console.log('Access granted, navigating to messages')
        router.push(`/messages?profile=${profile.value.name}`)
      } else {
        console.log('Access denied, showing upgrade dialog')
        showUpgradeDialog.value = true
      }
    } else {
      console.log('No profile found')
      toast.error('Unable to verify your profile. Please try again.')
    }
  } catch (error) {
    console.error('Error checking subscription:', error)
    toast.error('Unable to verify subscription. Please try again.')
  }
}

async function addToShortlist() {
  if (!currentUserProfile.value) return
  
  try {
    const response = await call('shaadi.shaadi.api.search.add_to_shortlist', {
      profile_id: currentUserProfile.value.name,
      shortlisted_profile_id: profile.value.name,
      category: 'Liked'
    })
    
    // Update local status
    if (response.interaction_status) {
      profileStatus.value = response.interaction_status
    }
    
    toast.success('Added to shortlist!')
  } catch (error) {
    console.error('Error adding to shortlist:', error)
    toast.error(error.message || 'Failed to add to shortlist')
  }
}

async function removeFromShortlist() {
  if (!currentUserProfile.value) return
  
  try {
    await call('shaadi.shaadi.api.search.remove_from_shortlist', {
      profile_id: currentUserProfile.value.name,
      shortlisted_profile_id: profile.value.name
    })
    
    // Update local status
    await loadProfileStatus()
    
    toast.success('Removed from shortlist!')
  } catch (error) {
    console.error('Error removing from shortlist:', error)
    toast.error(error.message || 'Failed to remove from shortlist')
  }
}

async function withdrawInterest() {
  if (!profileStatus.value?.sent_interest?.name) {
    toast.error('No interest found to withdraw')
    return
  }
  
  try {
    await call('shaadi.shaadi.api.matchmaking.withdraw_interest', {
      match_request_id: profileStatus.value.sent_interest.name
    })
    
    // Update local status
    await loadProfileStatus()
    
    toast.success('Interest withdrawn successfully!')
  } catch (error) {
    console.error('Error withdrawing interest:', error)
    toast.error(error.message || 'Failed to withdraw interest')
  }
}

function getInterestButtonText() {
  if (!profileStatus.value) return 'Send Interest'
  
  if (profileStatus.value.sent_interest) {
    switch (profileStatus.value.sent_interest.status) {
      case 'Pending':
        return 'Interest Sent'
      case 'Accepted':
        return 'Interest Accepted'
      case 'Declined':
        return 'Interest Declined'
      case 'Withdrawn':
        return 'Send Interest'
      default:
        return 'Send Interest'
    }
  }
  
  return profileStatus.value.can_send_interest ? 'Send Interest' : 'Cannot Send'
}

function getShortlistButtonText() {
  if (!profileStatus.value) return 'Add to Shortlist'
  
  if (profileStatus.value.shortlist_status) {
    return 'Remove from Shortlist'
  }
  
  return profileStatus.value.can_shortlist ? 'Add to Shortlist' : 'Cannot Shortlist'
}

function canSendInterest() {
  return profileStatus.value?.can_send_interest || false
}

function canWithdrawInterest() {
  return profileStatus.value?.sent_interest?.status === 'Pending'
}

function canShortlist() {
  return profileStatus.value?.can_shortlist || false
}

function isShortlisted() {
  return !!profileStatus.value?.shortlist_status
}

async function reportProfile() {
  const reason = prompt('Please specify the reason for reporting this profile:')
  if (!reason) return
  
  try {
    await call('frappe.client.insert', {
      doc: {
        doctype: 'Report Abuse',
        reporter: currentUserProfile.value.name,
        reported_profile: profile.value.name,
        reason: 'Other',
        description: reason
      }
    })
    toast.success('Report submitted. Our team will review it.')
  } catch (error) {
    console.error('Error reporting profile:', error)
    toast.error('Failed to submit report')
  }
}

function getInitials(name) {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

function formatHeight(cm) {
  if (!cm) return 'Not specified'
  const feet = Math.floor(cm / 30.48)
  const inches = Math.round((cm % 30.48) / 2.54)
  return `${feet}'${inches}" (${cm} cm)`
}

function formatDate(date) {
  if (!date) return 'Never'
  const d = new Date(date)
  const now = new Date()
  const diff = now - d
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) return 'Today'
  if (days === 1) return 'Yesterday'
  if (days < 7) return `${days} days ago`
  if (days < 30) return `${Math.floor(days / 7)} weeks ago`
  return d.toLocaleDateString()
}
</script>
