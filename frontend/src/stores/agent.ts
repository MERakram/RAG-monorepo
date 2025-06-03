import { defineStore, createPinia } from "pinia";
import piniaPersistedstate from "pinia-plugin-persistedstate";
import { User } from "../models";
import { useAgentsApi } from "../api";

const { agentsApi: api } = useAgentsApi();

const pinia = createPinia();
pinia.use(piniaPersistedstate);

export const useAgentStore = defineStore("storeAgent", {
  state: (): AgentType => {
    return {
      id: 0,
      username: "",
      sideToggell: false,
      role: "",
      active: false,
      isLoggedIn: false,
      accessToken: "",
      refreshToken: "",
    };
  },

  actions: {
    async signIn(username: string, password: string): Promise<boolean> {
      let tokens: { accessToken: string; refreshToken: string };

      try {
        const { data, status } = await api.signin({ username, password });
        if (status !== 200 && status !== 201) {
          console.log("Sign in failed", status);
          return false;
        }
        tokens = {
          accessToken: data.access_token,
          refreshToken: data.refresh_token,
        };
      } catch {
        console.log("Sign in failed");
        return false;
      }

      this.setTokens(tokens);

      try {
        const { data: userData, status: userStatus } = await api.me();
        if (userStatus !== 200) {
          this.loggedOut();
          this.$reset();
          console.log("Failed to fetch user details", userStatus);
          return false;
        }

        if (!userData.active) {
          this.loggedOut();
          this.$reset();
          console.log("Account not active");
          return false;
        }

        this.setUser(userData);
        this.isLoggedIn = true;
        return true;
      } catch (error) {
        this.loggedOut();
        this.$reset();
        console.log("Error verifying user status", error);
        return false;
      }
    },

    async signUp(payload: {
      email: string;
      password: string;
      username: string;
    }): Promise<boolean> {
      try {
        const { status } = await api.signup(payload);
        if (status !== 201 && status !== 200) {
          return false;
        }
        return true;
      } catch (error: unknown) {
        
        return false;
      }
    },

    async changePassword(
      oldPassword: string,
      newPassword: string
    ): Promise<boolean> {
      const { agentsApi: api } = useAgentsApi();
      try {
        await api.changePassword({
          oldPassword: oldPassword,
          newPassword: newPassword,
        });
        
      } catch (error: unknown) {
        return false;
      }
      return true;
    },

    async changeUserName(
      firstname: string,
      lastname: string
    ): Promise<boolean> {
      const { agentsApi: api } = useAgentsApi();
      try {
        await api.patch({
          profile: {
            firstname,
            lastname,
          },
        });
        
        this.isLoggedIn = true;
        // this.setUser(data);
      } catch (error: unknown) {
        return false;
      }
      return true;
    },

    async update(user: User): Promise<boolean> {
      try {
        const data = await api.patch(user);
        this.setUser(data.data);
      } catch {
        return false;
      }
      return true;
    },

    async checkToken(): Promise<boolean> {
      try {
        const jwt = parseJwt(this.accessToken);
        if (jwt.exp > Date.now() / 1000) return true;

        // Token is expired
        this.loggedOut(); // Set isLoggedIn to false
        return false;
      } catch {
        this.loggedOut(); // Handle invalid tokens
        return false;
      }
    },

    // async refreshingToken(): Promise<boolean> {
    //   try {
    //     const refresh = parseJwt(this.refreshToken);
    //     if (refresh.exp < Date.now() / 1000) throw new Error('Expired token');
    //     const { data } = await api.refreshingToken();
    //     this.setTokens(data);
    //   } catch {
    //     this.logout();
    //     return false;
    //   }
    //   return true;
    // },
    async toggell(): Promise<boolean> {
      try {
        this.sideToggell = !this.sideToggell;
      } catch {
        return false;
      }
      return true;
    },
    async logout(): Promise<boolean> {
      this.$reset();
      this.loggedOut();
      return true;
    },

    setTokens(payload: { accessToken: string; refreshToken: string }) {
      this.accessToken = payload.accessToken;
      this.refreshToken = payload.refreshToken;
    },

    loggedOut() {
      this.isLoggedIn = false;
    },

    setUser(payload: Omit<AgentType, "accessToken">) {
      if (payload.id) {
        this.id = payload.id;
      }
      if (payload.active) {
        this.active = payload.active;
      }
      if (payload.role) {
        this.role = payload.role;
      }
      if (payload.username) {
        this.username = payload.username;
      }
    },
  },

  persist: true,
});

const parseJwt = (token: string) => {
  const base64Url = token.split(".")[1];
  const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
  const jsonPayload = decodeURIComponent(
    window
      .atob(base64)
      .split("")
      .map(function (c) {
        return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
      })
      .join("")
  );

  return JSON.parse(jsonPayload);
};

type AgentType = {
  id: number;
  sideToggell: boolean;
  active: boolean;
  username: string;
  role: string;
  isLoggedIn: boolean;
  accessToken: string;
  refreshToken: string;
};

export { useAgentsApi };
