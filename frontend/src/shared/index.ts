import type { ChatData } from "../composables/useHelloWorld";
import { useIDBKeyval } from "@vueuse/integrations/useIDBKeyval";
import OpenAI from "openai";

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
const apiKeyKey = computed(() => {
  return `apiKey-${serviceUrl.value}`;
});

const modelKeyKey = computed(() => {
  return `model-${serviceUrl.value}`;
});

const selectedCollectionKey = computed(() => {
  return `selectedCollection-${serviceUrl.value}`;
});

export const model = useLocalStorage(modelKeyKey, "");
export const apiKey = useLocalStorage(apiKeyKey, "");
export const selectedCollection = useLocalStorage(selectedCollectionKey, "");

const defaultHeaders = computed(() => {
  const headers: Record<string, string | null> = {
    "x-stainless-timeout": null,
    "x-stainless-os": null,
    "x-stainless-version": null,
    "x-stainless-package-version": null,
    "x-stainless-runtime-version": null,
    "x-stainless-runtime": null,
    "x-stainless-arch": null,
    "x-stainless-retry-count": null,
    "x-stainless-lang": null,
  };
  if (platform.value === "ollama") {
    Object.keys(headers).forEach((key) => (headers[key] = null));
    headers["Content-Type"] = "application/json";
  }
  return headers;
});

export const client = computed(() => {
  const config = {
    apiKey: platform.value === "ollama" ? "ollama" : apiKey.value,
    baseURL: serviceUrl.value,
    dangerouslyAllowBrowser: true,
    defaultHeaders: defaultHeaders.value,
  };

  return new OpenAI(config);
});

export function useCurrentChat() {
  const route = useRoute();
  const id = computed(() => {
    return route.params.id as string;
  });
  return computed(() => {
    return chatHistory.value.find((chat) => chat.id === id.value) ?? null;
  });
}
