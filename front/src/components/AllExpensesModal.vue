<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-container">
      <h2>이번 달 전체 지출 내역</h2>
      <ul>
        <li v-for="item in currentMonthExpenses" :key="item._index">
          <template v-if="editingItem && editingItem._index === item._index">
            <input v-model="editingItem.date" type="date" />
            <input v-model="editingItem.category" type="text" />
            <input v-model.number="editingItem.amount" type="number" />
            <button @click="saveEdit">저장</button>
            <button @click="cancelEdit">취소</button>
          </template>
          <template v-else>
            {{ item.date }} - {{ item.category }} - {{ item.amount }}원
            <button @click="startEdit(item)">수정</button>
            <button @click="deleteItem(item._index)">삭제</button>
          </template>
        </li>
      </ul>
      <button @click="$emit('close')">닫기</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTransactionStore } from '@/stores/transactions'

const store = useTransactionStore()
const editingItem = ref(null)

// 오늘 날짜 기준 월 필터
const today = new Date()
const year = today.getFullYear()
const month = String(today.getMonth() + 1).padStart(2, '0')
const prefix = `${year}-${month}`

onMounted(() => {
  console.log('[DEBUG] 전체 거래내역:', store.transactions)
})

const currentMonthExpenses = computed(() => {
  return store.transactions
    .map((t, i) => ({ ...t, _index: i })) // index 추가
    .filter(tx => tx.date.startsWith(prefix))
})

function startEdit(item) {
  editingItem.value = { ...item }
}
function cancelEdit() {
  editingItem.value = null
}
function saveEdit() {
  store.updateTransaction(editingItem.value._index, { ...editingItem.value })
  editingItem.value = null
}
function deleteItem(index) {
  store.deleteTransaction(index)
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}
.modal-container {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  width: 50%;
  max-height: 80%;
  overflow-y: auto;
}
</style>