<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-12rem)]">
        <!-- Conversations List -->
        <Card class="lg:col-span-1 overflow-hidden flex flex-col">
          <div class="p-4 border-b border-gray-200">
            <h2 class="text-lg font-semibold text-gray-900">Messages</h2>
            <div class="mt-3">
              <Input
                v-model="searchQuery"
                type="text"
                placeholder="Search conversations..."
              >
                <template #prefix>
                  <FeatherIcon name="search" class="w-4 h-4 text-gray-400" />
                </template>
              </Input>
            </div>
          </div>

          <!-- Conversations -->
          <div class="flex-1 overflow-y-auto">
            <div v-if="loadingConversations" class="p-4 space-y-3">
              <div v-for="i in 5" :key="i" class="animate-pulse flex items-center space-x-3">
                <div class="w-12 h-12 bg-gray-200 rounded-full"></div>
                <div class="flex-1">
                  <div class="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                  <div class="h-3 bg-gray-200 rounded w-1/2"></div>
                </div>
              </div>
            </div>

            <div v-else-if="filteredConversations.length > 0" class="divide-y divide-gray-200">
              <button
                v-for="conversation in filteredConversations"
                :key="conversation.name"
                @click="selectConversation(conversation)"
                :class="[
                  'w-full p-4 flex items-start space-x-3 hover:bg-gray-50 transition-colors text-left',
                  selectedConversation?.name === conversation.name ? 'bg-pink-50' : ''
                ]"
              >
                <div class="relative w-12 h-12 bg-gradient-to-br from-pink-100 to-purple-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <FeatherIcon name="user" class="w-6 h-6 text-pink-600" />
                  <!-- Online Status Indicator -->
                  <div v-if="conversation.other_participant_online" class="absolute -bottom-0.5 -right-0.5 w-4 h-4 bg-green-500 border-2 border-white rounded-full"></div>
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between mb-1">
                    <div class="flex items-center space-x-2 min-w-0">
                      <h3 class="text-sm font-semibold text-gray-900 truncate">{{ conversation.other_participant_name || 'Unknown' }}</h3>
                      <span v-if="conversation.other_participant_online" class="text-xs text-green-600 font-medium">Online</span>
                    </div>
                    <span class="text-xs text-gray-500 flex-shrink-0">{{ formatTime(conversation.last_message_on) }}</span>
                  </div>
                  <p class="text-sm text-gray-600 truncate">{{ conversation.last_message_text || 'No messages yet' }}</p>
                  <div class="flex items-center justify-between mt-1">
                    <span v-if="!conversation.other_participant_online" class="text-xs text-gray-400">{{ conversation.other_participant_status || 'Offline' }}</span>
                    <span v-if="conversation.unread_count > 0" class="inline-block px-2 py-0.5 text-xs font-medium bg-pink-600 text-white rounded-full ml-auto">
                      {{ conversation.unread_count }}
                    </span>
                  </div>
                </div>
              </button>
            </div>

            <div v-else class="p-8 text-center">
              <FeatherIcon name="message-circle" class="w-12 h-12 text-gray-300 mx-auto mb-3" />
              <p class="text-gray-600">No conversations yet</p>
            </div>
          </div>
        </Card>

        <!-- Chat Area -->
        <Card class="lg:col-span-2 overflow-hidden flex flex-col">
          <div v-if="selectedConversation">
            <!-- Chat Header -->
            <div class="p-4 border-b border-gray-200 flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-gradient-to-br from-pink-100 to-purple-100 rounded-full flex items-center justify-center">
                  <FeatherIcon name="user" class="w-5 h-5 text-pink-600" />
                </div>
                <div>
                  <h3 class="text-sm font-semibold text-gray-900">{{ selectedConversation.other_profile_name }}</h3>
                  <p class="text-xs text-gray-500">{{ selectedConversation.other_profile_city }}</p>
                </div>
              </div>
              <Button variant="subtle" size="sm" @click="viewProfile(selectedConversation.other_profile_id)">
                <template #prefix>
                  <FeatherIcon name="eye" class="w-4 h-4" />
                </template>
                View Profile
              </Button>
            </div>

            <!-- Messages -->
            <div ref="messagesContainer" class="flex-1 overflow-y-auto p-4 space-y-4">
              <div v-if="loadingMessages" class="space-y-3">
                <div v-for="i in 5" :key="i" class="animate-pulse">
                  <div :class="i % 2 === 0 ? 'flex justify-end' : 'flex justify-start'">
                    <div class="max-w-xs">
                      <div class="h-16 bg-gray-200 rounded-lg"></div>
                    </div>
                  </div>
                </div>
              </div>

              <div v-else-if="messages.length > 0">
                <div
                  v-for="message in messages"
                  :key="message.name"
                  :class="[
                    'flex',
                    message.is_own_message ? 'justify-end' : 'justify-start'
                  ]"
                >
                  <div :class="[
                    'max-w-xs lg:max-w-md px-4 py-2 rounded-lg',
                    message.is_own_message
                      ? 'bg-pink-600 text-white'
                      : 'bg-gray-200 text-gray-900'
                  ]">
                    <p class="text-sm">{{ message.message_text }}</p>
                    <p :class="[
                      'text-xs mt-1',
                      message.is_own_message ? 'text-pink-100' : 'text-gray-500'
                    ]">
                      {{ formatTime(message.sent_on) }}
                    </p>
                  </div>
                </div>
              </div>

              <div v-else class="text-center py-12">
                <FeatherIcon name="message-circle" class="w-12 h-12 text-gray-300 mx-auto mb-3" />
                <p class="text-gray-600">No messages yet. Start the conversation!</p>
              </div>
              
              <!-- Typing Indicator -->
              <div v-if="isTyping" class="flex justify-start">
                <div class="max-w-xs px-4 py-2 rounded-lg bg-gray-200">
                  <div class="flex space-x-1">
                    <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                    <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                    <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Message Input -->
            <div class="p-4 border-t border-gray-200">
              <form @submit.prevent="sendMessage" class="flex items-end space-x-2">
                <div class="flex-1">
                  <Input
                    v-model="newMessage"
                    type="text"
                    placeholder="Type your message..."
                    :disabled="sendingMessage"
                  />
                </div>
                <Button
                  type="submit"
                  variant="solid"
                  :loading="sendingMessage"
                  :disabled="!newMessage.trim()"
                >
                  <template #prefix>
                    <FeatherIcon name="send" class="w-4 h-4" />
                  </template>
                  Send
                </Button>
              </form>
            </div>
          </div>

          <!-- No Conversation Selected -->
          <div v-else class="flex-1 flex items-center justify-center">
            <div class="text-center">
              <FeatherIcon name="message-square" class="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 class="text-lg font-semibold text-gray-900 mb-2">Select a conversation</h3>
              <p class="text-gray-600">Choose a conversation from the list to start messaging</p>
            </div>
          </div>
        </Card>
      </div>
    </div>

    <!-- Subscription Required Dialog -->
    <Dialog 
      v-model="showUpgradeModal"
      :options="dialogOptions"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { call, Button, Card, Input, FeatherIcon, Dialog, toast } from 'frappe-ui'
