<!-- TopHeader.vue -->
<template>
  <header class="top-header">
    <div class="title-area">
      <span class="icon">🏠</span>
      <h1>홈 화면</h1>
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
  padding: 1.25rem 2rem;
  border-bottom: 1px solid #ddd;
  background-color: white;
  flex-shrink: 0;
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

.logout-button {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}

.logout-button:hover {
  background-color: #d32f2f;
}
</style>
