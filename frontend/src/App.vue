<script setup lang="ts">
import { RokuProvider } from '@roku-ui/vue'
import { loadShiki } from './utils'
import { useI18n } from "vue-i18n";
import { toast, Toaster } from 'vue-sonner'
import 'vue-sonner/style.css'
import { DEFAULT_TOAST_DURATION } from './shared/constants'

// Global drag and drop state
const isDragOver = ref(false);
const draggedFile = ref<File | null>(null);

const { t } = useI18n();
const route = useRoute();

// Check if global drag should be disabled based on current route
const isGlobalDragDisabled = computed(() => {
  return route.name === 'compare' || route.path.includes('/compare')
});

function validateFile(file: File): boolean {
  const validTypes = ["application/pdf"];
  const maxSize = 10 * 1024 * 1024; // 10MB

  if (!validTypes.includes(file.type)) {
    toast.error(t('chat.fileUpload.invalidFileType'), {
      description: t('chat.fileUpload.invalidFileTypeDetail'),
      duration: DEFAULT_TOAST_DURATION,
    });
    return false;
  }

  if (file.size > maxSize) {
    toast.error(t('chat.fileUpload.fileTooLarge'), {
      description: t('chat.fileUpload.fileTooLargeDetail'),
      duration: DEFAULT_TOAST_DURATION,
    });
    return false;
  }

  return true;
}

// Provide global state to child components
provide('globalDragState', {
  isDragOver,
  draggedFile
});

// Global drag event handlers
function handleGlobalDragEnter(event: DragEvent) {
  // Don't handle global drag on compare page
  if (isGlobalDragDisabled.value) return;
  
  event.preventDefault();
  
  // Only show overlay for files
  const types = event.dataTransfer?.types;
  if (types && types.includes('Files')) {
    isDragOver.value = true;
  }
}

function handleGlobalDragOver(event: DragEvent) {
  // Don't handle global drag on compare page
  if (isGlobalDragDisabled.value) return;
  
  event.preventDefault();
  // Keep the drag state active while dragging over the app
}

function handleGlobalDragLeave(event: DragEvent) {
  // Don't handle global drag on compare page
  if (isGlobalDragDisabled.value) return;
  
  event.preventDefault();
  
  // Use a small timeout to check if we're really leaving the app
  // This prevents flickering when moving between child elements
  setTimeout(() => {
    // Check if the mouse is still within the app boundaries
    const appContainer = document.querySelector('.app-container') as HTMLElement;
    if (!appContainer) return;
    
    const rect = appContainer.getBoundingClientRect();
    
    // Get current mouse position from the last known position
    const mouseX = event.clientX;
    const mouseY = event.clientY;
    
    // If mouse is outside the app container, hide the overlay
    if (mouseX < rect.left || mouseX > rect.right || 
        mouseY < rect.top || mouseY > rect.bottom) {
      isDragOver.value = false;
    }
  }, 50);
}

function handleGlobalDrop(event: DragEvent) {
  // Don't handle global drag on compare page
  if (isGlobalDragDisabled.value) return;
  
  event.preventDefault();
  isDragOver.value = false;
  
  const files = event.dataTransfer?.files;
  const file = files?.[0];

  if (file && file.type === "application/pdf") {
    if (validateFile(file)) {
      draggedFile.value = file;
      // Emit a custom event to notify components
      window.dispatchEvent(new CustomEvent('pdf-file-dropped', { detail: file }));
    }
  } else if (file) {
    toast.warning(t('messages.warning'), {
      description: t('chat.fileUpload.onlyPdfSupported'),
      duration: DEFAULT_TOAST_DURATION,
    });
  }
}

// Add a global mouse leave handler to detect when dragging outside the window
function handleWindowDragLeave(event: DragEvent) {
  // If the drag leaves the window entirely, hide the overlay
  if (event.clientX <= 0 || event.clientY <= 0 || 
      event.clientX >= window.innerWidth || event.clientY >= window.innerHeight) {
    isDragOver.value = false;
  }
}

// Add a more reliable way to detect drag cancellation
function handleDragEnd() {
  isDragOver.value = false;
}

onMounted(async () => {
  await loadShiki();
  
  // Add global event listeners for better drag detection
  document.addEventListener('dragleave', handleWindowDragLeave);
  document.addEventListener('dragend', handleDragEnd);
});

onUnmounted(() => {
  // Clean up global event listeners
  document.removeEventListener('dragleave', handleWindowDragLeave);
  document.removeEventListener('dragend', handleDragEnd);
});
</script>

