<script setup lang="ts">
import type { ChatMessage } from "../composables/useHelloWorld";
import { useScrollToBottom } from "../composables/useScrollToBottom";
import { useCurrentChat, model, selectedCollection } from "../shared";
import { generateId, isMobile, setChat } from "../utils";
import { streamRagChat } from "../composables/useRAG";
import { useI18n } from "vue-i18n";
import { useRagApi } from "../api/rag";
import PdfFileUpload from "./PdfFileUpload.vue";
import { toast } from "vue-sonner";
import { TOAST_DURATION } from "../shared/constants";

const { t } = useI18n();
const { ragApi } = useRagApi();

const router = useRouter();

const lastUsage = ref({
  prompt_tokens: 0,
  completion_tokens: 0,
});

const conversation = shallowRef<ChatMessage[]>([]);
const currentChat = useCurrentChat();

// PDF file upload state
const attachedFile = ref<File | null>(null);
const pdfUploadRef = ref<InstanceType<typeof PdfFileUpload> | null>(null);

// Create a proper event handler function that can be referenced for cleanup
const handleFileDropped = (event: Event) => {
  const customEvent = event as CustomEvent;
  const file = customEvent.detail as File;
  
  // Only set the file, don't call onFileSelected to avoid duplicate toasts
  attachedFile.value = file;
  
  // Show toast notification only here for drag & drop
  toast.success(t('chat.fileUpload.fileAttached'), {
    description: `${file.name} ${t('chat.fileUpload.fileAttachedDetail')}`,
    duration: TOAST_DURATION.SHORT,
  });
};

// Listen for global file drops
onMounted(() => {
  textareaRef.value?.focus();
  
  // Listen for PDF files dropped anywhere in the app
  window.addEventListener('pdf-file-dropped', handleFileDropped);
});

onUnmounted(() => {
  // Clean up event listener
  window.removeEventListener('pdf-file-dropped', handleFileDropped);
});

watch([currentChat], () => {
  if (currentChat.value) {
    lastUsage.value = {
      prompt_tokens: 0,
      completion_tokens: 0,
    };
  }
});

watchEffect(() => {
  if (currentChat.value) {
    conversation.value = currentChat.value.conversation;
  } else {
    conversation.value = [];
  }
});

async function generateSummary(text: string) {
  try {
    // Use backend API endpoint instead of direct Ollama call
    const response = await ragApi.generateSummary(text, "mistral-small3.1:latest");
    console.log("Summary response:", response.data.summary);
    return response.data.summary || "Chat";
  } catch (error) {
    console.error("Error generating summary:", error);
    return "Chat";
  }
}

const groupedConversation = computed(() => {
  const result: ChatMessage[][] = [];
  let group: ChatMessage[] = [];
  for (const c of conversation.value) {
    if (c.role === "system") {
      continue;
    }
    if (c.role === "assistant") {
      group.push(c);
      result.push(group);
      group = [];
    } else {
      group.push(c);
    }
  }
  if (group.length) {
    result.push(group);
  }
  return result;
});
const enableAutoScroll = ref(false);
function scrollToBottomSmoothly(
  element: { scrollTop: number; scrollHeight: number; clientHeight: number },
  duration: number
) {
  const start = element.scrollTop;
  const end = element.scrollHeight - element.clientHeight;
  const distance = end - start;
  const startTime = performance.now();
  function easeInOutQuad(
    time: number,
    start: number,
    change: number,
    duration: number
  ) {
    time /= duration / 2;
    if (time < 1) {
      return (change / 2) * time * time + start;
    }
    time--;
    return (-change / 2) * (time * (time - 2) - 1) + start;
  }

  function scroll() {
    const currentTime = performance.now();
    const timeElapsed = currentTime - startTime;
    element.scrollTop = easeInOutQuad(timeElapsed, start, distance, duration);
    if (timeElapsed < duration) {
      requestAnimationFrame(scroll);
    } else {
      element.scrollTop = end;
      enableAutoScroll.value = true;
    }
  }

  scroll();
}

