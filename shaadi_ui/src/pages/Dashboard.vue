<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Welcome back, {{ userProfile?.full_name }}!</h1>
        <p class="text-gray-600 mt-1">Find your perfect match today</p>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <Card class="bg-gradient-to-br from-blue-500 to-blue-600 text-white">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-blue-100 text-sm">Profile Views</p>
              <p class="text-3xl font-bold mt-1">{{ stats.profile_views || 0 }}</p>
            </div>
            <div class="bg-white bg-opacity-20 p-3 rounded-lg">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
              </svg>
            </div>
          </div>
        </Card>

        <Card class="bg-gradient-to-br from-purple-500 to-purple-600 text-white">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-purple-100 text-sm">Interests Received</p>
              <p class="text-3xl font-bold mt-1">{{ stats.interests_received || 0 }}</p>
            </div>
            <div class="bg-white bg-opacity-20 p-3 rounded-lg">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
              </svg>
            </div>
          </div>
        </Card>

        <Card class="bg-gradient-to-br from-pink-500 to-pink-600 text-white">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-pink-100 text-sm">Mutual Matches</p>
              <p class="text-3xl font-bold mt-1">{{ stats.mutual_matches || 0 }}</p>
            </div>
            <div class="bg-white bg-opacity-20 p-3 rounded-lg">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
              </svg>
            </div>
          </div>
        </Card>

        <Card class="bg-gradient-to-br from-green-500 to-green-600 text-white">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-green-100 text-sm">Unread Messages</p>
              <p class="text-3xl font-bold mt-1">{{ stats.unread_messages || 0 }}</p>
            </div>
            <div class="bg-white bg-opacity-20 p-3 rounded-lg">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/>
              </svg>
            </div>
          </div>
        </Card>
      </div>

      <!-- Profile Completion -->
      <Card v-if="userProfile && userProfile.profile_completeness < 100" class="mb-8 bg-yellow-50 border-yellow-200">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Complete Your Profile</h3>
            <p class="text-gray-600 text-sm mb-3">{{ userProfile.profile_completeness }}% complete - Add more details to get better matches!</p>
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div 
                class="bg-gradient-to-r from-yellow-400 to-orange-500 h-2 rounded-full transition-all duration-500"
                :style="{ width: `${userProfile.profile_completeness}%` }"
              ></div>
            </div>
          </div>
          <Button variant="solid" theme="blue" class="ml-4" @click="$router.push('/my-profile')">
            Complete Profile
          </Button>
        </div>
      </Card>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Main Content -->
        <div class="lg:col-span-2 space-y-8">
          <!-- Top Matches -->
          <div>
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-2xl font-bold text-gray-900">Top Matches for You</h2>
              <Button variant="ghost" @click="$router.push('/matches')">
                View All →
              </Button>
            </div>
            
            <div v-if="recommendations.loading" class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card v-for="i in 4" :key="i" class="animate-pulse">
                <div class="h-48 bg-gray-200 rounded-lg mb-4"></div>
                <div class="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div class="h-4 bg-gray-200 rounded w-1/2"></div>
              </Card>
            </div>

            <div v-else-if="recommendations.data && recommendations.data.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 overflow-hidden">
              <ProfileCard 
                v-for="profile in recommendations.data.slice(0, 6)"
                :key="profile.name"
                :profile="profile"
                :interestSent="sentInterests.has(profile.name)"
                @click="viewProfile(profile)"
                @send-interest="sendInterest"
                @shortlist="addToShortlist"
                class="w-full min-w-0"
              />
            </div>

            <Card v-else class="text-center py-12">
              <p class="text-gray-500">No matches found yet. Complete your profile to get better recommendations!</p>
            </Card>
          </div>

          <!-- Recent Activity -->
          <div>
            <h2 class="text-2xl font-bold text-gray-900 mb-4">Recent Activity</h2>
            <Card>
              <div class="space-y-4">
                <div v-for="activity in recentActivity" :key="activity.id" class="flex items-start gap-4 pb-4 border-b border-gray-100 last:border-0 last:pb-0">
                  <div class="flex-shrink-0">
                    <div class="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-white">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
                      </svg>
                    </div>
                  </div>
                  <div class="flex-1">
                    <p class="text-sm text-gray-900">{{ activity.message }}</p>
                    <p class="text-xs text-gray-500 mt-1">{{ formatTime(activity.time) }}</p>
                  </div>
                </div>
              </div>
            </Card>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Quick Actions -->
          <Card>
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
            <div class="space-y-2">
              <Button 
                variant="subtle" 
                size="md"
                class="w-full !justify-start"
                @click="$router.push('/browse')"
              >
                <template #prefix>
                  <FeatherIcon name="search" class="w-4 h-4" />
                </template>
                Browse Profiles
              </Button>
              <Button 
                variant="subtle" 
                size="md"
                class="w-full !justify-start"
                @click="$router.push('/search')"
              >
                <template #prefix>
                  <FeatherIcon name="filter" class="w-4 h-4" />
                </template>
                Advanced Search
              </Button>
              <Button 
                variant="subtle" 
                size="md"
                class="w-full !justify-start"
                @click="$router.push('/messages')"
              >
                <template #prefix>
                  <FeatherIcon name="message-circle" class="w-4 h-4" />
                </template>
                Messages
              </Button>
              <Button 
                variant="subtle" 
                size="md"
                class="w-full !justify-start"
                @click="$router.push('/interests')"
              >
                <template #prefix>
                  <FeatherIcon name="heart" class="w-4 h-4" />
                </template>
                Interests
              </Button>
            </div>
          </Card>

          <!-- Subscription Info -->
          <Card v-if="userProfile" class="bg-gradient-to-br from-purple-50 to-pink-50 border-purple-200">
            <div class="text-center">
              <div class="inline-flex items-center justify-center w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full mb-3">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"/>
                </svg>
              </div>
              <h3 class="text-lg font-semibold text-gray-900 mb-1">
                {{ userProfile.subscription_plan || 'Free' }} Plan
              </h3>
              <p class="text-sm text-gray-600 mb-4">Upgrade for unlimited access</p>
              <Button variant="solid" size="md" class="w-full" @click="$router.push('/subscription')">
                <template #prefix>
                  <FeatherIcon name="zap" class="w-4 h-4" />
                </template>
                Upgrade Now
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { call, Button, Card, FeatherIcon, toast } from 'frappe-ui'
import ProfileCard from '@/components/ProfileCard.vue'

