import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import AnalysisView from '@/views/AnalysisView.vue'
import GuideView from '@/views/GuideView.vue'
import SettingsView from '@/views/SettingsView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/analysis', name: 'analysis', component: AnalysisView },
  { path: '/guide', name: 'guide', component: GuideView },
  { path: '/settings', name: 'settings', component: SettingsView },

  // 기존 하위 경로도 필요시 유지
  { path: '/analysis/summary', component: HomeView },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router