import { session } from '@/data/session'
import { getSocket } from '@/socket'
import { useNotifications } from '@/composables/useNotifications'

const router = useRouter()
const route = useRoute()
const socket = getSocket()
const { decrementUnreadCount } = useNotifications()

const loadingConversations = ref(true)
const loadingMessages = ref(false)
const sendingMessage = ref(false)
const conversations = ref([])
const selectedConversation = ref(null)
const messages = ref([])  
const newMessage = ref('')
const searchQuery = ref('')
const isTyping = ref(false)
const typingTimeout = ref(null)
const showUpgradeModal = ref(false)
const hasSubscription = ref(true)
const messagesContainer = ref(null)
const statusUpdateInterval = ref(null)
const notificationPermission = ref(Notification.permission)
const totalUnreadCount = computed(() => {
  return conversations.value.reduce((sum, conv) => sum + (conv.unread_count || 0), 0)
})

const dialogOptions = computed(() => ({
  title: 'Subscription Required',
  message: 'To send and receive messages with other members, you need an active subscription plan. Upgrade now to unlock unlimited messaging and connect with potential matches!',
  disableOutsideClickToClose: true,
  actions: [
    {
      label: 'Upgrade Now',
      variant: 'solid',
      onClick: () => {
        goToSubscription()
        showUpgradeModal.value = false
      }
    },
    {
      label: 'Go to Dashboard',
      variant: 'outline',
      onClick: () => {
        router.push('/dashboard')
        showUpgradeModal.value = false
      }
    }
  ]
}))

