<script setup lang="ts">
import { ref, computed, defineComponent } from "vue";
import { md } from "../utils";
import type { VNode } from "vue";

const props = withDefaults(
  defineProps<{
    content: string;
    reasoning?: string;
    loading: boolean;
  }>(),
  {
    reasoning: "",
  }
);

// --- Enhanced Thinking Extraction ---
// This improved version handles partial <think> tags during streaming
function extractThinking(text: string) {
  if (!text) return { mainContent: "", thinkingContent: "", isThinking: false };

  // Check for incomplete thinking section - detect if we're within a <think> tag
  // but haven't received the closing </think> yet
  const thinkStartIndex = text.indexOf("<think>");
  if (thinkStartIndex >= 0) {
    const thinkEndIndex = text.indexOf("</think>", thinkStartIndex);

    // If we found an opening tag but no closing tag, we're in an incomplete thinking section
    if (thinkEndIndex === -1) {
      const thinkingContent = text.substring(thinkStartIndex + 7); // +7 to skip '<think>'
      return {
        mainContent: text.substring(0, thinkStartIndex),
        thinkingContent: thinkingContent,
        isThinking: true,
      };
    }

    // Complete thinking tag (both opening and closing tags found)
    const thinkRegex = /<think>([\s\S]*?)<\/think>/g;
    let match;
    let cleanContent = text;
    let allThinkingContent = "";

    // Extract all thinking sections
    while ((match = thinkRegex.exec(text)) !== null) {
      allThinkingContent +=
        (allThinkingContent ? "\n\n" : "") + match[1].trim();
      cleanContent = cleanContent.replace(match[0], "");
    }

    return {
      mainContent: cleanContent.trim(),
      thinkingContent: allThinkingContent,
      isThinking: false,
    };
  }

  // No thinking tags found
  return { mainContent: text, thinkingContent: "", isThinking: false };
}

function extractSources(text: string) {
  const sourcesRegex = /\n\n\*\*Sources:\*\*\n([\s\S]*?)$/;
  const match = text?.match?.(sourcesRegex);
  if (match && match[1]) {
    const cleanContent = text.replace(sourcesRegex, "");
    return {
      contentWithoutSources: cleanContent.trim(),
      sourcesContent: `**Sources:**\n${match[1].trim()}`,
    };
  }
  return { contentWithoutSources: text || "", sourcesContent: "" };
}

