<template>
<HeaderBar />

  <div class="signup-container">
    <h2>회원가입</h2>
    <form @submit.prevent="handleSignup">
      <label>이름</label>
      <input v-model="name" type="text" required />

      <label>이메일</label>
      <input v-model="email" type="email" required />

      <label>비밀번호</label>
      <input v-model="password" type="password" required />

      <label>비밀번호 확인</label>
      <input v-model="confirmPassword" type="password" required />

      <button type="submit">회원가입</button>
    </form>

    <p class="error" v-if="errorMessage">{{ errorMessage }}</p>
    <p class="success" v-if="successMessage">{{ successMessage }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import HeaderBar from '@/components/HeaderBar.vue'

const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')

const errorMessage = ref('')
const successMessage = ref('')

const handleSignup = async () => {
  if (password.value !== confirmPassword.value) {
    errorMessage.value = '비밀번호가 일치하지 않습니다.'
    return
  }

  try {
    const response = await axios.post('http://localhost:8000/api/signup/', {
      name: name.value,
      email: email.value,
      password: password.value,
    })
    successMessage.value = '회원가입이 완료되었습니다.'
    errorMessage.value = ''
  } catch (error) {
    errorMessage.value = '회원가입 중 오류가 발생했습니다.'
    successMessage.value = ''
    console.error(error)
  }
}
</script>

<style scoped>
.signup-container {
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
  background-color: #0051ffbd;
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
