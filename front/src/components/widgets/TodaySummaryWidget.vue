<script setup>
import { computed } from 'vue'
import { useTransactionStore } from '@/stores/transactions'
import { forceUpdate } from '@/stores/summaryTrigger'

const props = defineProps({
  date: String
})

const store = useTransactionStore()

const today = computed(() => props.date || new Date().toISOString().split('T')[0])


const todayList = computed(() => {
  forceUpdate.value // trigger reactivity
  return store.transactions
    .map((t, i) => ({ ...t, _index: i }))
    .filter(t => {
      const txDate = new Date(t.date).toISOString().split('T')[0]
      const targetDate = new Date(today.value).toISOString().split('T')[0]
      return txDate === targetDate
    })
})

const todaySpending = computed(() => {
  const value = todayList.value
    .reduce((acc, cur) => acc + Math.abs(parseInt(cur.amount)), 0)
  return value
})

const recommendedSpending = 30000 // 임시값, 추후 백엔드 연동 가능
const statusMessage = computed(() => {
  const rate = todaySpending.value / recommendedSpending
  if (rate <= 0.5) return '아주 훌륭해요! 😊'
  else if (rate <= 1.0) return '잘 소비하고 있어요! 🙂'
  else return '예산 초과 주의! ⚠️'
})
</script>

<template>
  <div class="today-summary-widget">
    <h3>📅 오늘 요약</h3>
    <p>총 지출: ₩{{ Number(todaySpending).toLocaleString() }}</p>
    <p>권장 지출: ₩{{ recommendedSpending.toLocaleString() }}</p>
    <p>📌 {{ statusMessage }}</p>
  </div>
</template>

<style scoped>
.today-summary-widget {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 2rem;
  border-radius: 1.25rem;
  background-color: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  font-family: 'Noto Sans KR', sans-serif;
  font-size: 1rem;
  color: #222;
  max-width: 100%;
}

.today-summary-widget h3 {
  font-size: 1.4rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: bold;
}

.today-summary-widget p {
  margin: 0;
  line-height: 1.6;
  font-size: 1.05rem;
}
</style>