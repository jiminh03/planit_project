import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import AnalysisView from '@/views/AnalysisView.vue'
import GuideView from '@/views/GuideView.vue'
import SettingsView from '@/views/SettingsView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import { useUserStore } from '@/stores/user'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/signup', name: 'signup', component: SignupView },
  { path: '/home', name:'home', component: HomeView },
  { path: '/analysis', name: 'analysis', component: AnalysisView },
  { path: '/guide', name: 'guide', component: GuideView },
  { path: '/settings', name: 'settings', component: SettingsView },
  { path: '/analysis/summary', component: HomeView },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const publicPages = ['/login', '/signup']
  const userStore = useUserStore()
  userStore.restore()

  const authRequired = !publicPages.includes(to.path)
  const isLoggedIn = userStore.isLoggedIn

  if (authRequired && !isLoggedIn) {
    next({ path: '/login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router