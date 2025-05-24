<template>
  <div class="card-scroll-wrapper">
    <div class="card-grid">
      <div class="card" v-for="(card, index) in cards" :key="index">
        <p class="card-title">{{ card.title }}</p>
        <p class="card-content">{{ card.content }}</p>
      </div>
    </div>
  </div>
</template>


<script setup>
const cards = [
  { title: '제목1', content: '' },
  { title: '제목2', content: '' },
  { title: '제목3', content: '' },
  { title: '구독 서비스', content: '' },
  { title: '절약 시뮬레이션', content: '' }
]
</script>


<style scoped>
.card-scroll-wrapper {
  height: 100%;
  width: 100%;
  overflow-y: auto;
  padding-right: 0.5rem;
  min-width: 600px;
}

.card-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  width: 100%;
  padding-bottom: 2rem;
}

.card {
  margin-top: 80px;
  background-color: rgba(180, 180, 180, 0.2); /* 밝은 회색 느낌의 투명 배경 */
  backdrop-filter: blur(6px);
  border: 1px solid rgba(255, 255, 255, 0.12); /* 흐릿한 외곽선 */
  color: var(--text-color);
  border-radius: 12px;
  padding: 1rem;
  min-height: 500px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style>
