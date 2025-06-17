<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

const languages = [
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'fr', name: 'Français', flag: '🇫🇷' }
]

function switchLanguage(langCode: string) {
  locale.value = langCode
  localStorage.setItem('locale', langCode)
}
</script>

<template>
  <div class="relative">
    <select
      :value="locale"
      class="appearance-none bg-neutral-800 border border-neutral-700 rounded-lg px-3 py-2 text-sm text-white focus:border-neutral-500 focus:outline-none cursor-pointer"
      @change="switchLanguage(($event.target as HTMLSelectElement).value)"
    >
      <option
        v-for="lang in languages"
        :key="lang.code"
        :value="lang.code"
      >
        {{ lang.flag }} {{ lang.name }}
      </option>
    </select>
  </div>
</template>