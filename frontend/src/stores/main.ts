import { defineStore } from "pinia";

export const useMainStore = defineStore("main", {
  state: () => ({
    /* User */
    profile: { firstname: "", lastname: "", clientType: "" },
    userAvatar: "",

    /* Field focus with ctrl+k (to register only once) */
    isFieldFocusRegistered: false,
  }),
  actions: {
    setUser(payload: any) {
      if (payload.profile) {
        this.profile = payload.profile;
      }
      if (payload.avatar) {
        this.userAvatar = payload.avatar;
      }
    },
  },
  // persist: true,
});