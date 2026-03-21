<template>
  <div class="min-h-screen bg-shaadi-base">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Interests</h1>
        <p class="text-gray-600 dark:text-gray-400 mt-1">Manage interests sent and received</p>
      </div>

      <!-- Tabs -->
      <div class="mb-6">
        <div class="flex items-center space-x-2 border-b border-gray-200 dark:border-gray-800">
          <button
            @click="activeTab = 'received'"
            :class="[
              'px-4 py-3 text-sm font-medium border-b-2 transition-colors',
              activeTab === 'received'
                ? 'border-pink-600 text-pink-600'
                : 'border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:border-gray-300 dark:hover:border-gray-600'
            ]"
          >
            Received
            <span class="ml-2 px-2 py-0.5 text-xs rounded-full bg-pink-100 dark:bg-pink-900/30 text-pink-600 dark:text-pink-400">
              {{ receivedInterests.filter(i => i.status === 'Pending').length }}
            </span>
          </button>
          <button
            @click="activeTab = 'sent'"
            :class="[
              'px-4 py-3 text-sm font-medium border-b-2 transition-colors',
              activeTab === 'sent'
                ? 'border-pink-600 text-pink-600'
                : 'border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:border-gray-300 dark:hover:border-gray-600'
            ]"
          >
            Sent
            <span class="ml-2 px-2 py-0.5 text-xs rounded-full bg-gray-100 dark:bg-gray-800 dark:text-gray-300">
              {{ sentInterests.length }}
            </span>
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="space-y-4">
        <Card v-for="i in 3" :key="i" class="animate-pulse p-6 bg-shaadi-surface border-shaadi rounded-xl">
          <div class="flex items-center space-x-4">
            <div class="w-16 h-16 bg-gray-200 dark:bg-shaadi-dk-overlay rounded-full"></div>
            <div class="flex-1">
              <div class="h-4 bg-gray-200 dark:bg-shaadi-dk-overlay rounded w-1/4 mb-2"></div>
              <div class="h-3 bg-gray-200 dark:bg-shaadi-dk-overlay rounded w-1/2"></div>
            </div>
          </div>
        </Card>
      </div>

      <!-- Received Interests -->
      <div v-else-if="activeTab === 'received'">
        <div v-if="receivedInterests.length > 0" class="space-y-4">
          <Card v-for="interest in receivedInterests" :key="interest.name" class="p-6 hover:shadow-lg transition-shadow bg-shaadi-surface border-shaadi rounded-xl">
            <div class="flex items-start justify-between">
              <div class="flex items-start space-x-4 flex-1">
                <!-- Profile Image -->
                <div class="w-16 h-16 bg-gradient-to-br from-pink-100 to-purple-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <FeatherIcon name="user" class="w-8 h-8 text-pink-600" />
                </div>
                
                <!-- Profile Info -->
                <div class="flex-1">
                  <div class="flex items-center space-x-2 mb-1">
                    <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{{ interest.full_name }}</h3>
                    <span 
                      :class="[
                        'px-2 py-0.5 text-xs rounded-full',
                        interest.status === 'Accepted' ? 'bg-green-100 text-green-700' :
                        interest.status === 'Declined' ? 'bg-red-100 text-red-700' :
                        'bg-yellow-100 text-yellow-700'
                      ]"
                    >
                      {{ interest.status }}
                    </span>
                  </div>
                  <p class="text-sm text-gray-600 dark:text-gray-300 mb-2">{{ interest.age }} years • {{ interest.city }}</p>
                  <p v-if="interest.message" class="text-sm text-gray-700 dark:text-gray-300 italic">"{{ interest.message }}"</p>
                  <p class="text-xs text-gray-500 dark:text-gray-400 mt-2">{{ formatDate(interest.sent_on) }}</p>
                </div>
              </div>

              <!-- Actions -->
              <div v-if="interest.status === 'Pending'" class="flex items-center space-x-2 ml-4">
                <Button variant="solid" size="sm" @click="respondToInterest(interest.name, 'Accepted')">
                  <template #prefix>
                    <FeatherIcon name="check" class="w-4 h-4" />
                  </template>
                  Accept
                </Button>
                <Button variant="outline" size="sm" @click="respondToInterest(interest.name, 'Declined')">
                  <template #prefix>
                    <FeatherIcon name="x" class="w-4 h-4" />
                  </template>
                  Decline
                </Button>
                <Button variant="subtle" size="sm" @click="viewProfile(interest.sender)">
                  <FeatherIcon name="eye" class="w-4 h-4" />
                </Button>
              </div>
              <div v-else class="ml-4">
                <Button variant="subtle" size="sm" @click="viewProfile(interest.sender)">
                  <FeatherIcon name="eye" class="w-4 h-4" />
                </Button>
              </div>
            </div>
          </Card>
        </div>
        <Card v-else class="text-center py-12 bg-shaadi-surface border-shaadi rounded-xl">
          <FeatherIcon name="heart" class="w-12 h-12 text-gray-300 dark:text-gray-700 mx-auto mb-4" />
          <p class="text-gray-600 dark:text-gray-400">No interests received yet</p>
        </Card>
      </div>

      <!-- Sent Interests -->
      <div v-else-if="activeTab === 'sent'">
        <div v-if="sentInterests.length > 0" class="space-y-4">
          <Card v-for="interest in sentInterests" :key="interest.name" class="p-6 hover:shadow-lg transition-shadow bg-shaadi-surface border-shaadi rounded-xl">
            <div class="flex items-start justify-between">
              <div class="flex items-start space-x-4 flex-1">
                <!-- Profile Image -->
                <div class="w-16 h-16 bg-gradient-to-br from-pink-100 to-purple-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <FeatherIcon name="user" class="w-8 h-8 text-pink-600" />
                </div>
                
                <!-- Profile Info -->
                <div class="flex-1">
                  <div class="flex items-center space-x-2 mb-1">
                    <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{{ interest.full_name }}</h3>
                    <span 
                      :class="[
                        'px-2 py-0.5 text-xs rounded-full',
                        interest.status === 'Accepted' ? 'bg-green-100 text-green-700' :
                        interest.status === 'Declined' ? 'bg-red-100 text-red-700' :
                        'bg-yellow-100 text-yellow-700'
                      ]"
                    >
                      {{ interest.status }}
                    </span>
                  </div>
                  <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">{{ interest.age }} years • {{ interest.city }}</p>
                  <p v-if="interest.message" class="text-sm text-gray-700 dark:text-gray-300 italic">"{{ interest.message }}"</p>
                  <p class="text-xs text-gray-500 dark:text-gray-400 mt-2">Sent {{ formatDate(interest.sent_on) }}</p>
                </div>
              </div>

              <!-- Actions -->
              <div class="ml-4">
                <Button variant="subtle" size="sm" @click="viewProfile(interest.receiver)">
                  <FeatherIcon name="eye" class="w-4 h-4" />
                </Button>
              </div>
            </div>
          </Card>
        </div>
        <Card v-else class="text-center py-12 bg-shaadi-surface border-shaadi rounded-xl">
          <FeatherIcon name="send" class="w-12 h-12 text-gray-300 dark:text-gray-700 mx-auto mb-4" />
          <p class="text-gray-600 dark:text-gray-400 mb-4">You haven't sent any interests yet</p>
          <Button variant="solid" @click="$router.push('/browse')">
            <template #prefix>
              <FeatherIcon name="search" class="w-4 h-4" />
            </template>
            Browse Profiles
          </Button>
        </Card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { call, Button, Card, FeatherIcon, toast } from 'frappe-ui'

