<template>
  <div class="signup-page">
    <h2>회원가입</h2>
    <form @submit.prevent="signup">
      <input v-model="name" placeholder="이름을 입력하세요" required />
      <input v-model="email" type="email" placeholder="이메일을 입력하세요" required />
      <input v-model="password" type="password" placeholder="비밀번호를 입력하세요" required />
      <button type="submit">회원가입</button>
    </form>
    <p>이미 계정이 있으신가요? <span @click="goToLogin" style="color:blue; cursor:pointer">로그인하기</span></p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import axios from 'axios'

const name = ref('')
const email = ref('')
const password = ref('')
const router = useRouter()
const userStore = useUserStore()

const signup = async () => {
  if (!name.value || !email.value || !password.value) {
    alert('모든 항목을 입력해주세요.')
    return
  }

  try {
    const response = await axios.post('http://localhost:8000/api/signup/', {
      username: name.value,
      email: email.value,
      password: password.value,
    })
    alert('회원가입 성공! 로그인 페이지로 이동합니다.')
    router.push('/login')
  } catch (error) {
    alert('회원가입 실패: ' + (error.response?.data?.error || '서버 오류'))
  }
}

const goToLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.signup-page {
  max-width: 400px;
  margin: 50px auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
button {
  padding: 8px;
}
</style>