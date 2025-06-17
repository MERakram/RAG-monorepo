import { primaryColor } from "@roku-ui/vue";
import { createApp } from "vue";
import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';
import { createPinia } from "pinia";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import App from "./App.vue";
import router from "./router";
import i18n from "./locales";

import "@unocss/reset/tailwind.css";
import "virtual:uno.css";
import "katex/dist/katex.min.css";

primaryColor.value = "#9b95b8";

export const apiUrl = import.meta.env.VITE_API_URL

const app = createApp(App);

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

app.use(PrimeVue, {
    theme: {
        preset: Aura
    }
});
app.use(i18n);
app.use(pinia);
app.use(router);
router.isReady().then(() => app.mount('#app'));
