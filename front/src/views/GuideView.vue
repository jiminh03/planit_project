<template>
  <div class="content">
    <p>GuideView</p>
  </div>
</template>

<script setup>

</script>

<style scoped >
.layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.content-body {
  flex: 1;
  padding: 2rem;
  box-sizing: border-box;
  overflow: auto;
}

.content {
  padding: 1rem;
  flex: 1;
}
</style>