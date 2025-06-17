import vue from "@vitejs/plugin-vue";
import vueJsx from "@vitejs/plugin-vue-jsx";
import UnoCSS from "unocss/vite";
import AutoImport from "unplugin-auto-import/vite";
import Components from "unplugin-vue-components/vite";
import { defineConfig } from "vite";
import { VitePWA } from "vite-plugin-pwa";

export default defineConfig(({ mode }) => ({
  // Only use define for production builds
  ...(mode === "production" && {
    define: {
      "import.meta.env.VITE_API_URL": '"__VITE_API_URL__"',
      "import.meta.env.VITE_OLLAMA_BASE_URL": '"__VITE_OLLAMA_BASE_URL__"',
    },
  }),
  preview: {
    port: 3002,
    allowedHosts: ["localhost", "mia.ulysmcm.com"],
  },
  // for dev
  server: {
    port: 3001,
  },
  plugins: [
    vue(),
    vueJsx(),
    UnoCSS(),
    Components({
      dirs: ["./src/components", "./src/views"],
      dts: "./src/components.d.ts",
    }),
    AutoImport({
      imports: ["vue", "@vueuse/core", "vue-router"],
      dirs: ["./src/composables", "./src/locale"],
      dts: "./src/auto-import.d.ts",
    }),
    VitePWA({
      registerType: "autoUpdate",
      includeAssets: ["favicon.ico", "apple-touch-icon.png"],
      workbox: {
        maximumFileSizeToCacheInBytes: 10 * 1024 * 1024,
      },
      manifest: {
        name: "Chat UI",
        short_name: "Chat UI",
        description: "A chat application built with Gemini UI Style",
        theme_color: "#131314",
        icons: [
          {
            src: "pwa-64x64.png",
            sizes: "64x64",
            type: "image/png",
          },
          {
            src: "pwa-192x192.png",
            sizes: "192x192",
            type: "image/png",
          },
          {
            src: "pwa-512x512.png",
            sizes: "512x512",
            type: "image/png",
          },
          {
            src: "maskable-icon-512x512.png",
            sizes: "512x512",
            type: "image/png",
            purpose: "maskable",
          },
        ],
      },
    }),
  ],
}));
