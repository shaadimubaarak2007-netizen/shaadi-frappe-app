<template>
  <div :class="containerClass">
    <div class="relative">
      <svg :width="svgSize" :height="svgSize" class="transform -rotate-90">
        <!-- Background circle -->
        <circle
          :cx="center"
          :cy="center"
          :r="radius"
          :stroke-width="strokeWidth"
          stroke="currentColor"
          class="text-gray-200"
          fill="none"
        />
        <!-- Progress circle -->
        <circle
          :cx="center"
          :cy="center"
          :r="radius"
          :stroke-width="strokeWidth"
          :stroke="strokeColor"
          fill="none"
          :stroke-dasharray="circumference"
          :stroke-dashoffset="dashOffset"
          stroke-linecap="round"
          class="transition-all duration-500"
        />
      </svg>
      <div class="absolute inset-0 flex items-center justify-center">
        <span :class="textClass">{{ score }}%</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  score: {
    type: Number,
    required: true,
    validator: (value) => value >= 0 && value <= 100
  },
  size: {
    type: String,
    default: 'md', // sm, md, lg
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  }
})

const sizes = {
  sm: { svg: 60, stroke: 4, text: 'text-xs' },
  md: { svg: 80, stroke: 6, text: 'text-sm' },
  lg: { svg: 120, stroke: 8, text: 'text-lg' }
}

const config = computed(() => sizes[props.size])
const svgSize = computed(() => config.value.svg)
const strokeWidth = computed(() => config.value.stroke)
const textClass = computed(() => `font-bold ${config.value.text}`)
const center = computed(() => svgSize.value / 2)
const radius = computed(() => (svgSize.value - strokeWidth.value) / 2)
const circumference = computed(() => 2 * Math.PI * radius.value)
const dashOffset = computed(() => circumference.value - (props.score / 100) * circumference.value)

const containerClass = computed(() => {
  const base = 'inline-flex items-center justify-center'
  return base
})

const strokeColor = computed(() => {
  if (props.score >= 80) return '#10B981' // green
  if (props.score >= 60) return '#F59E0B' // yellow
  if (props.score >= 40) return '#F97316' // orange
  return '#EF4444' // red
})
</script>
