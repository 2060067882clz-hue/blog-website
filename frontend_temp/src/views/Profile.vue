<template>
  <div class="profile-container">
    <div class="profile-card">
      <h2>个人中心</h2>
      <p>欢迎回来，<strong>{{ nickname }}</strong>！</p>
      <button @click="logout">退出登录</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const nickname = ref(localStorage.getItem('nickname') || '用户')
const router = useRouter()

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('nickname')
  router.push('/login')
}
</script>

<style scoped>
.profile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: #f0f2f5;
}
.profile-card {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  text-align: center;
}
.profile-card button {
  margin-top: 20px;
  padding: 8px 24px;
  background: #f56c6c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>