<template>
  <div class="calendar-section">
    <div class="calendar-header">
      <div class="calendar-title-area">
        <h2>
          <button @click="goToPrevMonth">&lt;</button>
          <select v-model="selectedYear" @change="onYearOrMonthChange">
            <option v-for="y in [2024, 2025, 2026]" :key="y" :value="y">{{ y }}년</option>
          </select>
          <select v-model="selectedMonth" @change="onYearOrMonthChange">
            <option v-for="m in 12" :key="m" :value="m">{{ m }}월</option>
          </select>
          <button @click="goToNextMonth">&gt;</button>
        </h2>
      </div>
      <div class="expense-check-button">
        <button @click="viewAllExpenses">이번 달 지출내역 확인</button>
      </div>
    </div>

    <div class="calendar-grid">
      <div class="day-header" v-for="day in days" :key="day">{{ day }}</div>
      <div v-for="(cell, index) in calendarCells" :key="index" class="calendar-cell" @click="selectDate(cell.date)">
        <div class="date-label">{{ cell.date?.split('-')[2] || '' }}</div>
        <div class="entry-group">
          <div v-if="cell.incomeTotal" class="entry income">+{{ formatCurrency(cell.incomeTotal) }}</div>
          <div v-if="cell.expenseTotal" class="entry expense">-{{ formatCurrency(cell.expenseTotal) }}</div>
        </div>
      </div>
    </div>

    <ModalForm v-if="isModalOpen" :date="selectedDate" @close="handleModalClose" @update="handleModalUpdate" />
    <AllExpensesModal v-if="isAllModalOpen" :expenses="store.transactions" @close="isAllModalOpen = false" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useTransactionStore } from '@/stores/transactions'
import { forceUpdate } from '@/stores/summaryTrigger'
import ModalForm from '@/components/ModalForm.vue'
import AllExpensesModal from './AllExpensesModal.vue'

const store = useTransactionStore()

const days = ['일', '월', '화', '수', '목', '금', '토']
const currentDate = ref(new Date())
const selectedMonth = ref(currentDate.value.getMonth() + 1)
const selectedYear = ref(currentDate.value.getFullYear())
const selectedDate = ref('')
const isModalOpen = ref(false)
const isAllModalOpen = ref(false)

defineEmits(['close'])

function selectDate(date) {
  selectedDate.value = date
  isModalOpen.value = true
}

function viewAllExpenses() {
  isAllModalOpen.value = true
}

function onYearOrMonthChange() {
  currentDate.value = new Date(selectedYear.value, selectedMonth.value - 1)
}

function goToPrevMonth() {
  const prev = new Date(currentDate.value)
  prev.setMonth(prev.getMonth() - 1)
  currentDate.value = prev
  selectedYear.value = prev.getFullYear()
  selectedMonth.value = prev.getMonth() + 1
}

function goToNextMonth() {
  const next = new Date(currentDate.value)
  next.setMonth(next.getMonth() + 1)
  currentDate.value = next
  selectedYear.value = next.getFullYear()
  selectedMonth.value = next.getMonth() + 1
}

function getStartDay(year, month) {
  return new Date(year, month - 1, 1).getDay()
}

function getEndDate(year, month) {
  return new Date(year, month, 0).getDate()
}

const calendarCells = computed(() => {
  const cells = []
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth() + 1
  const startDay = getStartDay(year, month)
  const endDate = getEndDate(year, month)

  for (let i = 0; i < startDay; i++) {
    cells.push({})
  }

  for (let day = 1; day <= endDate; day++) {
    const dateStr = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`
    const txs = store.getByDate(dateStr)
    const incomeTotal = txs.filter(t => t.amount > 0).reduce((sum, t) => sum + t.amount, 0)
    const expenseTotal = txs.filter(t => t.amount < 0).reduce((sum, t) => sum + t.amount, 0)

    cells.push({
      date: dateStr,
      incomeTotal,
      expenseTotal,
    })
  }

  return cells
})

function formatCurrency(val) {
  if (typeof val !== 'number') return '-'
  return Math.abs(val).toLocaleString('ko-KR') + '원'
}

function handleModalClose() {
  isModalOpen.value = false
  store.fetchTransactions(selectedYear.value, selectedMonth.value)
  forceUpdate.value++
}

function handleModalUpdate() {
  store.fetchTransactions(selectedYear.value, selectedMonth.value)
  forceUpdate.value++
}
</script>


<style scoped>
.calendar-section {
  width: 50%;
  height: 100%;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  min-width: 720px;
  font-family: 'Segoe UI', sans-serif;
}

.calendar-header {
  text-align: center;
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 2rem;
}

.calendar-title-area {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  font-size: 24px;
  gap: 12px;
}

.expense-check-button {
  text-align: right;
  padding: 0 1rem;
  margin-bottom: 1.2rem;
}

select,
button {
  background-color: var(--card-bg-color);
  color: var(--text-color);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  padding: 6px 14px;
  font-size: 18px;
  transition: background-color 0.3s ease;
}

.calendar-grid {
  display: grid;
  /* margin-top: 0;
  padding-top: 0; */
  grid-template-columns: repeat(7, 1fr);
  /* grid-template-rows: 50px repeat(6, 220px); */
  gap: 4px;
}

.day-header {
  text-align: center;
  font-weight: bold;
  color: #444;
  font-size: 20px;
  background-color: #fafafa;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;
}

.calendar-cell {
  aspect-ratio: 1 / 1;
  /* height: 220px; */
  height: auto;
  padding: 10px;
  background-color: #e9e9e9;
  border: 1px solid #ccc;
  /* border-radius: 10px; */
  font-size: 16px;
  cursor: pointer;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden;
  transition: transform 0.15s ease;
}

.calendar-cell:hover {
  background-color: #f0f0f0;
  transform: scale(1.02);
}

.date-label {
  font-weight: bold;
  font-size: 18px;
  color: #222;
  align-self: flex-start;
}

.entry-group {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 6px;
}

.entry {
  font-size: 16px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.income {
  color: #007bff;
  font-weight: 600;
}

.expense {
  color: #dc3545;
  font-weight: 600;
}
</style>
