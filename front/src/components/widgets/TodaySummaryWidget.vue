<template>
  <div class="today-summary-widget">
    <h3>📅 {{ todayLabel }}</h3>
    <p>오늘 총 지출: ₩{{ displayTodaySpending }}</p>
    <p>이번달 총 지출: ₩{{ displayMonthlyTotal }}</p>
    <p>권장 지출: ₩{{ displayRecommendedSpending }}</p>
    <p>이번달 목표 예산: ₩{{ budget }}</p>
    <p><strong>오늘 지출률:</strong> {{ todaySpendingRate }}%</p>
    <div class="progress-bar">
      <div class="progress-fill" :style="{ width: todaySpendingRate + '%' }"></div>
    </div>

    <p><strong>이번달 지출률:</strong> {{ monthlySpendingRate }}%</p>
    <div class="progress-bar">
      <div class="progress-fill" :style="{ width: monthlySpendingRate + '%' }"></div>
    </div>

    <p><strong>이번달 경과율:</strong> {{ monthlyProgressRate }}%</p>
    <div class="progress-bar">
      <div class="progress-fill" :style="{ width: monthlyProgressRate + '%' }"></div>
    </div>
    <p>{{ hasEmotion ? '😊 감정 기록 완료됨' : '😶 감정을 기록해보세요' }}</p>
    <p>📌 {{ statusMessage }}</p>
  </div>
</template>


<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import axios from 'axios'
import { useTransactionStore } from '@/stores/transactions'
import { forceUpdate } from '@/stores/summaryTrigger'

const props = defineProps({
  date: String
})

const store = useTransactionStore()

const today = computed(() => {
  if (props.date) return props.date
  const now = new Date()
  const offset = now.getTimezoneOffset() * 60000
  const koreaTime = new Date(now.getTime() - offset + 9 * 60 * 60 * 1000)
  return koreaTime.toISOString().split('T')[0]
})

const budget = ref(0)
const monthlyTotal = ref(0)
const recommendedSpending = ref(0)
const hasEmotion = ref(false)
const todaySpending = ref(0)

const fetchSummaryData = async () => {
  try {
    const now = new Date()
    const year = now.getFullYear()
    const month = now.getMonth() + 1

    const [budgetRes, todayRes, statsRes] = await Promise.all([
      axios.get('/api/setting/budget/', {
        params: { year, month }
      }).catch(error => {
        if (error.response && (error.response.status === 400 || error.response.status === 404)) {
          console.warn('📭 예산 정보 없음, 기본값 0 사용')
          return { data: {} }
        }
        throw error
      }),
      axios.get('/api/home/today-summary/'),
      axios.get('/api/home/monthly-summary-stats/', {
        params: { year, month }
      })
    ])
    console.log('✅ 예산 응답:', budgetRes.data)
    console.log('✅ 오늘 요약 응답:', todayRes.data)
    console.log('✅ 통계 응답:', statsRes.data)

    if (budgetRes?.data?.budget !== undefined) {
      budget.value = budgetRes.data.budget
    } else {
      console.warn('📭 예산 정보 없음, 기본값 0 사용')
      budget.value = 0
    }
    todaySpending.value = Math.abs(todayRes.data.total_expense || 0)
    hasEmotion.value = !!todayRes.data.has_emotion
    monthlyTotal.value = Math.abs(statsRes.data.total_expense || 0)
    recommendedSpending.value = todayRes.data.recommended_daily_budget ?? 1
  } catch (err) {
    console.error('❌ 요약 데이터 불러오기 실패:', err)
    budget.value = 0
    todaySpending.value = 0
    hasEmotion.value = false
    monthlyTotal.value = 0
  }
}

onMounted(fetchSummaryData)

watch(forceUpdate, async (val) => {
  console.log('[🌀 forceUpdate 감지됨]', val)
  await nextTick()
  await fetchSummaryData()
})

watch(() => store.transactions, async () => {
  console.log('[🌀 트랜잭션 변경 감지됨]')
  await nextTick()
  await fetchSummaryData()
}, { deep: true })

watch(() => props.date, async () => {
  await fetchSummaryData()
})

const todayList = computed(() => {
  const _ = forceUpdate.value // explicitly trigger reactivity
  return store.transactions
    .map((t, i) => ({ ...t, _index: i }))
    .filter(t => {
      const txDate = new Date(t.date).toISOString().split('T')[0]
      const targetDate = new Date(today.value).toISOString().split('T')[0]
      return txDate === targetDate
    })
})

const statusMessage = computed(() => {
  const rate = recommendedSpending.value
    ? todaySpending.value / recommendedSpending.value
    : 0
  return rate <= 1.0 ? '잘 소비하고 있어요! 🙂' : '예산 초과 주의! ⚠️'
})

const todayLabel = computed(() => {
  const days = ['일', '월', '화', '수', '목', '금', '토']
  const dateObj = new Date(today.value)
  const offset = dateObj.getTimezoneOffset() * 60000
  const koreaDate = new Date(dateObj.getTime() - offset + 9 * 60 * 60 * 1000)
  const weekday = days[koreaDate.getDay()]
  return `${koreaDate.getMonth() + 1}월 ${koreaDate.getDate()}일 (${weekday})`
})


const displayTodaySpending = computed(() => {
  return Math.abs(todaySpending.value ?? 0).toLocaleString()
})

const displayRecommendedSpending = computed(() => {
  return Math.abs(recommendedSpending.value ?? 0).toLocaleString()
})

const displayMonthlyTotal = computed(() => {
  return Math.abs(monthlyTotal.value ?? 0).toLocaleString()
})

const todaySpendingRate = computed(() => {
  return recommendedSpending.value
    ? Math.min(Math.max((todaySpending.value / recommendedSpending.value) * 100, 0), 999).toFixed(1)
    : 0
})

const monthlySpendingRate = computed(() => {
  return budget.value
    ? Math.min((monthlyTotal.value / budget.value) * 100, 999).toFixed(1)
    : 0
})

const monthlyProgressRate = computed(() => {
  const now = new Date()
  const totalDays = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate()
  const currentDay = now.getDate()
  return Math.round((currentDay / totalDays) * 100)
})

</script>


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

.progress-bar {
  width: 100%;
  height: 12px;
  background-color: #ddd;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  background-color: #4caf50;
  transition: width 0.3s ease-in-out;
}

</style>