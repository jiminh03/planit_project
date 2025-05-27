<template>
  <div class="analysis-page">
    <h2 class="title">💡 GPT 소비 도우미 분석 결과</h2>

    <div v-if="isLoading">분석 중입니다...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="card-container">
      <div class="card" v-if="results.summary">
        <h3 class="card-title">📊 1. 소비 패턴 요약</h3>
        <p class="card-content" v-html="results.summary" />
      </div>
      <div class="card" v-if="results.strategy">
        <h3 class="card-title">💡 2. 대체 전략 제안</h3>
        <p class="card-content" v-html="results.strategy" />
      </div>
      <div class="card" v-if="results.fixed">
        <h3 class="card-title">📦 3. 정기 지출 정리</h3>
        <p class="card-content" v-html="results.fixed" />
      </div>
      <div class="card" v-if="results.simulation">
        <h3 class="card-title">🔥 4. 절약 시뮬레이션</h3>
        <p class="card-content" v-html="results.simulation" />
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
  summary: '',
  strategy: '',
  fixed: '',
  simulation: ''
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
      '/api/helper/analysis/',
      { email: userStore.email },
      {
        headers: {
          'X-CSRFToken': getCSRFToken(),
          'Content-Type': 'application/json'
        },
        withCredentials: true
      }
    )
    results.value.summary = res.data.summary_result.replaceAll('\n', '<br/>')
    results.value.strategy = res.data.strategy_result.replaceAll('\n', '<br/>')
    results.value.fixed = res.data.fixed_result.replaceAll('\n', '<br/>')
    results.value.simulation = res.data.simulation_result.replaceAll('\n', '<br/>')
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
