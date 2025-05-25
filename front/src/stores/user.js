// stores/user.js
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    isLoggedIn: false,
    username: '',
    email: '',
    userId: null,
  }),
  actions: {
    login(user) {
      this.isLoggedIn = true
      this.username = user.username
      this.email = user.email
      this.userId = user.id
      localStorage.setItem('isLoggedIn', true)
      localStorage.setItem('username', user.username)
      localStorage.setItem('email', user.email)
      localStorage.setItem('userId', user.id)
      console.log('User logged in:', {
        isLoggedIn: this.isLoggedIn,
        username: this.username,
        email: this.email,
        userId: this.userId,
      })
    },
    logout() {
      this.isLoggedIn = false
      this.username = ''
      this.email = ''
      this.userId = null
      localStorage.removeItem('isLoggedIn')
      localStorage.removeItem('username')
      localStorage.removeItem('email')
      localStorage.removeItem('userId')
      console.log('User logged out')
    },
    restore() {
      this.isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
      this.username = localStorage.getItem('username') || ''
      this.email = localStorage.getItem('email') || ''
      this.userId = localStorage.getItem('userId') ? Number(localStorage.getItem('userId')) : null
      console.log('User state restored:', {
        isLoggedIn: this.isLoggedIn,
        username: this.username,
        email: this.email,
        userId: this.userId,
      })
    }
  }
})