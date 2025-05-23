<!-- App.vue -->
<template>
  <router-view />
</template>


<script setup>
import { onMounted } from 'vue'

const theme = 'light' // 또는 localStorage 등

onMounted(() => {
  document.body.className = theme // body에 직접 적용
})
</script>

<style>
html, body, #app {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  /* overflow: hidden; */
  box-sizing: border-box;
}

*, *::before, *::after {
  box-sizing: inherit;
}
background-color: var(--bg-color);
color: var(--text-color);

body {
  font-family: sans-serif;
}

body.light {
  --bg-color: #fff;
  --text-color: #000;
}

body.dark {
  --bg-color: #1e1e1e;
  --text-color: #f0f0f0;
}
.sidebar {
  background-color: var(--bg-color);
  color: var(--text-color);
}

</style>
