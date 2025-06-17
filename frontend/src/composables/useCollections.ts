import { ref, onMounted, watch } from "vue";
import { platform, selectedCollection } from "../shared";

// Default collection values - easy to change later
const DEFAULT_COLLECTION_RAG = "IEC 61850";

export function useCollections() {
  const collections = ref<string[]>([]);
  const isLoading = ref(false);
  const error = ref<Error | null>(null);

  function getDefaultCollection(fetchedCollections: string[]): string {
    if (fetchedCollections.length === 0) return "";

    // Check if the default collection exists in the fetched collections, otherwise use first available
    return fetchedCollections.includes(DEFAULT_COLLECTION_RAG)
      ? DEFAULT_COLLECTION_RAG
      : fetchedCollections[0];
  }

  async function fetchCollections() {
    if (platform.value === "rag") {
      isLoading.value = true;
      error.value = null;
      try {
        // Placeholder data:
        const fetchedCollections = [
          "EN 50470",
          "IEC 60051",
          "IEC 60688",
          "IEC 61557",
          "IEC 61810",
          "IEC 61850",
          "IEC 61010",
          "IEC 61326",
          "IEC 61869",
          "IEC 62053",
        ];

        collections.value = fetchedCollections;

        // Auto-select the default collection if none is selected
        if (fetchedCollections.length > 0 && !selectedCollection.value) {
          selectedCollection.value = getDefaultCollection(fetchedCollections);
        }
      } catch (err) {
        console.error("Failed to fetch collections:", err);
        error.value = err as Error;

        // Auto-select fallback collection if none is selected
        if (!selectedCollection.value) {
          console.warn("Using fallback collection due to error");
        }
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
