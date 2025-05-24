<template>
  <div class="content">
    <div class="settings-section">
      <h2>사용자 정보 설정</h2>
      <SettingsCard :items="['비밀번호 변경', '내 소비 데이터 다운로드', '계정 탈퇴', '감정/지출 기록 삭제']" @open-modal="handleOpenModal" />

      <h2>월 수입 설정</h2>
      <SettingsCard :items="['고정지출 항목 입력', '월 목표 지출액 설정', '지출 초과시 알림 여부 설정']" @open-modal="handleOpenModal" />

      <h2>목표 설정</h2>
      <SettingsCard :items="['소비 절감 목표 설정', '자동 추천 전략', '챌린지 확인 / 수정']" @open-modal="handleOpenModal" />
    </div>
  </div>
  <SettingsItemModal v-if="isModalOpen" :title="selectedItem" @close="closeModal" />
</template>

<script setup>
import { ref } from 'vue'
import SettingsCard from '@/components/SettingsCard.vue'
import SettingsItemModal from '@/components/SettingsItemModal.vue'

const isModalOpen = ref(false)
const selectedItem = ref('')

function handleOpenModal(item) {
  selectedItem.value = item
  isModalOpen.value = true
}

function closeModal() {
  isModalOpen.value = false
}
</script>

<style scoped >
.layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.content-body {
  flex: 1;
  padding: 2rem;
  box-sizing: border-box;
  overflow: auto;
}

.content {
  padding: 1rem;
  flex: 1;
}

.settings-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.settings-section h2 {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.settings-card {
  list-style: none;
  padding: 0;
  margin: 0;
  background: rgba(180, 180, 180, 0.2);
  backdrop-filter: blur(6px);
  border: 1px solid rgba(0, 0, 0, 0.05);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  color: var(--text-color);
}

.settings-card li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid var(--divider-color);
  font-size: 0.95rem;
}

.settings-card li:last-child {
  border-bottom: none;
}

.arrow {
  font-size: 1.2rem;
  color: var(--text-color);
}
</style>