function splitContent(msg: string) {
  if (!msg) return "";
  const sentences = msg.split(
    /(?<=[。？！；、，\n])|(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=[.?!`])/g
  );
  if (
    sentences.length > 0 &&
    !/[.?!。？！；，、`\n]$/.test(sentences[sentences.length - 1])
  ) {
    sentences.pop();
  }
  if (sentences.length > 0 && /^\d+\./.test(sentences[sentences.length - 1])) {
    sentences.pop();
  }
  return sentences.join("");
}

// --- Parsed Content Computeds ---
const parsedContentFromProps = computed(() => {
  return extractThinking(props.content);
});

// Check if we're currently streaming thinking content
const isStreamingThinking = computed(() => {
  return props.loading && parsedContentFromProps.value.isThinking;
});

const contentAfterThinking = computed(() => {
  // When streaming thinking content, don't show anything in main content area
  if (isStreamingThinking.value) {
    return "";
  }
  return parsedContentFromProps.value.mainContent;
});

const sourcesAndContent = computed(() =>
  extractSources(contentAfterThinking.value)
);

// Final content string (without sources/thinking)
const baseContent = computed(() => {
  return sourcesAndContent.value.contentWithoutSources;
});

const sourcesText = computed(() => sourcesAndContent.value.sourcesContent);
const reasoningText = computed(() => {
  // During streaming, if we're in a thinking state, use the extracted thinking content
  if (parsedContentFromProps.value.thinkingContent) {
    return parsedContentFromProps.value.thinkingContent;
  }
  return props.reasoning || "";
});

// --- UI State ---
const reasoningCollapsed = ref(true); // Start collapsed by default

// Allow toggling even during streaming thinking
const toggleReasoning = () => {
  reasoningCollapsed.value = !reasoningCollapsed.value;
};

const sourcesCollapsed = ref(true);
const toggleSources = () => {
  sourcesCollapsed.value = !sourcesCollapsed.value;
};
const sourceCount = computed(() => {
  if (!sourcesText.value) return 0;
  const matches = sourcesText.value.match(/^\* /gm);
  return matches ? matches.length : 0;
});
const shouldCollapseSources = computed(() => sourceCount.value > 5);
const showCopyTooltip = ref(false);

// --- Content Rendering Logic ---
function editResult(childrenRaw: VNode[]): VNode[] {
  const children = childrenRaw.flat(20);
  for (let i = 0; i < children.length; i++) {
    const child = children[i];
    if (typeof child.children === "string") {
      child.props = { ...child.props };
    }
    if (
      child.children &&
      Array.isArray(child.children) &&
      child.children.length > 0
    ) {
      editResult(child.children as VNode[]);
    }
  }
  return children;
}

const formattedBaseContent = computed(() => splitContent(baseContent.value));

// During streaming, if we're in thinking mode, don't render any main content
const mainContentTextToRender = computed(() => {
  if (props.loading) {
    // When streaming thinking content, don't show anything in main content
    if (isStreamingThinking.value) {
      return "";
    }
    // For normal streaming, show content directly
    return baseContent.value;
  } else {
    // After streaming is done, show formatted content
    return formattedBaseContent.value;
  }
});

// VNodes for the main content - direct rendering during streaming
const contentVNodes = computed(() => {
  try {
    // Skip rendering if we're in thinking mode
    if (isStreamingThinking.value) {
      return [] as unknown as VNode[];
    }

    // For direct streaming updates, render the raw markdown
    const textToRender = mainContentTextToRender.value;

    // Using basic rendering during streaming for maximum responsiveness
    const vnodes = md.render(textToRender, {
      sanitize: true,
    }) as unknown as VNode[];

    // Return raw VNodes during streaming, only apply editResult when complete
    return props.loading ? vnodes : editResult(vnodes);
  } catch (error) {
    console.error("Error rendering markdown:", error);
    return [
      { children: `Error rendering content: ${error}` },
    ] as unknown as VNode[];
  }
});

// Standard computed for reasoning and sources
const reasoningVNodes = computed(() => {
  return md.render(reasoningText.value || "", {
    sanitize: true,
  }) as unknown as VNode[];
});

const sourcesVNodes = computed(() => {
  return md.render(sourcesText.value || "", {
    sanitize: true,
  }) as unknown as VNode[];
});

// --- Child Components for Rendering ---
const StreamMarkdownContent = defineComponent({
  setup() {
    return () => {
      return contentVNodes.value;
    };
  },
});

const StreamMarkdownReasoning = defineComponent({
  setup() {
    return () => reasoningVNodes.value;
  },
});

const StreamMarkdownSources = defineComponent({
  setup() {
    return () => sourcesVNodes.value;
  },
});

// --- Copy Functionality ---
function copyContentToClipboard() {
  const textToCopy = props.loading ? props.content : formattedBaseContent.value;
  navigator.clipboard
    .writeText(textToCopy)
    .then(() => {
      showCopyTooltip.value = true;
      setTimeout(() => {
        showCopyTooltip.value = false;
      }, 2000);
    })
    .catch((err) => console.error(`Failed to copy content: ${err}`));
}
</script>

<template>
  <div class="relative">
    <div>
      <!-- Reasoning Section -->
      <div
        v-if="reasoningText && reasoningText.length > 0"
        class="mb-4 min-w-full w-full overflow-hidden rounded-xl bg-blue-900/20 transition-all duration-300"
      >
        <div
          class="flex items-center justify-between px-4 py-2 cursor-pointer"
          @click="toggleReasoning"
        >
          <div
            class="flex items-center text-xs font-medium text-blue-300 dark:text-blue-200"
          >
            {{
              isStreamingThinking
                ? "Thinking..."
                : "Thinking Process"
            }}
            <!-- Add pulsing indicator when thinking is happening (visible even when collapsed) -->
            <div
              v-if="isStreamingThinking"
              class="ml-2 h-2 w-2 rounded-full bg-blue-400 animate-pulse"
            ></div>
          </div>
          <button class="text-blue-300 dark:text-blue-200">
            <i
              :class="
                reasoningCollapsed
                  ? 'i-tabler-chevron-down'
                  : 'i-tabler-chevron-up'
              "
              class="h-4 w-4"
            />
          </button>
        </div>
        <div
          v-show="!reasoningCollapsed"
          class="px-4 py-2 text-xs prose text-blue-300 dark:text-blue-200 border-t border-blue-800/30 overflow-auto"
        >
          <StreamMarkdownReasoning />
          <div v-if="isStreamingThinking" class="mt-1 animate-pulse">
            <span class="text-blue-300 dark:text-blue-200 text-opacity-70">
              Thinking in progress...
            </span>
          </div>
        </div>
      </div>

      <!-- Main Content Area with Copy Button -->
      <div class="relative mb-2">
        <div class="absolute right-0 top-0 z-10">
          <button
            class="h-8 w-8 flex items-center justify-center rounded bg-transparent p-1.5 opacity-50 transition-all duration-200 hover:bg-black/5 hover:opacity-100 dark:hover:bg-white/10"
            aria-label="Copy markdown content"
            @click="copyContentToClipboard"
          >
            <i
              class="i-tabler-copy h-5 w-5 text-neutral-500 dark:text-neutral-4"
            />
            <div
              v-if="showCopyTooltip"
              class="pointer-events-none absolute right-0 whitespace-nowrap rounded bg-black/70 px-2 py-1 text-xs text-white -bottom-7 dark:bg-white/70 dark:text-black"
            >
              Copied!
            </div>
          </button>
        </div>
      </div>

      <!-- Main Content Render -->
      <div
        key="prose-main-content"
        class="hover text-sm prose prose-neutral children:mt-0 md:text-base prose-code:text-sm prose-h1:text-3xl prose-h2:text-xl prose-h3:text-lg prose-h4:text-base prose-h5:text-base dark:prose-invert prose-code:after:content-none prose-code:before:content-none max-w-full w-full"
      >
        <!-- Show thinking indicator when streaming but not in thinking mode -->
        <p
          v-if="
            props.loading && !mainContentTextToRender && !isStreamingThinking
          "
          class="text-gray-500 italic"
        >
          Processing...
        </p>
        <!-- No content message when not loading -->
        <p
          v-else-if="!props.loading && !mainContentTextToRender"
          class="text-gray-500 italic"
        >
          No content
        </p>
        <!-- Actual content -->
        <StreamMarkdownContent v-else-if="mainContentTextToRender" />
      </div>

      <!-- Sources Section -->
      <div
        v-if="sourcesText && sourcesText.length > 0"
        class="mt-4 min-w-full w-full overflow-hidden rounded-xl bg-gray-100/20 dark:bg-gray-800/20 transition-all duration-300"
      >
        <div
          v-if="shouldCollapseSources"
          class="flex items-center justify-between px-4 py-2 cursor-pointer"
          @click="toggleSources"
        >
          <div class="text-xs font-medium text-gray-700 dark:text-gray-300">
            Sources ({{ sourceCount }})
          </div>
          <button class="text-gray-700 dark:text-gray-300">
            <i
              :class="
                sourcesCollapsed
                  ? 'i-tabler-chevron-down'
                  : 'i-tabler-chevron-up'
              "
              class="h-4 w-4"
            />
          </button>
        </div>
        <div
          :class="{
            'px-4 py-2': shouldCollapseSources,
            'border-t border-gray-200/30 dark:border-gray-700/30':
              shouldCollapseSources && !sourcesCollapsed,
          }"
          v-show="!shouldCollapseSources || !sourcesCollapsed"
          class="text-xs prose text-gray-700 dark:text-gray-300 overflow-auto"
        >
          <StreamMarkdownSources />
        </div>
      </div>
    </div>
  </div>
</template>

<style>
li > p {
  margin: 0.25em 0em !important;
}
.code-content > pre {
  padding: 0px !important;
}
.code-content pre {
  margin: 0px !important;
}
code:not(pre code) {
  background-color: #222 !important;
  border-radius: 0.25rem;
  border: 1px solid #444;
  padding: 0.125rem 0.5rem;
}
</style>
