<template>
  <section class="auth-shell">
    <div class="auth-backdrop auth-backdrop-left"></div>
    <div class="auth-backdrop auth-backdrop-right"></div>

    <div class="auth-card">
      <aside class="auth-showcase">
        <p class="eyebrow">Course Portal</p>
        <h1>欢迎回到课程项目平台</h1>
        <p class="showcase-copy">
          在一个更轻盈、更聚焦的界面里完成登录，继续查看你的课程资料与个人信息。
        </p>

        <ul class="showcase-points">
          <li>清晰的输入反馈与禁用状态</li>
          <li>真实连接后端登录接口</li>
          <li>移动端也保持稳定的阅读体验</li>
        </ul>
      </aside>

      <div class="auth-panel">
        <div class="panel-header">
          <p class="panel-kicker">账号登录</p>
          <h2>开始进入你的工作台</h2>
          <p class="panel-copy">输入后端账号和密码后即可进入个人中心。</p>
        </div>

        <div class="field-group">
          <label for="username">用户名</label>
          <input
            id="username"
            v-model.trim="username"
            type="text"
            placeholder="请输入用户名"
            autocomplete="username"
            @keyup.enter="login"
          />
        </div>

        <div class="field-group">
          <label for="password">密码</label>
          <input
            id="password"
            v-model.trim="password"
            type="password"
            placeholder="请输入密码"
            autocomplete="current-password"
            @keyup.enter="login"
          />
        </div>

        <p class="helper-text">演示账号：admin / Admin123456</p>
        <p v-if="errorMessage" class="form-message">{{ errorMessage }}</p>

        <button class="submit-button" @click="login" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { loginRequest, saveAuth } from '../services/auth'

const username = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')
const router = useRouter()

const login = async () => {
  if (!username.value || !password.value) {
    errorMessage.value = '请输入用户名和密码'
    return
  }

  loading.value = true
  errorMessage.value = ''

  try {
    const data = await loginRequest({
      username: username.value,
      password: password.value,
    })

    saveAuth(data)
    router.push('/profile')
  } catch (error) {
    errorMessage.value = error.message || '登录失败，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-shell {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  padding: 32px;
  display: grid;
  place-items: center;
  background:
    radial-gradient(circle at top left, rgba(244, 196, 48, 0.28), transparent 32%),
    radial-gradient(circle at bottom right, rgba(14, 116, 144, 0.2), transparent 28%),
    linear-gradient(135deg, #f6efe5 0%, #f7f7f2 48%, #edf4f3 100%);
}

.auth-backdrop {
  position: absolute;
  border-radius: 999px;
  filter: blur(16px);
  opacity: 0.8;
  pointer-events: none;
}

.auth-backdrop-left {
  width: 280px;
  height: 280px;
  top: -56px;
  left: -60px;
  background: rgba(184, 115, 51, 0.24);
}

.auth-backdrop-right {
  width: 360px;
  height: 360px;
  right: -120px;
  bottom: -100px;
  background: rgba(38, 84, 124, 0.18);
}

.auth-card {
  position: relative;
  z-index: 1;
  width: min(1040px, 100%);
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  border-radius: 28px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(98, 74, 46, 0.08);
  box-shadow: 0 30px 80px rgba(73, 54, 34, 0.14);
  backdrop-filter: blur(18px);
}

.auth-showcase {
  padding: 56px;
  color: #1f2933;
  background:
    linear-gradient(160deg, rgba(255, 248, 238, 0.92), rgba(245, 238, 229, 0.78)),
    #fff;
}

.eyebrow,
.panel-kicker {
  margin: 0 0 14px;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: #9a6b3c;
}

.auth-showcase h1 {
  margin: 0;
  font-size: clamp(2.2rem, 4vw, 3.8rem);
  line-height: 1.04;
  letter-spacing: -0.04em;
}

.showcase-copy,
.panel-copy {
  margin: 18px 0 0;
  font-size: 1rem;
  line-height: 1.7;
  color: #52606d;
}

.showcase-points {
  margin: 36px 0 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 14px;
}

.showcase-points li {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.55);
  box-shadow: inset 0 0 0 1px rgba(154, 107, 60, 0.08);
}

.showcase-points li::before {
  content: '';
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
  background: linear-gradient(135deg, #b7791f, #d69e2e);
}

.auth-panel {
  padding: 56px 48px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: rgba(255, 255, 255, 0.78);
}

.panel-header h2 {
  margin: 0;
  font-size: 1.9rem;
  color: #102a43;
}

.field-group {
  display: grid;
  gap: 10px;
  margin-top: 24px;
}

.field-group label {
  font-size: 0.95rem;
  font-weight: 600;
  color: #334e68;
}

.field-group input {
  width: 100%;
  box-sizing: border-box;
  border: 1px solid rgba(16, 42, 67, 0.12);
  border-radius: 16px;
  padding: 15px 16px;
  font-size: 1rem;
  color: #102a43;
  background: rgba(255, 255, 255, 0.92);
  outline: none;
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease,
    transform 0.2s ease;
}

.field-group input::placeholder {
  color: #9aa5b1;
}

.field-group input:focus {
  border-color: rgba(154, 107, 60, 0.52);
  box-shadow: 0 0 0 4px rgba(214, 158, 46, 0.14);
  transform: translateY(-1px);
}

.helper-text {
  margin: 16px 0 0;
  font-size: 0.92rem;
  color: #7b8794;
}

.form-message {
  margin: 18px 0 0;
  padding: 12px 14px;
  border-radius: 14px;
  background: rgba(186, 42, 42, 0.09);
  color: #a61b1b;
  font-size: 0.95rem;
}

.submit-button {
  margin-top: 24px;
  width: 100%;
  border: none;
  border-radius: 16px;
  padding: 15px 18px;
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  color: #fffdf7;
  cursor: pointer;
  background: linear-gradient(135deg, #9a6b3c 0%, #c2843f 55%, #d6a14b 100%);
  box-shadow: 0 18px 30px rgba(154, 107, 60, 0.24);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    opacity 0.2s ease;
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 22px 34px rgba(154, 107, 60, 0.28);
}

.submit-button:disabled {
  cursor: not-allowed;
  opacity: 0.72;
  box-shadow: none;
}

@media (max-width: 900px) {
  .auth-shell {
    padding: 20px;
  }

  .auth-card {
    grid-template-columns: 1fr;
  }

  .auth-showcase,
  .auth-panel {
    padding: 32px 24px;
  }

  .auth-showcase h1 {
    font-size: 2.4rem;
  }
}
</style>
