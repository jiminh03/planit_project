<template>
  <div class="app-layout">
    <TopHeader class="top-header" />
    <div class="scroll-wrapper">
      <div v-if="!isAuthPage" class="main-layout">
        <div v-if="!userStore.isLoggedIn && !isAuthPage && introImages.length" class="intro-images">
          <img v-for="(img, index) in introImages" :key="index" :src="img" class="full-width-img" alt="Planit 소개 이미지" />
        </div>
        <div v-if="userStore.isLoggedIn">
          <SidebarMenu />
        </div>
        <div class="content-view">
          <router-view />
        </div>
      </div>
      <div v-else class="content-view">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onBeforeMount } from 'vue'
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import TopHeader from '@/components/TopHeader.vue'
import SidebarMenu from '@/components/SidebarMenu.vue'
import { useUserStore } from '@/stores/user'

import introImage1 from '@/assets/001.png'
import introImage2 from '@/assets/002.png'
import introImage3 from '@/assets/003.png'
import introImage4 from '@/assets/004.png'
import introImage5 from '@/assets/005.png'

const introImages = [introImage1, introImage2, introImage3, introImage4, introImage5]
console.log('Loaded introImages:', introImages)

onBeforeMount(() => {
  const savedTheme = localStorage.getItem('theme') || 'system'
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  const resolvedTheme = savedTheme === 'system' ? (prefersDark ? 'dark' : 'light') : savedTheme
  document.documentElement.setAttribute('data-theme', resolvedTheme)
})

const route = useRoute()
const authPaths = ['/login', '/signup']
const isAuthPage = computed(() => authPaths.includes(route.path))
const userStore = useUserStore()
</script>

<style>
html, body, #app {
  margin: 0;
  padding: 0;
  width: 100%;
  min-height: 100vh;
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

html[data-theme='light'] {
  --bg-color: #fff;
  --text-color: #000;
}

html[data-theme='light'] {
  --sidebar-bg-color: #f8f8f8;
  --sidebar-text-color: #222;
  --logout-button-bg: #f44336;
  --logout-button-hover: #d32f2f;
  --logout-button-text: #fff;
}

html[data-theme='dark'] {
  --bg-color: #3f3f3f;
  --text-color: #f0f0f0;
}

html[data-theme='dark'] {
  --sidebar-bg-color: #1e1e1e;
  --sidebar-text-color: #ffffff;
  --logout-button-bg: #b71c1c;
  --logout-button-hover: #8e0000;
  --logout-button-text: #fff;
}

.app-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-layout {
  display: block;
}

.scroll-wrapper {
  flex: 1;
  overflow-y: auto;
  height: 100%;
}

.content-view {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.top-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  background-color: var(--sidebar-bg-color);
}
.full-width-img {
  width: 100%;
  height: auto;
  display: block;
}
</style>
