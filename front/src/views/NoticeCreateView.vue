<template>
  <div class="notice-create">
    <h2>공지사항 작성</h2>
    <form @submit.prevent="submitNotice">
      <input v-model="title" type="text" placeholder="제목을 입력하세요" required />
      <textarea v-model="content" placeholder="내용을 입력하세요" required></textarea>
      <button type="submit">작성 완료</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import axios from 'axios'

const title = ref('')
const content = ref('')
const router = useRouter()
const userStore = useUserStore()

onMounted(() => {
  if (!userStore.isAdmin) {
    alert('접근 권한이 없습니다.')
    router.push('/')
  }
})

const submitNotice = async () => {
  try {
    await axios.post('http://localhost:8000/api/accounts/notice/create/', {
      title: title.value,
      content: content.value
    })
    alert('공지사항이 등록되었습니다.')
    router.push('/notice')
  } catch (error) {
    alert('작성 실패: ' + error.response?.data?.detail || error.message)
  }
}
</script>

<style scoped>
.notice-create {
  max-width: 600px;
  margin: 0 auto;
}
.notice-create input,
.notice-create textarea {
  display: block;
  width: 100%;
  margin-bottom: 12px;
  padding: 8px;
  font-size: 16px;
}
</style>