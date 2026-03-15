<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Browse Profiles</h1>
        <p class="text-gray-600 mt-1">Discover your perfect match</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <!-- Filters Sidebar -->
        <div class="lg:col-span-1">
          <FilterPanel v-model="filters" @apply="applyFilters" />
        </div>

        <!-- Profiles Grid -->
        <div class="lg:col-span-3">
          <!-- View Toggle & Sort -->
          <div class="flex items-center justify-between mb-6">
            <div class="flex items-center gap-2">
              <Button 
                :variant="viewMode === 'grid' ? 'solid' : 'subtle'"
                size="sm"
                @click="viewMode = 'grid'"
              >
                <FeatherIcon name="grid" class="w-4 h-4" />
              </Button>
              <Button 
                :variant="viewMode === 'list' ? 'solid' : 'subtle'"
                size="sm"
                @click="viewMode = 'list'"
              >
                <FeatherIcon name="list" class="w-4 h-4" />
              </Button>
            </div>

            <div class="flex items-center gap-2">
              <span class="text-sm text-gray-600">Sort by:</span>
              <FormControl
                type="select"
                v-model="sortBy"
                @change="loadProfiles"
                :options="[
                  { label: 'Best Match', value: 'match_score' },
                  { label: 'Recently Active', value: 'last_active' },
                  { label: 'Age', value: 'age' },
                  { label: 'Newest First', value: 'created' }
                ]"
                size="sm"
              />
            </div>
          </div>

          <!-- Loading State -->
          <div v-if="loading" :class="viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6' : 'space-y-4'">
            <Card v-for="i in 6" :key="i" class="animate-pulse">
              <div class="h-48 bg-gray-200 rounded-lg mb-4"></div>
              <div class="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
              <div class="h-4 bg-gray-200 rounded w-1/2"></div>
            </Card>
          </div>

          <!-- Profiles Grid View -->
          <div v-else-if="profiles.length > 0 && viewMode === 'grid'" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
            <ProfileCard 
              v-for="profile in profiles" 
              :key="profile.name"
              :profile="profile"
              @click="viewProfile(profile)"
              @send-interest="sendInterest(profile)"
              @shortlist="addToShortlist(profile)"
            />
          </div>

          <!-- Profiles List View -->
          <div v-else-if="profiles.length > 0 && viewMode === 'list'" class="space-y-4">
            <Card 
              v-for="profile in profiles" 
              :key="profile.name"
              class="hover:shadow-lg transition-shadow cursor-pointer"
              @click="viewProfile(profile)"
            >
              <div class="flex gap-6">
                <div class="flex-shrink-0 relative">
                  <img 
                    v-if="profile.profile_photo" 
                    :src="profile.profile_photo" 
                    :alt="profile.full_name"
                    class="w-32 h-32 object-cover rounded-lg"
                  />
                  <div v-else class="w-32 h-32 bg-gradient-to-br from-purple-100 to-pink-100 rounded-lg flex items-center justify-center">
                    <span class="text-3xl font-bold text-purple-600">{{ getInitials(profile.full_name) }}</span>
                  </div>
                  <!-- Online Status Indicator -->
                  <div v-if="profile.is_online" class="absolute -bottom-1 -right-1 w-6 h-6 bg-green-500 border-3 border-white rounded-full flex items-center justify-center">
                    <div class="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                  </div>
                </div>
                <div class="flex-1">
                  <div class="flex items-start justify-between">
                    <div>
                      <div class="flex items-center gap-2 mb-1">
                        <h3 class="text-xl font-semibold text-gray-900">{{ profile.full_name }}</h3>
                        <span v-if="profile.is_online" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          <div class="w-2 h-2 bg-green-400 rounded-full mr-1"></div>
                          Online
                        </span>
                      </div>
                      <div class="text-sm text-gray-600 mt-1 space-y-1">
                        <div>{{ profile.age }} years • {{ formatHeight(profile.height_cm) }}</div>
                        <div>{{ profile.education }}</div>
                        <div>{{ profile.occupation }}</div>
                        <div class="flex items-center gap-1">
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                          </svg>
                          {{ profile.city }}, {{ profile.state }}
                        </div>
                        <div v-if="!profile.is_online" class="text-xs text-gray-400">
                          {{ profile.status_text || 'Offline' }}
                        </div>
                      </div>
                    </div>
                    <MatchPercentage v-if="profile.match_score" :score="profile.match_score" size="sm" />
                  </div>
                  <div class="mt-4 flex gap-2">
                    <!-- Dynamic Interest Button -->
                    <Button 
                      v-if="canSendInterest(profile)"
                      variant="solid" 
                      theme="blue" 
                      @click.stop="sendInterest(profile)"
                    >
                      {{ getInterestButtonText(profile) }}
                    </Button>
                    <Button 
                      v-else-if="canWithdrawInterest(profile)"
                      variant="outline" 
                      theme="red" 
                      @click.stop="withdrawInterest(profile)"
                    >
                      Withdraw Interest
                    </Button>
                    <Button 
                      v-else
                      variant="ghost" 
                      :disabled="true"
                    >
                      {{ getInterestButtonText(profile) }}
                    </Button>
                    
                    <!-- Dynamic Shortlist Button -->
                    <Button 
                      v-if="!isShortlisted(profile) && canShortlist(profile)"
                      variant="outline" 
                      @click.stop="addToShortlist(profile)"
                    >
                      {{ getShortlistButtonText(profile) }}
                    </Button>
                    <Button 
                      v-else-if="isShortlisted(profile)"
                      variant="outline" 
                      theme="red" 
                      @click.stop="removeFromShortlist(profile)"
                    >
                      {{ getShortlistButtonText(profile) }}
                    </Button>
                    <Button 
                      v-else
                      variant="ghost" 
                      :disabled="true"
                    >
                      {{ getShortlistButtonText(profile) }}
                    </Button>
                  </div>
                </div>
              </div>
            </Card>
          </div>

          <!-- Empty State -->
          <Card v-else class="text-center py-12">
            <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
            <p class="text-gray-500 text-lg">No profiles found</p>
            <p class="text-gray-400 text-sm mt-1">Try adjusting your filters</p>
          </Card>

          <!-- Load More -->
          <div v-if="profiles.length > 0 && hasMore" class="mt-8 text-center">
            <Button variant="outline" @click="loadMore" :loading="loadingMore">
              Load More Profiles
            </Button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { call, Button, Card, FormControl, FeatherIcon, toast } from 'frappe-ui'
