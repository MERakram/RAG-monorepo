import axios from "axios";
import { useAgentStore } from "../stores";

const apiUrl = import.meta.env.VITE_API_URL;
const client = axios.create({ baseURL: apiUrl });
client.defaults.headers.common["Content-Type"] = "application/json";

export function useApi() {
  const axios = async () => {
    const store = useAgentStore();
    if (await store.checkToken()) {
      const auth = `Bearer ${store.accessToken}`;
      client.defaults.headers.common["Authorization"] = auth;
    }
    return client;
  };
  return { axios };
}

export const abstractApi = (apiUrl: string, name: string) => {
  return () => {
    const { axios } = useApi();
    const url = apiUrl;

    const api = {
      all: async (filters = "") => {
        return (await axios()).get(url + '/' + filters);
      },

      one: async (id: number) => {
        return (await axios()).get(url + "/" + id);
      },

      post: async (data: any) => {
        return (await axios()).post(url, data);
      },

      patch: async (id: number, data: any) => {
        return (await axios()).patch(url + "/" + id, data);
      },

      put: async (id: number, data: any) => {
        return (await axios()).put(url + "/" + id, data);
      },

      delete: async (id: number) => {
        return (await axios()).delete(url + "/" + id);
      },

      raw: async () => {
        return await axios();
      },

      getApiUrl: () => {
        return url;
      },
    };

    return { [name]: api };
  };
};