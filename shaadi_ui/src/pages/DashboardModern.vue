<template>
  <DashboardLayout @open-search="openSearch">
    <!-- Navbar -->
    <template #navbar>
      <div class="flex items-center justify-between h-16 px-6">
        <div class="flex items-center gap-4">
          <h1 class="text-xl font-semibold text-highlighted">Dashboard</h1>
        </div>
        <div class="flex items-center gap-3">
          <Button
            icon="bell"
            variant="ghost"
            class="relative"
            @click="openNotifications"
          >
            <span v-if="stats.unread_messages > 0" class="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full"></span>
          </Button>
          <Button
            icon="plus"
            label="Quick Action"
            variant="solid"
            class="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700"
          />
        </div>
      </div>
    </template>

    <!-- Toolbar -->
    <template #toolbar>
      <div class="flex items-center justify-between px-6 py-3">
        <div class="flex items-center gap-3">
          <p class="text-sm text-muted">
            Welcome back, <span class="font-semibold text-highlighted">{{ userName }}</span>!
          </p>
        </div>
        <div class="flex items-center gap-2">
          <Button icon="refresh-cw" variant="ghost" size="sm" @click="refreshData" :loading="refreshing">
            Refresh
          </Button>
        </div>
      </div>
    </template>

    <!-- Main Content -->
    <div class="space-y-6">
      <!-- Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard
          title="Profile Views"
          :value="stats.profile_views"
          icon="eye"
          :variation="12.5"
          color="blue"
          @click="$router.push('/analytics')"
        />
        <StatsCard
          title="Matches"
          :value="stats.mutual_matches"
          icon="users"
          :variation="8.3"
          color="green"
          @click="$router.push('/matches')"
        />
        <StatsCard
          title="Interests Sent"
          :value="stats.interests_sent"
          icon="heart"
          :variation="-5.2"
          color="pink"
          @click="$router.push('/interests')"
        />
        <StatsCard
          title="Messages"
          :value="stats.unread_messages"
          icon="message-circle"
          :variation="15.7"
          color="purple"
          @click="$router.push('/messages')"
        />
      </div>

      <!-- Profile Completion Alert -->
      <div
        v-if="userProfile && userProfile.profile_completeness < 100"
        class="bg-gradient-to-r from-yellow-50 to-orange-50 border border-yellow-200 rounded-lg p-6"
      >
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-2">
              <FeatherIcon name="alert-circle" class="w-5 h-5 text-yellow-600" />
              <h3 class="text-lg font-semibold text-gray-900">Complete Your Profile</h3>
            </div>
            <p class="text-sm text-gray-600 mb-3">
              Your profile is {{ userProfile.profile_completeness }}% complete. Add more details to get better matches!
            </p>
            <div class="w-full bg-gray-200 rounded-full h-2 mb-3">
              <div
                class="bg-gradient-to-r from-yellow-400 to-orange-500 h-2 rounded-full transition-all duration-500"
                :style="{ width: `${userProfile.profile_completeness}%` }"
              ></div>
            </div>
          </div>
          <Button
            label="Complete Now"
            variant="solid"
            class="ml-4 bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-600 hover:to-orange-600"
            @click="$router.push('/my-profile')"
          />
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Left Column - Top Matches -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Top Matches -->
          <div class="bg-white rounded-lg border border-default p-6">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-xl font-semibold text-highlighted">Top Matches for You</h2>
              <Button
                label="View All"
                variant="ghost"
                icon-right="arrow-right"
                @click="$router.push('/matches')"
              />
            </div>

            <!-- Loading State -->
            <div v-if="recommendations.loading" class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div v-for="i in 4" :key="i" class="animate-pulse">
                <div class="h-48 bg-gray-200 rounded-lg mb-3"></div>
                <div class="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div class="h-4 bg-gray-200 rounded w-1/2"></div>
              </div>
            </div>

            <!-- Matches Grid -->
            <div
              v-else-if="recommendations.data && recommendations.data.length > 0"
              class="grid grid-cols-1 md:grid-cols-2 gap-4"
            >
              <ProfileCard
                v-for="profile in recommendations.data.slice(0, 4)"
                :key="profile.name"
                :profile="profile"
                :interestSent="sentInterests.has(profile.name)"
                @click="viewProfile(profile)"
                @send-interest="sendInterest"
                @shortlist="addToShortlist"
              />
            </div>

            <!-- Empty State -->
            <div v-else class="text-center py-12">
              <FeatherIcon name="users" class="w-12 h-12 text-gray-400 mx-auto mb-3" />
              <p class="text-gray-500">No matches found yet.</p>
              <p class="text-sm text-gray-400 mt-1">Complete your profile to get better recommendations!</p>
            </div>
          </div>

          <!-- Recent Activity -->
          <div class="bg-white rounded-lg border border-default p-6">
            <h2 class="text-xl font-semibold text-highlighted mb-4">Recent Activity</h2>
            <div class="space-y-4">
              <div
                v-for="activity in recentActivity"
                :key="activity.id"
                class="flex items-start gap-4 pb-4 border-b border-gray-100 last:border-0 last:pb-0"
              >
                <div class="flex-shrink-0">
                  <div class="w-10 h-10 rounded-full bg-gradient-to-br from-pink-500 to-purple-500 flex items-center justify-center text-white">
                    <FeatherIcon :name="activity.icon" class="w-5 h-5" />
                  </div>
                </div>
                <div class="flex-1">
                  <p class="text-sm text-highlighted">{{ activity.message }}</p>
                  <p class="text-xs text-muted mt-1">{{ formatTime(activity.time) }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column - Sidebar -->
        <div class="space-y-6">
          <!-- Quick Actions -->
          <div class="bg-white rounded-lg border border-default p-6">
            <h3 class="text-lg font-semibold text-highlighted mb-4">Quick Actions</h3>
            <div class="space-y-2">
              <Button
                icon="search"
                label="Browse Profiles"
                variant="subtle"
                block
                class="justify-start"
                @click="$router.push('/browse')"
              />
              <Button
                icon="filter"
                label="Advanced Search"
                variant="subtle"
                block
                class="justify-start"
                @click="$router.push('/search')"
              />
              <Button
                icon="message-circle"
                label="Messages"
                variant="subtle"
                block
                class="justify-start"
                @click="$router.push('/messages')"
              />
              <Button
                icon="heart"
                label="Interests"
                variant="subtle"
                block
                class="justify-start"
                @click="$router.push('/interests')"
              />
            </div>
          </div>

          <!-- Subscription Card -->
          <div class="bg-gradient-to-br from-purple-50 to-pink-50 border border-purple-200 rounded-lg p-6">
            <div class="text-center">
              <div class="inline-flex items-center justify-center w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full mb-3">
                <FeatherIcon name="zap" class="w-6 h-6 text-white" />
              </div>
              <h3 class="text-lg font-semibold text-highlighted mb-1">
                {{ userProfile?.subscription_plan || 'Free' }} Plan
              </h3>
              <p class="text-sm text-muted mb-4">Upgrade for unlimited access</p>
              <Button
                icon="zap"
                label="Upgrade Now"
                variant="solid"
                block
                class="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
                @click="$router.push('/subscription')"
              />
            </div>
          </div>

          <!-- Tips Card -->
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <div class="flex items-start gap-3">
              <FeatherIcon name="lightbulb" class="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
              <div>
                <h3 class="text-sm font-semibold text-highlighted mb-1">Profile Tip</h3>
                <p class="text-xs text-muted">
                  Profiles with photos get 10x more responses. Upload a clear photo to increase your chances!
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { call, Button, FeatherIcon } from 'frappe-ui'
import DashboardLayout from '@/components/DashboardLayout.vue'
import StatsCard from '@/components/StatsCard.vue'
import ProfileCard from '@/components/ProfileCard.vue'
import { session } from '@/data/session'

const router = useRouter()

const userProfile = ref(null)
const refreshing = ref(false)
const stats = ref({
  profile_views: 0,
  interests_sent: 0,
  mutual_matches: 0,
  unread_messages: 0
})
const recommendations = ref({
  loading: false,
  data: []
})
const sentInterests = ref(new Set())

const recentActivity = ref([
  {
    id: 1,
    icon: 'eye',
    message: 'Your profile was viewed by 3 members',
    time: new Date(Date.now() - 2 * 60 * 60 * 1000)
  },
  {
    id: 2,
    icon: 'users',
    message: 'You have 2 new match recommendations',
    time: new Date(Date.now() - 5 * 60 * 60 * 1000)
  },
  {
    id: 3,
    icon: 'heart',
    message: 'Someone sent you an interest',
    time: new Date(Date.now() - 24 * 60 * 60 * 1000)
  }
])

const userName = computed(() => {
  return userProfile.value?.full_name || session.user?.full_name || session.user?.email || 'User'
})

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
      limit: 4
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
    stats.value.profile_views = userProfile.value.view_count || 0

    const interests = await call('shaadi.shaadi.api.matchmaking.get_received_interests', {
      profile_id: userProfile.value.name
    })
    stats.value.interests_sent = interests?.filter(i => i.status === 'Pending').length || 0

    const mutualMatchesCount = await call('shaadi.shaadi.api.matchmaking.get_mutual_matches_count')
    stats.value.mutual_matches = mutualMatchesCount || 0

    const sent = await call('shaadi.shaadi.api.matchmaking.get_sent_interests', {
      profile_id: userProfile.value.name
    })
    sentInterests.value = new Set((sent || []).map(i => i.receiver))
  } catch (error) {
    console.error('Error loading stats:', error)
  }
}

async function refreshData() {
  refreshing.value = true
  await Promise.all([
    loadUserProfile(),
    loadRecommendations(),
    loadStats()
  ])
  refreshing.value = false
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

    sentInterests.value.add(profile.name)
    await loadStats()
  } catch (error) {
    console.error('Error sending interest:', error)
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
  } catch (error) {
    console.error('Error adding to shortlist:', error)
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

function openSearch() {
  console.log('Open search')
}

function openNotifications() {
  console.log('Open notifications')
}
</script>
