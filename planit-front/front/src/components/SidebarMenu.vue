<template>
  <div class="sidebar">
    <nav class="menu">
      <!-- 홈 화면 -->
      <div class="menu-group-wrapper">
        <router-link to="/" class="menu-group" exact-active-class="active">
          <img src="@/assets/home_icon.png" alt="홈 화면" class="icon" />
          <span class="menu-group-title">홈 화면</span>
        </router-link>
      </div>

      <!-- 내 소비 분석 -->
      <div class="menu-group-wrapper">
        <router-link to="/analysis" class="menu-group">
          <span class="menu-group-title">내 소비 분석</span>
        </router-link>
        <div class="submenu">
          <router-link to="/analysis/summary" class="menu-subitem">한 줄 분석</router-link>
          <router-link to="/analysis/pattern" class="menu-subitem">소비 패턴 분석</router-link>
          <router-link to="/analysis/date" class="menu-subitem">날짜별 소비 패턴</router-link>
          <router-link to="/analysis/emotion" class="menu-subitem">감정-소비 관계</router-link>
          <router-link to="/analysis/category" class="menu-subitem">카테고리별 분석</router-link>
          <router-link to="/analysis/type" class="menu-subitem">소비 성향 진단</router-link>
          <router-link to="/analysis/feedback" class="menu-subitem">개인 맞춤형 피드백</router-link>
        </div>
      </div>

      <!-- 지출 도우미 -->
      <div class="menu-group-wrapper">
        <router-link to="/guide" class="menu-group">
          <img src="@/assets/lightbulb_icon.png" alt="지출 도우미" class="icon" />
          <span class="menu-group-title">지출 도우미</span>
        </router-link>
        <div class="submenu">
          <router-link to="/guide/message" class="menu-subitem">개선이 필요한 메시지</router-link>
          <router-link to="/guide/strategy" class="menu-subitem">대체 소비 전략</router-link>
          <router-link to="/guide/simulation" class="menu-subitem">절약 시뮬레이션</router-link>
          <router-link to="/guide/fixed" class="menu-subitem">고정/정기지출 정리 제안</router-link>
          <router-link to="/guide/combo" class="menu-subitem">전략 조합 시뮬 결과</router-link>
        </div>
      </div>

      <!-- 설정 -->
      <div class="menu-group-wrapper">
        <router-link to="/settings" class="menu-group">
          <img src="@/assets/settings_icon.png" alt="설정" class="icon" />
          <span class="menu-group-title">설정</span>
        </router-link>
        <div class="submenu">
          <router-link to="/settings" class="menu-subitem">설정</router-link>
        </div>
      </div>
    </nav>
  </div>
</template>

<script setup>
// no logic needed
</script>

<style scoped>
.sidebar {
  width: 220px;
  min-width: 220px;
  background-color: #f8f8f8;
  padding: 1rem;
  box-sizing: border-box;
  border-right: 1px solid #ddd;
  height: 100%;
  overflow: auto;
}

.menu-group-wrapper {
  position: relative;
}

.menu-group-wrapper:hover .submenu {
  display: block;
}

.menu {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  align-items: center;
  height: 100%;
}

.menu-group {
  display: flex;
  align-items: center;
  margin-top: 1.5rem;
  text-decoration: none;
}

.menu-group-title {
  margin-left: 6px;
  font-weight: bold;
  font-size: 15px;
  color: #222;
}

.submenu {
  display: none;
  flex-direction: column;
}

.menu-subitem {
  padding-left: 32px;
  font-size: 14px;
  color: #333;
  text-decoration: none;
  display: block;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background 0.2s;
}

.menu-subitem:hover {
  background-color: #eee;
}

.active {
  background-color: #e0e0e0;
  font-weight: bold;
}

.icon {
  width: 24px;
  height: 24px;
  margin-right: 4px;
}
</style>