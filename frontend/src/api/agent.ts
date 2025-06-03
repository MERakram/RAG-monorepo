import axios from "axios";

import { useAgentStore } from "../stores";

const apiUrl = import.meta.env.VITE_API_URL;

export const useAgentsApi = () => {
  const client = axios.create({ baseURL: apiUrl });
  const url = "authentication";
  const _axios = async () => {
    const store = useAgentStore();
    if (await store.checkToken()) {
      const auth = `Bearer ${store.accessToken}`;
      client.defaults.headers.common["Authorization"] = auth;
    }

    return client;
  };

  const api = {
    me: async () => {
      return (await _axios()).get(url + "/me");
    },

    signin: async (data: any) => {
      const params = new URLSearchParams();
      params.append("username", data.username);
      params.append("password", data.password);
      return (await _axios()).post(url + "/sign-in", params, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });
    },

    signup: async (data: any) => {
      return (await _axios()).post(url + "/sign-up", data);
    },

    refreshingToken: async () => {
      return (await _axios()).post(url + "/refresh");
    },

    patch: async (data: any) => {
      return (await _axios()).patch(url + "/me", data);
    },

    changePassword: async (data: any) => {
      return (await _axios()).post(url + "/change-password", data);
    },

    raw: async () => {
      return await _axios();
    },

    getApiUrl: () => {
      return url;
    },
  };

  return { agentsApi: api };
};
