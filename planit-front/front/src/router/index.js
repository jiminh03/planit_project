import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/analysis/summary', component: HomeView },
  { path: '/analysis/pattern', component: HomeView },
  { path: '/analysis/date', component: HomeView },
  { path: '/analysis/emotion', component: HomeView },
  { path: '/analysis/category', component: HomeView },
  { path: '/analysis/type', component: HomeView },
  { path: '/analysis/feedback', component: HomeView },
  { path: '/guide/message', component: HomeView },
  { path: '/guide/strategy', component: HomeView },
  { path: '/guide/simulation', component: HomeView },
  { path: '/guide/fixed', component: HomeView },
  { path: '/guide/combo', component: HomeView },
  { path: '/settings', component: HomeView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
