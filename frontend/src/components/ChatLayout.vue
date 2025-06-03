<script setup lang="ts">
import type { ChatMessage } from "../composables/useHelloWorld";
import { useScrollToBottom } from "../composables/useScrollToBottom";
import { useCurrentChat, platform, model, selectedCollection } from "../shared";
import { generateId, isMobile, setChat } from "../utils";
import { streamOllamaChat } from "../composables/useOllama";
import { streamRagChat } from "../composables/useRAG";

import { useToast } from "primevue/usetoast";

const toast = useToast();

const router = useRouter();

const lastUsage = ref({
  prompt_tokens: 0,
  completion_tokens: 0,
});

const conversation = shallowRef<ChatMessage[]>([]);
const currentChat = useCurrentChat();

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
    // Simple Ollama request for summary
    const ollamaServiceUrl = import.meta.env.VITE_OLLAMA_BASE_URL;
    const endpoint = `${ollamaServiceUrl}/api/chat`;

    // Simple Ollama request for summary
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "mistral-small3.1:latest",
        messages: [
          {
            role: "system",
            content:
              "Please summarize the user's text and return the title of the text without adding any additional information. The title MUST in less than 4 words. Use the text language to summarize the text. Do not add any punctuation or markdown annotation.",
          },
          {
            role: "user",
            content: `Summarize the following text in less than 4 words: ${text}`,
          },
        ],
        stream: false,
      }),
    });

    const data = await response.json();
    console.log("Summary response:", data.message.content);
    return data.message?.content || "Chat";
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
    toast.add({
      severity: "error",
      summary: "Error",
      detail: "Please select a model first.",
      life: 3000,
    });
    return;
  }
  if (!selectedCollection.value) {
    toast.add({
      severity: "error",
      summary: "Error",
      detail: "Please select a collection first.",
      life: 3000,
    });
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
    input.value = "";

    conversation.value = [
      ...conversation.value,
      { role: "user", content },
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

    const filteredConversation = conversation.value
      .slice(0, -1)
      .filter((d) => d.role !== "error")
      .map((d) => {
        if (d.role === "assistant") {
          delete d.reasoning;
        }
        return d;
      });

    try {
      // Start streaming based on the selected platform
      laststartedAtMS.value = Date.now();
      lastEndedAtMS.value = 0;
      let totalTokens = 0;

      // Choose the appropriate streaming function based on the platform
      const streamFunction =
        platform.value === "rag" ? streamRagChat : streamOllamaChat;

      for await (const chunk of streamFunction(filteredConversation)) {
        if (laststartedAtMS.value === 0) {
          laststartedAtMS.value = Date.now();
        }

        // Extract content using all possible formats for compatibility
        const content =
          chunk.message?.content || chunk.content || chunk.delta || "";
        if (content) {
          // Create a *new* message object with updated content
          const updatedMessage = {
            ...lastMessage,
            content: lastMessage.content + content,
          };

          // Find the index of the lastMessage in the conversation
          const lastMessageIndex = conversation.value.length - 1;

          // Create a new conversation array with the updated message
          const newConversation = [...conversation.value];
          newConversation[lastMessageIndex] = updatedMessage;

          // Update conversation reference to trigger reactivity
          conversation.value = newConversation;

          // Update lastMessage reference to point to the new object
          lastMessage = updatedMessage;

          // Let Vue update the UI before processing the next chunk
          await nextTick();
        }

        // Update token estimation
        totalTokens += 1;
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
      console.error("Ollama chat error:", err);
      lastMessage.role = "error";
      lastMessage.content =
        err instanceof Error ? err.message : "Error communicating with Ollama";
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

onMounted(() => {
  textareaRef.value?.focus();
});

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
            Hi there!
          </div>
          <div class="animate-fade-delay text-2xl lg:text-4xl md:text-3xl">
            <div class="op-25">What can I help you today?</div>
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
        <div class="relative z-10 max-w-830px w-full overflow-hidden leading-0">
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
            class="input-enter-animate z-10 w-full flex-grow-0 bg-[#1e1e1f] px-6 py-4 pr-14 text-lg text-[#e3e3e3] outline-1 outline-none transition-all focus:bg-neutral-8 hover:bg-neutral-8 focus-visible:outline-1 focus-visible:outline-transparent focus-visible:outline-offset-0"
            placeholder="Input your question here"
            @keydown.stop.up="
              async (e) => {
                if (!(input === '')) return;
                const target = e.target as HTMLTextAreaElement;
                if (target.selectionStart === 0) {
                  const currentIdx = inputHistory.history.value
                    .map((d) => d.snapshot)
                    .indexOf(input);
                  if (currentIdx === -1) {
                    input = inputHistory.history.value[0].snapshot;
                  } else {
                    input =
                      inputHistory.history.value[
                        (currentIdx + 1) % inputHistory.history.value.length
                      ].snapshot;
                  }
                }
              }
            "
            @keypress.stop.prevent.enter="onEnter"
          />
        </div>
        <div
          class="animate-fade-delay flex animate-delay-500 gap-2 pb-3 pt-1 text-xs color-[#c4c7c5]"
        >
          <span v-if="lastEndedAtMS && laststartedAtMS">
            Last response time:
            {{
              lastEndedAtMS - laststartedAtMS < 1000
                ? `${lastEndedAtMS - laststartedAtMS}ms`
                : `${((lastEndedAtMS - laststartedAtMS) / 1000).toFixed(2)}s`
            }}
          </span>
          <span v-else> CA-NormExpert Chat </span>
        </div>
      </div>
    </MainContainer>
  </BaseContainer>
</template>
