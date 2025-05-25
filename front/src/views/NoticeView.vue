<template>
  <div class="notice-container">
    <h1>📢 공지사항</h1>
    <table class="notice-table">
      <thead>
        <tr>
          <th>번호</th>
          <th>제목</th>
          <th>등록일</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(notice, index) in notices" :key="notice.id">
          <td>{{ notices.length - index }}</td>
          <td>
            <router-link :to="`/notice/${notice.id}`">
              {{ notice.title }}
            </router-link>
          </td>
          <td>{{ new Date(notice.created_at).toLocaleDateString() }}</td>
        </tr>
      </tbody>
    </table>
    <div class="pagination">
      <button disabled>&laquo;</button>
      <button disabled>‹</button>
      <button class="active">1</button>
      <button>2</button>
      <button>3</button>
      <button>4</button>
      <button>5</button>
      <button>›</button>
      <button>&raquo;</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const notices = ref([])

onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/accounts/notice/')
    notices.value = response.data
  } catch (error) {
    console.error('공지사항 로딩 실패:', error)
  }
})
</script>

<style scoped>
.notice-container {
  padding: 20px;
  font-family: Arial, sans-serif;
  text-align: center;
}

h1 {
  color: #333;
  margin-bottom: 10px;
  font-weight: bold;
}

.notice-table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
  margin-bottom: 15px;
}

.notice-table th, .notice-table td {
  border-bottom: 1px solid #ccc;
  padding: 12px 10px;
}

.notice-table th {
  font-weight: 600;
  background-color: #f9f9f9;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 8px;
}

.pagination button {
  border: 1px solid #ccc;
  background-color: white;
  border-radius: 4px;
  padding: 6px 10px;
  cursor: pointer;
  font-weight: 600;
  user-select: none;
}

.pagination button.active {
  background-color: #2563eb;
  color: white;
  border-color: #2563eb;
}

.pagination button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}
</style>