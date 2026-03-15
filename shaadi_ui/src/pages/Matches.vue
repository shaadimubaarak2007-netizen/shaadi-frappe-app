<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-50 to-purple-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold bg-gradient-to-r from-pink-600 to-purple-600 bg-clip-text text-transparent">
          Discover Your Match
        </h1>
        <p class="text-gray-600 mt-2">Swipe right to like, left to pass</p>
      </div>

      <!-- Mode Toggle -->
      <div class="flex justify-center mb-8">
        <div class="bg-white rounded-full p-1 shadow-lg">
          <button
            @click="viewMode = 'swipe'"
            :class="[
              'px-6 py-2 rounded-full text-sm font-medium transition-all',
              viewMode === 'swipe'
                ? 'bg-gradient-to-r from-pink-500 to-purple-500 text-white shadow-md'
                : 'text-gray-600 hover:text-gray-900'
            ]"
          >
            <FeatherIcon name="heart" class="w-4 h-4 inline mr-2" />
            Swipe Mode
          </button>
          <button
            @click="switchToMyMatches"
            :class="[
              'px-6 py-2 rounded-full text-sm font-medium transition-all',
              viewMode === 'grid'
                ? 'bg-gradient-to-r from-pink-500 to-purple-500 text-white shadow-md'
                : 'text-gray-600 hover:text-gray-900'
            ]"
          >
            <FeatherIcon name="users" class="w-4 h-4 inline mr-2" />
            My Matches
          </button>
        </div>
      </div>

      <!-- Swipe Mode -->
      <div v-if="viewMode === 'swipe'" class="flex justify-center">
        <SwipeStack
          ref="swipeStack"
          @match="handleMatch"
          @swipe="handleSwipe"
          @empty="handleEmpty"
        />
      </div>

      <!-- My Matches Mode (Mutual Matches Only) -->
      <div v-else>
        <!-- Header -->
        <div class="mb-6 text-center">
          <h2 class="text-2xl font-bold text-gray-900">My Mutual Matches</h2>
          <p class="text-gray-600 mt-1">Profiles where both of you liked each other</p>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Card v-for="i in 6" :key="i" class="animate-pulse">
            <div class="h-48 bg-gray-200 rounded-lg mb-4"></div>
            <div class="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
            <div class="h-4 bg-gray-200 rounded w-1/2"></div>
          </Card>
        </div>

        <!-- Mutual Matches Grid -->
        <div v-else-if="mutualMatches.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <ProfileCard
            v-for="profile in mutualMatches"
            :key="profile.name"
            :profile="profile"
            @click="viewProfile(profile)"
            @sendInterest="sendInterest"
            @shortlist="addToShortlist"
          />
        </div>

        <!-- Empty State -->
        <Card v-else class="text-center py-12">
          <div class="flex flex-col items-center">
            <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
              <FeatherIcon name="heart" class="w-8 h-8 text-gray-400" />
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">No mutual matches yet</h3>
            <p class="text-gray-600 mb-6">Start swiping to find your perfect match!</p>
            <Button variant="solid" @click="viewMode = 'swipe'">
              <template #prefix>
                <FeatherIcon name="heart" class="w-4 h-4" />
              </template>
              Start Swiping
            </Button>
          </div>
        </Card>
      </div>

      <!-- Match Modal -->
      <MatchModal
        :show="showMatchModal"
        :matched-profile="matchedProfile"
        :match-score="matchScore"
        @close="closeMatchModal"
        @message="startConversation"
        @continue="continueSwipe"
      />

      <!-- Stats Bar -->
      <div v-if="viewMode === 'swipe'" class="fixed bottom-4 left-1/2 transform -translate-x-1/2">
        <div class="bg-white rounded-full px-6 py-3 shadow-lg flex items-center gap-4">
          <div class="flex items-center gap-2">
            <div class="w-3 h-3 bg-red-400 rounded-full"></div>
            <span class="text-sm text-gray-600">{{ passCount }} passed</span>
          </div>
          <div class="flex items-center gap-2">
            <div class="w-3 h-3 bg-green-400 rounded-full"></div>
            <span class="text-sm text-gray-600">{{ likeCount }} liked</span>
          </div>
          <div class="flex items-center gap-2">
            <div class="w-3 h-3 bg-pink-400 rounded-full"></div>
            <span class="text-sm text-gray-600">{{ matchCount }} matches</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { call, Button, Card, FeatherIcon, toast } from 'frappe-ui'
