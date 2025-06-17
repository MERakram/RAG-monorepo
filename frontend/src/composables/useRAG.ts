import { useRagApi } from "../api/rag";
import { model, selectedCollection } from "../shared";
import type { ChatMessage } from "./useHelloWorld";

// Function to extract numeric part from collection names
function extractCollectionId(
  collectionName: string | null | undefined
): string | undefined {
  if (!collectionName) return undefined;

  // Remove "IEC ", "EN ", and any spaces, return just the numeric part
  return collectionName
    .replace(/^(IEC|EN)\s+/i, "") // Remove IEC or EN prefix with spaces
    .trim(); // Remove any remaining spaces
}

export async function* streamRagChat(messages: ChatMessage[]) {
  const { ragApi } = useRagApi();

  try {
    console.log("Using RAG service with model:", model.value);

    const lastUserMessage =
      [...messages].filter((m) => m.role === "user").pop()?.content || "";

    const collectionName = extractCollectionId(selectedCollection.value);

    if (!collectionName) {
      throw new Error("No collection selected");
    }

    const payload = {
      query: lastUserMessage.trim(),
      model: model.value || undefined,
      collection_name: collectionName,
    };

    // Use the ragApi chatStream function (returns fetch Response)
    const response = await ragApi.chatStream(payload);

    if (!response.body) {
      throw new Error("No response body");
    }

    // Handle fetch ReadableStream properly for real streaming
    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split("\n").filter((line) => line.trim());

        for (const line of lines) {
          try {
            const data = JSON.parse(line);

            if (data.done) {
              if (data.sources) {
                console.log("Received sources:", data.sources);
                yield {
                  content: data.sources,
                  delta: data.sources,
                  message: {
                    content: data.sources,
                  },
                };
              }
              continue;
            }

            const content = data.message?.content || data.content || "";

            if (content) {
              yield {
                content,
                delta: content,
                message: {
                  content,
                },
              };
            }
          } catch (parseError) {
            console.warn("Failed to parse streaming chunk:", line);
          }
        }
      }
    } finally {
      reader.releaseLock();
    }
  } catch (error: any) {
    console.error("RAG service error:", error);
    throw new Error(`RAG service error: ${error.message || "Unknown error"}`);
  }
}

export async function* streamCompareStandards(
  file1Content: string,
  file1Name: string,
  file2Content: string,
  file2Name: string,
  mode: string
) {
  const { ragApi } = useRagApi();

  try {
    console.log("Using comparison service with model:", model.value);
    console.log("Comparison mode:", mode);

    // Use sanitizeCollectionName instead of extractCollectionId to handle prefixes and spaces
    const collectionName = extractCollectionId(selectedCollection.value);

    if (!collectionName) {
      throw new Error("No collection selected");
    }

    const payload = {
      file1_content: file1Content,
      file1_name: file1Name,
      file2_content: file2Content,
      file2_name: file2Name,
      mode: mode,
      model: model.value || undefined,
      collection_name: collectionName,
    };

    // Use the ragApi compareStream function (returns fetch Response)
    const response = await ragApi.compareStream(payload);

    if (!response.body) {
      throw new Error("No response body");
    }

    // Handle fetch ReadableStream properly for real streaming
    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split("\n").filter((line) => line.trim());

        for (const line of lines) {
          try {
            const data = JSON.parse(line);

            if (data.done) {
              if (data.sources) {
                console.log("Received sources:", data.sources);
                yield {
                  content: data.sources,
                  delta: data.sources,
                  message: {
                    content: data.sources,
                  },
                };
              }
              continue;
            }

            const content = data.message?.content || data.content || "";

            if (content) {
              yield {
                content,
                delta: content,
                message: {
                  content,
                },
              };
            }
          } catch (parseError) {
            console.warn("Failed to parse streaming chunk:", line);
          }
        }
      }
    } finally {
      reader.releaseLock();
    }
  } catch (error: any) {
    console.error("Comparison service error:", error);
    throw new Error(
      `Comparison service error: ${error.message || "Unknown error"}`
    );
  }
}

export async function fetchRagModels() {
  const { ragApi } = useRagApi();

  try {
    const response = await ragApi.getModels();
    return response.data.models;
  } catch (error: any) {
    console.error("Failed to fetch RAG models:", error);
    throw new Error(
      `Failed to fetch models: ${error.message || "Unknown error"}`
    );
  }
}
