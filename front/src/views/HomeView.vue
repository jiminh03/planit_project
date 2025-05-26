<template>
  <div class="content-body">
    <CalendarSection @open-modal="openModal" />
    <CardWidgets :date="selectedDate" />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import CalendarSection from '../components/CalendarSection.vue'
import CardWidgets from '../components/CardWidgets.vue'
import { useTransactionStore } from '@/stores/transactions'
import { useUserStore } from '@/stores/user'

const isModalOpen = ref(false)
const selectedDate = ref(new Date().toISOString().slice(0, 10))

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
  selectedDate.value = new Date().toISOString().slice(0, 10)
}

const transactionStore = useTransactionStore()
const userStore = useUserStore()

const now = new Date()
const year = ref(now.getFullYear())
const month = ref(now.getMonth() + 1)

onMounted(async () => {
  if (userStore.isLoggedIn) {
    await transactionStore.fetchAllTransactions()
  } else {
    console.warn('❌ HomeView.vue에서 잘못된 fetchAllTransactions 호출 차단:', {
      isLoggedIn: userStore.isLoggedIn
    })
  }
})

watch(
  () => userStore.isLoggedIn,
  async (isLoggedIn) => {
    if (isLoggedIn) {
      await transactionStore.fetchAllTransactions()
    }
  }
)
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
  flex-wrap: nowrap;           /* ✅ 줄바꿈 금지 */
  width: 100%;
  height: 100%;
  padding: 2rem;
  gap: 2rem;
  overflow-x: auto;            /* ✅ 수평 스크롤 허용 */
  box-sizing: border-box;
}


</style>