const router = useRouter()

const userProfile = ref(null)
const stats = ref({
  profile_views: 0,
  interests_received: 0,
  mutual_matches: 0,
  unread_messages: 0
})
const recommendations = ref({
  loading: false,
  data: []
})
const sentInterests = ref(new Set())

const recentActivity = ref([
  { id: 1, message: 'Your profile was viewed by 3 members', time: new Date(Date.now() - 2 * 60 * 60 * 1000) },
  { id: 2, message: 'You have 2 new match recommendations', time: new Date(Date.now() - 5 * 60 * 60 * 1000) },
  { id: 3, message: 'Someone sent you an interest', time: new Date(Date.now() - 24 * 60 * 60 * 1000) }
])

onMounted(async () => {
  await loadUserProfile()
  await loadRecommendations()
  await loadStats()
})

async function loadUserProfile() {
  try {
    const response = await call('shaadi.shaadi.api.auth.get_current_member_profile')
    userProfile.value = response
  } catch (error) {
    console.error('Error loading profile:', error)
  }
}

async function loadRecommendations() {
  if (!userProfile.value) return
  
  try {
    recommendations.value.loading = true
    const response = await call('shaadi.shaadi.api.matchmaking.get_recommendations', {
      profile_id: userProfile.value.name,
      limit: 6
    })
    recommendations.value.data = response || []
  } catch (error) {
    console.error('Error loading recommendations:', error)
    recommendations.value.data = []
  } finally {
    recommendations.value.loading = false
  }
}

async function loadStats() {
  if (!userProfile.value) return
  
  try {
    // Load various stats
    stats.value.profile_views = userProfile.value.view_count || 0
    
    // Get interests received count
    const interests = await call('shaadi.shaadi.api.matchmaking.get_received_interests', {
      profile_id: userProfile.value.name
    })
    stats.value.interests_received = interests?.filter(i => i.status === 'Pending').length || 0
    
    // Get actual mutual matches count
    const mutualMatchesCount = await call('shaadi.shaadi.api.matchmaking.get_mutual_matches_count')
    stats.value.mutual_matches = mutualMatchesCount || 0
    
    // Load sent interests to track button state
    const sent = await call('shaadi.shaadi.api.matchmaking.get_sent_interests', {
      profile_id: userProfile.value.name
    })
    sentInterests.value = new Set((sent || []).map(i => i.receiver))
  } catch (error) {
    console.error('Error loading stats:', error)
  }
}

function viewProfile(profile) {
  router.push(`/profile/${profile.name}`)
}

async function sendInterest(profile) {
  if (!userProfile.value) return
  
  try {
    await call('shaadi.shaadi.api.matchmaking.send_interest', {
      receiver_profile: profile.name,
      message: 'I am interested in your profile'
    })
    
    // Add to sent interests set
    sentInterests.value.add(profile.name)
    
    // Reload stats to update counts
    await loadStats()
    
    createToast({
      title: 'Success',
      text: 'Interest sent successfully!',
      icon: 'check',
      iconClasses: 'text-green-600'
    })
  } catch (error) {
    console.error('Error sending interest:', error)
    createToast({
      title: 'Error',
      text: error.message || 'Failed to send interest',
      icon: 'x',
      iconClasses: 'text-red-600'
    })
  }
}

async function addToShortlist(profile) {
  if (!userProfile.value) return
  
  try {
    await call('shaadi.shaadi.api.search.add_to_shortlist', {
      profile_id: userProfile.value.name,
      shortlisted_profile_id: profile.name,
      category: 'Liked'
    })
    createToast({
      title: 'Success',
      text: 'Added to shortlist!',
      icon: 'star',
      iconClasses: 'text-yellow-600'
    })
  } catch (error) {
    console.error('Error adding to shortlist:', error)
    createToast({
      title: 'Error',
      text: error.message || 'Failed to add to shortlist',
      icon: 'x',
      iconClasses: 'text-red-600'
    })
  }
}

function formatTime(date) {
  const now = new Date()
  const diff = now - new Date(date)
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(hours / 24)
  
  if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`
  if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`
  return 'Just now'
}
</script>
