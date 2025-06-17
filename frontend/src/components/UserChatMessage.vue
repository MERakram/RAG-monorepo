<script setup lang="ts">
const props = defineProps<{
  content: string
}>()
</script>

<template>
  <div class="flex-1">
    <pre
      class="whitespace-pre-wrap font-inherit text-neutral-100 leading-relaxed text-base"
      v-text="props.content"
    />
  </div>
</template>
