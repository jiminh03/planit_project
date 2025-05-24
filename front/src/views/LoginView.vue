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
import { useTransactionStore } from '@/stores/transactions'
import axios from 'axios'

const email = ref('')
const password = ref('')
const router = useRouter()
const userStore = useUserStore()
const transactionStore = useTransactionStore()

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

    // ✅ 로그인 후 전체 거래내역 불러오기
    await transactionStore.fetchAllTransactions()

    router.push('/home')
  } catch (error) {
    console.error('로그인 실패:', error)
    if (error.response) {
      console.error('응답 상태:', error.response.status)
      console.error('응답 데이터:', error.response.data)
      alert('로그인 실패: ' + (error.response.data?.detail || '인증 오류'))
    } else {
      alert('로그인 실패: 서버에 연결할 수 없습니다.')
    }
  }
}

const goToSignup = () => {
  router.push('/signup')
}
</script>