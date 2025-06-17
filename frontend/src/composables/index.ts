import { platform, model } from "../shared";
import { fetchRagModels } from "./useRAG";

// Default values - easy to change later
const DEFAULT_MODEL_RAG = "qwen3:30b-a3b";

export function useModels() {
  const models = ref<string[]>([]);

  function getDefaultModel(fetchedModels: string[]): string {
    if (fetchedModels.length === 0) return "";
    
    let defaultModel = "";
    
    // Set platform-specific defaults
    switch (platform.value) {
      case "rag":
        defaultModel = DEFAULT_MODEL_RAG;
        break;
      default:
        console.warn(`No default model set for platform: ${platform.value}`);
        break;
    }
    
    // Check if the default model exists in the fetched models, otherwise use first available
    return fetchedModels.includes(defaultModel) ? defaultModel : fetchedModels[0];
  }

  async function fetchAndSetModels() {
    try {
      let fetchedModels: string[] = [];
      
      if (platform.value === "rag") {
        fetchedModels = await fetchRagModels();
      }
      
      models.value = fetchedModels;
      
      // Auto-select the default model if none is selected
      if (fetchedModels.length > 0 && !model.value) {
        model.value = getDefaultModel(fetchedModels);
      }
    } catch (error) {
      console.error(error);
    }
  }

  onMounted(async () => {
    await fetchAndSetModels();
  });

  return models;
}
