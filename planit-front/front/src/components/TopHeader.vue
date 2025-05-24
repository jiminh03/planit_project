<template>
  <header class="top-header">
    <div class="title-area">
      <router-link to="/" class="menu-group" exact-active-class="active">
        <img src="@/assets/logo.png" alt="LOGO" class="icon" />
      </router-link>
    </div>
    <button class="logout-button" @click="handleLogout">로그아웃</button>
  </header>
</template>


<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function handleLogout() {
  alert('로그아웃 되었습니다.')
  router.push('/login')
}
</script>

<style scoped>
.top-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 2rem 0.1rem 2rem;
  border-bottom: 1px solid #ddd;
  background-color: var(--sidebar-bg-color);
  color: var(--sidebar-text-color);
  flex-shrink: 0;
  z-index: 1000;
  position: relative;
}

.title-area {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.title-area h1 {
  font-size: 20px;
  font-weight: bold;
  margin: 0;
}

.icon {
  width: 150x;
  height: 60px;
}

.logout-button {
  background-color: var(--logout-button-bg);
  color: var(--logout-button-text);
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}

.logout-button:hover {
  background-color: var(--logout-button-hover);
}
</style>
