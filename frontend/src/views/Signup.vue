<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAgentStore } from "../stores/agent";
// import { useMainStore } from "../stores/main";

const email = ref("");
const username = ref("");
const password = ref("");
const confirmPassword = ref("");
const errorMessage = ref("");

const router = useRouter();
const authStore = useAgentStore();
// const mainStore = useMainStore();

async function handleSignup() {
  errorMessage.value = "";
  if (password.value !== confirmPassword.value) {
    errorMessage.value = "Passwords do not match.";
    return;
  }

  if (!email.value || !username.value || !password.value) {
    errorMessage.value = "All fields are required.";
    return;
  }

  const success = await authStore.signUp({
    email: email.value,
    username: username.value,
    password: password.value,
  });

  if (success) {
    // Toast is handled in the store action
    router.push({ name: "signIn" });
  } else {
    // Error toast is handled in the store action, but you can set a local error too if needed
    // errorMessage.value = mainStore.toasts[mainStore.toasts.length -1]?.message || "Signup failed. Please try again.";
  }
}
</script>

<template>
  <div class="flex min-h-screen items-center justify-center bg-[#131314] p-4">
    <div class="w-full max-w-md rounded-xl bg-[#1a1a1a] p-8 shadow-xl">
      <h2 class="mb-8 text-center text-3xl font-bold text-white">Sign Up</h2>
      <form @submit.prevent="handleSignup">
        <div class="mb-6">
          <label
            for="email"
            class="mb-2 block text-sm font-medium text-neutral-300"
            >Email</label
          >
          <input
            id="email"
            v-model="email"
            type="email"
            class="w-full rounded-lg border border-neutral-700 bg-neutral-800 p-3 text-white placeholder-neutral-500 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50"
            placeholder="Enter your email"
            required
          />
        </div>
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
            placeholder="Choose a username"
            required
          />
        </div>
        <div class="mb-6">
          <label
            for="password"
            class="mb-2 block text-sm font-medium text-neutral-300"
            >Password</label
          >
          <input
            id="password"
            v-model="password"
            type="password"
            class="w-full rounded-lg border border-neutral-700 bg-neutral-800 p-3 text-white placeholder-neutral-500 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50"
            placeholder="Create a password"
            required
          />
        </div>
        <div class="mb-6">
          <label
            for="confirmPassword"
            class="mb-2 block text-sm font-medium text-neutral-300"
            >Confirm Password</label
          >
          <input
            id="confirmPassword"
            v-model="confirmPassword"
            type="password"
            class="w-full rounded-lg border border-neutral-700 bg-neutral-800 p-3 text-white placeholder-neutral-500 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50"
            placeholder="Confirm your password"
            required
          />
        </div>
        <div v-if="errorMessage" class="mb-4 text-sm text-red-400">
          {{ errorMessage }}
        </div>
        <button
          type="submit"
          class="w-full rounded-lg bg-purple-600 px-4 py-3 text-lg font-semibold text-white transition-colors hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-[#1a1a1a]"
        >
          Create Account
        </button>
        <p class="mt-6 text-center text-sm text-neutral-400">
          Already have an account?
          <router-link
            :to="{ name: 'signIn' }"
            class="font-medium text-purple-400 hover:text-purple-300"
            >Login</router-link
          >
        </p>
      </form>
    </div>
  </div>
</template>