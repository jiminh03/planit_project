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

const app = createApp(App)

app.use(createPinia())
app.use(router)

const userStore = useUserStore()
userStore.restore()

// 로그인 상태 백엔드에서 재확인
axios.get('/api/accounts/me/')
  .then(res => {
    userStore.login(res.data)
  })
  .catch(() => {
    userStore.logout()
  })

app.mount('#app')

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