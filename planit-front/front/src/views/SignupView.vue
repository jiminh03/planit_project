<template>
  <div class="signup-container">
    <h2>회원가입</h2>
    <input v-model="username" placeholder="사용자 이름 입력" />
    <input v-model="password" type="password" placeholder="비밀번호 입력" />
    <button @click="signup">회원가입</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const username = ref('')
const password = ref('')
const router = useRouter()
const userStore = useUserStore()

const signup = () => {
  if (username.value.trim() === '' || password.value.trim() === '') {
    alert('이름과 비밀번호를 입력해주세요.')
    return
  }

  userStore.login(username.value)
  router.push('/home')
}
</script>