<template>
  <ul class="settings-card">
    <li
      v-for="(item, index) in items"
      :key="index"
      @click="$emit('open-modal', item)"
    >
      {{ item }} <span class="arrow">›</span>
    </li>
  </ul>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    required: true,
  }
})
</script>

<style scoped>
.settings-card {
  list-style: none;
  padding: 0;
  margin: 0;
  background: var(--card-bg-color);
  border: none;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  color: var(--text-color);
}

.settings-card li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid var(--divider-color);
  font-size: 0.95rem;
  cursor: pointer;
}

.settings-card li:last-child {
  border-bottom: none;
}

.arrow {
  font-size: 1.2rem;
  color: var(--text-color);
}
:deep(body.dark) .settings-card {
  background: #2c2c2c;
}

:deep(body.dark) .settings-card li {
  border-bottom: 1px solid #444;
}

:deep(body.dark) .arrow {
  color: #ccc;
}
</style>

