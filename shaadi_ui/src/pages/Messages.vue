<template>
  <div class="min-h-screen bg-shaadi-base">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-10rem)]">
        <!-- Conversations List -->
        <Card class="lg:col-span-1 overflow-hidden flex flex-col shadow-sm bg-shaadi-surface border-shaadi">
          <div class="p-5 border-b border-shaadi bg-shaadi-surface">
            <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-1">Messages</h2>
            <p class="text-xs text-gray-500 dark:text-gray-400">{{ conversations.length }} conversation{{ conversations.length !== 1 ? 's' : '' }}</p>
            <div class="mt-4">
              <Input
                v-model="searchQuery"
                type="text"
                placeholder="Search conversations..."
                class="w-full"
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
                <div class="w-12 h-12 bg-gray-200 dark:bg-shaadi-dk-overlay rounded-full"></div>
                <div class="flex-1">
                  <div class="h-4 bg-gray-200 dark:bg-shaadi-dk-overlay rounded w-3/4 mb-2"></div>
                  <div class="h-3 bg-gray-200 dark:bg-shaadi-dk-overlay rounded w-1/2"></div>
                </div>
              </div>
            </div>

            <div v-else-if="filteredConversations.length > 0" class="divide-y divide-gray-200 dark:divide-gray-800">
              <button
                v-for="conversation in filteredConversations"
                :key="conversation.name"
                @click="selectConversation(conversation)"
                :class="[
                  'w-full p-4 flex items-start space-x-3 hover:bg-gray-50 dark:hover:bg-gray-800 transition-all duration-200 text-left border-l-3',
                  selectedConversation?.name === conversation.name 
                    ? 'bg-pink-50 dark:bg-pink-900/20 border-l-pink-500' 
                    : 'border-l-transparent hover:border-l-gray-300 dark:hover:border-l-gray-600'
                ]">
              >
                <div class="relative w-14 h-14 bg-gradient-to-br from-pink-100 to-purple-100 dark:from-pink-900 dark:to-purple-900 rounded-full flex items-center justify-center flex-shrink-0 ring-2 ring-white dark:ring-gray-800 shadow-sm">
                  <FeatherIcon name="user" class="w-7 h-7 text-pink-600 dark:text-pink-400" />
                  <!-- Online Status Indicator -->
                  <div v-if="conversation.other_participant_online" class="absolute bottom-0 right-0 w-4 h-4 bg-green-500 border-2 border-white rounded-full"></div>
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between mb-1.5">
                    <div class="flex items-center space-x-2 min-w-0 flex-1">
                      <h3 class="text-sm font-semibold text-gray-900 dark:text-white truncate">{{ conversation.other_participant_name || 'Unknown' }}</h3>
                      <span v-if="conversation.other_participant_online" class="flex items-center text-xs text-green-600 font-medium">
                        <span class="w-1.5 h-1.5 bg-green-500 rounded-full mr-1"></span>
                        Online
                      </span>
                    </div>
                    <span class="text-xs text-gray-400 dark:text-gray-500 flex-shrink-0 ml-2">{{ formatTime(conversation.last_message_on) }}</span>
                  </div>
                  <div class="flex items-center justify-between">
                    <p :class="[
                      'text-sm truncate flex-1',
                      conversation.unread_count > 0 ? 'text-gray-900 dark:text-white font-medium' : 'text-gray-500 dark:text-gray-400'
                    ]">{{ conversation.last_message_text || 'No messages yet' }}</p>
                    <span v-if="conversation.unread_count > 0" class="inline-flex items-center justify-center min-w-[20px] h-5 px-1.5 text-xs font-bold bg-pink-600 text-white rounded-full ml-2 flex-shrink-0">
                      {{ conversation.unread_count > 99 ? '99+' : conversation.unread_count }}
                    </span>
                  </div>
                </div>
              </button>
            </div>

            <div v-else class="p-8 text-center">
              <FeatherIcon name="message-circle" class="w-12 h-12 text-gray-300 dark:text-gray-700 mx-auto mb-3" />
              <p class="text-gray-600 dark:text-gray-400">No conversations yet</p>
            </div>
          </div>
        </Card>

        <!-- Chat Area -->
        <Card class="lg:col-span-2 overflow-hidden flex flex-col shadow-sm bg-shaadi-surface border-shaadi">
          <div v-if="selectedConversation" class="flex flex-col h-full">
            <!-- Chat Header -->
            <div class="p-5 border-b border-shaadi flex items-center justify-between bg-shaadi-surface">
              <div class="flex items-center space-x-3">
                <div class="relative w-12 h-12 bg-gradient-to-br from-pink-100 to-purple-100 dark:from-pink-900 dark:to-purple-900 rounded-full flex items-center justify-center ring-2 ring-white dark:ring-gray-800 shadow-sm">
                  <FeatherIcon name="user" class="w-6 h-6 text-pink-600 dark:text-pink-400" />
                  <div v-if="selectedConversation.other_participant_online" class="absolute bottom-0 right-0 w-3.5 h-3.5 bg-green-500 border-2 border-white rounded-full"></div>
                </div>
                <div>
                  <h3 class="text-base font-semibold text-gray-900 dark:text-white">{{ selectedConversation.other_participant_name }}</h3>
                  <p class="text-xs text-gray-500 dark:text-gray-400 flex items-center">
                    <span v-if="selectedConversation.other_participant_online" class="text-green-600 font-medium">Active now</span>
                    <span v-else>{{ selectedConversation.other_participant_status || 'Offline' }}</span>
                  </p>
                </div>
              </div>
              <div class="flex items-center gap-2">
                <Button variant="ghost" size="sm" @click="viewProfile(selectedConversation.other_participant)">
                  <template #prefix>
                    <FeatherIcon name="user" class="w-4 h-4" />
                  </template>
                  Profile
                </Button>
              </div>
            </div>

            <!-- Messages -->
            <div ref="messagesContainer" class="flex-1 overflow-y-auto p-6 space-y-1 bg-shaadi-base">
              <div v-if="loadingMessages" class="space-y-3">
                <div v-for="i in 5" :key="i" class="animate-pulse">
                  <div :class="i % 2 === 0 ? 'flex justify-end' : 'flex justify-start'">
                    <div class="max-w-xs">
                      <div class="h-16 bg-gray-200 dark:bg-shaadi-dk-overlay rounded-lg"></div>
                    </div>
                  </div>
                </div>
              </div>

              <div v-else-if="messages.length > 0" class="space-y-4">
                <div
                  v-for="message in messages"
                  :key="message.name"
                  :class="[
                    'flex items-end gap-2',
                    message.is_own_message ? 'justify-end' : 'justify-start'
                  ]"
                >
                  <div :class="[
                    'max-w-xs lg:max-w-md px-4 py-3 rounded-2xl shadow-sm',
                    message.is_own_message
                      ? 'bg-gradient-to-br from-pink-500 to-pink-600 text-white rounded-br-md'
                      : 'bg-shaadi-surface text-gray-900 dark:text-white border border-shaadi rounded-bl-md'
                  ]">
                    <p class="text-sm leading-relaxed break-words">{{ message.message_text }}</p>
                    <div :class="[
                      'flex items-center gap-1 mt-1.5',
                      message.is_own_message ? 'justify-end' : 'justify-start'
                    ]">
                      <p :class="[
                        'text-xs',
                        message.is_own_message ? 'text-pink-100' : 'text-gray-400 dark:text-gray-500'
                      ]">
                        {{ formatTime(message.sent_on) }}
                      </p>
                      <FeatherIcon 
                        v-if="message.is_own_message" 
                        name="check" 
                        class="w-3 h-3 text-pink-100" 
                      />
                    </div>
                  </div>
                </div>
              </div>

              <div v-else class="text-center py-12">
                <FeatherIcon name="message-circle" class="w-12 h-12 text-gray-300 dark:text-gray-700 mx-auto mb-3" />
                <p class="text-gray-600 dark:text-gray-400">No messages yet. Start the conversation!</p>
              </div>
              
              <!-- Typing Indicator -->
              <div v-if="isTyping" class="flex justify-start items-end gap-2">
                <div class="px-4 py-3 rounded-2xl rounded-bl-md bg-shaadi-surface border border-shaadi shadow-sm">
                  <div class="flex space-x-1.5">
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.15s"></div>
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.3s"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Message Input -->
            <div class="message-input-area px-6 py-4 border-t border-shaadi bg-shaadi-surface">
              <form @submit.prevent="sendMessage" class="flex items-end gap-3">
                <div class="flex-1">
                  <Input
                    v-model="newMessage"
                    type="text"
                    placeholder="Type a message..."
                    :disabled="sendingMessage"
                    class="w-full rounded-xl !px-4 !py-3 !h-auto"
                    @input="sendTypingIndicator"
                  />
                </div>
                <Button
                  type="submit"
                  :loading="sendingMessage"
                  :disabled="!newMessage.trim()"
                  class="bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700 text-white px-6"
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
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Select a conversation</h3>
              <p class="text-gray-600 dark:text-gray-400">Choose a conversation from the list to start messaging</p>
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
    toast({
      title: 'Error',
      text: 'Failed to open conversation',
      icon: 'alert-circle',
      iconClasses: 'text-red-500'
    })
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
      toast({
        title: 'Message Limit Reached',
        text: 'Please upgrade your subscription to continue messaging.',
        icon: 'alert-circle',
        iconClasses: 'text-red-500'
      })
      // Optionally redirect to subscription page
      setTimeout(() => router.push('/subscription'), 2000)
    } else {
      toast({
        title: 'Error',
        text: error.message || 'Failed to send message',
        icon: 'alert-circle',
        iconClasses: 'text-red-500'
      })
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
    toast({
      title: 'New Message',
      text: `New message from ${data.sender_name}`,
      icon: 'message-circle',
      iconClasses: 'text-blue-500'
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
