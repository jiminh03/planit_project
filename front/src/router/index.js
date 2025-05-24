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

  const isLoggedIn = userStore.isLoggedIn
  const isPublic = publicPages.includes(to.path)

  if (!isPublic && !isLoggedIn) {
    next({ path: '/login', query: { redirect: to.fullPath } })
  } else if (to.path === '/home' && !isLoggedIn) {
    next('/login')  // 혹시라도 명시적으로 홈 접근을 막고 싶다면
  } else {
    next()
  }
})

export default router