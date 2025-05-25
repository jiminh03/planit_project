<template>
    <div class="signup-container">
      <h2>로그인</h2>
      <input v-model="email" placeholder="사용자 이름 입력" />
      <input v-model="password" type="password" placeholder="비밀번호 입력" />
      <button @click="login">로그인</button>
      <button @click="goToSignup">회원가입</button>
      <button class="google-split-button" @click="loginWithGoogle">
        <div class="google-icon-box">
          <img src="@/assets/google-logo.jpeg" alt="G" class="google-icon" />
        </div>
        <div class="google-text-box">
          Google로 로그인
        </div>
      </button>
      <button class="naver-split-button" @click="loginWithNaver">
        <div class="naver-icon-box">
          <img src="@/assets/naver-logo.jpg" alt="N" class="naver-icon" />
        </div>
        <div class="naver-text-box">
          네이버 아이디로 로그인
        </div>
      </button>
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

const loginWithGoogle = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/accounts/google/login-url/', {
      withCredentials: true
    })
    console.log('✅ Google auth URL:', res.data.auth_url)
    window.location.href = res.data.auth_url
  } catch (error) {
    console.error('❌ Google 로그인 요청 실패:', error)
    alert('구글 로그인 요청에 실패했습니다.')
  }
}

const loginWithNaver = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/accounts/naver/login-url/', {
      withCredentials: true
    })
    console.log('✅ Naver auth URL:', res.data.auth_url)
    window.location.href = res.data.auth_url
  } catch (error) {
    console.error('❌ Naver 로그인 요청 실패:', error)
    alert('네이버 로그인 요청에 실패했습니다.')
  }
}

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
  transform: translateX(-50%);
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


.google-split-button {
  display: flex;
  width: 100%;
  height: 52px;
  border: 1px solid #ddd;
  padding: 0;
  border-radius: 8px;
  overflow: hidden;
  font-weight: 700;
  cursor: pointer;
  background-color: white;
}

.google-icon-box {
  width: 52px;
  background-color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  border-right: 1px solid #ddd;
}

.google-icon {
  width: 24px;
  height: 24px;
}

.google-text-box {
  flex: 1;
  background-color: white;
  color: #444;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.naver-split-button {
  display: flex;
  width: 100%;
  height: 52px;
  border: none;
  padding: 0;
  border-radius: 8px;
  overflow: hidden;
  font-weight: 700;
  cursor: pointer;
}

.naver-icon-box {
  width: 52px;
  background-color: #03C75A;
  display: flex;
  align-items: center;
  justify-content: center;
}

.naver-icon {
  width: 24px;
  height: 24px;
}

.naver-text-box {
  flex: 1;
  background-color: #03C75A;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}
</style>