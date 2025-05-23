<!-- ModalForm.vue -->
<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-container">
      <!-- ✅ 좌측: 오늘의 기록 리스트 -->
      <div class="modal-left">
    <h3>{{ date }}의 내역</h3>
    <div
      v-for="item in todayList"
      :key="item._index"
      class="record-item"
    >
      <span :class="item.amount > 0 ? 'income' : 'expense'">
        {{ item.amount.toLocaleString() }}원
      </span>
      <span>{{ item.category || item.source }}</span>
      <span>{{ emojiMap[item.emotion] }}</span>

      <!-- 수정/삭제 버튼 -->
      <button @click="editItem(item)">✏️</button>
      <button @click="deleteItem(item._index)">🗑️</button>
    </div>
  </div>
      <!-- ✅ 우측: 탭 + 폼 입력 -->
      <div class="modal-right">
        <div class="tabs">
          <span :class="{ active: tab === 'expense' }" @click="tab = 'expense'">지출</span>
          <span :class="{ active: tab === 'income' }" @click="tab = 'income'">수입</span>
        </div>

        <component
          :is="tabMap[tab]"
          :date="date"
          :editing="editingItem"
          @save="handleSave"
          @close="$emit('close')"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useTransactionStore } from '@/stores/transactions'
import ExpenseForm from './ExpenseForm.vue'
import IncomeForm from './IncomeForm.vue'

const props = defineProps({ date: String })
const tab = ref('expense')
const tabMap = { expense: ExpenseForm, income: IncomeForm }

const store = useTransactionStore()

const todayList = computed(() => store.getByDate(props.date))

const emojiMap = {
  happy: '😀',
  neutral: '😐',
  sad: '😟'
}
const editingItem = ref(null)

function handleEdit(item) {
  editingItem.value = item
}
const emit = defineEmits(['edit'])

function editItem(item) {
  editingItem.value = { ...item }
  tab.value = item.amount > 0 ? 'income' : 'expense'
  // emit('edit', item)  // 폼에 데이터 전달
}

function deleteItem(index) {
  if (confirm('정말 삭제하시겠습니까?')) {
    store.deleteTransaction(index)
  }
}

// function handleSave(data) {
//   if (data._index !== undefined) {
//     store.updateTransaction(data._index, data)
//   } else {
//     store.addTransaction(data)
//   }
//   editingItem.value = null
// }

function handleSave(data) {
  if (data._index !== undefined && data._index !== null) {
    store.updateTransaction(data._index, data)
  } else {
    store.addTransaction(data)
  }
  editingItem.value = null
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
  background: #f0f0f0;
  padding: 1rem;
  overflow-y: auto;
}
.record-item {
  display: flex;
  justify-content: space-between;
  padding: 0.4rem;
  border-bottom: 1px solid #ccc;
  font-size: 14px;
}
.record-item .income {
  color: blue;
}
.record-item .expense {
  color: red;
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
.tabs span {
  cursor: pointer;
  padding-bottom: 4px;
  border-bottom: 2px solid transparent;
}
.tabs .active {
  font-weight: bold;
  border-color: #007bff;
}
</style>
