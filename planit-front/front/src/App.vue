<template>
  <ThemeSelector />
  <div class="app-layout">
    <TopHeader />
    <div class="main-layout">
      <SidebarMenu />
      <div class="content-view">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup>
import TopHeader from '@/components/TopHeader.vue'
import SidebarMenu from '@/components/SidebarMenu.vue'
import { onMounted } from 'vue'
import { useThemeStore } from '@/stores/useThemeStore'
import ThemeSelector from './components/ThemeSelector.vue'
const themeStore = useThemeStore()

onMounted(() => {
  themeStore.applyTheme()

  // 시스템 설정 변경 감지
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    if (themeStore.theme === 'system') {
      themeStore.applyTheme()
    }
  })
})
</script>

<style>
html, body, #app {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}

*, *::before, *::after {
  box-sizing: inherit;
}

body {
  font-family: sans-serif;
  background-color: var(--bg-color);
  color: var(--text-color);
}

:root[data-theme='light'] {
  --bg-color: #fff;
  --text-color: #000;
}

:root[data-theme='light'] {
  --sidebar-bg-color: #f8f8f8;
  --sidebar-text-color: #222;
  --logout-button-bg: #f44336;
  --logout-button-hover: #d32f2f;
  --logout-button-text: #fff;
}

:root[data-theme='dark'] {
  --bg-color: #1e1e1e;
  --text-color: #f0f0f0;
}

:root[data-theme='dark'] {
  --sidebar-bg-color: #1e1e1e;
  --sidebar-text-color: #ffffff;
  --logout-button-bg: #b71c1c;
  --logout-button-hover: #8e0000;
  --logout-button-text: #fff;
}

.app-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.main-layout {
  display: flex;
  flex: 1;
}

.content-view {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}
</style>
