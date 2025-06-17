<script setup lang="ts">
import { Btn } from '@roku-ui/vue'
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useCollections } from '../composables/useCollections' // New composable

const { t } = useI18n()

// Define models
const modelValue = defineModel<boolean>() // For v-model (visibility)
const currentSelectedCollection = defineModel<string | null | undefined>('selectedCollection')

// Search functionality
const searchQuery = ref('')
const collections = useCollections() // Use the new composable

const highlightedIndex = ref(-1)
const modalRef = ref<HTMLElement | null>(null)
const searchInputRef = ref<HTMLInputElement | null>(null)

const filteredCollections = computed(() => {
  if (!searchQuery.value) {
    return collections.value
  }
  const query = searchQuery.value.toLowerCase()
  return collections.value.filter(collection =>
    collection.toLowerCase().includes(query),
  )
})

watch([searchQuery], () => {
  highlightedIndex.value = -1
})

function handleKeyDown(event: KeyboardEvent) {
  if (!modelValue.value) return // Only handle keys if modal is open

  switch (event.key) {
    case 'Escape':
      closeModal()
      break
    case 'ArrowDown':
      event.preventDefault()
      if (filteredCollections.value.length > 0) {
        highlightedIndex.value = (highlightedIndex.value + 1) % filteredCollections.value.length
      }
      break
    case 'ArrowUp':
      event.preventDefault()
      if (filteredCollections.value.length > 0) {
        highlightedIndex.value = (highlightedIndex.value - 1 + filteredCollections.value.length) % filteredCollections.value.length
      }
      break
    case 'Enter':
      if (highlightedIndex.value >= 0 && filteredCollections.value[highlightedIndex.value]) {
        updateCollection(filteredCollections.value[highlightedIndex.value])
        event.stopPropagation()
      }
      break
    default:
      // Allow typing in search input
      break
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown)
  watch(modelValue, (newValue) => {
    if (newValue) {
      searchQuery.value = '' // Reset search on open
      highlightedIndex.value = -1
      // Focus search input when modal opens
      setTimeout(() => searchInputRef.value?.focus(), 0)
    }
  })
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleKeyDown)
})

// Update collection function
function updateCollection(collectionName: string | null | undefined) {
  currentSelectedCollection.value = collectionName
  modelValue.value = false // Close modal after selection
}

// Close modal
function closeModal() {
  modelValue.value = false
  searchQuery.value = '' // Reset search on close
}
</script>

<template>
  <Teleport to="body">
    <Transition
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
      enter-active-class="transition ease-out duration-200"
      leave-active-class="transition ease-in duration-150"
    >
      <div
        v-if="modelValue"
        ref="modalRef"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm"
        @click.self="closeModal"
      >
        <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 mx-4 max-w-md w-full overflow-hidden rounded-xl bg-[#1a1a1a] shadow-lg">
          <div class="flex items-center justify-between border-b border-neutral-800 p-4">
            <h3 class="text-lg text-white font-medium">
              {{ t('nav.selectNorme') }}
            </h3>
            <Btn
              icon
              rounded="full"
              color="white"
              variant="transparent"
              hover-variant="light"
              @click="closeModal"
            >
              <i class="i-tabler-x text-xl" />
            </Btn>
          </div>

          <!-- Search bar -->
          <div class="border-b border-neutral-800 p-4">
            <div class="relative">
              <i class="i-tabler-search absolute left-3 top-1/2 transform text-neutral-400 -translate-y-1/2" />
              <input
                ref="searchInputRef"
                v-model="searchQuery"
                type="text"
                class="w-full rounded-lg bg-neutral-800 p-2 pl-10 pr-8 text-white outline-none transition-colors focus:bg-neutral-700 focus:ring-2 focus:ring-neutral-600 placeholder-neutral-500"
                :placeholder="t('common.search') + ' ' + t('nav.normes').toLowerCase() + '...'"
              >
              <button
                v-if="searchQuery"
                class="absolute right-3 top-1/2 transform text-neutral-400 transition-colors -translate-y-1/2 hover:text-white"
                @click="searchQuery = ''"
              >
                <i class="i-tabler-x text-sm" />
              </button>
            </div>
          </div>

          <div class="max-h-96 overflow-y-auto p-2">
            <div v-if="filteredCollections.length > 0">
              <div
                v-for="(collectionOption, index) in filteredCollections"
                :key="collectionOption"
                class="mb-1 flex cursor-pointer items-center gap-3 rounded-lg p-3 transition-colors hover:bg-neutral-800"
                :class="{ 'bg-neutral-700': collectionOption === currentSelectedCollection || index === highlightedIndex }"
                @click="updateCollection(collectionOption)"
              >
                <div class="h-8 w-8 flex flex-shrink-0 items-center justify-center rounded-full bg-neutral-800">
                  <i class="i-tabler-database text-green-400" /> <!-- Collection icon -->
                </div>
                <div class="flex flex-col">
                  <span class="truncate text-sm text-white font-medium">{{ collectionOption }}</span>
                  <!-- You might want to add a description or other info here -->
                </div>
                <div class="ml-auto flex-shrink-0">
                  <i
                    v-if="collectionOption === currentSelectedCollection"
                    class="i-tabler-check text-green-400"
                  />
                </div>
              </div>
            </div>
            <div
              v-else
              class="p-4 text-center text-neutral-400"
            >
              <i class="i-tabler-info-circle text-xl" />
              <p class="mt-2">
                {{ t('messages.noNormesFound') }}
              </p>
            </div>
          </div>

          <div class="flex justify-end border-t border-neutral-800 p-4">
            <button
              class="rounded-lg bg-neutral-700 px-4 py-2 text-sm text-white font-medium transition-colors hover:bg-neutral-600"
              @click="closeModal"
            >
              {{ t('common.close') }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>