const router = useRouter()
const loading = ref(true)
const activeTab = ref('received')
const receivedInterests = ref([])
const sentInterests = ref([])

async function loadInterests() {
  loading.value = true
  try {
    const [received, sent] = await Promise.all([
      call('shaadi.shaadi.api.matchmaking.get_received_interests'),
      call('shaadi.shaadi.api.matchmaking.get_sent_interests')
    ])
    receivedInterests.value = received || []
    sentInterests.value = sent || []
  } catch (error) {
    console.error('Error loading interests:', error)
  } finally {
    loading.value = false
  }
}

async function respondToInterest(interestId, status) {
  try {
    console.log('Responding to interest:', interestId, status)
    
    await call('shaadi.shaadi.api.matchmaking.respond_to_interest', {
      match_request_id: interestId,
      action: status
    })
    
    console.log('Interest response successful')
    
    // Show success toast
    toast({
      title: `Interest ${status}`,
      text: `You have ${status.toLowerCase()} this interest`,
      icon: 'check'
    })
    
    // Reload interests list
    await loadInterests()
  } catch (error) {
    console.error('Error responding to interest:', error)
    
    // Show error toast
    toast({
      title: 'Error',
      text: error.message || 'Failed to respond to interest',
      icon: 'alert-circle'
    })
  }
}

function viewProfile(profileId) {
  router.push(`/profile/${profileId}`)
}

function formatDate(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) return 'Today'
  if (days === 1) return 'Yesterday'
  if (days < 7) return `${days} days ago`
  if (days < 30) return `${Math.floor(days / 7)} weeks ago`
  return date.toLocaleDateString()
}

onMounted(() => {
  loadInterests()
})
</script>
