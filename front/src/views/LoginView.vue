<template>
  <div class="login-page">
    <div class="signup-container">
      <h2>로그인</h2>
      <input v-model="email" placeholder="사용자 이름 입력" />
      <input v-model="password" type="password" placeholder="비밀번호 입력" />
      <button @click="login">로그인</button>
      <button @click="goToSignup">회원가입</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import TopHeader from '@/components/TopHeader.vue'

const email = ref('')
const password = ref('')
const router = useRouter()
const userStore = useUserStore()

import axios from 'axios'

const login = async () => {
  if (!email.value.trim() || !password.value.trim()) {
    alert('이름과 비밀번호를 입력해주세요.')
    return
  }

  try {
    const res = await axios.post('http://localhost:8000/api/accounts/login/', {
      email: email.value,
      password: password.value
    }, { withCredentials: true })

    alert('로그인 성공!')
    userStore.login(email.value)
    router.push('/home')
  } catch (error) {
    alert('로그인 실패: ' + (error.response?.data?.error || '서버 오류'))
  }
}

const goToSignup = () => {
  router.push('/signup')
}
</script>