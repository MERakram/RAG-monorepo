<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { toast } from 'vue-sonner'
import { DEFAULT_TOAST_DURATION } from '../shared/constants'

const { t } = useI18n()

const props = defineProps<{
  modelValue?: File | null
  disabled?: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [file: File | null]
  'file-selected': [file: File]
  'file-removed': []
}>()

const fileInputRef = ref<HTMLInputElement | null>(null)
const isDragging = ref(false)

const selectedFile = computed({
  get: () => props.modelValue,
  set: (value: File | null) => emit('update:modelValue', value)
})

function handleFileSelect(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  
  if (file && validateFile(file)) {
    selectedFile.value = file
    emit('file-selected', file)
  }
}

function handleDrop(event: DragEvent) {
  event.preventDefault()
  isDragging.value = false
  
  if (props.disabled) return
  
  const files = event.dataTransfer?.files
  const file = files?.[0]
  
  if (file && validateFile(file)) {
    selectedFile.value = file
    emit('file-selected', file)
  }
}

function handleDragOver(event: DragEvent) {
  event.preventDefault()
  if (!props.disabled) {
    isDragging.value = true
  }
}

function handleDragLeave(event: DragEvent) {
  event.preventDefault()
  // Only set to false if we're leaving the entire drop zone
  const currentTarget = event.currentTarget as HTMLElement
  const relatedTarget = event.relatedTarget as Node
  if (!currentTarget?.contains(relatedTarget)) {
    isDragging.value = false
  }
}

function validateFile(file: File): boolean {
  const validTypes = ['application/pdf']
  const maxSize = 10 * 1024 * 1024 // 10MB
  
  if (!validTypes.includes(file.type)) {
    toast.error(t('chat.fileUpload.invalidFileType'), {
      description: t('chat.fileUpload.invalidFileTypeDetail'),
      duration: DEFAULT_TOAST_DURATION,
    })
    return false
  }
  
  if (file.size > maxSize) {
    toast.error(t('chat.fileUpload.fileTooLarge'), {
      description: t('chat.fileUpload.fileTooLargeDetail'),
      duration: DEFAULT_TOAST_DURATION,
    })
    return false
  }
  
  return true
}

function removeFile() {
  selectedFile.value = null
  emit('file-removed')
  if (fileInputRef.value) {
    fileInputRef.value.value = ''
  }
}

function openFileDialog() {
  if (!props.disabled && fileInputRef.value) {
    fileInputRef.value.click()
  }
}

function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// Expose methods to be called by the parent component
defineExpose({
  openFileDialog,
  removeFile
})
</script>

<template>
  <div class="file-upload-container">
    <!-- Hidden file input -->
    <input
      ref="fileInputRef"
      type="file"
      accept=".pdf"
      style="display: none"
      :disabled="disabled"
      @change="handleFileSelect"
    />
    
    <!-- Drop zone (shown when no file is selected) -->
    <div 
      v-if="!selectedFile"
      class="drop-zone"
      :class="{
        'drop-zone-active': isDragging,
        'drop-zone-disabled': disabled
      }"
      @click="openFileDialog"
      @drop="handleDrop"
      @dragover="handleDragOver"
      @dragleave="handleDragLeave"
    >
      <div class="drop-zone-content">
        <i class="i-tabler-cloud-upload text-4xl text-neutral-400 mb-3" />
        <div class="text-sm text-neutral-300 font-medium mb-1">
          Drop your PDF here or click to browse
        </div>
        <div class="text-xs text-neutral-500">
          Maximum file size: 10MB
        </div>
      </div>
    </div>
    
    <!-- Selected file display (shown when a file is selected) -->
    <div v-else class="selected-file">
      <div class="file-info">
        <i class="i-tabler-file-text text-red-400 text-xl mr-3" />
        <div class="file-details">
          <div class="file-name text-sm text-neutral-200 font-medium">
            {{ selectedFile.name }}
          </div>
          <div class="file-size text-xs text-neutral-400">
            {{ formatFileSize(selectedFile.size) }}
          </div>
        </div>
      </div>
      <button
        class="remove-btn"
        :disabled="disabled"
        @click.stop="removeFile"
        title="Remove file"
      >
        <i class="i-tabler-x text-lg" />
      </button>
    </div>
  </div>
</template>

<style scoped>
.file-upload-container {
  width: 100%;
}

.drop-zone {
  border: 2px dashed #404040;
  border-radius: 12px;
  padding: 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(30, 30, 31, 0.5);
  min-height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.drop-zone:hover:not(.drop-zone-disabled) {
  border-color: #6366f1;
  background: rgba(99, 102, 241, 0.1);
}

.drop-zone-active {
  border-color: #6366f1;
  background: rgba(99, 102, 241, 0.15);
  transform: scale(1.02);
}

.drop-zone-disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.drop-zone-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.selected-file {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: rgba(40, 40, 41, 0.8);
  border: 1px solid #404040;
  border-radius: 12px;
  transition: all 0.2s ease;
}

.selected-file:hover {
  background: rgba(40, 40, 41, 0.9);
  border-color: #505050;
}

.file-info {
  display: flex;
  align-items: center;
  flex: 1;
  overflow: hidden;
}

.file-details {
  flex: 1;
  min-width: 0;
}

.file-name {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.4;
}

.remove-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: transparent;
  border: none;
  color: #aaa;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-left: 12px;
  flex-shrink: 0;
}

.remove-btn:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.remove-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>