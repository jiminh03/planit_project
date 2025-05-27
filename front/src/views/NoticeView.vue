<template>
  <div class="notice-container">
    <h1>📢 공지사항</h1>

    <div style="text-align: right; margin-bottom: 6px" v-if="userStore.isAdmin">
      <!-- <button class="plain-write-button" @click="$router.push('/notice/create')">글쓰기</button> -->
    </div>

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
          <td>{{ (currentPage - 1) * pageSize + index + 1 }}</td>
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
      <!-- 이전 페이지 -->
      <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1">‹</button>

      <!-- 페이지 번호 -->
      <button v-for="page in totalPages" :key="page" @click="changePage(page)"
        :class="{ active: currentPage === page }">
        {{ page }}
      </button>

      <!-- 다음 페이지 -->
      <button @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages">›</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const notices = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const pageSize = ref(10)  // 페이지 사이즈 동적으로 계산

const fetchNotices = async (page = 1) => {
  try {
    const response = await axios.get(`http://localhost:8000/api/accounts/notice/?page=${page}`)

    if (Array.isArray(response.data)) {
      notices.value = response.data
      totalPages.value = 1
      pageSize.value = 10
    } else {
      notices.value = response.data.results
      pageSize.value = response.data.page_size || response.data.results.length || 10
      totalPages.value = Math.ceil(response.data.count / pageSize.value)
    }

    currentPage.value = page
  } catch (error) {
    console.error('공지사항 로딩 실패:', error)
  }
}

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    fetchNotices(page)
  }
}

onMounted(() => {
  fetchNotices()
})
</script>

<style scoped>
.notice-container {
  padding: 20px;
  font-family: Arial, sans-serif;
  text-align: center;
}

h1 {
  font-size: 32px;
  font-weight: 800;
  text-align: center;
  margin-bottom: 16px;
  color: black;
}

.notice-table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
  margin-bottom: 15px;
}

.notice-table th,
.notice-table td {
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
  align-items: center;
  gap: 6px;
  margin-top: 16px;
}

.pagination button {
  min-width: 36px;
  height: 36px;
  font-size: 14px;
  font-weight: bold;
  border: 1px solid #000000;
  border-radius: 8px;
  background-color: #000000;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pagination button.active {
  background-color: #2563eb;
  color: white;
  border-color: #2563eb;
}

.pagination button:disabled {
  background-color: black;
  color: white;
  border-color: black;
  cursor: not-allowed;
  opacity: 1;
  /* 흐려지지 않게 */

}

.plain-write-button {
  all: unset;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
}
</style>
