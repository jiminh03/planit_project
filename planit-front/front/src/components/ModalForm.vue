<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-container">
      <!-- 좌측: 지출 내역 로그 -->
      <div class="modal-left">
        <h3>오늘의 지출 내역</h3>
        <div
          class="expense-item"
          v-for="item in expenseList"
          :key="item.id"
        >
          <span>{{ item.amount }}</span>
          <span>{{ item.category }}</span>
          <span>{{ emojiMap[item.emotion] || '' }}</span>
          <span @click="editItem(item)" class="icon">✏️</span>
          <span @click="deleteItem(item.id)" class="icon">❌</span>
        </div>
      </div>

      <!-- 우측: 탭 + 입력 폼 -->
      <div class="modal-right">
        <div class="tabs">
          <span :class="['tab', activeTab === 'expense' ? 'active' : '']"
                @click="activeTab = 'expense'">지출</span>
          <span :class="['tab', activeTab === 'income' ? 'active' : '']"
                @click="activeTab = 'income'">수입</span>
        </div>

        <component
          :is="tabComponentMap[activeTab]"
          :date="date"
          :editing-item="editingItem"
          @save="handleSave"
          />
          <!-- @close="$emit('close')" -->
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ExpenseForm from './ExpenseForm.vue'
import IncomeForm from './IncomeForm.vue'


const emojiMap = {
  happy: '😀',
  neutral: '😐',
  sad: '😟'
}


const props = defineProps({
  date: {
    type: String,
    required: true,
  }
})

const activeTab = ref('expense')

// 좌측 리스트 상태
const expenseList = ref([])

// 수정 중인 항목
const editingItem = ref(null)

const tabComponentMap = {
  expense: ExpenseForm,
  income: IncomeForm,
}

// 저장 처리
function handleSave(data) {
  if (editingItem.value) {
    const idx = expenseList.value.findIndex(item => item.id === editingItem.value.id)
    if (idx !== -1) {
      expenseList.value[idx] = { ...editingItem.value, ...data }
    }
    editingItem.value = null
  } else {
    expenseList.value.push({ id: Date.now(), ...data })   // ✅ 새로 추가
  }
}


// 삭제 처리
function deleteItem(id) {
  expenseList.value = expenseList.value.filter(item => item.id !== id)
}

// 수정 진입
function editItem(item) {
  activeTab.value = 'expense'
  editingItem.value = { ...item }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-container {
  display: flex;
  background: white;
  width: 800px;
  height: 500px;
  border-radius: 16px;
  overflow: hidden;
}

.modal-left {
  width: 50%;
  background: #ddd;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.modal-right {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

.tabs {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 1rem;
}
.tab {
  font-size: 18px;
  font-weight: 500;
  cursor: pointer;
  padding-bottom: 4px;
  border-bottom: 2px solid transparent;
}
.tab.active {
  font-weight: bold;
  border-color: #333;
}

.expense-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f6f6f6;
  padding: 0.5rem;
  border-radius: 6px;
  font-size: 14px;
}
.icon {
  cursor: pointer;
}
</style>
