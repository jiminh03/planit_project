<template>
  <div class="theme-selector">
    <label><input type="radio" value="light" v-model="themeStore.theme" @change="themeStore.applyTheme" /> 라이트 모드</label>
    <hr class="settings-divider" />
    <label><input type="radio" value="dark" v-model="themeStore.theme" @change="themeStore.applyTheme" /> 다크 모드</label>
    <hr class="settings-divider" />
    <label><input type="radio" value="system" v-model="themeStore.theme" @change="themeStore.applyTheme" /> 시스템 설정 따르기</label>
  </div>
</template>

<script setup>
import { useThemeStore } from '@/stores/useThemeStore'
const themeStore = useThemeStore()
</script>

<style scoped >
.theme-selector {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px;
  color: var(--text-color);
}

label {
  font-weight: 500;
}

.settings-divider {
  margin: 0;
  border: none;
  border-bottom: 1px solid var(--divider-color, #e2e0e0);
}
</style>