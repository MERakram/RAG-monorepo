<script setup lang="ts">
import { BtnGroup, Paper } from '@roku-ui/vue'
import StreamContent from '../components/StreamContent.vue'
import { model, selectedCollection } from '../shared'
import { streamCompareStandards } from '../composables/useRAG'
import { useScrollToBottom } from '../composables/useScrollToBottom'
import { useI18n } from 'vue-i18n'
import { toast } from 'vue-sonner'
import { watchEffect } from 'vue'
import { DEFAULT_TOAST_DURATION } from '../shared/constants'

const { t } = useI18n()
const router = useRouter()

// File upload state
const file1 = ref<File | null>(null)
const file2 = ref<File | null>(null)
const file1Content = ref('')
const file2Content = ref('')
const isDragging1 = ref(false)
const isDragging2 = ref(false)
const isHovering1 = ref(false)
const isHovering2 = ref(false)

// Comparison state
const compareMode = useLocalStorage<'technical' | 'compliance' | 'differences' | 'similarities'>('compare.mode', 'technical')
const comparisonResult = ref('')
const loading = ref(false)

// Scroll management (after loading is declared)
const scrollContainer = ref<HTMLElement | null>(null)
const enableAutoScroll = ref(true)

// Use the scroll to bottom composable
useScrollToBottom(scrollContainer, 50, enableAutoScroll)

// Watch for streaming state to manage auto-scroll
watchEffect(() => {
  if (loading.value) {
    enableAutoScroll.value = true
  }
})

// File handling functions
function handleDrop1(e: DragEvent) {
  e.preventDefault()
  e.stopPropagation()
  isDragging1.value = false
  isHovering1.value = false
  const files = e.dataTransfer?.files
  if (files && files.length > 0) {
    handleFileSelect(files[0], 1)
  }
}

function handleDrop2(e: DragEvent) {
  e.preventDefault()
  e.stopPropagation()
  isDragging2.value = false
  isHovering2.value = false
  const files = e.dataTransfer?.files
  if (files && files.length > 0) {
    handleFileSelect(files[0], 2)
  }
}

function handleDragOver(e: DragEvent) {
  e.preventDefault()
  e.stopPropagation()
}

function handleDragEnter1(e: DragEvent) {
  e.preventDefault()
  e.stopPropagation()
  isDragging1.value = true
}

function handleDragLeave1(e: DragEvent) {
  e.preventDefault()
  e.stopPropagation()
  // Only hide if leaving the dropzone completely
  const target = e.currentTarget as HTMLElement
  const related = e.relatedTarget as Node
  if (!target || !target.contains(related)) {
    isDragging1.value = false
  }
}

function handleDragEnter2(e: DragEvent) {
  e.preventDefault()
  e.stopPropagation()
  isDragging2.value = true
}

function handleDragLeave2(e: DragEvent) {
  e.preventDefault()
  e.stopPropagation()
  // Only hide if leaving the dropzone completely
  const target = e.currentTarget as HTMLElement
  const related = e.relatedTarget as Node
  if (!target || !target.contains(related)) {
    isDragging2.value = false
  }
}

function handleMouseEnter1() {
  isHovering1.value = true
}

function handleMouseLeave1() {
  isHovering1.value = false
}

function handleMouseEnter2() {
  isHovering2.value = true
}

function handleMouseLeave2() {
  isHovering2.value = false
}

function handleFileInput1(e: Event) {
  const input = e.target as HTMLInputElement
  if (input.files && input.files.length > 0) {
    handleFileSelect(input.files[0], 1)
  }
}

function handleFileInput2(e: Event) {
  const input = e.target as HTMLInputElement
  if (input.files && input.files.length > 0) {
    handleFileSelect(input.files[0], 2)
  }
}

