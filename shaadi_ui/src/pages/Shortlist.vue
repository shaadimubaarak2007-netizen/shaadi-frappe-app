<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">My Shortlist</h1>
          <p class="text-gray-600 mt-1">Profiles you've saved for later</p>
        </div>
        <div class="flex items-center space-x-2">
          <span class="text-sm text-gray-600">{{ shortlistedProfiles.length }} profiles</span>
        </div>
      </div>

      <!-- Category Tabs -->
      <div class="mb-6">
        <div class="flex items-center space-x-2 border-b border-gray-200">
          <button
            v-for="category in categories"
            :key="category.value"
            @click="activeCategory = category.value"
            :class="[
              'px-4 py-3 text-sm font-medium border-b-2 transition-colors',
              activeCategory === category.value
                ? 'border-pink-600 text-pink-600'
                : 'border-transparent text-gray-600 hover:text-gray-900 hover:border-gray-300'
            ]"
          >
            {{ category.label }}
            <span class="ml-2 px-2 py-0.5 text-xs rounded-full bg-gray-100">
              {{ getCategoryCount(category.value) }}
            </span>
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card v-for="i in 6" :key="i" class="animate-pulse">
          <div class="h-48 bg-gray-200 rounded-lg mb-4"></div>
          <div class="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
          <div class="h-4 bg-gray-200 rounded w-1/2"></div>
        </Card>
      </div>

      <!-- Shortlist Grid -->
      <div v-else-if="filteredProfiles.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="item in filteredProfiles" :key="item.name" class="relative">
          <ProfileCard
            :profile="item"
            @click="viewProfile(item)"
            @sendInterest="sendInterest"
            @shortlist="() => {}"
          />
          <!-- Remove Button -->
          <button
            @click="removeFromShortlist(item.name)"
            class="absolute top-2 right-2 w-8 h-8 bg-white rounded-full shadow-lg flex items-center justify-center hover:bg-red-50 transition-colors z-10"
          >
            <FeatherIcon name="x" class="w-4 h-4 text-red-600" />
          </button>
          <!-- Category Badge -->
          <div class="absolute top-2 left-2 px-2 py-1 bg-white rounded-full shadow-sm text-xs font-medium z-10">
            {{ item.category }}
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <Card v-else class="text-center py-12">
        <div class="flex flex-col items-center">
          <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
            <FeatherIcon name="star" class="w-8 h-8 text-gray-400" />
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">No profiles in shortlist</h3>
          <p class="text-gray-600 mb-6">Start adding profiles you're interested in</p>
          <Button variant="solid" @click="$router.push('/browse')">
            <template #prefix>
              <FeatherIcon name="search" class="w-4 h-4" />
            </template>
            Browse Profiles
          </Button>
        </div>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { call, Button, Card, FeatherIcon, toast } from 'frappe-ui'
import ProfileCard from '@/components/ProfileCard.vue'

const router = useRouter()
const loading = ref(true)
const shortlistedProfiles = ref([])
const activeCategory = ref('all')

const categories = [
  { label: 'All', value: 'all' },
  { label: 'Liked', value: 'Liked' },
  { label: 'Maybe', value: 'Maybe' },
  { label: 'Favorites', value: 'Favorites' }
]

const filteredProfiles = computed(() => {
  if (activeCategory.value === 'all') return shortlistedProfiles.value
  return shortlistedProfiles.value.filter(p => p.category === activeCategory.value)
})

function getCategoryCount(category) {
  if (category === 'all') return shortlistedProfiles.value.length
  return shortlistedProfiles.value.filter(p => p.category === category).length
}

async function loadShortlist() {
  loading.value = true
  try {
    // Get current user profile first
    const userProfile = await call('shaadi.shaadi.api.auth.get_current_member_profile')
    if (!userProfile?.name) {
      throw new Error('User profile not found')
    }
    
    const response = await call('shaadi.shaadi.api.search.get_shortlisted_profiles', {
      profile_id: userProfile.name
    })
    shortlistedProfiles.value = response || []
  } catch (error) {
    console.error('Error loading shortlist:', error)
    shortlistedProfiles.value = []
  } finally {
    loading.value = false
  }
}

async function removeFromShortlist(shortlistId) {
  if (!confirm('Remove this profile from shortlist?')) return
  
  try {
    await call('shaadi.shaadi.api.search.remove_from_shortlist', {
      shortlist_id: shortlistId
    })
    await loadShortlist()
  } catch (error) {
    console.error('Error removing from shortlist:', error)
    createToast({
      title: 'Error',
      text: error.message || 'Failed to remove from shortlist',
      icon: 'x',
      iconClasses: 'text-red-600'
    })
  }
}

function viewProfile(profile) {
  // Handle both direct profile object and nested profile_data structure
  const profileId = profile.shortlisted_profile || profile.name
  router.push(`/profile/${profileId}`)
}

async function sendInterest(profile) {
  try {
    await call('shaadi.shaadi.api.matchmaking.send_interest', {
      receiver_profile: profile.name,
      message: 'I am interested in your profile'
    })
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

onMounted(() => {
  loadShortlist()
})
</script>
