import type { ChatData } from "../composables/useHelloWorld";
import { useIDBKeyval } from "@vueuse/integrations/useIDBKeyval";

export const chatHistoryIDB = useIDBKeyval<ChatData[]>("chatHistory", [], {
  shallow: true,
});
export const chatHistory = computed({
  get: () => chatHistoryIDB.data.value,
  set: (value: ChatData[]) => {
    chatHistoryIDB.data.value = value;
  },
});

export const platform = useLocalStorage("platform", "rag");
export const serviceUrl = computed(() => {
  switch (platform.value) {
    case "ollama":
      return import.meta.env.VITE_OLLAMA_BASE_URL;
    case "rag":
      return import.meta.env.VITE_API_URL+"/rag";
  }
});

const modelKeyKey = computed(() => {
  return `model-${serviceUrl.value}`;
});

const selectedCollectionKey = computed(() => {
  return `selectedCollection-${serviceUrl.value}`;
});

export const model = useLocalStorage(modelKeyKey, "");
export const selectedCollection = useLocalStorage(selectedCollectionKey, "");

export function useCurrentChat() {
  const route = useRoute();
  const id = computed(() => {
    return route.params.id as string;
  });
  return computed(() => {
    return chatHistory.value.find((chat) => chat.id === id.value) ?? null;
  });
}