async function handleFileSelect(file: File, slot: 1 | 2) {
  // Validate file type
  const allowedTypes = ['.pdf', '.txt', '.doc', '.docx', '.md']
  const fileName = file.name.toLowerCase()
  const isValidType = allowedTypes.some(type => fileName.endsWith(type))
  
  if (!isValidType) {
    toast.error(t('compare.errors.invalidFileType'), {
      description: t('compare.errors.invalidFileTypeDetail'),
      duration: DEFAULT_TOAST_DURATION,
    })
    return
  }

  if (slot === 1) {
    file1.value = file
    file1Content.value = await readFileContent(file)
  } else {
    file2.value = file
    file2Content.value = await readFileContent(file)
  }
}

async function readFileContent(file: File): Promise<string> {
  if (file.type === 'application/pdf') {
    // For PDF files, we'll need to extract text
    // This is a simplified version - in production you might want to use PDF.js
    return `[PDF Content from ${file.name}] - PDF text extraction would be implemented here`
  } else {
    // For text-based files
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.onload = () => resolve(reader.result as string)
      reader.onerror = reject
      reader.readAsText(file)
    })
  }
}

function removeFile(slot: 1 | 2) {
  if (slot === 1) {
    file1.value = null
    file1Content.value = ''
  } else {
    file2.value = null
    file2Content.value = ''
  }
}

// Comparison function
async function generateComparison() {
  if (!file1.value || !file2.value) {
    toast.error(t('compare.errors.missingFiles'), {
      description: t('compare.errors.missingFilesDetail'),
      duration: DEFAULT_TOAST_DURATION,
    })
    return
  }

  if (!model.value) {
    toast.error(t('compare.errors.noModelSelected'), {
      description: t('compare.errors.noModelSelectedDetail'),
      duration: DEFAULT_TOAST_DURATION,
    })
    return
  }

  if (!selectedCollection.value) {
    toast.error(t('compare.errors.noCollectionSelected'), {
      description: t('compare.errors.noCollectionSelectedDetail'),
      duration: DEFAULT_TOAST_DURATION,
    })
    return
  }

  loading.value = true
  comparisonResult.value = ''

  try {
    // Use the streamCompareStandards function from useRAG composable
    const stream = streamCompareStandards(
      file1Content.value,
      file1.value.name,
      file2Content.value,
      file2.value.name,
      compareMode.value
    )

    for await (const chunk of stream) {
      if (chunk.content) {
        comparisonResult.value += chunk.content
      }
    }
  } catch (error: any) {
    console.error('Comparison error:', error)
    toast.error(t('compare.errors.comparisonFailed'), {
      description: error.message || t('compare.errors.comparisonFailedDetail'),
      duration: DEFAULT_TOAST_DURATION,
    })
  } finally {
    loading.value = false
  }
}

function onHomeClick() {
  router.push('/')
}
</script>

