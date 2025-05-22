<template>
  <div class="calendar-section">
    <div class="calendar-header">
      <h2>{{ year }}년 {{ month }}월 ▼</h2>
    </div>
    <div class="calendar-grid">
      <div class="day-header" v-for="day in days" :key="day">{{ day }}</div>

      <div
        v-for="(cell, index) in calendarCells"
        :key="index"
        class="calendar-cell"
        :class="{ selected: cell.date === selectedDate }"
        @click="selectDate(cell.date)"
      >
        <div class="date-label">{{ cell.date?.split('-')[2] || '' }}</div>
        <div v-if="cell.emotion" class="emoji">{{ cell.emotion }}</div>
        <div v-if="cell.amount" :class="cell.amount > 0 ? 'plus' : 'minus'">
          {{ formatCurrency(cell.amount) }}

        </div>
      </div>
    </div>

    <div class="selected-info" v-if="selectedDate">
      <p><strong>선택 날짜:</strong> {{ selectedDate }}</p>
      <p>소비 금액: {{ formatCurrency(selectedCell?.amount) }}</p>
      <p>감정 상태: {{ selectedCell?.emotion || '없음' }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineEmits } from 'vue'

// 날짜 정보
const year = 2025
const month = 5
const days = ['일', '월', '화', '수', '목', '금', '토']

const emit = defineEmits(['open-modal'])

// 가상의 날짜별 데이터
const mockData = {
  '2025-05-01': { amount: -1200 },
  '2025-05-02': { amount: -20000, emotion: '😊' },
  '2025-05-03': { amount: -100000, emotion: '😊' },
  '2025-05-10': { amount: -17000 },
  '2025-05-17': { amount: 103507, count: 2 },
  '2025-05-19': { amount: 5400 },
  '2025-05-31': { amount: -35000, tag: '카드 결제일' },
}

// 날짜 선택
const selectedDate = ref('')
const selectedCell = computed(() => mockData[selectedDate.value] || null)

function selectDate(date) {
  selectedDate.value = date
  emit('open-modal', date)
}

// 1일이 무슨 요일인지 파악
function getStartDay(year, month) {
  return new Date(year, month - 1, 1).getDay()
}

// 해당 달의 총 날짜 수
function getEndDate(year, month) {
  return new Date(year, month, 0).getDate()
}

// 전체 셀 구성
const calendarCells = computed(() => {
  const cells = []
  const startDay = getStartDay(year, month)
  const endDate = getEndDate(year, month)

  // 앞의 공백 셀
  for (let i = 0; i < startDay; i++) {
    cells.push({})
  }

  // 날짜 셀
  for (let day = 1; day <= endDate; day++) {
    const dateStr = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`
    const data = mockData[dateStr]
    cells.push({ date: dateStr, ...data })
  }

  return cells
})

function formatCurrency(val) {
  if (typeof val !== 'number') return '-'
  return val.toLocaleString('ko-KR') + '원'
}
</script>

<style scoped>


/* 수정된 달력 스타일 */
.calendar-section {
  width: 50%;         /* ✅ 좌측 절반 */
  height: 100%;       /* ✅ 이게 핵심 */
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
}

.calendar-header {
  line-height: 1;
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 1rem;
}

.calendar-grid {
  display: grid;
  margin-top: 0;
  padding-top: 0;
  grid-template-columns: repeat(7, 1fr);
  /* ✅ 핵심 수정: 요일 헤더는 작게, 날짜 행들은 크게 */
  grid-template-rows: 30px repeat(6, 200px);
  gap: 4px;
}

.day-header {
  text-align: center;
  font-weight: bold;
  color: gray;
  font-size: 14px;
  /* ✅ 요일 헤더 수직 정렬 */
  display: flex;
  align-items: center;
  justify-content: center;
  height: 30px; /* 요일 헤더 높이 고정 */
}

.calendar-cell {
  height: 200px; /* 날짜 셀 높이 명시 */
  padding: 6px;
  background: #f4f4f4;
  border-radius: 6px;
  text-align: right;
  font-size: 11px;
  cursor: pointer;
  position: relative;
  box-sizing: border-box;
  /* ✅ 내용 배치 개선 */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.calendar-cell:hover {
  background-color: #eaeaea;
}

.calendar-cell.selected {
  border: 2px solid #007bff;
}

.date-label {
  font-weight: bold;
  font-size: 14px;
  align-self: flex-end; /* 오른쪽 정렬 */
}

.emoji {
  position: absolute;
  top: 4px;
  left: 6px;
  font-size: 16px;
}

/* ✅ 금액 표시 개선 */
.minus, .plus {
  font-size: 10px;
  margin-top: auto;
  text-align: right;
}

.minus {
  color: red;
}

.plus {
  color: blue;
}

.selected-info {
  margin-top: 1rem;
  font-size: 14px;
  background-color: #f9f9f9;
  padding: 1rem;
  border-radius: 8px;
}

/* ✅ 더 컴팩트한 버전 (선택사항)
.calendar-grid.compact {
  grid-template-rows: 25px repeat(6, 80px);
  gap: 2px;
}

.calendar-grid.compact .day-header {
  height: 25px;
  font-size: 12px;
}

.calendar-grid.compact .calendar-cell {
  height: 80px;
  padding: 4px;
} */
</style>
