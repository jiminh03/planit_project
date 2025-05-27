import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import AnalysisView from '@/views/AnalysisView.vue'
import GuideView from '@/views/GuideView.vue'
import SettingsView from '@/views/SettingsView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import { useUserStore } from '@/stores/user'
import Mainview from '@/views/Mainview.vue'
import NoticeView from '@/views/NoticeView.vue'
import NoticeDetailView from '@/views/NoticeDetailView.vue'
// import NoticeCreateView from '@/views/NoticeCreateView.vue'

const routes = [
  { path: '/', redirect: '/main' },
  { path: '/main', name: 'main', component: Mainview },
  { path: '/notice', name: 'notice', component: NoticeView },
  // { path: '/notice/create', name: 'NoticeCreate', component: NoticeCreateView },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/signup', name: 'signup', component: SignupView },
  { path: '/home', name: 'home', component: HomeView },
  { path: '/analysis', name: 'analysis', component: AnalysisView },
  { path: '/guide', name: 'guide', component: GuideView },
  { path: '/settings', name: 'settings', component: SettingsView },
  { path: '/analysis/summary', component: HomeView },
  { path: '/notice/:id', name: 'NoticeDetail', component: NoticeDetailView },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const publicPaths = ['/login', '/signup', '/main', '/notice']
  const userStore = useUserStore()
  await userStore.restore()

  const isLoggedIn = userStore.isLoggedIn
  const isPublic = publicPaths.some(path => to.path.startsWith(path))

  // 🔒 로그인 안 한 유저가 보호 페이지 접근 시
  if (!isPublic && !isLoggedIn) {
    next({ path: '/main', query: { redirect: to.fullPath } })

    // ✅ 로그인 했고, 쿼리에 redirect가 있는 경우 → 해당 경로로 이동 + 쿼리 제거
  } else if (to.query.redirect && isLoggedIn) {
    const redirectPath = to.query.redirect
    next(redirectPath)  // 한 번 이동하고
    router.replace(redirectPath) // 쿼리 제거

    // 🎯 그 외는 정상 이동
  } else {
    next()
  }
})


export default router
