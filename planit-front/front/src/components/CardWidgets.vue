<template>
  <div class="card-scroll-wrapper">
    <div class="card-grid">
      <div class="card" v-for="(card, index) in cards" :key="index">
        <p class="card-title">카드 {{ index + 1 }}</p>
        <p class="card-content">이곳에 요약 정보가 들어갑니다.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
const cards = [1, 2, 3, 4, 5]
</script>

<style scoped>
.card-scroll-wrapper {
  height: 100%;
  width: 100%;
  overflow-y: auto;
  padding-right: 0.5rem;
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
  background-color: #eee;
  border-radius: 12px;
  padding: 1rem;
  min-height: 500px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style>