const scrollArea = ref<HTMLElement | null>(null);
const input = ref("");
const inputHistory = useManualRefHistory(input);
const streaming = ref(false);
const textareaRef = ref<HTMLTextAreaElement | null>(null);
const rows = ref(1);
watch(
  [input, textareaRef],
  () => {
    nextTick(() => {
      if (textareaRef.value) {
        const targetRows = getNumberOfLines(textareaRef.value);
        rows.value = targetRows;
      }
    });
  },
  { immediate: true }
);
function getNumberOfLines(textarea: HTMLTextAreaElement) {
  textarea.style.height = "0px";
  const style = window.getComputedStyle(textarea);
  const lineHeight = Number.parseInt(style.lineHeight);
  const padding =
    Number.parseInt(style.paddingTop) + Number.parseInt(style.paddingBottom);
  const textareaHeight = textarea.scrollHeight - padding;
  const numberOfLines = Math.ceil(textareaHeight / lineHeight);
  textarea.style.height = "";
  return numberOfLines;
}
watch(currentChat, () => {
  textareaRef.value?.focus();
});
const laststartedAtMS = ref(0);
const lastEndedAtMS = ref(0);

async function onSubmit() {
  if (!model.value) {
    toast.error("Please select a model first.");
    return;
  }
  if (!selectedCollection.value) {
    toast.error("Please select a collection first.");
    return;
  }

  if (input.value.trim() === "" || streaming.value) {
    return;
  }
  streaming.value = true;
  let chat = currentChat.value;
  if (!chat) {
    // Create a new chat history entry at the start
    const id = generateId();
    chat = {
      id,
      title: null,
      conversation: conversation.value,
      token: {
        inTokens: 0,
        outTokens: 0,
      },
    };
    setChat(chat);
    router.push({
      name: "chat",
      params: {
        id,
      },
    });
  }

  try {
    const content = `${input.value.trim()}\n`;
    inputHistory.commit();
    const currentInput = input.value;
    const currentFile = attachedFile.value; // Store reference before clearing
    input.value = "";

    // Clear attached file immediately after capturing it
    attachedFile.value = null;

    // Display user message (with file indicator if attached)
    const userContent = currentFile
      ? `${content}📎 ${currentFile.name}`
      : content;

    conversation.value = [
      ...conversation.value,
      { role: "user", content: userContent },
      { role: "assistant", content: "", reasoning: "" },
    ];
    setChat(toRaw({ ...chat, conversation: conversation.value }));
    nextTick(() => {
      const el = scrollArea.value;
      if (el) {
        scrollToBottomSmoothly(el, 1000);
      }
    });
    let lastMessage = conversation.value[conversation.value.length - 1];

    try {
      // Start streaming based on whether file was attached
      laststartedAtMS.value = Date.now();
      lastEndedAtMS.value = 0;
      let totalTokens = 0;

      if (currentFile) {
        // Use file upload endpoint
        console.log("Sending query with attached file:", currentFile.name);
        const response = await ragApi.chatWithFile(
          currentInput.trim(),
          currentFile,
          model.value
        );

        // Simulate streaming for consistency
        const responseText = response.data.response || "No response received.";
        const chunks = responseText.split(" ");

        for (const chunk of chunks) {
          if (chunk.trim()) {
            const updatedMessage = {
              ...lastMessage,
              content: lastMessage.content + chunk + " ",
            };

            const lastMessageIndex = conversation.value.length - 1;
            const newConversation = [...conversation.value];
            newConversation[lastMessageIndex] = updatedMessage;
            conversation.value = newConversation;
            lastMessage = updatedMessage;

            await nextTick();
            await new Promise((resolve) => setTimeout(resolve, 30)); // Small delay for visual effect
            totalTokens += 1;
          }
        }
      } else {
        // Use regular streaming without file
        const filteredConversation = conversation.value
          .slice(0, -1)
          .filter((d) => d.role !== "error")
          .map((d) => {
            if (d.role === "assistant") {
              delete d.reasoning;
            }
            return d;
          });

        const streamFunction = streamRagChat;

        for await (const chunk of streamFunction(filteredConversation)) {
          if (laststartedAtMS.value === 0) {
            laststartedAtMS.value = Date.now();
          }

          const content =
            chunk.message?.content || chunk.content || chunk.delta || "";
          if (content) {
            const updatedMessage = {
              ...lastMessage,
              content: lastMessage.content + content,
            };

            const lastMessageIndex = conversation.value.length - 1;
            const newConversation = [...conversation.value];
            newConversation[lastMessageIndex] = updatedMessage;
            conversation.value = newConversation;
            lastMessage = updatedMessage;

            await nextTick();
          }

          totalTokens += 1;
        }
      }

      // Update token usage estimation
      lastEndedAtMS.value = Date.now();
      lastUsage.value = {
        prompt_tokens: content.length / 4,
        completion_tokens: totalTokens,
      };

      if (chat) {
        chat.token.inTokens += Math.round(content.length / 4);
        chat.token.outTokens += totalTokens;
      }
    } catch (err) {
      console.error("Chat error:", err);
      lastMessage.role = "error";
      lastMessage.content =
        err instanceof Error ? err.message : "Error communicating with the service";
    }
  } finally {
    streaming.value = false;

    if (chat) {
      chat.conversation = conversation.value;
      chat = toRaw(chat);
      setChat(chat);
      if (!chat.title) {
        const firstUserMessage = conversation.value.find(
          (d) => d.role === "user"
        );
        if (!firstUserMessage) return;
        const summary = await generateSummary(firstUserMessage.content);
        setChat({
          ...chat,
          title: summary,
        });
      }
    }
  }
}

