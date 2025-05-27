// stores/user.js
import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore('user', {
  state: () => ({
    isLoggedIn: false,
    username: '',
    email: '',
    userId: null,
    isAdmin: false,
  }),
  actions: {
    login(user) {
      this.isLoggedIn = true
      this.username = user.username
      this.email = user.email
      this.userId = user.id
      this.isAdmin = user.isAdmin ?? user.is_staff ?? false
      localStorage.setItem('isLoggedIn', true)
      localStorage.setItem('username', user.username)
      localStorage.setItem('email', user.email)
      localStorage.setItem('userId', user.id)
      localStorage.setItem('isAdmin', this.isAdmin)
      console.log('User logged in:', {
        isLoggedIn: this.isLoggedIn,
        username: this.username,
        email: this.email,
        userId: this.userId,
        isAdmin: this.isAdmin,
      })
      console.log('로그인 응답 객체:', user)
    },
    logout() {
      function getCookie(name) {
        const value = `; ${document.cookie}`
        const parts = value.split(`; ${name}=`)
        if (parts.length === 2) return parts.pop().split(';').shift()
      }
      const csrfToken = getCookie('csrftoken')

      return axios.post('/api/accounts/logout/', {}, {
        headers: {
          'X-CSRFToken': csrfToken
        },
        withCredentials: true
      })
        .then(() => {
          this.isLoggedIn = false
          this.username = ''
          this.email = ''
          this.userId = null
          this.isAdmin = false
          localStorage.removeItem('isLoggedIn')
          localStorage.removeItem('username')
          localStorage.removeItem('email')
          localStorage.removeItem('userId')
          localStorage.removeItem('isAdmin')
          console.log('User logged out')
        })
        .catch((error) => {
          console.error('Logout failed:', error)
        })
    },
    async restore() {
      try {
        const response = await axios.get('/api/accounts/me/', {
          withCredentials: true
        })

        const user = response.data
        this.isLoggedIn = true
        this.username = user.username
        this.email = user.email
        this.userId = user.id
        this.isAdmin = user.isAdmin ?? user.is_staff ?? false

        console.log('User restored from server session:', user)
      } catch (error) {
        // 세션 없음 → 로그아웃 상태 유지
        this.isLoggedIn = false
        this.username = ''
        this.email = ''
        this.userId = null
        this.isAdmin = false
        console.warn('❌ 세션이 만료되어 로그인 복원 실패')
      }
    },

    async fetchHelperAnalysis() {
      try {
        const csrfToken = this.getCookie('csrftoken')
        const response = await axios.post(
          '/api/helper/analysis/',
          { email: this.email },  // ✅ store에서 보관 중인 이메일 사용
          {
            headers: {
              'X-CSRFToken': csrfToken,
              'Content-Type': 'application/json',
            },
            withCredentials: true,
          }
        )
        return response.data.result
      } catch (error) {
        throw error.response?.data?.error || '서버 오류 발생'
      }
    },

    // ✅ 쿠키 꺼내는 함수도 store 안에 정의
    getCookie(name) {
      const value = `; ${document.cookie}`
      const parts = value.split(`; ${name}=`)
      if (parts.length === 2) return parts.pop().split(';').shift()
    },

  }
})