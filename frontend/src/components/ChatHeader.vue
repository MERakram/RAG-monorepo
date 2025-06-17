<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { model, platform, selectedCollection } from '../shared'
import { getPlatformIcon, getPlatformName } from '../utils'
import SelectModelModal from './SelectModelModal.vue'
import SelectCollectionModal from './SelectCollectionModal.vue' 
import LanguageSwitcher from './LanguageSwitcher.vue'
import { useAgentStore } from '../stores/agent'

const { t, locale } = useI18n()
const showSelectModelModal = ref(false)
const showSelectCollectionModal = ref(false) 
const showMobileMenu = ref(false)
const showSettingsDropdown = ref(false)
const router = useRouter()
const agentStore = useAgentStore()

const languages = [
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'fr', name: 'Français', flag: '🇫🇷' }
]

function switchLanguage(langCode: string) {
  locale.value = langCode
  localStorage.setItem('locale', langCode)
  showSettingsDropdown.value = false
}

async function handleLogout() {
  await agentStore.logout()
  showSettingsDropdown.value = false
  router.push({ name: 'signIn' })
}
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
    
    <!-- Static RAG display - visible on all devices -->
    <div class="flex items-center gap-2 px-3 py-2 text-sm font-medium lg:px-4 lg:py-2.5">
      <div class="text-lg leading-0">
        <component :is="() => getPlatformIcon(platform)" />
      </div>
      {{ getPlatformName(platform) }}
    </div>

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
          <span class="pl-2 text-sm font-medium">{{ t('chat.model') }}</span>
        </div>
        <button
          class="min-w-36 flex items-center justify-between rounded-full bg-[#1e1e1f] px-6 py-2 text-sm text-[#e3e3e3] transition-all focus:border-neutral-500/50 hover:bg-[#252526] focus:ring-2 focus:ring-neutral-500/20"
          @click="showSelectModelModal = true"
        >
          <span class="truncate pr-2">{{ model || t('chat.selectModelPlaceholder') }}</span>
          <i class="i-tabler-chevron-down text-xs opacity-60" />
        </button>
      </div>

      <!-- New Collection Selection for Desktop -->
      <div class="flex items-center gap-2">
        <div class="flex items-center pr-2 text-lg">
          <i class="i-tabler-database text-green-400" />
          <span class="pl-2 text-sm font-medium">{{ t('nav.normes') }}</span>
        </div>
        <button
          class="min-w-36 flex items-center justify-between rounded-full bg-[#1e1e1f] px-6 py-2 text-sm text-[#e3e3e3] transition-all focus:border-neutral-500/50 hover:bg-[#252526] focus:ring-2 focus:ring-neutral-500/20"
          @click="showSelectCollectionModal = true"
        >
          <span class="truncate pr-2">{{ selectedCollection || t('nav.selectNorme') }}</span>
          <i class="i-tabler-chevron-down text-xs opacity-60" />
        </button>
      </div>

      <!-- Settings Dropdown Button -->
      <div class="relative">
        <button
          class="flex items-center justify-center rounded-full p-2 text-lg hover:bg-neutral-8"
          @click="showSettingsDropdown = !showSettingsDropdown"
        >
          <i class="i-tabler-settings text-neutral-400" />
        </button>

        <!-- Settings Dropdown Menu -->
        <div
          v-if="showSettingsDropdown"
          class="absolute right-0 top-full mt-2 w-48 bg-[#1e1e1f] border border-neutral-700 rounded-lg shadow-lg z-50"
          @click.stop
        >
          <div class="p-2">
            <div class="px-3 py-2 text-xs font-medium text-neutral-400 uppercase tracking-wide">
              {{ t('translate.language') }}
            </div>
            <div class="space-y-1">
              <button
                v-for="lang in languages"
                :key="lang.code"
                class="w-full flex items-center gap-3 px-3 py-2 text-sm text-left rounded-md transition-colors hover:bg-neutral-700"
                :class="{ 'bg-neutral-700 text-white': locale === lang.code, 'text-neutral-300': locale !== lang.code }"
                @click="switchLanguage(lang.code)"
              >
                <span class="text-base">{{ lang.flag }}</span>
                <span>{{ lang.name }}</span>
                <i v-if="locale === lang.code" class="i-tabler-check ml-auto text-green-400" />
              </button>
            </div>
            
            <!-- Logout Button -->
            <div class="border-t border-neutral-700 mt-2 pt-2">
              <button
                class="w-full flex items-center gap-3 px-3 py-2 text-sm text-left rounded-md transition-colors hover:bg-red-600/20 text-red-400 hover:text-red-300"
                @click="handleLogout"
              >
                <i class="i-tabler-logout text-base" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Click outside to close dropdown -->
      <div
        v-if="showSettingsDropdown"
        class="fixed inset-0 z-40"
        @click="showSettingsDropdown = false"
      />
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
            {{ t('nav.settings') }}
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
              <i class="i-tabler-cube text-purple-400" />
              {{ t('chat.model') }}
            </label>
            <button
              class="w-full flex items-center justify-between rounded-lg bg-[#1e1e1f] px-4 py-2 text-sm text-[#e3e3e3] transition-all focus:border-neutral-500/50 hover:bg-[#252526] focus:ring-2 focus:ring-neutral-500/20"
              @click="showSelectModelModal = true; showMobileMenu = false"
            >
              <span class="truncate">{{ model || t('chat.selectModelPlaceholder') }}</span>
              <i class="i-tabler-chevron-down text-xs opacity-60" />
            </button>
          </div>

          <!-- New Collection Selection for Mobile Menu -->
          <div class="flex flex-col gap-2">
            <label class="flex items-center gap-2 text-sm font-medium">
              <i class="i-tabler-database text-green-400" />
              {{ t('nav.normes') }}
            </label>
            <button
              class="w-full flex items-center justify-between rounded-lg bg-[#1e1e1f] px-4 py-2 text-sm text-[#e3e3e3] transition-all focus:border-neutral-500/50 hover:bg-[#252526] focus:ring-2 focus:ring-neutral-500/20"
              @click="showSelectCollectionModal = true; showMobileMenu = false"
            >
              <span class="truncate">{{ selectedCollection || t('nav.selectNorme') }}</span>
              <i class="i-tabler-chevron-down text-xs opacity-60" />
            </button>
          </div>

          <!-- Language Switcher for Mobile -->
          <div class="flex flex-col gap-2">
            <label class="flex items-center gap-2 text-sm font-medium">
              <i class="i-tabler-language text-blue-400" />
              {{ t('translate.language') }}
            </label>
            <LanguageSwitcher />
          </div>

          <!-- Logout Button for Mobile -->
          <div class="border-t border-neutral-700 pt-4">
            <button
              class="w-full flex items-center gap-3 px-3 py-2 text-sm rounded-md transition-colors hover:bg-red-600/20 text-red-400 hover:text-red-300"
              @click="handleLogout"
            >
              <i class="i-tabler-logout text-base" />
              <span>Logout</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>