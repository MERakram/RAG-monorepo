<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAgentStore } from "../stores/agent";

const username = ref("");
const password = ref("");
const errorMessage = ref("");
const showPassword = ref(false);

const router = useRouter();
const authStore = useAgentStore();

async function handleLogin() {
  errorMessage.value = "";
  if (await authStore.signIn(username.value, password.value)) {
    router.push({ name: "chat-home" });
  } else {
    errorMessage.value = "Invalid username or password.";
  }
}

function togglePasswordVisibility() {
  showPassword.value = !showPassword.value;
}
</script>

<template>
  <div class="flex min-h-screen items-center justify-center bg-[#131314] p-4">
    <div class="w-full max-w-md rounded-xl bg-[#1a1a1a] p-8 shadow-xl">
      <h2 class="mb-8 text-center text-3xl font-bold text-white">Login</h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-6">
          <label
            for="username"
            class="mb-2 block text-sm font-medium text-neutral-300"
            >Username</label
          >
          <input
            id="username"
            v-model="username"
            type="text"
            class="w-full rounded-lg border border-neutral-700 bg-neutral-800 p-3 text-white placeholder-neutral-500 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50"
            placeholder="Enter your username"
            required
          />
        </div>
        <div class="mb-6">
          <label
            for="password"
            class="mb-2 block text-sm font-medium text-neutral-300"
            >Password</label
          >
          <div class="relative">
            <input
              id="password"
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              class="w-full rounded-lg border border-neutral-700 bg-neutral-800 p-3 pr-12 text-white placeholder-neutral-500 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50"
              placeholder="Enter your password"
              required
            />
            <button
              type="button"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-neutral-400 hover:text-neutral-300 transition-colors"
              @click="togglePasswordVisibility"
            >
              <i 
                :class="showPassword ? 'i-tabler-eye-off' : 'i-tabler-eye'" 
                class="text-lg"
              />
            </button>
          </div>
        </div>
        <div v-if="errorMessage" class="mb-4 text-sm text-red-400">
          <img src="../assets/tenor.gif" alt="Error" class="w-full h-auto" />
        </div>
        <button
          type="submit"
          class="w-full rounded-lg bg-purple-600 px-4 py-3 text-lg font-semibold text-white transition-colors hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-[#1a1a1a]"
        >
          Login
        </button>
        <p class="mt-6 text-center text-sm text-neutral-400">
          Don't have an account?
          <router-link
            :to="{ name: 'signUp' }"
            class="font-medium text-purple-400 hover:text-purple-300"
            >Sign Up</router-link
          >
        </p>
      </form>
    </div>
  </div>
</template>