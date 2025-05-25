<template>
  <div class="notice-detail-container">
    <div class="notice-box">
      <h1 class="notice-title">{{ notice.title }}</h1>
      <p class="notice-date">작성일: {{ formatDate(notice.created_at) }}</p>
      <div class="notice-content">
        <pre style="white-space: pre-wrap;">{{ notice.content }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const notice = ref({})

function formatDate(dateStr) {
  if (!dateStr) return '날짜 없음'
  const date = new Date(dateStr)
  return isNaN(date.getTime()) ? '날짜 오류' : date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(async () => {
  try {
    const id = route.params.id
    const response = await axios.get(`http://localhost:8000/api/accounts/notice/${id}/`)
    console.log('✅ 응답 전체:', response)

    // 예상 응답 구조에 따라 처리
    if (response.data && response.data.content) {
      notice.value = response.data
    } else {
      console.warn('⚠️ 예상치 못한 응답 구조입니다:', response.data)
    }
  } catch (err) {
    console.error('❌ 공지사항 상세 불러오기 실패:', err)
  }
})
</script>

<style scoped>
.notice-detail-container {
  max-width: 800px;
  margin: 60px auto;
  padding: 24px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 0 12px rgba(0,0,0,0.05);
}

.notice-box {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.notice-title {
  font-size: 28px;
  font-weight: bold;
  border-bottom: 1px solid #ccc;
  padding-bottom: 0;
  margin-bottom: 0;
}

.notice-date {
  font-size: 14px;
  color: #888;
  margin-top: 0;
}

.notice-content {
  font-size: 16px;
  line-height: 1.6;
}
</style>