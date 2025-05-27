<template>
  <div class="app-layout">
    <TopHeader class="top-header" />

    <div class="main-layout">
      <!-- ✅ 사이드바 조건부 렌더링 -->
      <SidebarMenu v-if="showSidebar" />

      <div class="content-view" :style="{ marginLeft: showSidebar ? '220px' : '0' }">
        <!-- ✅ 인트로 이미지 조건부 렌더링 -->
        <div v-if="showIntroImages && introImages.length" class="intro-images">
          <img v-for="(img, index) in introImages" :key="index" :src="img" class="full-width-img" alt="Planit 소개 이미지" />
        </div>

        <!-- ✅ 페이지 본문 영역 -->
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeMount } from 'vue'
import { useRoute } from 'vue-router'
import TopHeader from '@/components/TopHeader.vue'
import SidebarMenu from '@/components/SidebarMenu.vue'
import { useUserStore } from '@/stores/user'

import introImage1 from '@/assets/001.png'
import introImage2 from '@/assets/002.png'
import introImage3 from '@/assets/003.png'
import introImage4 from '@/assets/004.png'
import introImage5 from '@/assets/005.png'

const route = useRoute()
const userStore = useUserStore()

// 🔹 사이드바가 없어야 할 경로
const sidebarExcludedPaths = ['/login', '/signup', '/main', '/main/features', '/main/intro']

// 🔹 인트로 이미지가 나올 경로
const introImagePaths = ['/main', '/main/features', '/main/intro']

// 🔹 사이드바 조건부 표시
const showSidebar = computed(() => {
  const path = route.path
  const isExcluded = sidebarExcludedPaths.includes(path)
  const isNoticePage = path.startsWith('/notice')
  const isLoggedIn = userStore.isLoggedIn

  if (isExcluded) return false
  if (isNoticePage) return isLoggedIn
  return true
})

// 🔹 인트로 이미지 조건부 표시
const showIntroImages = computed(() => {
  const path = route.path
  return !userStore.isLoggedIn && introImagePaths.includes(path)
})

// 🔹 인트로 이미지 배열
const introImages = [introImage1, introImage2, introImage3, introImage4, introImage5]

// 🔹 테마 설정
onBeforeMount(() => {
  const savedTheme = localStorage.getItem('theme') || 'system'
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  const resolvedTheme = savedTheme === 'system' ? (prefersDark ? 'dark' : 'light') : savedTheme
  document.documentElement.setAttribute('data-theme', resolvedTheme)
})
</script>

<style>
html,
body,
#app {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}

*,
*::before,
*::after {
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
  --sidebar-bg-color: #f8f8f8;
  --sidebar-text-color: #222;
  --logout-button-bg: #f44336;
  --logout-button-hover: #d32f2f;
  --logout-button-text: #fff;
}

html[data-theme='dark'] {
  --bg-color: #3f3f3f;
  --text-color: #f0f0f0;
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
  overflow: hidden;
}

.content-view {
  flex: 1;
  /* padding: 20px; */
  overflow-y: auto;
  height: calc(100vh - 64px);
  /* TopHeader 높이 고려 */
  transition: margin-left 0.2s ease;
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
