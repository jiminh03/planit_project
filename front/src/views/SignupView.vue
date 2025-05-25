<template>
  <div class="signup-page">
    <h2>회원가입</h2>
    <form @submit.prevent="signup">
      <input v-model="username" placeholder="아이디를 입력하세요" required />
      <input v-model="email" type="email" placeholder="이메일을 입력하세요" required />
      <input v-model="password" type="password" placeholder="비밀번호를 입력하세요" required />

      <input v-model="name" placeholder="이름을 입력하세요" required />
      <input v-model.number="age" type="number" min="1" placeholder="나이를 입력하세요" required />

      <div class="gender-group">
        <label>
          <input type="radio" value="male" v-model="gender" /> 남성
        </label>
        <label>
          <input type="radio" value="female" v-model="gender" /> 여성
        </label>
      </div>

      <button type="submit">회원가입</button>
    </form>
    <p>
      이미 계정이 있으신가요?
      <span @click="goToLogin" style="color:blue; cursor:pointer">로그인하기</span>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

// 쿠키에서 CSRF 토큰을 가져오는 함수
function getCookie(name) {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
}

const username = ref('')
const email = ref('')
const password = ref('')
const name = ref('')
const age = ref(null)
const gender = ref('male')
const router = useRouter()

const signup = async () => {
  if (!username.value || !email.value || !password.value || !name.value || !age.value || !gender.value) {
    alert('모든 항목을 입력해주세요.')
    return
  }

  const csrfToken = getCookie('csrftoken')

  try {
    await axios.post(
      'http://localhost:8000/api/accounts/signup/',
      {
        username: username.value,
        email: email.value,
        password: password.value,
        name: name.value,
        age: age.value,
        gender: gender.value
      },
      {
        headers: {
          'X-CSRFToken': csrfToken
        },
        withCredentials: true
      }
    )
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
.gender-group {
  display: flex;
  gap: 20px;
  padding-top: 8px;
}
</style>