const filteredConversations = computed(() => {
  if (!searchQuery.value) return conversations.value
  const query = searchQuery.value.toLowerCase()
  return conversations.value.filter(c =>
    c.other_profile_name.toLowerCase().includes(query)
  )
})

async function loadConversations() {
  loadingConversations.value = true
  try {
    const response = await call('shaadi.shaadi.api.messaging.get_conversations')
    conversations.value = response || []
    
    // Auto-select or create conversation if profile param exists
    if (route.query.profile) {
      await handleProfileParameter()
    }
  } catch (error) {
    console.error('Error loading conversations:', error)
  } finally {
    loadingConversations.value = false
  }
}

async function handleProfileParameter() {
  const profileId = route.query.profile
  
  try {
    // Try to find existing conversation
    let conv = conversations.value.find(c => c.other_profile_id === profileId)
    
    // If not found, create or get conversation
    if (!conv) {
      console.log('Creating/getting conversation for profile:', profileId)
      const response = await call('shaadi.shaadi.api.messaging.get_or_create_conversation', {
        other_profile_id: profileId
      })
      
      // Add to conversations list
      conversations.value.unshift(response)
      conv = response
    }
    
    // Select the conversation
    if (conv) {
      await selectConversation(conv)
    }
  } catch (error) {
    console.error('Error handling profile parameter:', error)
    toast.error('Failed to open conversation')
  }
}

async function selectConversation(conversation) {
  selectedConversation.value = conversation
  await loadMessages(conversation.name)
  
  // Mark conversation as read
  if (conversation.unread_count > 0) {
    await markConversationAsRead(conversation.name)
  }
}

async function loadMessages(conversationId) {
  loadingMessages.value = true
  try {
    const response = await call('shaadi.shaadi.api.messaging.get_messages', {
      conversation_id: conversationId
    })
    messages.value = response || []
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('Error loading messages:', error)
  } finally {
    loadingMessages.value = false
  }
}

async function sendMessage() {
  if (!newMessage.value.trim() || !selectedConversation.value) return
  
  sendingMessage.value = true
  try {
    const response = await call('shaadi.shaadi.api.messaging.send_message', {
      conversation_id: selectedConversation.value.name,
      message_text: newMessage.value
    })
    
    // Immediately add sent message to display
    if (response && response.message_data) {
      messages.value.push(response.message_data)
      newMessage.value = ''
      await nextTick()
      scrollToBottom()
    }
  } catch (error) {
    console.error('Error sending message:', error)
    
    // Check if it's a subscription limit error
    if (error.message && error.message.includes('subscription')) {
      toast.error('Message limit reached! Please upgrade your subscription to continue messaging.', {
        duration: 6,
        action: {
          label: 'Upgrade Now',
          onClick: () => router.push('/subscription')
        }
      })
    } else {
      toast.error(error.message || 'Failed to send message')
    }
  } finally {
    sendingMessage.value = false
  }
}

function viewProfile(profileId) {
  router.push(`/profile/${profileId}`)
}