import ProfileCard from '@/components/ProfileCard.vue'
import FilterPanel from '@/components/FilterPanel.vue'
import MatchPercentage from '@/components/MatchPercentage.vue'
import { getSocket } from '@/socket'

const router = useRouter()

const viewMode = ref('grid')
const sortBy = ref('match_score')
const filters = ref({})
const profiles = ref([])
const loading = ref(true)
const loadingMore = ref(false)
const hasMore = ref(true)
const offset = ref(0)
const limit = 12
const profileStatuses = ref({})
const socket = getSocket()

onMounted(() => {
  loadProfiles()
  setupSocketListeners()
})

onUnmounted(() => {
  cleanupSocketListeners()
})

function setupSocketListeners() {
  if (socket) {
    socket.on('interest_sent', handleInterestUpdate)
    socket.on('profile_shortlisted', handleShortlistUpdate)
    socket.on('interest_response', handleInterestResponse)
  }
}

function cleanupSocketListeners() {
  if (socket) {
    socket.off('interest_sent', handleInterestUpdate)
    socket.off('profile_shortlisted', handleShortlistUpdate)
    socket.off('interest_response', handleInterestResponse)
  }
}

function handleInterestUpdate(data) {
  // Update status for affected profiles
  if (profileStatuses.value[data.receiver]) {
    loadProfileStatus(data.receiver)
  }
  if (profileStatuses.value[data.sender]) {
    loadProfileStatus(data.sender)
  }
}

function handleShortlistUpdate(data) {
  // Update status for shortlisted profile
  if (profileStatuses.value[data.shortlisted_profile]) {
    loadProfileStatus(data.shortlisted_profile)
  }
}

function handleInterestResponse(data) {
  // Update status when interest is accepted/declined
  if (profileStatuses.value[data.sender]) {
    loadProfileStatus(data.sender)
  }
  if (profileStatuses.value[data.receiver]) {
    loadProfileStatus(data.receiver)
  }
}

async function loadProfileStatus(profileId) {
  try {
    const status = await call('shaadi.shaadi.api.matchmaking.get_profile_interaction_status', {
      profile_id: profileId
    })
    profileStatuses.value[profileId] = status
  } catch (error) {
    console.error(`Error loading status for profile ${profileId}:`, error)
  }
}

async function loadProfiles() {
  try {
    loading.value = true
    offset.value = 0
    
    const response = await call('shaadi.shaadi.api.search.search_profiles', {
      filters: filters.value,
      limit: limit,
      offset: 0
    })
    
    profiles.value = response || []
    hasMore.value = response && response.length === limit
    
    // Load interaction status for each profile
    await loadProfileStatuses(profiles.value)
  } catch (error) {
    console.error('Error loading profiles:', error)
    profiles.value = []
  } finally {
    loading.value = false
  }
}

async function loadProfileStatuses(profileList) {
  try {
    const statusPromises = profileList.map(async (profile) => {
      try {
        const status = await call('shaadi.shaadi.api.matchmaking.get_profile_interaction_status', {
          profile_id: profile.name
        })
        profileStatuses.value[profile.name] = status
      } catch (error) {
        console.error(`Error loading status for profile ${profile.name}:`, error)
        profileStatuses.value[profile.name] = {
          can_send_interest: true,
          can_shortlist: true,
          sent_interest: null,
          shortlist_status: null
        }
      }
    })
    
    await Promise.all(statusPromises)
  } catch (error) {
    console.error('Error loading profile statuses:', error)
  }
}

