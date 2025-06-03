<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { apiKey, model, platform, selectedCollection } from '../shared'
import { getPlatformIcon, getPlatformName } from '../utils'
import SelectModelModal from './SelectModelModal.vue'
import SelectCollectionModal from './SelectCollectionModal.vue' 
import SelectPresetModal from './SelectPresetModal.vue' 

const showSelectModelModal = ref(false)
const showSelectCollectionModal = ref(false) 
const showMobileMenu = ref(false)
const showSelectPresetModal = ref(false)
const router = useRouter()
</script>

<template>
  <header class="flex flex-shrink-0 items-center justify-between gap-4 px-4 py-3 text-lg lg:h-72px lg:px-6">
    <!-- New Conversation Button for small screens -->
    <button
      class="flex items-center justify-center rounded-full p-2 text-lg lg:hidden hover:bg-neutral-8"
      @click="router.push('/')"
    >
      <i class="i-tabler-plus text-neutral-400" />
    </button>
    <!-- Platform selection (was Model selection) - visible on all devices -->
    <button
      class="flex cursor-pointer items-center gap-2 rounded-full px-3 py-2 text-sm font-medium transition-colors hover:bg-neutral-8 lg:px-4 lg:py-2.5"
      @click="showSelectPresetModal = true"
    >
      <div class="text-lg leading-0">
        <component :is="() => getPlatformIcon(platform)" />
      </div>
      {{ getPlatformName(platform) }}
      <i class="i-tabler-chevron-down ml-1 text-xs opacity-60" />
    </button>

    <SelectPresetModal
      v-model="showSelectPresetModal"
    />

    <SelectModelModal
      v-model="showSelectModelModal"
      v-model:selected-model="model"
    />
    <!-- New SelectCollectionModal component -->
    <SelectCollectionModal
      v-model="showSelectCollectionModal"
      v-model:selected-collection="selectedCollection"
    />
    <!-- Desktop view - row of inputs -->
    <div class="hidden lg:flex lg:items-center lg:gap-3">

      <div class="flex items-center gap-2">
        <div class="flex items-center pr-2 text-lg">
          <i class="i-tabler-cube text-purple-400" />
          <span class="pl-2 text-sm font-medium">Model</span>
        </div>
        <button
          class="min-w-36 flex items-center justify-between rounded-full bg-[#1e1e1f] px-6 py-2 text-sm text-[#e3e3e3] transition-all focus:border-neutral-500/50 hover:bg-[#252526] focus:ring-2 focus:ring-neutral-500/20"
          @click="showSelectModelModal = true"
        >
          <span class="truncate pr-2">{{ model || 'Select Model' }}</span>
          <i class="i-tabler-chevron-down text-xs opacity-60" />
        </button>
      </div>

      <!-- New Collection Selection for Desktop -->
      <div class="flex items-center gap-2">
        <div class="flex items-center pr-2 text-lg">
          <i class="i-tabler-database text-green-400" /> <!-- Collection icon -->
          <span class="pl-2 text-sm font-medium">Collection</span>
        </div>
        <button
          class="min-w-36 flex items-center justify-between rounded-full bg-[#1e1e1f] px-6 py-2 text-sm text-[#e3e3e3] transition-all focus:border-neutral-500/50 hover:bg-[#252526] focus:ring-2 focus:ring-neutral-500/20"
          @click="showSelectCollectionModal = true"
        >
          <span class="truncate pr-2">{{ selectedCollection || 'Select Collection' }}</span>
          <i class="i-tabler-chevron-down text-xs opacity-60" />
        </button>
      </div>
    </div>

    <!-- Mobile view - menu toggle -->
    <button
      class="flex items-center justify-center rounded-full p-2 text-lg lg:hidden hover:bg-neutral-8"
      @click="showMobileMenu = !showMobileMenu"
    >
      <i class="i-tabler-settings text-neutral-400" />
    </button>

    <!-- Mobile menu drawer -->
    <div
      v-if="showMobileMenu"
      class="fixed inset-0 z-50 bg-black/50 lg:hidden"
      @click.self="showMobileMenu = false"
    >
      <div class="absolute right-0 top-0 h-full w-64 bg-[#121212] p-4 shadow-lg">
        <div class="mb-6 flex items-center justify-between">
          <h3 class="text-lg font-medium">
            Settings
          </h3>
          <button
            class="rounded-full p-1 hover:bg-neutral-8"
            @click="showMobileMenu = false"
          >
            <i class="i-tabler-x text-lg" />
          </button>
        </div>

        <div class="flex flex-col gap-6">
          <div class="flex flex-col gap-2">
            <label class="flex items-center gap-2 text-sm font-medium">
              <i class="i-tabler-key text-blue-400" />
              API Key
            </label>
            <input
              v-model="apiKey"
              placeholder="API Key"
              class="w-full rounded-lg bg-[#1e1e1f] px-4 py-2 text-sm text-[#e3e3e3] outline-none transition-all focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20"
              type="password"
            >
          </div>

          <div class="flex flex-col gap-2">
            <label class="flex items-center gap-2 text-sm font-medium">
              <i class="i-tabler-cube text-purple-400" />
              Model
            </label>
            <button
              class="w-full flex items-center justify-between rounded-lg bg-[#1e1e1f] px-4 py-2 text-sm text-[#e3e3e3] transition-all focus:border-neutral-500/50 hover:bg-[#252526] focus:ring-2 focus:ring-neutral-500/20"
              @click="showSelectModelModal = true; showMobileMenu = false"
            >
              <span class="truncate">{{ model || 'Select Model' }}</span>
              <i class="i-tabler-chevron-down text-xs opacity-60" />
            </button>
          </div>

          <!-- New Collection Selection for Mobile Menu -->
          <div class="flex flex-col gap-2">
            <label class="flex items-center gap-2 text-sm font-medium">
              <i class="i-tabler-database text-green-400" /> <!-- Collection icon -->
              Collection
            </label>
            <button
              class="w-full flex items-center justify-between rounded-lg bg-[#1e1e1f] px-4 py-2 text-sm text-[#e3e3e3] transition-all focus:border-neutral-500/50 hover:bg-[#252526] focus:ring-2 focus:ring-neutral-500/20"
              @click="showSelectCollectionModal = true; showMobileMenu = false"
            >
              <span class="truncate">{{ selectedCollection || 'Select Collection' }}</span>
              <i class="i-tabler-chevron-down text-xs opacity-60" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>