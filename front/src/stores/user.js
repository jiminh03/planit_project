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
    restore() {
      this.isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
      this.username = localStorage.getItem('username') || ''
      this.email = localStorage.getItem('email') || ''
      this.userId = localStorage.getItem('userId') ? Number(localStorage.getItem('userId')) : null
      this.isAdmin = localStorage.getItem('isAdmin') === 'true'
      console.log('User state restored:', {
        isLoggedIn: this.isLoggedIn,
        username: this.username,
        email: this.email,
        userId: this.userId,
        isAdmin: this.isAdmin,
      })
    }
  }
})