<template>
  <div class="app-layout">
    <div v-if="!isAuthPage" class="main-layout">
      <div v-if="userStore.isLoggedIn">
        <SidebarMenu />
      </div>
      <div class="content-view">
        <router-view />
        <div>로그인 상태 (userStore): {{ userStore.isLoggedIn }}</div>
        <div>사이드바 존재 여부: {{ sidebarExists }}</div>
      </div>
    </div>
    <div v-else class="content-view">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import TopHeader from '@/components/TopHeader.vue'
import SidebarMenu from '@/components/SidebarMenu.vue'
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'

const route = useRoute()

const authPaths = ['/login', '/signup']

const isAuthPage = computed(() => authPaths.includes(route.path))

const userStore = useUserStore()
const sidebarExists = ref(false)

watch(
  () => userStore.isLoggedIn,
  (val) => {
    sidebarExists.value = val
  },
  { immediate: true }
)
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

.top-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  background-color: var(--sidebar-bg-color);
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
  padding: 20px;
  overflow-y: auto;
}
</style>