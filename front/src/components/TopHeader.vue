<template>
  <header class="top-header">
    <div class="title-area">
      <div class="menu-group" @click="goHome" style="cursor: pointer">
        <img src="@/assets/logo.png" alt="LOGO" class="icon" />
      </div>
    </div>

    <nav class="nav-tabs">
      <ul class="nav-list">
        <li
          v-if="!userStore.isLoggedIn"
          class="nav-item"
          :class="{ active: activeTab === 'features' }"
          @click="goToFeatures"
        >
          기능
        </li>
        <li
          v-if="!userStore.isLoggedIn"
          class="nav-item"
          :class="{ active: activeTab === 'signup' }"
          @click="goToSignup"
        >
          회원가입
        </li>
        <li
          v-if="!userStore.isLoggedIn"
          class="nav-item"
          :class="{ active: activeTab === 'login' }"
          @click="goToLogin"
        >
          로그인
        </li>
      </ul>
    </nav>

    <div class="right-buttons" v-if="userStore.isLoggedIn">
      <button
        class="logout-button"
        @click="goToNotice"
      >
        공지사항
      </button>
      <button
        class="logout-button logout"
        @click="handleLogout"
      >
        로그아웃
      </button>
    </div>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ref } from 'vue'

const router = useRouter()
const userStore = useUserStore()
userStore.restore()

const activeTab = ref('features')

function setActiveTab(tab) {
  activeTab.value = tab
}

function goToFeatures() {
  setActiveTab('features')
  router.push('/features')
}

function goToNotice() {
  setActiveTab('notice')
  router.push('/notice')
}

function goToSignup() {
  setActiveTab('signup')
  router.push('/signup')
}

function goToLogin() {
  setActiveTab('login')
  router.push('/login')
}

async function handleLogout() {
  try {
    await userStore.logout()
    alert('로그아웃 되었습니다.')
    router.push('/login')
  } catch (error) {
    console.error('로그아웃 실패', error)
    alert('로그아웃에 실패했습니다.')
  }
}

function goHome() {
  if (userStore.isLoggedIn) {
    router.push('/home')
  } else {
    router.push('/main')
  }
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
  position: sticky;
  top: 0;
  width: 100%;
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
  width: 150px;
  height: 60px;
}

.gray-button {
  background-color: #cccccc;
  border: none;
  padding: 8px 16px;
  font-weight: bold;
  cursor: pointer;
  border-radius: 6px;
  margin-right: 20px;
}

.nav-tabs {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-list {
  display: flex;
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  margin-left: 20px;
  font-weight: bold;
  cursor: pointer;
  color: var(--sidebar-text-color);
}

.nav-item.active {
  color: blue;
  border-bottom: 2px solid blue;
}
.logout-button {
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
  background-color: var(--logout-button-bg);
  color: var(--logout-button-text);
}
.logout-button.logout:hover {
  background-color: var(--logout-button-hover);
}

</style>