<template>
  <BaseContainer>
    <AsideContainer>
      <div class="mt-104px pb-4">
        <button
          class="min-w-130px flex items-center gap-4 rounded-full bg-neutral-8 px-4 py-3 leading-0 disabled:pointer-events-none hover:bg-neutral-7 disabled:op-50"
          @click="onHomeClick"
        >
          <i class="i-tabler-home h-5 w-5" />
          <span class="flex-grow-1 text-sm">
            {{ t('common.home') }}
          </span>
        </button>
      </div>
    </AsideContainer>
    <MainContainer>
      <ChatHeader />
      <div
        ref="scrollContainer"
        is="main"
        class="h-full flex flex-col overflow-x-hidden overflow-y-auto"
      >
        <div class="m-auto max-w-6xl w-full flex flex-col gap-6 px-4 py-8 font-medium">
          <!-- Header -->
          <div>
            <div class="mb-8 text-3.5rem">
              <div class="gradient-text">
                {{ t('compare.title') }}
              </div>
            </div>
            
            <!-- Comparison Mode Selection -->
            <div class="animate-fade-delay mb-8">
              <div class="mb-4 text-lg font-medium">{{ t('compare.analysisMode') }}</div>
              <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
                <BtnGroup
                  v-model="compareMode"
                  color="primary"
                  class="shadow-md children:py-3 children:h-full! children:min-w-120px! children:border-neutral-700! first-children:rounded-2xl last-children:rounded-2xl"
                  :unselectable="false"
                  :selections="[
                    { label: t('compare.modes.technical'), value: 'technical' },
                    { label: t('compare.modes.compliance'), value: 'compliance' },
                    { label: t('compare.modes.differences'), value: 'differences' },
                    { label: t('compare.modes.similarities'), value: 'similarities' },
                  ]"
                />
                
                <!-- Generate Comparison Button (moved here) -->
                <button
                  :disabled="!file1 || !file2 || loading"
                  class="px-5 py-2 bg-gradient-to-r from-primary-500 to-primary-600 text-white rounded-xl font-medium text-base transition-all hover:from-primary-600 hover:to-primary-700 hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed border border-primary-300/50 relative overflow-hidden group flex items-center shadow-md"
                  @click="generateComparison"
                >
                  <span class="absolute inset-0 border border-primary-300/0 rounded-xl transition-all duration-300 group-hover:border-primary-300/80 group-hover:scale-105 group-hover:opacity-70"></span>
                  <i v-if="loading" class="i-tabler-loader h-4 w-4 animate-spin mr-2" />
                  <i v-else class="i-tabler-analyze h-4 w-4 mr-2" />
                  {{ loading ? t('compare.generatingComparison') : t('compare.generateComparison') }}
                </button>
              </div>
            </div>

            <!-- File Upload Areas -->
            <div class="animate-fade-delay grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
              <!-- File 1 Upload -->
              <div class="relative">
                <h3 class="mb-4 text-lg font-medium">{{ t('compare.standard1') }}</h3>
                <div
                  :class="{
                    'border-primary-500 bg-primary-500/10 scale-102': isDragging1,
                    'border-green-500 bg-green-500/10': file1,
                    'border-neutral-700': !isDragging1 && !file1,
                    'border-neutral-600 bg-neutral-800/80 scale-101': isHovering1 && !file1 && !isDragging1
                  }"
                  class="relative h-200px flex flex-col items-center justify-center border-2 border-dashed rounded-2xl bg-neutral-800/50 p-6 transition-all duration-200 ease-out cursor-pointer"
                  @drop="handleDrop1"
                  @dragover="handleDragOver"
                  @dragenter="handleDragEnter1"
                  @dragleave="handleDragLeave1"
                  @mouseenter="handleMouseEnter1"
                  @mouseleave="handleMouseLeave1"
                >
                  <input
                    v-if="!file1"
                    type="file"
                    accept=".pdf,.txt,.doc,.docx,.md"
                    class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    @change="handleFileInput1"
                  >
                  
                  <div v-if="!file1" class="text-center">
                    <i 
                      :class="{
                        'text-primary-400 scale-110': isDragging1,
                        'text-neutral-300': isHovering1,
                        'text-neutral-400': !isHovering1 && !isDragging1
                      }"
                      class="i-tabler-cloud-upload h-12 w-12 mb-4 transition-all duration-200" 
                    />
                    <p 
                      :class="{
                        'text-primary-300': isDragging1,
                        'text-neutral-200': isHovering1,
                        'text-neutral-300': !isHovering1 && !isDragging1
                      }"
                      class="text-lg mb-2 transition-colors duration-200"
                    >
                      {{ t('compare.dropFileHere') }}
                    </p>
                    <p class="text-sm text-neutral-500">{{ t('compare.supportedFormats') }}</p>
                  </div>
                  
                  <div v-else class="text-center w-full pointer-events-none">
                    <i class="i-tabler-file-check h-12 w-12 text-green-400/80 mb-4" />
                    <p class="text-lg text-green-300/80 mb-2 max-w-full truncate" :title="file1.name">{{ file1.name }}</p>
                    <p class="text-sm text-neutral-400 mb-4">
                      {{ (file1.size / 1024 / 1024).toFixed(2) }} MB
                    </p>
                    <button
                      class="px-4 py-2 bg-red-600/80 text-white rounded-lg hover:bg-red-700 transition-colors pointer-events-auto"
                      @click.stop.prevent="removeFile(1)"
                    >
                      {{ t('common.remove') }}
                    </button>
                  </div>
                </div>
              </div>

              <!-- File 2 Upload -->
              <div class="relative">
                <h3 class="mb-4 text-lg font-medium">{{ t('compare.standard2') }}</h3>
                <div
                  :class="{
                    'border-primary-500 bg-primary-500/10 scale-102': isDragging2,
                    'border-green-500 bg-green-500/10': file2,
                    'border-neutral-700': !isDragging2 && !file2,
                    'border-neutral-600 bg-neutral-800/80 scale-101': isHovering2 && !file2 && !isDragging2
                  }"
                  class="relative h-200px flex flex-col items-center justify-center border-2 border-dashed rounded-2xl bg-neutral-800/50 p-6 transition-all duration-200 ease-out cursor-pointer"
                  @drop="handleDrop2"
                  @dragover="handleDragOver"
                  @dragenter="handleDragEnter2"
                  @dragleave="handleDragLeave2"
                  @mouseenter="handleMouseEnter2"
                  @mouseleave="handleMouseLeave2"
                >
                  <input
                    v-if="!file2"
                    type="file"
                    accept=".pdf,.txt,.doc,.docx,.md"
                    class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    @change="handleFileInput2"
                  >
                  
                  <div v-if="!file2" class="text-center">
                    <i 
                      :class="{
                        'text-primary-400 scale-110': isDragging2,
                        'text-neutral-300': isHovering2,
                        'text-neutral-400': !isHovering2 && !isDragging2
                      }"
                      class="i-tabler-cloud-upload h-12 w-12 mb-4 transition-all duration-200" 
                    />
                    <p 
                      :class="{
                        'text-primary-300': isDragging2,
                        'text-neutral-200': isHovering2,
                        'text-neutral-300': !isHovering2 && !isDragging2
                      }"
                      class="text-lg mb-2 transition-colors duration-200"
                    >
                      {{ t('compare.dropFileHere') }}
                    </p>
                    <p class="text-sm text-neutral-500">{{ t('compare.supportedFormats') }}</p>
                  </div>
                  
                  <div v-else class="text-center w-full pointer-events-none">
                    <i class="i-tabler-file-check h-12 w-12 text-green-400/80 mb-4" />
                    <p class="text-lg text-green-300/80 mb-2 max-w-full truncate" :title="file2.name">{{ file2.name }}</p>
                    <p class="text-sm text-neutral-400 mb-4">
                      {{ (file2.size / 1024 / 1024).toFixed(2) }} MB
                    </p>
                    <button
                      class="px-4 py-2 bg-red-600/80 text-white rounded-lg hover:bg-red-700 transition-colors pointer-events-auto"
                      @click.stop.prevent="removeFile(2)"
                    >
                      {{ t('common.remove') }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Comparison Result -->
          <Paper
            v-if="comparisonResult || loading"
            :loading="loading"
            class="animate-fade-delay bg-surface-low/80 min-h-200px flex-shrink-1 border border-neutral-700/50 p-6 shadow-lg backdrop-blur-sm rounded-2xl!"
          >
            <!-- Show loading text when starting, even during streaming -->
            <div
              v-if="loading"
              class="flex items-center justify-center py-8 text-neutral-400"
            >
              <div class="text-center">
                <div class="loader border-primary-400 h-6 w-6 animate-spin border-t-2 border-b-transparent border-l-transparent border-r-transparent rounded-full mx-auto mb-3" />
                <p class="text-sm">{{ t('compare.analyzing') }}</p>
              </div>
            </div>
            
            <!-- Stream content below the loading indicator -->
            <StreamContent
              v-if="comparisonResult"
              class="max-w-full"
              :content="comparisonResult"
              :loading="loading"
            />
            
            <!-- Show when not loading and no content -->
            <div
              v-else-if="!loading && !comparisonResult"
              class="flex items-center justify-center py-8 text-neutral-500"
            >
              <p class="text-sm italic">{{ t('compare.noResults') }}</p>
            </div>
          </Paper>
        </div>
      </div>
    </MainContainer>
  </BaseContainer>
</template>