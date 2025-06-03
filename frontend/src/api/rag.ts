import { useApi } from "./api";
import { serviceUrl } from "../shared"; // Assuming serviceUrl.value is the base URL for your RAG service

export const useRagApi = () => {
  const { axios: getApiClient } = useApi();

  const RAG_BASE_URL = serviceUrl.value; 

  const ragApi = {
    chat: async (payload: { query: string; model?: string }) => {
      const apiClient = await getApiClient();
      return apiClient.post(`${RAG_BASE_URL}/chat`, payload);
    },

    getModels: async () => {
      const apiClient = await getApiClient();
      return apiClient.get(`${RAG_BASE_URL}/models`);
    },
  };

  return { ragApi };
};