async function loadMore() {
  if (!hasMore.value || loadingMore.value) return
  
  try {
    loadingMore.value = true
    offset.value += limit
    
    const response = await call('shaadi.shaadi.api.search.search_profiles', {
      filters: filters.value,
      limit: limit,
      offset: offset.value
    })
    
    if (response && response.length > 0) {
      profiles.value = [...profiles.value, ...response]
      hasMore.value = response.length === limit
      
      // Load interaction status for new profiles
      await loadProfileStatuses(response)
    } else {
      hasMore.value = false
    }
  } catch (error) {
    console.error('Error loading more profiles:', error)
    toast.error('Failed to load more profiles')
  } finally {
    loadingMore.value = false
  }
}

function applyFilters() {
  loadProfiles()
}

function viewProfile(profile) {
  router.push(`/profile/${profile.name}`)
}

async function sendInterest(profile) {
  try {
    const userProfile = await call('shaadi.shaadi.api.auth.get_current_member_profile')
    const response = await call('shaadi.shaadi.api.matchmaking.send_interest', {
      sender_profile: userProfile.name,
      receiver_profile: profile.name,
      message: 'I am interested in your profile'
    })
    
    // Update local status
    if (response.interaction_status) {
      profileStatuses.value[profile.name] = response.interaction_status
    }
    
    toast.success('Interest sent successfully!')
  } catch (error) {
    console.error('Error sending interest:', error)
    toast.error(error.message || 'Failed to send interest')
  }
}

async function addToShortlist(profile) {
  try {
    const userProfile = await call('shaadi.shaadi.api.auth.get_current_member_profile')
    const response = await call('shaadi.shaadi.api.search.add_to_shortlist', {
      profile_id: userProfile.name,
      shortlisted_profile_id: profile.name,
      category: 'Liked'
    })
    
    // Update local status
    if (response.interaction_status) {
      profileStatuses.value[profile.name] = response.interaction_status
    }
    
    toast.success('Added to shortlist!')
  } catch (error) {
    console.error('Error adding to shortlist:', error)
    toast.error(error.message || 'Failed to add to shortlist')
  }
}

async function removeFromShortlist(profile) {
  try {
    const userProfile = await call('shaadi.shaadi.api.auth.get_current_member_profile')
    await call('shaadi.shaadi.api.search.remove_from_shortlist', {
      profile_id: userProfile.name,
      shortlisted_profile_id: profile.name
    })
    
    // Update local status
    const updatedStatus = await call('shaadi.shaadi.api.matchmaking.get_profile_interaction_status', {
      profile_id: profile.name
    })
    profileStatuses.value[profile.name] = updatedStatus
    
    toast.success('Removed from shortlist!')
  } catch (error) {
    console.error('Error removing from shortlist:', error)
    toast.error(error.message || 'Failed to remove from shortlist')
  }
}

async function withdrawInterest(profile) {
  try {
    const status = profileStatuses.value[profile.name]
    if (!status?.sent_interest?.name) {
      toast.error('No interest found to withdraw')
      return
    }
    
    await call('shaadi.shaadi.api.matchmaking.withdraw_interest', {
      match_request_id: status.sent_interest.name
    })
    
    // Update local status
    const updatedStatus = await call('shaadi.shaadi.api.matchmaking.get_profile_interaction_status', {
      profile_id: profile.name
    })
    profileStatuses.value[profile.name] = updatedStatus
    
    toast.success('Interest withdrawn successfully!')
  } catch (error) {
    console.error('Error withdrawing interest:', error)
    toast.error(error.message || 'Failed to withdraw interest')
  }
}

function getInterestButtonText(profile) {
  const status = profileStatuses.value[profile.name]
  if (!status) return 'Send Interest'
  
  if (status.sent_interest) {
    switch (status.sent_interest.status) {
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
  
  return status.can_send_interest ? 'Send Interest' : 'Cannot Send'
}

function getShortlistButtonText(profile) {
  const status = profileStatuses.value[profile.name]
  if (!status) return 'Shortlist'
  
  if (status.shortlist_status) {
    return 'Remove from Shortlist'
  }
  
  return status.can_shortlist ? 'Add to Shortlist' : 'Cannot Shortlist'
}

function canSendInterest(profile) {
  const status = profileStatuses.value[profile.name]
  return status?.can_send_interest || false
}

function canWithdrawInterest(profile) {
  const status = profileStatuses.value[profile.name]
  return status?.sent_interest?.status === 'Pending'
}

function canShortlist(profile) {
  const status = profileStatuses.value[profile.name]
  return status?.can_shortlist || false
}

function isShortlisted(profile) {
  const status = profileStatuses.value[profile.name]
  return !!status?.shortlist_status
}

function getInitials(name) {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

function formatHeight(cm) {
  if (!cm) return ''
  const feet = Math.floor(cm / 30.48)
  const inches = Math.round((cm % 30.48) / 2.54)
  return `${feet}'${inches}"`
}
</script>
