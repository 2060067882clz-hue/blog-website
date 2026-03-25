<template>
  <div class="login-container">
    <div class="login-card">
      <h2>课程项目登录</h2>
      <input 
        v-model="username" 
        type="text" 
        placeholder="用户名"
        @keyup.enter="login"
      />
      <input 
        v-model="password" 
        type="password" 
        placeholder="密码"
        @keyup.enter="login"
      />
      <button @click="login" :disabled="loading">
        {{ loading ? '登录中...' : '登录' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const loading = ref(false)
const router = useRouter()

const login = async () => {
  if (!username.value || !password.value) {
    alert('请输入用户名和密码')
    return
  }
  
  loading.value = true
  
  // 模拟登录，等后端接口好了再替换
  setTimeout(() => {
    localStorage.setItem('token', 'fake-token-123')
    localStorage.setItem('nickname', username.value)
    loading.value = false
    router.push('/profile')
  }, 500)
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: #f0f2f5;
}
.login-card {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  width: 300px;
}
.login-card h2 {
  text-align: center;
  margin-bottom: 24px;
}
.login-card input {
  width: 100%;
  padding: 10px;
  margin-bottom: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}
.login-card button {
  width: 100%;
  padding: 10px;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}
.login-card button:disabled {
  background: #a0cfff;
  cursor: not-allowed;
}
</style>