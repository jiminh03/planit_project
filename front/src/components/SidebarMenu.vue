<template>
  <div class="sidebar">
    <nav class="menu">
      <!-- 홈 화면 -->
      <div class="menu-group-wrapper">
        <router-link to="/home" class="menu-group" exact-active-class="active" @click="toggleSubmenu('home')">
          <img src="@/assets/home_icon.png" alt="홈 화면" class="icon" />
          <span class="menu-group-title">홈 화면</span>
        </router-link>
      </div>

      <!-- 내 소비 분석 -->
      <div class="menu-group-wrapper">
        <router-link to="/analysis" class="menu-group" @click="toggleSubmenu('analysis')">
          <span class="menu-group-title">내 소비 분석</span>
        </router-link>
        <transition name="submenu-transition">
          <div class="submenu" v-show="activeMenu === 'analysis'">
            <div class="menu-subitem">한 줄 분석</div>
            <div class="menu-subitem">소비 패턴 분석</div>
            <div class="menu-subitem">날짜별 소비 패턴</div>
            <div class="menu-subitem">감정-소비 관계</div>
            <div class="menu-subitem">카테고리별 분석</div>
            <div class="menu-subitem">소비 성향 진단</div>
            <div class="menu-subitem">개인 맞춤형 피드백</div>
          </div>
        </transition>
      </div>

      <!-- 지출 도우미 -->
      <div class="menu-group-wrapper">
        <router-link to="/guide" class="menu-group" @click="toggleSubmenu('guide')">
          <img src="@/assets/lightbulb_icon.png" alt="지출 도우미" class="icon" />
          <span class="menu-group-title">지출 도우미</span>
        </router-link>
        <transition name="submenu-transition">
          <div class="submenu" v-show="activeMenu === 'guide'">
            <div class="menu-subitem">개선이 필요한 메시지</div>
            <div class="menu-subitem">대체 소비 전략</div>
            <div class="menu-subitem">절약 시뮬레이션</div>
            <div class="menu-subitem">고정/정기지출 정리 제안</div>
            <div class="menu-subitem">전략 조합 시뮬 결과</div>
          </div>
        </transition>
      </div>

      <!-- 설정 -->
      <div class="menu-group-wrapper">
        <router-link to="/settings" class="menu-group" @click="toggleSubmenu('settings')">
          <img src="@/assets/settings_icon.png" alt="설정" class="icon" />
          <span class="menu-group-title">설정</span>
        </router-link>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const activeMenu = ref(null)

const toggleSubmenu = (menuName) => {
  activeMenu.value = activeMenu.value === menuName ? null : menuName
}
</script>

<style scoped>
.sidebar {
  width: 220px;
  min-width: 220px;
  background-color: var(--sidebar-bg-color);
  padding: 1rem;
  box-sizing: border-box;
  border-right: 1px solid #ddd;
  height: 100%;
  overflow: auto;
}

.menu-group-wrapper {
  position: relative;
}

.menu {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  align-items: stretch;
  height: 100%;
}

.menu-group,
.menu-subitem {
  all: unset;
  display: flex;
  align-items: center;
  width: 100%;
  color: var(--sidebar-text-color);
  text-decoration: none;
  cursor: pointer;
}

.menu-group {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 4px 8px;
  min-height: 36px;
  margin-top: 1.5rem;
}

.menu-group-title {
  margin-left: 6px;
  font-weight: bold;
  font-size: 15px;
  color: var(--sidebar-text-color) !important;
}

.submenu {
  display: flex;
  align-items: center;
  flex-direction: column;
}

.menu-subitem {
  font-size: 14px;
  border-radius: 6px;
  transition: background 0.2s;
  padding: 4px 8px;
  text-align: center;
  width: 100%;
  display: flex;
  justify-content: center;
}

.menu-subitem:hover {
  background-color: var(--sidebar-hover-bg-color);
}

.active {
  background-color: var(--sidebar-active-bg-color);
  font-weight: bold;
}

.icon {
  width: 24px;
  height: 24px;
  margin-right: 4px;
  transition: filter 0.2s ease;
}

/* 다크모드에서 아이콘 색상 변경 */
[data-theme="dark"] .icon {
  filter: invert(1) brightness(0.9);
}

/* 시스템 다크모드 지원 */
@media (prefers-color-scheme: dark) {
  [data-theme="system"] .icon {
    filter: invert(1) brightness(0.9);
  }
}

.icon-dark-mode {
  filter: invert(1);
  width: 24px;
  height: 24px;
  margin-right: 4px;
}

.submenu-transition-enter-active,
.submenu-transition-leave-active {
  transition: max-height 0.3s ease, opacity 1.5s ease;
  overflow: hidden;
}
.submenu-transition-enter-from,
.submenu-transition-leave-to {
  max-height: 0;
  opacity: 0;
}
.submenu-transition-enter-to,
.submenu-transition-leave-from {
  max-height: 500px;
  opacity: 1;
}
</style>