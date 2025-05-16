// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import SignupView from '@/views/SignupView.vue'
import LoginView from '@/views/LoginView.vue'
import NoticeView from '@/views/NoticeView.vue'
import FeatureView from '@/views/FeatureView.vue'


const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/signup', name: 'Signup', component: SignupView },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/notices', name: 'Notices', component: NoticeView },  // ✅ 추가
  { path: '/features', name: 'Features', component: FeatureView },  // ✅ 추가
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
