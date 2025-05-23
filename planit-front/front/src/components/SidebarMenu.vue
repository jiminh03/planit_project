<!-- SidebarMenu.vue -->
<template>
  <div class="sidebar">
    <nav class="menu">
      <router-link to="/" class="menu-item" exact-active-class="active">🏠 홈 화면</router-link>

      <div class="menu-section">내 소비 분석</div>
      <router-link to="/analysis/summary" class="menu-item">한 줄 분석</router-link>
      <router-link to="/analysis/pattern" class="menu-item">소비 패턴 분석</router-link>
      <router-link to="/analysis/date" class="menu-item">날짜별 소비 패턴</router-link>
      <router-link to="/analysis/emotion" class="menu-item">감정-소비 관계</router-link>
      <router-link to="/analysis/category" class="menu-item">카테고리별 분석</router-link>
      <router-link to="/analysis/type" class="menu-item">소비 성향 진단</router-link>
      <router-link to="/analysis/feedback" class="menu-item">개인 맞춤형 피드백</router-link>

      <div class="menu-section">💡 지출 도우미</div>
      <router-link to="/guide/message" class="menu-item">개선이 필요한 메시지</router-link>
      <router-link to="/guide/strategy" class="menu-item">대체 소비 전략</router-link>
      <router-link to="/guide/simulation" class="menu-item">절약 시뮬레이션</router-link>
      <router-link to="/guide/fixed" class="menu-item">고정/정기지출 정리 제안</router-link>
      <router-link to="/guide/combo" class="menu-item">전략 조합 시뮬 결과</router-link>

      <div class="menu-section">⚙️ 설정</div>
      <router-link to="/settings" class="menu-item">설정</router-link>
    </nav>
  </div>
</template>

<style scoped>
.sidebar {
  width: 220px;
  min-width: 220px;
  height: 100vh;
  background-color: #f8f8f8;
  padding: 1rem;
  box-sizing: border-box;
  border-right: 1px solid #ddd;
  overflow: auto;
}

.menu {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.menu-section {
  margin-top: 1rem;
  font-weight: bold;
  color: #666;
}

.menu-item {
  text-decoration: none;
  color: #333;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background 0.2s;
}

.menu-item:hover {
  background-color: #eee;
}

.active {
  background-color: #e0e0e0;
  font-weight: bold;
}
</style>
