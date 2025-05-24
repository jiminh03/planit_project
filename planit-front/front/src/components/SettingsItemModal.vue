<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <h3>{{ title }}</h3>
      <p>설정 내용을 여기에 표시하세요.</p>
      <button @click="$emit('close')">닫기</button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex; justify-content: center; align-items: center;
  z-index: 9999;
}

.modal-content {
  background: #fff;
  color: var(--text-color);
  padding: 2rem;
  border-radius: 12px;
  min-width: 400px;
  max-width: 90vw;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  z-index: 10000;
}
</style>
