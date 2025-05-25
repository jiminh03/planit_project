// stores/useThemeStore.js
import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    theme: localStorage.getItem('theme') || 'system',
  }),
  getters: {
    currentTheme(state) {
      if (state.theme === 'system') {
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
      }
      return state.theme
    }
  },
  actions: {
    setTheme(newTheme) {
      this.theme = newTheme
      localStorage.setItem('theme', newTheme)
      this.applyTheme()
    },
    applyTheme() {
      if (!this.theme) {
        this.theme = localStorage.getItem('theme') || 'system'
      }
      const themeClass = this.currentTheme
      document.documentElement.setAttribute('data-theme', themeClass)
    }
  }
})