<template>
    <div class="signup-container">
      <h2>로그인</h2>
      <input v-model="email" placeholder="사용자 이름 입력" />
      <input v-model="password" type="password" placeholder="비밀번호 입력" />
      <button @click="login">로그인</button>
      <button @click="goToSignup">회원가입</button>
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
    userStore.login(res.data.user)  // 수정된 부분

    // 로그인 후 전체 거래내역 불러오기
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

<style>


.signup-container {
  position: fixed;
  top: 20%;
  left: 50%;
  width: 500px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 1px 6px rgba(0,0,0,0.1);
  padding: 32px 40px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 20px;
}


h2 {
  text-align: center;
  font-weight: 700;
  font-size: 28px;
  margin: 0 0 32px 0;
  color: #222;
}

input {
  height: 44px;
  border-radius: 8px;
  border: 1px solid #ddd;
  padding: 12px 16px;
  font-size: 16px;
  box-sizing: border-box;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

input::placeholder {
  color: #bbb;
}

input:focus {
  outline: none;
  border-color: #4A90E2;
  box-shadow: 0 0 0 3px rgba(74,144,226,0.15);
}

button {
  height: 52px;
  border-radius: 8px;
  background-color: #222;
  color: white;
  font-weight: 700;
  font-size: 16px;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

button:hover {
  background-color: #444;
}

.signup-container button:last-child {
  background-color: #ccc;
  color: #444;
  font-weight: 600;
  margin-top: 12px;
}

.signup-container button:last-child:hover {
  background-color: #bbb;
}
</style>