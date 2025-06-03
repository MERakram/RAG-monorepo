import { ref, onMounted } from "vue";
import { platform } from "../shared";

export function useCollections() {
  const collections = ref<string[]>([]);
  const isLoading = ref(false);
  const error = ref<Error | null>(null);

  async function fetchCollections() {
    if (platform.value === "rag") {
      isLoading.value = true;
      error.value = null;
      try {
        // Placeholder data:
        collections.value = [
          "EN 50470",
          "IEC 60051",
          "IEC 60688",
          "IEC 61326",
          "IEC 61557",
          "IEC 61810",
          "IEC 61850",
          "IEC 61869",
          "IEC 62053",
        ];
      } catch (err) {
        console.error("Failed to fetch collections:", err);
        error.value = err as Error;
        collections.value = ["default_collection"]; // Fallback or empty
      } finally {
        isLoading.value = false;
      }
    } else {
      // For other platforms like Ollama, you might have a fixed list or no collections
      collections.value = []; // Or a predefined list if applicable
    }
  }

  onMounted(() => {
    fetchCollections();
  });

  // Watch for platform changes to refetch if necessary
  watch(platform, () => {
    fetchCollections();
  });

  return collections;
}
