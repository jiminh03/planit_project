<template>
  <div class="home-container">
    <SidebarMenu />
    <div class="main-content">
      <TopHeader />
      <div class="content-body">
        <CalendarSection @open-modal="openModal" />
        <CardWidgets />
      </div>
        <ModalForm
          v-if="isModalOpen"
          :date="selectedDate"
          @close="closeModal"
          @save="handleSave"
        />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import SidebarMenu from '../components/SidebarMenu.vue'
import TopHeader from '../components/TopHeader.vue'
import CalendarSection from '../components/CalendarSection.vue'
import CardWidgets from '../components/CardWidgets.vue'
import ModalForm from '../components/ModalForm.vue'


const isModalOpen = ref(false)
const selectedDate = ref('')


function handleSave(payload) {
  console.log('저장된 데이터:', payload)
  // 저장 처리 로직 (예: 서버 전송, 상태 저장 등)
}

function openModal(date) {
  selectedDate.value = date
  isModalOpen.value = true
}

function closeModal() {
  isModalOpen.value = false
}
</script>

<style scoped>
.home-container {
  display: flex;
  height: 100vh;         /* ✅ 전체 화면 고정 */
  width: 100vw;
  overflow: hidden;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;          /* ✅ 자식이 height: 100%로 받을 수 있도록 */
  overflow: hidden;
}

.content-body {
  flex: 1;
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 100%; /* ✅ 유지 */
  padding: 2rem;
  gap: 2rem;

  /* 💥 변경 포인트 */
  overflow: hidden; /* ✅ 스크롤을 CardWidgets에서 처리하므로 이건 hidden 유지 */
  box-sizing: border-box;
}


</style>