function formatTime(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  const hours = Math.floor(diff / (1000 * 60 * 60))
  
  if (hours < 1) return 'Just now'
  if (hours < 24) return `${hours}h ago`
  if (hours < 48) return 'Yesterday'
  return date.toLocaleDateString()
}

function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

watch(() => messages.value.length, () => {
  nextTick(() => scrollToBottom())
})

// Real-time message handler
function handleNewMessage(data) {
  console.log('🔔 Received new message event:', data)
  console.log('Current conversation:', selectedConversation.value?.name)
  console.log('Is own message:', data.is_own_message)
  
  // Handle incoming message - only add if it's not our own message
  if (data.conversation === selectedConversation.value?.name && !data.is_own_message) {
    messages.value.push(data)
    nextTick(() => scrollToBottom())
    
    // Mark conversation as read if user is viewing it
    markConversationAsRead(data.conversation)
  }
  
  // Update conversation list to show latest message
  loadConversations()
  
  // Show notifications if message is not in current conversation
  if (!selectedConversation.value || data.conversation !== selectedConversation.value.name) {
    // Toast notification
    toast.info(`New message from ${data.sender_name}`, {
      duration: 5,
      action: {
        label: 'View',
        onClick: () => {
          const conv = conversations.value.find(c => c.name === data.conversation)
          if (conv) selectConversation(conv)
        }
      }
    })
    
    // Browser notification
    showBrowserNotification(data.sender_name, data.message_text)
    
    // Play notification sound (optional)
    playNotificationSound()
  }
}

// Typing indicator handler
function handleTypingIndicator(data) {
  if (selectedConversation.value && data.conversation === selectedConversation.value.name) {
    isTyping.value = data.is_typing
  }
}

// Send typing indicator
function sendTypingIndicator() {
  if (!selectedConversation.value) return
  
  clearTimeout(typingTimeout.value)
  
  call('shaadi.shaadi.api.realtime.typing_indicator', {
    conversation_id: selectedConversation.value.name,
    is_typing: true
  })
  
  typingTimeout.value = setTimeout(() => {
    call('shaadi.shaadi.api.realtime.typing_indicator', {
      conversation_id: selectedConversation.value.name,
      is_typing: false
    })
  }, 3000)
}

// Mark messages as read
async function markAsRead() {
  if (!selectedConversation.value) return
  
  try {
    await call('shaadi.shaadi.api.messaging.mark_as_read', {
      conversation_id: selectedConversation.value.name
    })
  } catch (error) {
    console.error('Error marking as read:', error)
  }
}

async function checkSubscription() {
  try {
    const profileResponse = await call('shaadi.shaadi.api.auth.get_current_member_profile')
    if (profileResponse?.name) {
      const response = await call('shaadi.shaadi.api.subscription.check_feature_access', {
        profile_id: profileResponse.name,
        feature: 'send_message'
      })
      hasSubscription.value = response?.has_access || false
    } else {
      hasSubscription.value = false
    }
  } catch (error) {
    console.error('Error checking subscription:', error)
    hasSubscription.value = false
  }
}

function goToSubscription() {
  router.push('/subscription')
}

// Request notification permission
async function requestNotificationPermission() {
  if ('Notification' in window && Notification.permission === 'default') {
    const permission = await Notification.requestPermission()
    notificationPermission.value = permission
  }
}

// Show browser notification
function showBrowserNotification(senderName, messageText) {
  if ('Notification' in window && Notification.permission === 'granted') {
    const notification = new Notification(`New message from ${senderName}`, {
      body: messageText.substring(0, 100),
      icon: '/assets/shaadi/images/logo.png',
      badge: '/assets/shaadi/images/logo.png',
      tag: 'shaadi-message',
      requireInteraction: false
    })
    
    notification.onclick = () => {
      window.focus()
      notification.close()
    }
    
    // Auto close after 5 seconds
    setTimeout(() => notification.close(), 5000)
  }
}

