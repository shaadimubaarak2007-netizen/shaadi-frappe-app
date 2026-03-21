<template>
  <div
    class="bg-white rounded-lg border border-default p-6 hover-lift cursor-pointer transition-all"
    :class="{ 'ring-2 ring-primary-200': active }"
    @click="handleClick"
  >
    <div class="flex items-start gap-4">
      <!-- Icon -->
      <div
        class="p-2.5 rounded-full ring ring-inset flex-shrink-0"
        :class="iconClasses"
      >
        <FeatherIcon :name="icon" class="w-5 h-5" />
      </div>

      <!-- Content -->
      <div class="flex-1 min-w-0">
        <p class="text-xs font-normal text-muted uppercase tracking-wide mb-1.5">
          {{ title }}
        </p>
        <div class="flex items-center gap-2">
          <span class="text-2xl font-semibold text-highlighted">
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
        <p v-if="subtitle" class="text-sm text-muted mt-1">
          {{ subtitle }}
        </p>
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
    pink: 'bg-pink-50 text-pink-600',
    purple: 'bg-purple-50 text-purple-600',
    blue: 'bg-blue-50 text-blue-600',
    green: 'bg-green-50 text-green-600',
    orange: 'bg-orange-50 text-orange-600'
  }
  const baseClass = colorMap[props.color] || colorMap.pink
  return `${baseClass} ring-primary-inset/25`
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
