<template>
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

body.light {
  --bg-color: #fff;
  --text-color: #000;
}

body.dark {
  --bg-color: #1e1e1e;
  --text-color: #f0f0f0;
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
