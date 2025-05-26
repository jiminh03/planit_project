<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-container">
      <h2>이번 달 거래 내역</h2>

      <div class="date-group" v-for="(items, date) in groupedByDate" :key="date">
        <h4 class="date-title">{{ date }}</h4>
        <div class="records-wrapper">
          <div v-for="item in items" :key="item._index" class="record-item">
            <template v-if="editingItem && editingItem._index === item._index">
              <input v-model="editingItem.date" type="date" />
              <input v-model="editingItem.category" type="text" />
              <input v-model.number="editingItem.amount" type="number" />
              <button @click="saveEdit">저장</button>
              <button @click="cancelEdit">취소</button>
            </template>
            <template v-else>
              <div class="record-main">
                <div :class="['amount', item.amount > 0 ? 'income' : 'expense']">
                  {{ item.amount > 0 ? '+' : '-' }}{{ Math.abs(item.amount).toLocaleString() }}원
                </div>
                <div class="meta">
                  <span v-if="item.amount < 0">🧾 {{ item.category }}</span>
                  <span v-else>💰 {{ item.source }}</span>
                  <span class="emoji">{{ emojiMap[item.emotion] || '😐' }}</span>
                </div>
              </div>
              <div class="record-buttons">
                <button @click="startEdit(item)">✏️</button>
                <button @click="deleteItem(item._index)">❌</button>
              </div>
            </template>
          </div>
        </div>
      </div>

      <button @click="$emit('close')" class="close-button">닫기</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useTransactionStore } from '@/stores/transactions'

const store = useTransactionStore()
const editingItem = ref(null)

const today = new Date()
const year = today.getFullYear()
const month = String(today.getMonth() + 1).padStart(2, '0')
const prefix = `${year}-${month}`

const currentMonthExpenses = computed(() => {
  return store.transactions
    .map((t, i) => ({ ...t, _index: i }))
    .filter(tx => tx.date.startsWith(prefix))
    .sort((a, b) => new Date(b.date) - new Date(a.date))
})

const groupedByDate = computed(() => {
  const result = {}
  currentMonthExpenses.value.forEach(item => {
    if (!result[item.date]) result[item.date] = []
    result[item.date].push(item)
  })
  return result
})

const emojiMap = {
  happy: '😀',
  neutral: '😐',
  sad: '😟',
}

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
  top: 0; left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex; justify-content: center; align-items: center;
  z-index: 999;
}
.modal-container {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  width: 60%;
  max-height: 80%;
  overflow-y: auto;
}
.date-title {
  margin-top: 1.5rem;
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
  border-bottom: 1px solid #ccc;
  padding-bottom: 0.3rem;
}
.records-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.record-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f7f7f7;
  padding: 0.8rem 1rem;
  border-radius: 8px;
  border: 1px solid #ddd;
}
.record-main {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}
.amount {
  font-weight: bold;
  font-size: 1rem;
}
.income {
  color: #007bff;
}
.expense {
  color: #dc3545;
}
.meta {
  font-size: 0.9rem;
  color: #555;
}
.emoji {
  margin-left: 0.5rem;
}
.record-buttons {
  display: flex;
  gap: 0.5rem;
}
.record-buttons button {
  padding: 0.4rem 0.7rem;
  border: none;
  border-radius: 5px;
  background: #eee;
  cursor: pointer;
}
.close-button {
  margin-top: 1rem;
  padding: 0.6rem 1.2rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
</style>
