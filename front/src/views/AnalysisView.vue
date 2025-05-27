<template>
  <div class="analysis-page">
    <h2 class="title">💡 GPT 소비 도우미 분석 결과</h2>

    <div v-if="isLoading">분석 중입니다...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="card-container">
      <div v-for="(card, index) in cards" :key="index" class="card">
        <h3 v-html="card.title" class="card-title" />
        <p v-html="card.content" class="card-content" />
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
const cards = ref([])
const userStore = useUserStore()

// ✅ CSRF 토큰 가져오기
const getCSRFToken = () => {
  const value = `; ${document.cookie}`
  const parts = value.split(`; csrftoken=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
  return ''
}

// ✅ GPT 분석 요청
const fetchGPTAnalysis = async () => {
  isLoading.value = true
  error.value = ''
  try {
    const response = await axios.post(
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
    const rawText = response.data.result

    // 항목별 분할: "###" 로 시작하는 제목 기준
    const sections = rawText.split(/(?=### )/g)
    cards.value = sections.map(section => {
      const [titleLine, ...bodyLines] = section.split('\n')
      return {
        title: titleLine.trim(),
        content: bodyLines.join('\n').trim().replaceAll('\n', '<br/>')
      }
    })
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