async function onEnter(e: KeyboardEvent) {
  if (e.isComposing) {
    return;
  }
  if (streaming.value) {
    return;
  }
  if (!input.value.trim()) {
    return;
  }
  const target = e.target as HTMLTextAreaElement;
  if (!isMobile.value && e.shiftKey && target) {
    const selectStart = target.selectionStart;
    input.value = `${input.value.slice(0, selectStart)}\n${input.value.slice(
      target.selectionEnd
    )}`;
    if (e.target) {
      nextTick(() => {
        const totalRows = target.value.split("\n").length;
        const targetRows = Math.min(totalRows, 3);
        rows.value = targetRows;
        target.selectionStart = selectStart + 1;
        target.selectionEnd = selectStart + 1;
        const lineHeight = Number.parseInt(
          window.getComputedStyle(target).lineHeight
        );
        target.scroll({
          top: lineHeight * totalRows,
        });
      });
    }
    return;
  }
  if (isMobile.value) {
    input.value += "\n";
    const target = e.target as HTMLTextAreaElement;
    if (e.target) {
      nextTick(() => {
        const rows = target.value.split("\n").length;
        target.rows = rows;
        target.scrollTop = target.scrollHeight;
      });
    }
    return;
  }
  onSubmit();
}
useScrollToBottom(scrollArea, 50, enableAutoScroll);
watchEffect(() => {
  if (streaming.value) {
    enableAutoScroll.value = false;
  }
});

// File handling functions
function onFileSelected(file: File) {
  attachedFile.value = file;
  toast.success(t('chat.fileUpload.fileAttached'), {
    description: `${file.name} ${t('chat.fileUpload.fileAttachedDetail')}`,
    duration: TOAST_DURATION.SHORT,
  });
}

function onFileRemoved() {
  attachedFile.value = null;
  toast.info(t('chat.fileUpload.fileRemoved'), {
    description: t('chat.fileUpload.fileRemovedDetail'),
    duration: TOAST_DURATION.SHORT,
  });
}

function openFileDialog() {
  pdfUploadRef.value?.openFileDialog();
}

