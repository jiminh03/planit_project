<template>
  <div class="login-page">
    <div class="signup-container">
      <h2>로그인</h2>
      <input v-model="username" placeholder="사용자 이름 입력" />
      <input v-model="password" type="password" placeholder="비밀번호 입력" />
      <button @click="signup">로그인</button>
      <button @click="goToSignup">회원가입</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import TopHeader from '@/components/TopHeader.vue'

const username = ref('')
const password = ref('')
const router = useRouter()
const userStore = useUserStore()

const signup = () => {
  if (username.value.trim() === '' || password.value.trim() === '') {
    alert('이름과 비밀번호를 입력해주세요.')
    return
  }

  userStore.login(username.value)  // 실제로는 가입 후 로그인 상태로 진입
  router.push('/home')
}

const goToSignup = () => {
  router.push('/signup')
}
</script>