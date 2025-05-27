<template>
  <div class="analysis-page">
    <h2 class="title">💡나의 소비 분석 결과</h2>

    <div v-if="isLoading">분석 중입니다...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="card-container">
      <div class="card" v-if="results.analysis1">
        <h3 class="card-title">📈 1. 월 지출 총액 분석</h3>
        <p class="card-content" v-html="results.analysis1" />
      </div>
      <div class="card" v-if="results.analysis2">
        <h3 class="card-title">🧾 2. 예산 초과 여부 및 원인 분석</h3>
        <p class="card-content" v-html="results.analysis2" />
      </div>
      <div class="card" v-if="results.analysis3">
        <h3 class="card-title">🔍 소비 성향 분석 (감정소비/계획소비/절약형 등)</h3>
        <p class="card-content" v-html="results.analysis3" />
      </div>
      <div class="card" v-if="results.advice">
        <h3 class="card-title"> ✨ 소비 개선을 위한 핵심 조언</h3>
        <p class="card-content" v-html="results.advice" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores/user'

const isLoading = ref(true)
const error = ref('')
const results = ref({
  analysis1: '',
  analysis2: '',
  analysis3: '',
  advice: ''
})
const userStore = useUserStore()

const getCSRFToken = () => {
  const value = `; ${document.cookie}`
  const parts = value.split(`; csrftoken=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
  return ''
}

const fetchGPTAnalysis = async () => {
  isLoading.value = true
  error.value = ''
  try {
    const res = await axios.post(
      '/api/report/summary/',
      { email: userStore.email },
      {
        headers: {
          'X-CSRFToken': getCSRFToken(),
          'Content-Type': 'application/json'
        },
        withCredentials: true
      }
    )
    results.value.analysis1 = res.data.analysis1_result.replaceAll('\n', '<br/>')
    results.value.analysis2 = res.data.analysis2_result.replaceAll('\n', '<br/>')
    results.value.analysis3 = res.data.analysis3_result.replaceAll('\n', '<br/>')
    results.value.advice = res.data.advice_result.replaceAll('\n', '<br/>')
  } catch (err) {
    error.value = err.response?.data?.error || '분석 요청 실패'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchGPTAnalysis()
})
</script>

<style scoped>
.analysis-page {
  padding: 2rem;
  background: #f9f9f9;
}

.title {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
}

.card-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.card {
  background-color: #ffffff;
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.06);
}

.card-title {
  font-size: 1.1rem;
  font-weight: bold;
  margin-bottom: 0.8rem;
}

.card-content {
  line-height: 1.6;
  font-size: 0.95rem;
  color: #333;
  white-space: normal;
}

.error {
  color: red;
  margin-top: 1rem;
}
</style>