import ProfileCard from '@/components/ProfileCard.vue'
import SwipeStack from '@/components/SwipeStack.vue'
import MatchModal from '@/components/MatchModal.vue'

const router = useRouter()
const loading = ref(true)
const matches = ref([])
const activeTab = ref('all')
const viewMode = ref('swipe') // 'swipe' or 'grid'

// Swipe mode data
const swipeStack = ref(null)
const showMatchModal = ref(false)
const matchedProfile = ref(null)
const matchScore = ref(0)

// Statistics
const passCount = ref(0)
const likeCount = ref(0)
const matchCount = ref(0)
const mutualMatches = ref([])

async function switchToMyMatches() {
  viewMode.value = 'grid'
  await loadMutualMatches()
}

async function loadSwipeStatistics() {
  try {
    const stats = await call('shaadi.shaadi.api.matchmaking.get_swipe_statistics')
    if (stats) {
      passCount.value = stats.passed || 0
      likeCount.value = stats.liked || 0
      matchCount.value = stats.matches || 0
    }
  } catch (error) {
    console.error('Error loading swipe statistics:', error)
  }
}


async function loadMutualMatches() {
  loading.value = true
  try {
    const response = await call('shaadi.shaadi.api.matchmaking.get_mutual_matches', {
      limit: 50
    })
    mutualMatches.value = response || []
    console.log('Mutual matches loaded:', mutualMatches.value.length)
  } catch (error) {
    console.error('Error loading mutual matches:', error)
    toast.error('Failed to load mutual matches')
    mutualMatches.value = []
  } finally {
    loading.value = false
  }
}

// Swipe handlers
async function handleSwipe({ action, profile, response }) {
  if (action === 'like') {
    likeCount.value++
    toast.success(`You liked ${profile.full_name}`)
  } else {
    passCount.value++
  }
  
  // Refresh statistics after each swipe
  await loadSwipeStatistics()
}

async function handleMatch({ profile, matchData }) {
  matchCount.value++
  matchedProfile.value = profile
  matchScore.value = matchData.match_score || 0
  showMatchModal.value = true
  
  // Reload mutual matches to include the new match
  await loadMutualMatches()
  
  // Refresh statistics
  await loadSwipeStatistics()
  
  toast.success(`🎉 It's a Match! You and ${profile.full_name} liked each other!`)
}

function handleEmpty() {
  toast.info('No more profiles available for now')
}

function closeMatchModal() {
  showMatchModal.value = false
  matchedProfile.value = null
  matchScore.value = 0
}

function startConversation(profile) {
  router.push(`/messages?profile=${profile.name}`)
}

function continueSwipe() {
  // Just close modal and continue swiping
  closeMatchModal()
}

function viewProfile(profile) {
  router.push(`/profile/${profile.name}`)
}

async function sendInterest(profile) {
  try {
    await call('shaadi.shaadi.api.matchmaking.send_interest', {
      receiver_profile: profile.name,
      message: 'I am interested in your profile'
    })
    toast.success('Interest sent successfully!')
  } catch (error) {
    console.error('Error sending interest:', error)
    toast.error(error.message || 'Failed to send interest')
  }
}

async function addToShortlist(profile) {
  try {
    await call('shaadi.shaadi.api.search.add_to_shortlist', {
      shortlisted_profile_id: profile.name,
      category: 'Liked'
    })
    toast.success('Added to shortlist!')
  } catch (error) {
    console.error('Error adding to shortlist:', error)
    toast.error(error.message || 'Failed to add to shortlist')
  }
}

onMounted(() => {
  // Load swipe statistics on page load
  loadSwipeStatistics()
})
</script>
