<template>
    <HeaderBar/>
  <div class="feature-container">
    <h2>주요 기능 소개</h2>
    <div class="feature-list">
      <div class="feature-card" v-for="item in features" :key="item.id">
        <h3>{{ item.title }}</h3>
        <p>{{ item.description }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import HeaderBar from '@/components/HeaderBar.vue';
import { ref } from 'vue'

const features = ref([
  {
    id: 1,
    title: '자동 소비 분류',
    description: '마이데이터를 분석하여 카드/계좌 소비 내역을 자동으로 카테고리화합니다.'
  },
  {
    id: 2,
    title: '감정 기반 소비 분석',
    description: '소비 내역과 감정 데이터를 연결하여 감정 기반 소비 성향을 분석합니다.'
  },
  {
    id: 3,
    title: '예산 가이드 제공',
    description: '월별 예산을 기반으로 매일 권장 지출 한도를 계산하여 제공합니다.'
  },
  {
    id: 4,
    title: '시각화된 리포트',
    description: '원형 그래프, 막대 차트 등으로 나의 소비 패턴을 직관적으로 확인할 수 있습니다.'
  },
])
</script>

<style scoped>
.feature-container {
  max-width: 1000px;
  margin: 50px auto;
  padding: 2rem;
  text-align: center;
}

.feature-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 2rem;
}

.feature-card {
  width: 220px;
  padding: 1.5rem;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  transition: transform 0.2s;
}

.feature-card:hover {
  transform: translateY(-4px);
}

.feature-card h3 {
  margin-bottom: 0.5rem;
  color: #333;
}

.feature-card p {
  font-size: 0.9rem;
  color: #555;
}
</style>
