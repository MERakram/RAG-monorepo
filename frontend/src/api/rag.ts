import { useApi } from "./api";
import { serviceUrl } from "../shared";

export const useRagApi = () => {
  const { axios: getApiClient } = useApi();
  const RAG_BASE_URL = serviceUrl.value;

  // Single API client instance
  const apiClientPromise = getApiClient();

  const ragApi = {
    chat: async (payload: {
      query: string;
      model?: string;
      collection_name: string;
    }) => {
      const apiClient = await apiClientPromise;
      return apiClient.post(`${RAG_BASE_URL}/chat`, payload);
    },

    chatStream: async (payload: {
      query: string;
      model?: string;
      collection_name: string;
    }) => {
      // For real streaming, we need fetch. Extract auth from axios client
      const apiClient = await apiClientPromise;
      const authHeader = apiClient.defaults.headers.common["Authorization"];

      const headers: Record<string, string> = {
        "Content-Type": "application/json",
        Accept: "application/x-ndjson",
      };

      if (authHeader && typeof authHeader === "string") {
        headers["Authorization"] = authHeader;
      }

      const response = await fetch(`${RAG_BASE_URL}/chat/stream`, {
        method: "POST",
        headers,
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return response;
    },
    
    chatWithFile: async (query: string, file: File, model?: string) => {
      const apiClient = await getApiClient();
      const formData = new FormData();
      formData.append("query", query);
      formData.append("file", file);
      if (model) {
        formData.append("model", model);
      }

      return apiClient.post(`${RAG_BASE_URL}/chat-with-file`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
    },

    uploadFile: async (file: File) => {
      const apiClient = await getApiClient();
      const formData = new FormData();
      formData.append("file", file);

      return apiClient.post(`${RAG_BASE_URL}/upload`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
    },

    getModels: async () => {
      const apiClient = await apiClientPromise;
      return apiClient.get(`${RAG_BASE_URL}/models`);
    },

    compare: async (payload: {
      file1_content: string;
      file1_name: string;
      file2_content: string;
      file2_name: string;
      mode: string;
      model?: string;
      collection_name: string;
    }) => {
      const apiClient = await apiClientPromise;
      return apiClient.post(`${RAG_BASE_URL}/compare`, payload);
    },

    compareStream: async (payload: {
      file1_content: string;
      file1_name: string;
      file2_content: string;
      file2_name: string;
      mode: string;
      model?: string;
      collection_name: string;
    }) => {
      // For real streaming, we need fetch. Extract auth from axios client
      const apiClient = await apiClientPromise;
      const authHeader = apiClient.defaults.headers.common["Authorization"];

      const headers: Record<string, string> = {
        "Content-Type": "application/json",
        Accept: "application/x-ndjson",
      };

      if (authHeader && typeof authHeader === "string") {
        headers["Authorization"] = authHeader;
      }

      const response = await fetch(`${RAG_BASE_URL}/compare/stream`, {
        method: "POST",
        headers,
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return response;
    },

    generateSummary: async (text: string, model?: string) => {
      const apiClient = await apiClientPromise;
      return apiClient.post(`${RAG_BASE_URL}/summary`, {
        text,
        model: model || "mistral-small3.1:latest",
      });
    },
  };

  return { ragApi };
};
