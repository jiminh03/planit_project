<template>
    <div class="signup-form-container">
      <h1 class="form-title">회원가입</h1>
      <form @submit.prevent="handleSubmit" class="signup-form">
        <div class="form-row">
          <div class="form-group">
            <label for="name">이름</label>
            <input id="name" v-model="formData.name" type="text" class="form-input" />
          </div>
          <div class="form-group">
            <label for="userId">이메일</label>
            <input id="userId" v-model="formData.userId" type="text" class="form-input" />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="age">나이</label>
            <input id="age" v-model="formData.age" type="number" class="form-input" />
          </div>
          <div class="form-group">
            <label for="password">비밀번호</label>
            <input id="password" v-model="formData.password" type="password" class="form-input" />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="gender">성별</label>
            <select id="gender" v-model="formData.gender" class="form-select">
              <option value="">선택해주세요</option>
              <option value="male">남성</option>
              <option value="female">여성</option>
            </select>
          </div>
          
        </div>

        <div class="form-row">
          <div class="form-group full-width">
            <label for="phone">전화번호</label>
            <input id="phone" v-model="formData.phone" type="tel" class="form-input" />
          </div>
          <div class="form-group empty"></div>
        </div>

        <button type="submit" class="submit-btn">회원가입 완료</button>
      </form>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const formData = ref({
  name: '',
  userId: '',
  age: '',
  password: '',
  gender: '',
  email: '',
  phone: ''
})

async function handleSubmit() {
  const payload = {
    username: formData.value.userId,
    email: formData.value.userId,
    password: formData.value.password,
    name: formData.value.name,
    age: formData.value.age,
    gender: formData.value.gender,
    phone: formData.value.phone
  }
  try {
    const response = await axios.post('/api/accounts/signup/', payload)
    if (response.status === 201 || response.status === 200) {
      alert('회원가입이 완료되었습니다. 로그인 페이지로 이동합니다.')
      window.location.href = '/login'
    } else {
      alert('회원가입에 실패했습니다. 다시 시도해주세요.')
    }
  } catch (error) {
    alert('오류가 발생했습니다: ' + (error.response?.data?.message || error.message))
  }
}
</script>

<style scoped>

.signup-form-container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 780px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 1px 6px rgba(0,0,0,0.1);
  padding: 42px 52px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

.form-title {
  text-align: center;
  font-weight: 700;
  font-size: 31px;
  margin-bottom: 47px;
  color: #222;
}

.signup-form {
  display: flex;
  flex-direction: column;
  gap: 26px;
}

.form-row {
  display: flex;
  gap: 31px;
}

.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group.full-width {
  flex: 1 1 100%;
}

.form-group.empty {
  flex: 1;
}

label {
  font-weight: 500;
  font-size: 14px;
  color: #333;
}

.form-input,
.form-select {
  padding: 16px 21px;
  border-radius: 8px;
  border: 1px solid #ddd;
  font-size: 18px;
  box-sizing: border-box;
  height: 57px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  background-color: #fff;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: #4A90E2;
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.15);
}

.submit-btn {
  width: 100%;
  padding: 21px 0;
  background-color: #222;
  border: none;
  border-radius: 8px;
  color: #fff;
  font-weight: 700;
  font-size: 21px;
  cursor: pointer;
  margin-top: 42px;
  transition: background-color 0.2s ease;
}

.submit-btn:hover {
  background-color: #444;
}

@media (max-width: 768px) {
  .signup-form-container {
    width: 100%;
    padding: 24px 16px;
  }
  .form-row {
    flex-direction: column;
    gap: 16px;
  }
  .form-group.empty {
    display: none;
  }
}
</style>