// Handle keyboard navigation for input history
function handleUpArrow(e: KeyboardEvent) {
  if (!(input.value === '')) return;
  const target = e.target as HTMLTextAreaElement;
  if (target.selectionStart === 0) {
    const currentIdx = inputHistory.history.value
      .map((d: any) => d.snapshot)
      .indexOf(input.value);
    if (currentIdx === -1) {
      input.value = inputHistory.history.value[0].snapshot;
    } else {
      input.value =
        inputHistory.history.value[
          (currentIdx + 1) % inputHistory.history.value.length
        ].snapshot;
    }
  }
}
</script>

<template>
  <BaseContainer>
    <ChatAside />
    <MainContainer>
      <ChatHeader />
      <div
        v-if="conversation.length <= 1"
        class="m-auto h-full max-w-5xl w-full overflow-x-hidden overflow-y-auto px-4 text-3.5rem font-medium leading-4rem"
      >
        <div class="md:mb-12 md:mt-8">
          <div class="gradient-text text-3xl lg:text-5xl md:text-4xl">
            {{ t("chat.greeting") }}
          </div>
          <div class="animate-fade-delay text-2xl lg:text-4xl md:text-3xl">
            <div class="op-25">{{ t("chat.subtitle") }}</div>
          </div>
        </div>
        <div class="mb-10 mt-20 flex gap-4">
          <div class="animate-fade-delay">
            <button
              class="group relative w-full overflow-hidden rounded-xl bg-neutral-8 border border-neutral-700 p-4 shadow-sm transition-all duration-200 hover:shadow-md hover:bg-neutral-7 hover:border-neutral-600 md:h-200px md:w-200px"
              @click="router.push({ name: 'compare' })"
            >
              <!-- Content -->
              <div class="relative z-10 flex h-full flex-col items-start justify-between">
                <!-- Icon and title section -->
                <div class="flex w-full items-center gap-3 md:flex-col md:items-start md:gap-2">
                  <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-500/20 transition-all duration-200 group-hover:bg-blue-500/30 md:h-12 md:w-12">
                    <i class="i-tabler-file-diff h-5 w-5 text-blue-400 md:h-6 md:w-6" />
                  </div>
                  <div class="flex-1 md:flex-initial md:mt-2">
                    <h3 class="text-base font-medium text-white transition-colors duration-200 group-hover:text-blue-200">
                      {{ t('compare.title') }}
                    </h3>
                  </div>
                </div>
                
                <!-- Description -->
                <div class="hidden w-full md:block">
                  <p class="text-xs leading-relaxed text-neutral-400 transition-colors duration-200 group-hover:text-neutral-300">
                    {{ t('compare.subtitle') }}
                  </p>
                </div>
                
                <!-- Arrow indicator -->
                <div class="ml-auto flex items-center md:ml-0 md:mt-auto">
                  <i class="i-tabler-arrow-right h-4 w-4 text-neutral-500 transition-all duration-200 group-hover:translate-x-1 group-hover:text-blue-400" />
                </div>
              </div>
            </button>
          </div>
        </div>
      </div>
      <div
        v-else
        ref="scrollArea"
        class="overflow-x-hidden overflow-y-auto last-children:min-h-[calc(100dvh-120px-72px)]"
      >
        <template v-for="(g, i) in groupedConversation" :key="i">
          <ChatMessage
            v-for="(c, j) in g"
            :key="j"
            :message="c"
            :loading="streaming && groupedConversation.length - 1 === i"
          />
        </template>
      </div>
      <div
        class="input-section relative min-h-120px flex shrink-0 flex-col items-center justify-end gap-1 px-4"
      >
        <!-- PDF File Attachment Area (above input) -->
        <div v-if="attachedFile" class="relative z-50 w-full max-w-830px mb-2">
          <div class="flex justify-start">
            <div class="flex items-center gap-3 px-4 py-2 bg-neutral-8/80 rounded-full border border-neutral-7/50 shadow-sm backdrop-blur-sm max-w-sm">
              <div class="flex items-center justify-center w-8 h-8 bg-red-400/20 rounded-full">
                <i class="i-tabler-file-type-pdf text-red-400 text-sm" />
              </div>
              <div class="flex-1 min-w-0">
                <div class="text-sm text-neutral-200 font-medium truncate">
                  {{ attachedFile.name.length > 25 ? attachedFile.name.substring(0, 22) + '...' : attachedFile.name }}
                </div>
                <div class="text-xs text-neutral-400 leading-tight">
                  {{ (attachedFile.size / (1024 * 1024)).toFixed(1) }}MB
                </div>
              </div>
              <button
                @click="onFileRemoved"
                class="flex items-center justify-center w-6 h-6 text-neutral-400 hover:text-red-400 hover:bg-red-400/20 rounded-full transition-colors"
                title="Remove file"
              >
                <i class="i-tabler-x text-sm" />
              </button>
            </div>
          </div>
        </div>

        <div class="relative z-10 max-w-830px w-full overflow-hidden leading-0">
          <!-- File attachment button (left side) -->
          <div class="pointer-events-none absolute h-full w-full flex items-center justify-start p-2">
            <button
              :disabled="streaming"
              class="pointer-events-auto z-20 h-10 w-10 flex items-center justify-center rounded-full color-[#c4c7c5] transition-all hover:bg-neutral-7"
              @click="openFileDialog"
              :title="t('chat.fileUpload.attachPdfFile')"
            >
              <i class="i-tabler-paperclip h-5 w-5" />
            </button>
          </div>

          <!-- Send button (right side) -->
          <div
            :class="{
              'right-[-48px]': !input.trim(),
              'right-0': input.trim(),
            }"
            class="pointer-events-none absolute h-full w-full flex items-center justify-end p-2 transition-right"
          >
            <button
              :disabled="streaming"
              :class="{
                'opacity-0': !input.trim(),
              }"
              class="pointer-events-auto z-20 h-12 w-12 flex items-center justify-center rounded-full color-[#c4c7c5] transition-all hover:bg-neutral-7"
              @click="onSubmit"
            >
              <i class="i-tabler-send h-6 w-6" />
            </button>
          </div>

          <textarea
            ref="textareaRef"
            v-model="input"
            type="text"
            style="
              resize: none;
              scrollbar-width: none;
              max-height: 300px;
              height: auto;
            "
            :rows="rows"
            :class="{
              'rounded-[3rem]': rows === 1,
              'rounded-[1rem]': rows !== 1,
            }"
            class="input-enter-animate z-10 w-full flex-grow-0 bg-[#1e1e1f] px-14 py-4 text-lg text-[#e3e3e3] outline-1 outline-none transition-all focus:bg-neutral-8 hover:bg-neutral-8 focus-visible:outline-1 focus-visible:outline-transparent focus-visible:outline-offset-0"
            :placeholder="attachedFile ? t('chat.inputPlaceholderWithFile') : t('chat.inputPlaceholder')"
            @keydown.stop.up="handleUpArrow"
            @keypress.stop.prevent.enter="onEnter"
          />
        </div>

        <!-- Hidden PDF upload component -->
        <PdfFileUpload
          ref="pdfUploadRef"
          v-model="attachedFile"
          :disabled="streaming"
          @file-selected="onFileSelected"
          @file-removed="onFileRemoved"
          style="display: none;"
        />

        <div
          class="animate-fade-delay flex animate-delay-500 gap-2 pb-3 pt-1 text-xs color-[#c4c7c5]"
        >
          <span v-if="lastEndedAtMS && laststartedAtMS">
            {{ t("chat.lastResponseTime") }}
            {{
              lastEndedAtMS - laststartedAtMS < 1000
                ? `${lastEndedAtMS - laststartedAtMS}ms`
                : `${((lastEndedAtMS - laststartedAtMS) / 1000).toFixed(2)}s`
            }}
          </span>
          <span v-else> {{ t("chat.appName") }} </span>
        </div>
      </div>
    </MainContainer>
  </BaseContainer>
</template>
