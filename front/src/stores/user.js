// stores/user.js
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    isLoggedIn: false,
    username: '',
  }),
  actions: {
    login(username) {
      this.isLoggedIn = true
      this.username = username
      localStorage.setItem('isLoggedIn', true)
      localStorage.setItem('username', username)
    },
    logout() {
      this.isLoggedIn = false
      this.username = ''
      localStorage.removeItem('isLoggedIn')
      localStorage.removeItem('username')
    },
    restore() {
      this.isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
      this.username = localStorage.getItem('username') || ''
    }
  }
})