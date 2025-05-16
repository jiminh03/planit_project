<template>
<HeaderBar />
  <div class="login-container">
    <h2>로그인</h2>
    <form @submit.prevent="handleLogin">
      <label>이메일</label>
      <input v-model="email" type="email" required />

      <label>비밀번호</label>
      <input v-model="password" type="password" required />

      <button type="submit">로그인</button>
    </form>

    <p class="error" v-if="errorMessage">{{ errorMessage }}</p>
    <p class="success" v-if="successMessage">{{ successMessage }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import HeaderBar from '@/components/HeaderBar.vue'

const email = ref('')
const password = ref('')
const errorMessage = ref('')
const successMessage = ref('')

const handleLogin = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/login/', {
      email: email.value,
      password: password.value,
    })

    successMessage.value = '로그인 성공!'
    errorMessage.value = ''
    // 🔐 토큰 저장 또는 상태 처리 추가 가능
    // 예: localStorage.setItem('token', response.data.token)

  } catch (err) {
    errorMessage.value = '로그인 실패. 이메일 또는 비밀번호를 확인하세요.'
    successMessage.value = ''
    console.error(err)
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 2rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #fff;
}

form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

input {
  padding: 0.5rem;
  font-size: 1rem;
}

button {
  padding: 0.7rem;
  background-color: #000000;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.error {
  color: red;
  margin-top: 1rem;
}

.success {
  color: green;
  margin-top: 1rem;
}
</style>
