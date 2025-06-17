import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import ChatView from "../views/Chat.vue";
import LoginView from "../views/Signin.vue";
import Signup from "../views/Signup.vue";
import { useAgentStore } from "../stores";

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    redirect: "/chat",
  },
  {
    path: "/sign-in",
    name: "signIn",
    component: LoginView,
    meta: { requiresAuth: false },
  },
  {
    path: '/sign-up',
    name: 'signUp',
    component: Signup,
    meta: { requiresAuth: false },
  },
  {
    path: '/chat',
    meta: { requiresAuth: true },
    children: [
      {
        name: 'chat-home',
        path: '',
        component: () => import('../views/Chat.vue'),
      },
      {
        name: 'chat',
        path: ':id',
        component: () => import('../views/Chat.vue'),
      },
    ],
  },
  {
    path: "/chat/:id",
    name: "chat",
    component: ChatView,
    meta: { requiresAuth: true },
  },
  {
    path: "/compare",
    name: "compare",
    component: () => import('../views/Compare.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: "/:pathMatch(.*)*",
    redirect: "/chat",
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
  scrollBehavior(_to, _from, savedPosition) {
    return savedPosition || { top: 0 };
  },
});

router.beforeEach(async (to, _from, next) => {
  const store = useAgentStore();

  // For routes requiring authentication, check if token is valid
  if (to.meta && to.meta.requiresAuth === true && store.isLoggedIn) {
    const isTokenValid = await store.checkToken();
    if (!isTokenValid) {
      return next({ name: "signIn" });
    }
  }

  // Continue with your existing logic
  if (to.name === "signIn") {
    next();
  } else if (store.isLoggedIn) {
    next();
  } else if (to.meta && to.meta.requiresAuth === false) {
    next();
  } else {
    next({ name: "signIn" });
  }
});

export default router;
