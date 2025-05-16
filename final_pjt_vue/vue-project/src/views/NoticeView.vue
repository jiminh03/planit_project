<!-- src/views/NoticeView.vue -->
<template>
<HeaderBar />
  <div class="notice-container">
    <h2>공지사항</h2>
    <ul class="notice-list">
      <li v-for="notice in notices" :key="notice.id">
        <h3>{{ notice.title }}</h3>
        <p class="date">{{ notice.date }}</p>
        <p class="content">{{ notice.content }}</p>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import HeaderBar from '@/components/HeaderBar.vue';

const notices = ref([
  { id: 1, title: '서비스 점검 안내', date: '2025-05-16', content: '5월 18일 02시부터 04시까지 시스템 점검이 진행됩니다.' },
  { id: 2, title: '신규 기능 출시', date: '2025-05-14', content: 'AI 소비 분석 기능이 추가되었습니다.' },
  { id: 3, title: '이벤트 안내', date: '2025-05-10', content: '5월 한정 신규 가입 이벤트 진행 중!' },
])
</script>

<style scoped>
.notice-container {
  max-width: 800px;
  margin: 50px auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.notice-list {
  list-style: none;
  padding: 0;
}

.notice-list li {
  border-bottom: 1px solid #eee;
  padding: 1rem 0;
}

.notice-list h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #333;
}

.notice-list .date {
  color: #999;
  font-size: 0.9rem;
  margin-top: 4px;
}

.notice-list .content {
  margin-top: 0.5rem;
  color: #444;
}
</style>
