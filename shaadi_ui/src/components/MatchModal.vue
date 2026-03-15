<template>
  <div v-if="show" class="match-modal-overlay" @click="closeModal">
    <div class="match-modal" @click.stop>
      <!-- Celebration Animation -->
      <div class="celebration-header">
        <div class="celebration-text">
          <h1 class="match-title">🎉 IT'S A MATCH! 🎉</h1>
          <p class="match-subtitle">You and {{ matchedProfile?.full_name }} liked each other!</p>
        </div>
      </div>

      <!-- Profile Photos -->
      <div class="profiles-section">
        <div class="profile-photos">
          <!-- Current User Photo -->
          <div class="profile-photo current-user">
            <img
              :src="currentUser?.profile_photo || '/assets/default-avatar.png'"
              :alt="currentUser?.full_name"
              class="photo"
            />
            <div class="photo-overlay">
              <FeatherIcon name="heart" class="heart-icon" />
            </div>
          </div>

          <!-- Heart Animation -->
          <div class="heart-animation">
            <div class="heart-burst">
              <FeatherIcon name="heart" class="floating-heart" />
              <FeatherIcon name="heart" class="floating-heart" />
              <FeatherIcon name="heart" class="floating-heart" />
            </div>
          </div>

          <!-- Matched User Photo -->
          <div class="profile-photo matched-user">
            <img
              :src="matchedProfile?.profile_photo || '/assets/default-avatar.png'"
              :alt="matchedProfile?.full_name"
              class="photo"
            />
            <div class="photo-overlay">
              <FeatherIcon name="heart" class="heart-icon" />
            </div>
          </div>
        </div>

        <!-- Match Details -->
        <div class="match-details">
          <div class="compatibility-score">
            <span class="score-label">Compatibility</span>
            <span class="score-value">{{ Math.round(matchScore || 0) }}%</span>
          </div>
          
          <div class="match-info">
            <div class="info-item">
              <FeatherIcon name="map-pin" class="info-icon" />
              <span>{{ matchedProfile?.city }}</span>
            </div>
            <div class="info-item">
              <FeatherIcon name="calendar" class="info-icon" />
              <span>{{ matchedProfile?.age }} years old</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="action-buttons">
        <Button
          variant="solid"
          size="lg"
          class="message-button"
          @click="startConversation"
        >
          <template #prefix>
            <FeatherIcon name="message-circle" class="w-5 h-5" />
          </template>
          Send Message
        </Button>
        
        <Button
          variant="outline"
          size="lg"
          class="continue-button"
          @click="keepSwiping"
        >
          <template #prefix>
            <FeatherIcon name="refresh-cw" class="w-5 h-5" />
          </template>
          Keep Swiping
        </Button>
      </div>

      <!-- Close Button -->
      <button class="close-button" @click="closeModal">
        <FeatherIcon name="x" class="w-6 h-6" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Button, FeatherIcon, call } from 'frappe-ui'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  matchedProfile: {
    type: Object,
    default: null
  },
  matchScore: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['close', 'message', 'continue'])

const router = useRouter()
const currentUser = ref(null)

// Load current user profile
async function loadCurrentUser() {
  try {
    const response = await call('shaadi.shaadi.api.auth.get_current_member_profile')
    currentUser.value = response
  } catch (error) {
    console.error('Error loading current user:', error)
  }
}

function closeModal() {
  emit('close')
}

function startConversation() {
  emit('message', props.matchedProfile)
  // Navigate to messages with the matched profile
  router.push(`/messages?profile=${props.matchedProfile?.name}`)
}

function keepSwiping() {
  emit('continue')
  closeModal()
}

// Handle escape key
function handleEscape(event) {
  if (event.key === 'Escape' && props.show) {
    closeModal()
  }
}

onMounted(() => {
  loadCurrentUser()
  document.addEventListener('keydown', handleEscape)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscape)
})
</script>

<style scoped>
.match-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

.match-modal {
  background: linear-gradient(135deg, #ff6b6b, #ff8e8e, #ffa8a8);
  border-radius: 24px;
  padding: 40px;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  animation: slideUp 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.celebration-header {
  text-align: center;
  margin-bottom: 32px;
}

.match-title {
  font-size: 32px;
  font-weight: 800;
  color: white;
  margin-bottom: 8px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  animation: bounce 0.6s ease-out;
}

.match-subtitle {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
}

.profiles-section {
  margin-bottom: 32px;
}

.profile-photos {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 40px;
  margin-bottom: 24px;
  position: relative;
}

.profile-photo {
  position: relative;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  border: 4px solid white;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  animation: photoZoom 0.5s ease-out;
}

.profile-photo.current-user {
  animation-delay: 0.2s;
}

.profile-photo.matched-user {
  animation-delay: 0.4s;
}

.photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.photo-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 107, 107, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.heart-icon {
  color: white;
  width: 24px;
  height: 24px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}

.heart-animation {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.heart-burst {
  position: relative;
  animation: heartPulse 1s ease-out infinite;
}

.floating-heart {
  position: absolute;
  color: white;
  width: 20px;
  height: 20px;
  animation: floatHeart 2s ease-out infinite;
}

.floating-heart:nth-child(1) {
  animation-delay: 0s;
  transform: rotate(0deg) translateX(30px);
}

.floating-heart:nth-child(2) {
  animation-delay: 0.3s;
  transform: rotate(120deg) translateX(30px);
}

.floating-heart:nth-child(3) {
  animation-delay: 0.6s;
  transform: rotate(240deg) translateX(30px);
}

.match-details {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 20px;
  backdrop-filter: blur(10px);
}

.compatibility-score {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

.score-label {
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
}

.score-value {
  font-size: 24px;
  font-weight: 700;
  color: white;
}

.match-info {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
}

.info-icon {
  width: 16px;
  height: 16px;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message-button {
  background: white;
  color: #ff6b6b;
  border: none;
  font-weight: 600;
}

.message-button:hover {
  background: #f8f9fa;
  transform: translateY(-2px);
}

.continue-button {
  background: transparent;
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.5);
  font-weight: 600;
}

.continue-button:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: white;
}

.close-button {
  position: absolute;
  top: 16px;
  right: 16px;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.close-button:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(50px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

@keyframes photoZoom {
  from {
    opacity: 0;
    transform: scale(0.5);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes heartPulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
}

@keyframes floatHeart {
  0% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
  100% {
    opacity: 0;
    transform: translateY(-40px) scale(0.5);
  }
}

/* Mobile responsiveness */
@media (max-width: 640px) {
  .match-modal {
    padding: 24px;
    margin: 20px;
  }
  
  .match-title {
    font-size: 24px;
  }
  
  .match-subtitle {
    font-size: 16px;
  }
  
  .profile-photos {
    gap: 24px;
  }
  
  .profile-photo {
    width: 100px;
    height: 100px;
  }
  
  .match-info {
    flex-direction: column;
    gap: 12px;
    align-items: center;
  }
}
</style>
