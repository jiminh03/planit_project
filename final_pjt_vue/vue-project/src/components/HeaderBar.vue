<template>
  <nav class="navbar">
    <div class="logo">MY 가계부</div>
    <ul class="menu">
      <li><router-link to="/features">기능</router-link></li>
      <li><router-link to="/notices">공지사항</router-link></li>
      <li><router-link to="/signup">회원가입</router-link></li>
      <li><router-link to="/login">로그인</router-link></li>
    </ul>
  </nav>
</template>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #fff;
  border-bottom: 1px solid #eee;
}

.logo {
  font-size: 1.2rem;
  font-weight: bold;
}

.menu {
  list-style: none;
  display: flex;
  gap: 1.5rem;
  margin: 0;
  padding: 0;
}

.menu li a {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  padding-bottom: 2px;
  border-bottom: 2px solid transparent;
  transition: 0.2s;
}

.menu li a:hover {
  border-color: #6a5acd;
  color: #6a5acd;
}
</style>
