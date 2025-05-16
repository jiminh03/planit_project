<template>
  <div>
    <HeaderBar />

    <section class="hero">
      <h1>마이데이터 기반 자동가계부</h1>
      <p class="desc">마이데이터를 연결하기만 하면, 자동으로 분류해서 지출과 수입을 보여주는 간편 가계부</p>
      <p class="sub">📌 내 입맛에 맞춰 카테고리를 재분류할 수 있어요</p>

      <div class="mockup-container">
        <img src="@/assets/image.jpg" alt="가계부 미리보기" />
      </div>
    </section>
  </div>
</template>

<script setup>
import HeaderBar from '@/components/HeaderBar.vue'
</script>

<style scoped>
.hero {
  text-align: center;
  padding: 3rem 2rem;
}

h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.desc {
  font-size: 1.1rem;
  color: #333;
}

.sub {
  font-size: 0.9rem;
  color: #888;
  margin-bottom: 2rem;
}

.mockup-container img {
  max-width: 100%;
  width: 720px;
  margin: 0 auto;
  display: block;
}
</style>
