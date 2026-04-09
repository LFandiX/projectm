<template>
  <div :class="['rounded-lg shadow-sm p-4 flex items-center', color]">
    <div class="text-3xl mr-4">{{ icon }}</div>
    <div>
      <h3 class="text-sm text-gray-600 font-medium">{{ title }}</h3>
      <p class="text-xl font-semibold text-gray-800">{{ value }}</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title: String,
    value: String,
    icon: String,
    color: {
      type: String,
      default: 'bg-white'
    }
  }
}
</script>
