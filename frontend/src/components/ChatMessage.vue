<script setup lang="ts">
import type { ChatMessage } from '../composables/useHelloWorld'
import StreamContent from './StreamContent.vue'
import UserChatMessage from './UserChatMessage.vue'
import ErrorChatMessage from './ErrorChatMessage.vue'

const props = defineProps<{
  message: ChatMessage
  loading: boolean
}>()
const message = computed(() => props.message)
const parsedContent = computed(() => {
  const content = message.value.content || ''
  
  // Check for file attachment in the format "content📎 filename"
  const fileMatch = content.match(/📎\s*(.+)$/)
  const hasFile = !!fileMatch
  const fileName = hasFile ? fileMatch[1].trim() : ''
  const textContent = hasFile ? content.replace(/📎\s*.+$/, '').trim() : content

  // Extract file size if available (this would need to be passed from the backend)
  // For now, we'll use a placeholder since the current implementation doesn't store file size
  const fileSize = hasFile ? '2.5MB' : '' // This should ideally come from the message data

  return {
    hasFile,
    fileName,
    fileSize,
    textContent,
  }
})
</script>

<template>
  <!-- User message - right aligned with max width 50% -->
  <div
    v-if="message.role === 'user'"
    class="w-full max-w-5xl mx-auto px-4 py-6 flex justify-end"
  >
    <div class="flex flex-col items-end gap-3 max-w-[50%]">
      <!-- Message container -->
      <div class="flex items-end gap-3">
        <div class="bg-neutral-700/60 backdrop-blur-sm rounded-2xl px-4 py-3 border border-neutral-600/30">
          <UserChatMessage :content="parsedContent.textContent" />
        </div>
        <div class="flex-shrink-0 w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center">
          <i class="i-fluent-person-28-filled text-white text-sm" />
        </div>
      </div>
      
      <!-- File attachment display - matching prompt bar container styling -->
      <div v-if="parsedContent.hasFile" class="flex items-center gap-2 px-3 py-1.5 bg-neutral-8/80 rounded-lg border border-neutral-7/50 shadow-sm backdrop-blur-sm max-w-sm">
        <div class="flex items-center justify-center w-6 h-6 bg-red-400/20 rounded-md">
          <i class="i-tabler-file-type-pdf text-red-400 text-xs" />
        </div>
        <div class="flex-1 min-w-0">
          <div class="text-xs text-neutral-200 font-medium truncate">
            {{ parsedContent.fileName.length > 25 ? parsedContent.fileName.substring(0, 22) + '...' : parsedContent.fileName }}
          </div>
          <div class="text-xs text-neutral-400 leading-tight">
            {{ parsedContent.fileSize }}
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Assistant message - left aligned with more spacing -->
  <div
    v-else-if="message.role === 'assistant'"
    class="w-full max-w-5xl mx-auto px-4 py-6 flex justify-start"
  >
    <div class="flex items-start gap-3 w-full">
      <div class="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center">
        <i 
          class="i-fluent-bot-48-filled text-white text-sm"
          :class="{ 'animate-pulse': loading && message.role === 'assistant' }"
        />
      </div>
      <div class="flex-1 py-1">
        <StreamContent
          :content="message.content"
          :reasoning="message.reasoning"
          :loading="loading"
        />
      </div>
    </div>
  </div>

  <!-- Error message - left aligned with error styling -->
  <div
    v-else-if="message.role === 'error'"
    class="w-full max-w-5xl mx-auto px-4 py-6 flex justify-start"
  >
    <div class="max-w-[70%] flex items-start gap-3">
      <div class="flex-shrink-0 w-8 h-8 rounded-full bg-red-500 flex items-center justify-center">
        <i class="i-fluent-error-circle-24-filled text-white text-sm" />
      </div>
      <div class="flex-1 py-1">
        <ErrorChatMessage :content="message.content" />
      </div>
    </div>
  </div>
</template>