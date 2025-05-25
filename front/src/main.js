import axios from 'axios'
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { useUserStore } from './stores/user'

axios.defaults.baseURL = 'http://localhost:8000'
axios.defaults.withCredentials = true

function getCookie(name) {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'))
  if (match) return match[2]
  return null
}

axios.interceptors.request.use(config => {
  const token = getCookie('csrftoken')
  if (token) {
    config.headers['X-CSRFToken'] = token
  }
  return config
})

// 초기 테마 적용 (Vue 앱 로딩 전에 HTML에 먼저 적용)
const savedTheme = localStorage.getItem('theme') || 'system'
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
const resolvedTheme = savedTheme === 'system' ? (prefersDark ? 'dark' : 'light') : savedTheme
document.documentElement.setAttribute('data-theme', resolvedTheme)

const app = createApp(App)

app.use(createPinia())
app.use(router)

const userStore = useUserStore()

// 로그인 상태 백엔드에서 재확인
axios.get('/api/accounts/me/')
  .then(res => {
    userStore.login({
      ...res.data,
      isAdmin: res.data.is_staff  // 명시적으로 추가
    })
  })
  .catch(() => {
    userStore.logout()
  })
  .finally(() => {
    // app.mount('#app')는 그대로 유지
    app.mount('#app')

    // Apply dark class to body based on localStorage
    if (localStorage.getItem('theme') === 'dark') {
      document.body.classList.add('dark')
    } else {
      document.body.classList.remove('dark')
    }
  })

const params = new URLSearchParams(window.location.search)
if (params.has('code') && params.has('state')) {
  axios.get(`http://localhost:8000/api/accounts/naver/callback/?code=${params.get('code')}&state=${params.get('state')}`, {
    withCredentials: true
  }).then(() => {
    window.location.href = '/home'
  }).catch(() => {
    alert('네이버 로그인 실패')
  })
}