// Play notification sound
function playNotificationSound() {
  try {
    const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIGGS57OihUBELTKXh8LJnHgU2jdXzzn0vBSp+zPLaizsKFGO56+mjUhELSKPf8LVpIAU4kNbz0YIyBSh6y/HajDwLFGC46Oqk')
    audio.volume = 0.3
    audio.play().catch(() => {})
  } catch (error) {
    // Ignore sound errors
  }
}

// Mark conversation as read
async function markConversationAsRead(conversationId) {
  try {
    // Get current unread count before marking as read
    const conv = conversations.value.find(c => c.name === conversationId)
    const unreadToDecrement = conv?.unread_count || 0
    
    await call('shaadi.shaadi.api.messaging.mark_conversation_read', {
      conversation_id: conversationId
    })
    
    // Update local conversation unread count
    if (conv) {
      conv.unread_count = 0
    }
    
    // Decrement global unread count in navigation badge
    if (unreadToDecrement > 0) {
      decrementUnreadCount(unreadToDecrement)
    }
  } catch (error) {
    console.error('Error marking conversation as read:', error)
  }
}

// Handle real-time user status updates
function handleUserStatusUpdate(data) {
  console.log('👤 User status update:', data)
  
  // Update conversation list with new online status
  const conversation = conversations.value.find(conv => 
    conv.other_participant === data.profile_id
  )
  
  if (conversation) {
    conversation.other_participant_online = data.is_online
    conversation.other_participant_status = data.is_online ? 'Online' : 'Last seen just now'
  }
}

onMounted(async () => {
  if (!session.isLoggedIn) {
    router.push('/signin')
    return
  }
  
  await checkSubscription()
  
  if (!hasSubscription.value) {
    showUpgradeModal.value = true
    return
  }
  
  await loadConversations()
  
  // Request notification permission
  await requestNotificationPermission()
  
  // Set up socket listeners if socket is available
  if (socket) {
    console.log('Setting up socket listeners, socket connected:', socket.connected)
    console.log('Socket ID:', socket.id)
    
    // Listen to ALL events for debugging
    socket.onAny((eventName, ...args) => {
      console.log(`📡 Socket event received: ${eventName}`, args)
    })
    
    socket.on('new_message', handleNewMessage)
    socket.on('typing_indicator', handleTypingIndicator)
    socket.on('user_status_update', handleUserStatusUpdate)
    
    // Log when socket connects/disconnects
    socket.on('connect', () => {
      console.log('✅ Socket connected successfully, ID:', socket.id)
    })
    socket.on('disconnect', () => {
      console.log('❌ Socket disconnected')
    })
    socket.on('connect_error', (error) => {
      console.error('Socket connection error:', error)
    })
  } else {
    console.warn('⚠️ Socket not available, real-time features disabled')
  }
  
  // Update online status
  try {
    await call('shaadi.shaadi.api.messaging.update_online_status', {
      is_online: true
    })
  } catch (error) {
    console.warn('Failed to update online status:', error)
  }
  
  // Set up periodic online status updates (every 2 minutes)
  statusUpdateInterval.value = setInterval(async () => {
    try {
      await call('shaadi.shaadi.api.messaging.update_online_status', {
        is_online: true
      })
    } catch (error) {
      console.warn('Failed to update online status:', error)
    }
  }, 120000) // 2 minutes
})

onUnmounted(() => {
  // Clean up socket listeners if socket is available
  if (socket) {
    socket.off('new_message', handleNewMessage)
    socket.off('typing_indicator', handleTypingIndicator)
    socket.off('user_status_update', handleUserStatusUpdate)
  }
  
  // Clear status update interval
  if (statusUpdateInterval.value) {
    clearInterval(statusUpdateInterval.value)
  }
  
  // Update online status to offline (fire and forget, no await needed on unmount)
  call('shaadi.shaadi.api.messaging.update_online_status', {
    is_online: false
  }).catch(error => {
    console.warn('Failed to update online status:', error)
  })
})
</script>
