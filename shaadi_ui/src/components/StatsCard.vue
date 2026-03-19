<template>
  <div
    class="bg-white rounded-lg border border-gray-200 p-6 hover-lift cursor-pointer transition-all"
    :class="{ 'ring-2 ring-primary-200': active }"
    @click="handleClick"
  >
    <div class="flex items-start justify-between">
      <!-- Content -->
      <div class="flex-1">
        <p class="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">
          {{ title }}
        </p>
        <div class="flex items-baseline gap-2 mb-1">
          <span class="text-2xl font-semibold text-gray-900">
            {{ formattedValue }}
          </span>
          <Badge
            v-if="variation !== null && variation !== undefined"
            :variant="variation > 0 ? 'success' : 'error'"
            size="sm"
            class="text-xs"
          >
            {{ variation > 0 ? '+' : '' }}{{ variation }}%
          </Badge>
        </div>
        <p v-if="subtitle" class="text-sm text-gray-600">
          {{ subtitle }}
        </p>
      </div>

      <!-- Icon -->
      <div
        class="p-2.5 rounded-full ring ring-inset"
        :class="iconClasses"
      >
        <FeatherIcon :name="icon" class="w-5 h-5" />
      </div>
    </div>

    <!-- Optional Footer -->
    <div v-if="$slots.footer" class="mt-4 pt-4 border-t border-gray-100">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Badge, FeatherIcon } from 'frappe-ui'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [String, Number],
    required: true
  },
  icon: {
    type: String,
    required: true
  },
  variation: {
    type: Number,
    default: null
  },
  subtitle: {
    type: String,
    default: ''
  },
  formatter: {
    type: Function,
    default: null
  },
  color: {
    type: String,
    default: 'pink',
    validator: (value) => ['pink', 'purple', 'blue', 'green', 'orange'].includes(value)
  },
  active: {
    type: Boolean,
    default: false
  },
  to: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['click'])

const formattedValue = computed(() => {
  if (props.formatter) {
    return props.formatter(props.value)
  }
  return props.value
})

const iconClasses = computed(() => {
  const colorMap = {
    pink: 'bg-pink-100 ring-pink-200 text-pink-600',
    purple: 'bg-purple-100 ring-purple-200 text-purple-600',
    blue: 'bg-blue-100 ring-blue-200 text-blue-600',
    green: 'bg-green-100 ring-green-200 text-green-600',
    orange: 'bg-orange-100 ring-orange-200 text-orange-600'
  }
  return colorMap[props.color] || colorMap.pink
})

const handleClick = () => {
  if (props.to) {
    // Navigate if 'to' prop is provided
    emit('click', props.to)
  } else {
    emit('click')
  }
}
</script>

<style scoped>
.hover-lift {
  transition: transform 200ms cubic-bezier(0.4, 0, 0.2, 1),
              box-shadow 200ms cubic-bezier(0.4, 0, 0.2, 1);
}

.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
}
</style>
