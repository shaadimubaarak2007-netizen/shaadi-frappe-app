<template>
  <div
    ref="cardRef"
    class="swipe-card"
    :class="{ 'swiping': isDragging }"
    :style="cardStyle"
    @mousedown="startDrag"
    @touchstart="startDrag"
  >
    <!-- Profile Image -->
    <div class="card-image">
      <img
        :src="profile.profile_photo || '/assets/default-avatar.png'"
        :alt="profile.full_name"
        class="w-full h-full object-cover"
      />
      
      <!-- Match Score Badge -->
      <div class="match-score-badge">
        {{ Math.round(profile.match_score || 0) }}% Match
      </div>
      
      <!-- Action Indicators -->
      <div class="action-indicator like-indicator" :class="{ active: showLikeIndicator }">
        <FeatherIcon name="heart" class="w-8 h-8" />
        <span>LIKE</span>
      </div>
      
      <div class="action-indicator pass-indicator" :class="{ active: showPassIndicator }">
        <FeatherIcon name="x" class="w-8 h-8" />
        <span>PASS</span>
      </div>
    </div>
    
    <!-- Profile Info -->
    <div class="card-info">
      <div class="profile-header">
        <h3 class="profile-name" :title="profile.full_name + ', ' + profile.age">
          {{ profile.full_name }}, {{ profile.age }}
        </h3>
        <div class="profile-location" :title="profile.city">
          <FeatherIcon name="map-pin" class="w-4 h-4 flex-shrink-0" />
          <span class="truncate">{{ profile.city }}</span>
        </div>
      </div>
      
      <div class="profile-details">
        <div class="detail-item" :title="profile.occupation">
          <FeatherIcon name="briefcase" class="w-4 h-4 flex-shrink-0" />
          <span class="truncate">{{ profile.occupation || 'Not specified' }}</span>
        </div>
        <div class="detail-item" :title="profile.education">
          <FeatherIcon name="book" class="w-4 h-4 flex-shrink-0" />
          <span class="truncate">{{ profile.education || 'Not specified' }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { FeatherIcon } from 'frappe-ui'

const props = defineProps({
  profile: {
    type: Object,
    required: true
  },
  isTopCard: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['swipe', 'dragStart', 'dragEnd'])

// Refs
const cardRef = ref(null)
const isDragging = ref(false)
const dragStartPos = ref({ x: 0, y: 0 })
const currentPos = ref({ x: 0, y: 0 })
const rotation = ref(0)

// Swipe thresholds
const SWIPE_THRESHOLD = 100
const MAX_ROTATION = 15

// Computed properties
const cardStyle = computed(() => ({
  transform: `translateX(${currentPos.value.x}px) translateY(${currentPos.value.y}px) rotate(${rotation.value}deg)`,
  zIndex: props.isTopCard ? 10 : 1,
  pointerEvents: props.isTopCard ? 'auto' : 'none'
}))

const showLikeIndicator = computed(() => currentPos.value.x > 50)
const showPassIndicator = computed(() => currentPos.value.x < -50)

// Touch/Mouse event handlers
function startDrag(event) {
  if (!props.isTopCard) return
  
  isDragging.value = true
  
  const clientX = event.type === 'mousedown' ? event.clientX : event.touches[0].clientX
  const clientY = event.type === 'mousedown' ? event.clientY : event.touches[0].clientY
  
  dragStartPos.value = { x: clientX, y: clientY }
  
  emit('dragStart')
  
  // Add event listeners
  if (event.type === 'mousedown') {
    document.addEventListener('mousemove', onDrag)
    document.addEventListener('mouseup', endDrag)
  } else {
    document.addEventListener('touchmove', onDrag, { passive: false })
    document.addEventListener('touchend', endDrag)
  }
  
  event.preventDefault()
}

function onDrag(event) {
  if (!isDragging.value) return
  
  const clientX = event.type === 'mousemove' ? event.clientX : event.touches[0].clientX
  const clientY = event.type === 'mousemove' ? event.clientY : event.touches[0].clientY
  
  const deltaX = clientX - dragStartPos.value.x
  const deltaY = clientY - dragStartPos.value.y
  
  currentPos.value = { x: deltaX, y: deltaY * 0.3 } // Reduce vertical movement
  rotation.value = (deltaX / window.innerWidth) * MAX_ROTATION * 2
  
  event.preventDefault()
}

function endDrag() {
  if (!isDragging.value) return
  
  const absX = Math.abs(currentPos.value.x)
  
  if (absX > SWIPE_THRESHOLD) {
    // Trigger swipe
    const direction = currentPos.value.x > 0 ? 'right' : 'left'
    const action = direction === 'right' ? 'like' : 'pass'
    
    // Animate card exit
    animateExit(direction)
    
    // Emit swipe event
    emit('swipe', { action, direction, profile: props.profile })
  } else {
    // Snap back to center
    animateReturn()
  }
  
  // Clean up event listeners
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', endDrag)
  document.removeEventListener('touchmove', onDrag)
  document.removeEventListener('touchend', endDrag)
  
  isDragging.value = false
  emit('dragEnd')
}

function animateExit(direction) {
  const exitX = direction === 'right' ? window.innerWidth : -window.innerWidth
  const exitRotation = direction === 'right' ? MAX_ROTATION : -MAX_ROTATION
  
  currentPos.value = { x: exitX, y: currentPos.value.y }
  rotation.value = exitRotation
  
  // Reset after animation
  setTimeout(() => {
    currentPos.value = { x: 0, y: 0 }
    rotation.value = 0
  }, 300)
}

function animateReturn() {
  currentPos.value = { x: 0, y: 0 }
  rotation.value = 0
}

// Programmatic swipe methods
function swipeLeft() {
  if (!props.isTopCard) return
  animateExit('left')
  emit('swipe', { action: 'pass', direction: 'left', profile: props.profile })
}

function swipeRight() {
  if (!props.isTopCard) return
  animateExit('right')
  emit('swipe', { action: 'like', direction: 'right', profile: props.profile })
}

// Expose methods to parent
defineExpose({
  swipeLeft,
  swipeRight
})

// Cleanup on unmount
onUnmounted(() => {
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', endDrag)
  document.removeEventListener('touchmove', onDrag)
  document.removeEventListener('touchend', endDrag)
})
</script>

<style scoped>
.swipe-card {
  position: absolute;
  width: 320px;
  height: 500px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  cursor: grab;
  transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  overflow: hidden;
  user-select: none;
}

.swipe-card.swiping {
  transition: none;
  cursor: grabbing;
}

.card-image {
  position: relative;
  height: 70%;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.match-score-badge {
  position: absolute;
  top: 16px;
  right: 16px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.action-indicator {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px;
  border-radius: 12px;
  font-weight: 700;
  font-size: 18px;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.action-indicator.active {
  opacity: 1;
}

.like-indicator {
  right: 20px;
  background: rgba(34, 197, 94, 0.9);
  color: white;
  border: 3px solid #22c55e;
}

.pass-indicator {
  left: 20px;
  background: rgba(239, 68, 68, 0.9);
  color: white;
  border: 3px solid #ef4444;
}

.card-info {
  height: 30%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.profile-header {
  margin-bottom: 12px;
}

.profile-name {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 100%;
}

.profile-location {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #6b7280;
  font-size: 14px;
  min-width: 0;
}

.profile-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #4b5563;
  font-size: 14px;
  min-width: 0;
}

.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Mobile responsiveness */
@media (max-width: 640px) {
  .swipe-card {
    width: 280px;
    height: 450px;
  }
  
  .profile-name {
    font-size: 20px;
  }
  
  .card-info {
    padding: 16px;
  }
}
</style>
