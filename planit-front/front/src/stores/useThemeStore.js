// stores/useThemeStore.js
import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    theme: 'system', // 기본값: 'system' | 'light' | 'dark'
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
      this.applyTheme()
    },
    applyTheme() {
      const themeClass = this.currentTheme
      document.documentElement.setAttribute('data-theme', themeClass)
    }
  }
})