<template>
  <div
    class="app-container h-screen w-screen"
    @dragenter="handleGlobalDragEnter"
    @dragover="handleGlobalDragOver"
    @dragleave="handleGlobalDragLeave"
    @drop="handleGlobalDrop"
  >
    <!-- Global Drag Overlay (appears anywhere in the app) -->
    <div
      v-if="isDragOver"
      class="fixed inset-0 z-[100] bg-black/60 backdrop-blur-sm flex items-center justify-center p-4"
    >
      <div class="bg-[#1e1e1f] rounded-xl p-12 border border-neutral-6 shadow-2xl max-w-2xl w-full mx-4 text-center">
        <div class="mb-6">
          <div class="inline-flex items-center justify-center w-24 h-24 bg-blue-500/20 rounded-full mb-4">
            <i class="i-tabler-file-upload text-5xl text-blue-400" />
          </div>
        </div>
        <h3 class="text-2xl font-medium text-neutral-100 mb-3">
          {{ t('chat.fileUpload.dragDropTitle') }}
        </h3>
        <p class="text-base text-neutral-400 mb-2">
          {{ t('chat.fileUpload.dragDropSubtitle') }}
        </p>
        <div class="flex items-center justify-center gap-2 text-sm text-neutral-500">
          <i class="i-tabler-file-type-pdf text-red-400" />
          <span>{{ t('chat.fileUpload.supportedFormats') }}</span>
        </div>
      </div>
    </div>

    <RokuProvider>
      <RouterView />
      <!-- Customized vue-sonner Toaster component -->
      <Toaster 
        theme="dark"
        position="bottom-right"
        rich-colors
        close-button
        :duration="4000"
        :toast-options="{
          style: {
            fontSize: '14px',
            padding: '12px 16px',
            minHeight: '48px',
            maxWidth: '350px'
          }
        }"
      />
    </RokuProvider>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

:root {
  font-family: "Roboto", Arial, sans-serif;
  font-optical-sizing: auto;
  font-style: normal;
  color-scheme: dark light;
  background-color: #1e1e1f !important;
}
/* :root {
  font-family: "harmonyos sans SC", "Noto Sans SC", sans-serif;
  font-optical-sizing: auto;
  font-style: normal;
  color-scheme: dark light;
  background-color: #1e1e1f !important;
} */

.input-section:before {
    content: "";
    position: absolute;
    top: -50px;
    width: 100%;
    height: 100px;
    pointer-events: none;
    background: -webkit-gradient(linear,left top,left bottom,from(#13131400),color-stop(60%,#131314));
    background: -webkit-linear-gradient(top,#13131400,#131314 60%);
    background: linear-gradient(180deg,#13131400,#131314 60%);
}
pre {
  outline: none;
}

.input-enter-animate {
  animation: inputEnter 0.5s forwards;
}
.animate-fade-delay {
  opacity: 0;
  animation: fade 0.5s forwards 0.2s;
}

textarea::-moz-placeholder {
  white-space: nowrap;
}

textarea::-webkit-placeholder {
  white-space: nowrap;
}

textarea::placeholder {
  white-space: nowrap;
}

.gradient-text {
  --gradient-color-1: #004183;
  --gradient-color-2: #0a57a5;
  --gradient-color-3: #c71d86;
  background: linear-gradient(74deg, var(--gradient-color-1), var(--gradient-color-2), var(--gradient-color-3), var(--gradient-color-3), var(--gradient-color-2), var(--gradient-color-1), var(--gradient-color-2), var(--gradient-color-3), rgba(0, 0, 0, 0), rgba(0, 0, 0, 0));
  background-size: 400% 100%;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  display: inline-block;
  animation: gradient-animation 2s forwards;
}

@keyframes gradient-animation {
  0% {
    background-position: 100% 0%;
    background-size: 800% 100%;
  }
  100% {
    background-position: 0% 0%;
    background-size: 400% 100%;
  }
}

@keyframes inputEnter {
  from {
    opacity: 0;
    width: 50%;
    translate: 25% 0%;
  }
  to {
    opacity: 1;
    width: 100%;
    translate: 0% 0%;
  }
}

@keyframes fade {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>

<style>
.fade-enter-active {
  transition: opacity 1s;
}

.fade-leave-active {
  position: absolute;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.fade-enter-to, .fade-leave-from {
  opacity: 1;
}
p {
  white-space: pre-wrap;
}
.line {
  transition: opacity 0.5s;
}

.fade-in {
    opacity: 0;
    animation: fadeIn 1s forwards;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}
</style>
