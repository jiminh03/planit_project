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
          <td>{{ (currentPage - 1) * 5 + index + 1 }}</td>
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
      <button :disabled="currentPage === 1" @click="changePage(currentPage - 1)">‹</button>

      <button
        v-for="page in totalPages"
        :key="page"
        :class="{ active: currentPage === page }"
        @click="changePage(page)"
      >
        {{ page }}
      </button>

      <button :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)">›</button>
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

const fetchNotices = async (page = 1) => {
  try {
    const response = await axios.get(`http://localhost:8000/api/accounts/notice/?page=${page}`)
    notices.value = response.data.results
    totalPages.value = Math.ceil(response.data.count / 5)  // assuming 5 per page
    currentPage.value = page
  } catch (error) {
    console.error('공지사항 로딩 실패:', error)
  }
}

onMounted(() => {
  fetchNotices()
})

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    fetchNotices(page)
  }
}
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

.write-button {
  background-color: #2563eb;
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 5px;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 12px;
}

.plain-write-button {
  all: unset;
  font-size: 15px;
  font-weight:500;
  cursor: pointer;
}
</style>