<template>
  <div class="calendar-section">
    <div class="calendar-header">
      <div class="calendar-title-area" style="display: flex; align-items: center; justify-content: center; position: relative;">
        <h2 style="display: flex; align-items: center;">
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
      <div style="margin-top: 0rem; text-align: right;">
        <button @click="viewAllExpenses">이번 달 지출내역 확인</button>
      </div>
    </div>

    <div class="calendar-grid">
      <div class="day-header" v-for="day in days" :key="day">{{ day }}</div>
      <div
        v-for="(cell, index) in calendarCells"
        :key="index"
        class="calendar-cell"
        @click="selectDate(cell.date)"
      >
        <div class="date-label">{{ cell.date?.split('-')[2] || '' }}</div>
        <!-- <div v-if="cell.amount" :class="cell.amount > 0 ? 'plus' : 'minus'">
          {{ formatCurrency(cell.amount) }} -->

        <!-- 수입 표시 -->
        <div v-if="cell.incomeTotal" class="plus">
          {{ formatCurrency(cell.incomeTotal) }}
        </div>
        <!-- 지출 표시 -->
        <div v-if="cell.expenseTotal" class="minus">
          {{ formatCurrency(cell.expenseTotal) }}
        </div>
      </div>
    </div>

    <!-- ✅ 모달 렌더링 -->
    <ModalForm
      v-if="isModalOpen"
      :date="selectedDate"
      @close="isModalOpen = false"
    />
    <AllExpensesModal
      v-if="isAllModalOpen"
      :expenses="store.transactions"
      @close="isAllModalOpen = false"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useTransactionStore } from '@/stores/transactions'
import ModalForm from '@/components/ModalForm.vue'
import AllExpensesModal from './AllExpensesModal.vue'

const store = useTransactionStore()
const days = ['일', '월', '화', '수', '목', '금', '토']
const currentDate = ref(new Date())
const selectedMonth = ref(currentDate.value.getMonth() + 1)
const selectedYear = ref(currentDate.value.getFullYear())
const selectedDate = ref('')
const isModalOpen = ref(false)

function selectDate(date) {
  if (typeof date === 'object') {
    selectedDate.value = date.toISOString().slice(0, 10)
  } else {
    selectedDate.value = date
  }
  isModalOpen.value = true
}

const isAllModalOpen = ref(false)


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

  for (let i = 0; i < startDay; i++) cells.push({})

  for (let day = 1; day <= endDate; day++) {
    const dateStr = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`
    const txs = store.getByDate(dateStr)
    const expenseTotal = txs
      .filter(t => t.amount < 0)
      .reduce((sum, t) => sum + t.amount, 0)

    const incomeTotal = txs
      .filter(t => t.amount > 0)
      .reduce((sum, t) => sum + t.amount, 0)

    cells.push({
      date: dateStr,
      expenseTotal,
      incomeTotal
    })
    // const totalAmount = txs.reduce((sum, t) => sum + t.amount, 0)
    // cells.push({ date: dateStr, amount: totalAmount })
  }



  return cells
})

function formatCurrency(val) {
  if (typeof val !== 'number') return '-'
  return val.toLocaleString('ko-KR') + '원'
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
}

.calendar-header {
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 1rem;
}

.calendar-header h2 {
  color: var(--text-color);
}


select,
button {
  background-color: var(--card-bg-color);
  color: var(--text-color);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 16px;
  transition: background-color 0.3s ease;
  margin: 0 8px;
}

select:focus,
button:focus {
  outline: none;
  border: 1px solid #7c3aed;
}

button:hover {
  background-color: rgba(255, 255, 255, 0.12);
  cursor: pointer;
}

.calendar-grid {
  display: grid;
  margin-top: 0;
  padding-top: 0;
  grid-template-columns: repeat(7, 1fr);
  grid-template-rows: 30px repeat(6, 200px);
  gap: 4px;
}

.day-header {
  text-align: center;
  font-weight: bold;
  color: gray;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 30px;
}

.calendar-cell {
  height: 200px;
  padding: 6px;
  background-color: rgba(180, 180, 180, 0.2); /* 연한 회색 느낌의 반투명 */
  backdrop-filter: blur(6px);
  border: 1px solid rgba(0, 0, 0, 0.05);
  border-radius: 6px;
  text-align: right;
  font-size: 11px;
  cursor: pointer;
  position: relative;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.calendar-cell:hover {
  background-color: var(--card-glass-hover);
}

.calendar-cell.selected {
  border: 2px solid #007bff;
}

.date-label {
  font-weight: bold;
  font-size: 14px;
  align-self: flex-end;
}

.emoji {
  position: absolute;
  top: 4px;
  left: 6px;
  font-size: 16px;
}

.minus, .plus {
  font-size: 10px;
  text-align: right;
}

.minus {
  color: red;
  order: 1; /* 지출은 아래쪽에 위치 */
}

.plus {
  color: blue;
  order: 0; /* 수입은 위쪽에 위치 */
}

.selected-info {
  margin-top: 1rem;
  font-size: 14px;
  background-color: var(--card-bg-color);
  padding: 1rem;
  border-radius: 8px;
}
</style>
