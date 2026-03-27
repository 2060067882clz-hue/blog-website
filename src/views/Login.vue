<template>
  <section class="auth-shell">
    <div class="ambient ambient-one"></div>
    <div class="ambient ambient-two"></div>
    <div class="ambient ambient-grid"></div>
    <div class="ambient ambient-rings"></div>

    <div class="auth-frame">
      <aside class="auth-showcase">
        <p class="eyebrow">Blog Space</p>
        <h1>进入你的博客空间</h1>
        <p class="showcase-copy">
          登录后继续浏览文章、查看个人信息，或注册一个新账号开始使用。
        </p>

        <div class="showcase-stack">
          <article class="metric-card glass-card">
            <span>{{ mode === 'login' ? '登录' : '注册' }}</span>
            <strong>{{ mode === 'login' ? '欢迎回来' : '创建账号' }}</strong>
            <small>简洁、安静、专注阅读</small>
          </article>

          <article class="signal-card glass-card">
            <div class="signal-orb"></div>
            <p>在这里进入博客，继续阅读、收藏和浏览你的内容。</p>
          </article>
        </div>

        <ul class="showcase-points">
          <li>简洁清晰的登录与注册入口</li>
          <li>稳定顺滑的表单切换体验</li>
          <li>更适合博客场景的克制表达</li>
        </ul>
      </aside>

      <div class="auth-panel glass-panel">
        <div class="mode-switch" :class="{ register: mode === 'register' }">
          <span class="mode-pill" aria-hidden="true"></span>
          <button
            type="button"
            class="mode-button"
            :class="{ active: mode === 'login' }"
            @click="switchMode('login')"
          >
            登录
          </button>
          <button
            type="button"
            class="mode-button"
            :class="{ active: mode === 'register' }"
            @click="switchMode('register')"
          >
            注册
          </button>
        </div>

        <div class="panel-header">
          <p class="panel-kicker">{{ mode === 'login' ? 'Sign In' : 'Sign Up' }}</p>
          <h2>{{ mode === 'login' ? '欢迎回来' : '注册账号' }}</h2>
          <p class="panel-copy">
            {{ mode === 'login'
              ? '输入账号和密码，继续浏览博客内容。'
              : '创建账号后即可进入博客个人页面。' }}
          </p>
        </div>

        <div class="forms-stage">
          <form
            class="auth-form-pane"
            :class="{ active: mode === 'login', inactive: mode !== 'login' }"
            @submit.prevent="submitAuth"
          >
            <div class="field-group">
              <label for="login-account">账号</label>
              <input
                id="login-account"
                v-model.trim="username"
                type="text"
                placeholder="请输入账号"
                autocomplete="username"
              />
            </div>

            <div class="field-group">
              <label for="login-password">密码</label>
              <input
                id="login-password"
                v-model.trim="password"
                type="password"
                placeholder="请输入密码"
                autocomplete="current-password"
              />
            </div>

            <div class="field-slot ghost-slot"></div>
            <div class="field-slot ghost-slot"></div>
          </form>

          <form
            class="auth-form-pane"
            :class="{ active: mode === 'register', inactive: mode !== 'register' }"
            @submit.prevent="submitAuth"
          >
            <div class="field-group">
              <label for="register-nickname">昵称</label>
              <input
                id="register-nickname"
                v-model.trim="displayName"
                type="text"
                placeholder="请输入昵称"
                autocomplete="nickname"
              />
            </div>

            <div class="field-group">
              <label for="register-account">账号</label>
              <input
                id="register-account"
                v-model.trim="username"
                type="text"
                placeholder="请输入账号"
                autocomplete="username"
              />
            </div>

            <div class="field-group">
              <label for="register-password">密码</label>
              <input
                id="register-password"
                v-model.trim="password"
                type="password"
                placeholder="请输入密码"
                autocomplete="new-password"
              />
            </div>

            <div class="field-group">
              <label for="confirm-password">确认密码</label>
              <input
                id="confirm-password"
                v-model.trim="confirmPassword"
                type="password"
                placeholder="请再次输入密码"
                autocomplete="new-password"
              />
            </div>
          </form>
        </div>

        <div class="panel-meta">
          <p class="helper-text">
            {{ mode === 'login' ? '演示账号：admin / Admin123456' : '注册账号至少 3 位，密码至少 6 位' }}
          </p>
          <span class="status-chip" :class="{ pending: loading }">
            {{ loading ? 'Processing' : 'Ready' }}
          </span>
        </div>

        <div class="message-stage">
          <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
          <p v-else-if="errorMessage" class="form-message">{{ errorMessage }}</p>
        </div>

        <button class="submit-button" @click="submitAuth" :disabled="loading">
          <span>
            {{
              loading
                ? mode === 'login'
                  ? '登录中...'
                  : '注册中...'
                : mode === 'login'
                  ? '进入博客'
                  : '创建账号并进入'
            }}
          </span>
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { loginRequest, registerRequest, saveAuth } from '../services/auth'

const router = useRouter()

const mode = ref('login')
const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const displayName = ref('')
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const resetMessages = () => {
  errorMessage.value = ''
  successMessage.value = ''
}

const switchMode = (nextMode) => {
  mode.value = nextMode
  resetMessages()
}

const validateLogin = () => {
  if (!username.value || !password.value) {
    errorMessage.value = '请输入账号和密码'
    return false
  }

  return true
}

const validateRegister = () => {
  if (!displayName.value || !username.value || !password.value || !confirmPassword.value) {
    errorMessage.value = '请完整填写注册信息'
    return false
  }

  if (displayName.value.length < 2) {
    errorMessage.value = '昵称至少需要 2 个字符'
    return false
  }

  if (username.value.length < 3) {
    errorMessage.value = '账号至少需要 3 个字符'
    return false
  }

  if (password.value.length < 6) {
    errorMessage.value = '密码至少需要 6 个字符'
    return false
  }

  if (password.value !== confirmPassword.value) {
    errorMessage.value = '两次输入的密码不一致'
    return false
  }

  return true
}

const submitAuth = async () => {
  resetMessages()

  const isValid = mode.value === 'login' ? validateLogin() : validateRegister()

  if (!isValid) {
    return
  }

  loading.value = true

  try {
    const data =
      mode.value === 'login'
        ? await loginRequest({
            username: username.value,
            password: password.value,
          })
        : await registerRequest({
            username: username.value,
            password: password.value,
            display_name: displayName.value,
          })

    saveAuth(data)
    successMessage.value = mode.value === 'login' ? '登录成功，正在进入个人中心' : '注册成功，正在进入个人中心'
    router.push('/profile')
  } catch (error) {
    errorMessage.value =
      error.message || (mode.value === 'login' ? '登录失败，请稍后重试' : '注册失败，请稍后重试')
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
  padding: 28px;
  display: grid;
  place-items: center;
  background:
    radial-gradient(circle at 14% 18%, rgba(255, 178, 36, 0.18), transparent 24%),
    radial-gradient(circle at 82% 20%, rgba(70, 230, 255, 0.14), transparent 24%),
    linear-gradient(135deg, #08111f 0%, #12233a 48%, #1f2e45 100%);
}

.ambient {
  position: absolute;
  pointer-events: none;
}

.ambient-one,
.ambient-two {
  border-radius: 999px;
  filter: blur(54px);
  opacity: 0.55;
}

.ambient-one {
  width: 320px;
  height: 320px;
  top: -82px;
  left: -44px;
  background: rgba(251, 191, 36, 0.28);
}

.ambient-two {
  width: 420px;
  height: 420px;
  right: -120px;
  bottom: -150px;
  background: rgba(34, 211, 238, 0.22);
}

.ambient-grid {
  inset: 0;
  background-image:
    linear-gradient(rgba(148, 163, 184, 0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(148, 163, 184, 0.08) 1px, transparent 1px);
  background-size: 42px 42px;
  mask-image: radial-gradient(circle at center, black 36%, transparent 86%);
  opacity: 0.28;
}

.ambient-rings {
  inset: auto auto 12% 8%;
  width: 260px;
  height: 260px;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow:
    0 0 0 28px rgba(255, 255, 255, 0.03),
    0 0 0 56px rgba(255, 255, 255, 0.02);
  opacity: 0.5;
}

.auth-frame {
  position: relative;
  z-index: 1;
  width: min(1180px, 100%);
  display: grid;
  grid-template-columns: 1.14fr 0.92fr;
  border-radius: 34px;
  overflow: hidden;
  background: rgba(8, 14, 28, 0.56);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow:
    0 36px 120px rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(24px) saturate(132%);
}

.auth-showcase {
  position: relative;
  padding: 64px 58px;
  color: #e7eff8;
  background:
    radial-gradient(circle at top left, rgba(250, 204, 21, 0.14), transparent 30%),
    linear-gradient(160deg, rgba(255, 255, 255, 0.055), rgba(255, 255, 255, 0.018));
}

.eyebrow,
.panel-kicker {
  margin: 0 0 14px;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.24em;
  text-transform: uppercase;
}

.eyebrow {
  color: #fbbf24;
}

.auth-showcase h1 {
  margin: 0;
  max-width: 8ch;
  font-size: clamp(2.8rem, 4.6vw, 4.9rem);
  line-height: 0.95;
  letter-spacing: -0.06em;
}

.showcase-copy {
  margin: 24px 0 0;
  max-width: 30rem;
  font-size: 1.02rem;
  line-height: 1.82;
  color: rgba(226, 232, 240, 0.76);
}

.showcase-stack {
  margin-top: 34px;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 210px;
  gap: 18px;
}

.glass-card,
.glass-panel,
.showcase-points li {
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.08),
    0 20px 44px rgba(0, 0, 0, 0.12);
}

.metric-card,
.signal-card,
.showcase-points li {
  border-radius: 24px;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.03));
  backdrop-filter: blur(22px) saturate(130%);
}

.metric-card {
  padding: 22px 24px;
  display: grid;
  gap: 8px;
}

.metric-card span,
.signal-card p,
.showcase-points li {
  color: rgba(226, 232, 240, 0.76);
}

.metric-card strong {
  font-size: 1.5rem;
  color: #f8fafc;
}

.metric-card small {
  color: rgba(148, 163, 184, 0.92);
}

.signal-card {
  position: relative;
  overflow: hidden;
  padding: 22px 20px;
  display: grid;
  align-content: end;
}

.signal-orb {
  position: absolute;
  top: 16px;
  right: 14px;
  width: 88px;
  height: 88px;
  border-radius: 50%;
  background:
    radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.88), rgba(255, 255, 255, 0.08) 42%, transparent 62%),
    linear-gradient(135deg, rgba(251, 191, 36, 0.58), rgba(34, 211, 238, 0.48));
  filter: blur(2px);
  opacity: 0.9;
}

.signal-card p {
  position: relative;
  z-index: 1;
  margin: 0;
  line-height: 1.75;
  font-size: 0.94rem;
}

.showcase-points {
  margin: 22px 0 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 14px;
}

.showcase-points li {
  padding: 16px 18px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.showcase-points li::before {
  content: '';
  width: 11px;
  height: 11px;
  border-radius: 50%;
  flex-shrink: 0;
  background: linear-gradient(135deg, #fbbf24, #22d3ee);
  box-shadow: 0 0 18px rgba(34, 211, 238, 0.55);
}

.auth-panel {
  padding: 42px 48px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.76), rgba(255, 255, 255, 0.58));
  backdrop-filter: blur(26px) saturate(150%);
}

.mode-switch {
  position: relative;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
  padding: 6px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.34);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.9),
    0 16px 32px rgba(15, 23, 42, 0.08);
  backdrop-filter: blur(20px);
}

.mode-pill {
  position: absolute;
  top: 6px;
  left: 6px;
  width: calc(50% - 10px);
  height: calc(100% - 12px);
  border-radius: 15px;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.66));
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.98),
    0 12px 24px rgba(148, 163, 184, 0.18);
  transform: translateX(0);
  transition:
    transform 0.46s cubic-bezier(0.22, 1, 0.36, 1),
    box-shadow 0.3s ease;
}

.mode-switch.register .mode-pill {
  transform: translateX(calc(100% + 8px));
}

.mode-button {
  position: relative;
  z-index: 1;
  border: none;
  border-radius: 15px;
  padding: 12px 14px;
  font-size: 0.95rem;
  font-weight: 700;
  color: #475569;
  background: transparent;
  cursor: pointer;
  transition:
    transform 0.22s ease,
    color 0.3s ease;
}

.mode-button.active {
  color: #0f172a;
}

.mode-button:not(.active) {
  color: #64748b;
}

.panel-header {
  margin-top: 28px;
}

.panel-kicker {
  color: #b45309;
}

.panel-header h2 {
  margin: 0;
  font-size: 2.1rem;
  color: #0f172a;
  letter-spacing: -0.04em;
}

.panel-copy {
  margin: 14px 0 0;
  color: #64748b;
  line-height: 1.75;
}

.forms-stage {
  position: relative;
  margin-top: 24px;
  min-height: 360px;
}

.auth-form-pane {
  position: absolute;
  inset: 0;
  display: grid;
  align-content: start;
  gap: 16px;
  transition:
    opacity 0.34s ease,
    transform 0.34s ease,
    filter 0.34s ease;
}

.auth-form-pane.active {
  opacity: 1;
  transform: translateX(0) scale(1);
  filter: blur(0);
  pointer-events: auto;
}

.auth-form-pane.inactive {
  opacity: 0;
  transform: translateX(18px) scale(0.985);
  filter: blur(8px);
  pointer-events: none;
}

.field-group,
.field-slot {
  min-height: 76px;
}

.field-group {
  display: grid;
  gap: 10px;
}

.field-group label {
  font-size: 0.95rem;
  font-weight: 600;
  color: #334155;
}

.field-group input {
  width: 100%;
  height: 56px;
  box-sizing: border-box;
  border: 1px solid rgba(255, 255, 255, 0.48);
  border-radius: 18px;
  padding: 0 18px;
  font-size: 1rem;
  color: #0f172a;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.74), rgba(255, 255, 255, 0.5));
  outline: none;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.96),
    0 12px 28px rgba(148, 163, 184, 0.12);
  backdrop-filter: blur(22px);
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease,
    transform 0.2s ease,
    background 0.2s ease;
}

.field-group input::placeholder {
  color: #94a3b8;
}

.field-group input:focus {
  transform: translateY(-1px);
  border-color: rgba(255, 255, 255, 0.78);
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.86), rgba(255, 255, 255, 0.6));
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 1),
    0 0 0 4px rgba(255, 255, 255, 0.22),
    0 14px 32px rgba(14, 165, 233, 0.12);
}

.ghost-slot {
  border-radius: 18px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.03));
  border: 1px solid rgba(255, 255, 255, 0.1);
  opacity: 0.35;
}

.panel-meta {
  margin-top: 4px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.helper-text {
  margin: 0;
  font-size: 0.92rem;
  color: #64748b;
}

.status-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 12px;
  border-radius: 999px;
  font-size: 0.82rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #0f766e;
  background: rgba(20, 184, 166, 0.12);
}

.status-chip::before {
  content: '';
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: currentColor;
}

.status-chip.pending {
  color: #b45309;
  background: rgba(245, 158, 11, 0.14);
}

.message-stage {
  min-height: 54px;
  margin-top: 16px;
}

.success-message,
.form-message {
  margin: 0;
  padding: 13px 15px;
  border-radius: 16px;
  font-size: 0.95rem;
  backdrop-filter: blur(18px);
}

.success-message {
  background: rgba(16, 185, 129, 0.12);
  color: #047857;
}

.form-message {
  background: rgba(239, 68, 68, 0.1);
  color: #b91c1c;
}

.submit-button {
  position: relative;
  width: 100%;
  border: none;
  border-radius: 20px;
  padding: 16px 20px;
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.03em;
  color: #fff;
  cursor: pointer;
  overflow: hidden;
  background: linear-gradient(135deg, #f59e0b 0%, #ea580c 45%, #0891b2 100%);
  box-shadow:
    0 24px 44px rgba(14, 116, 144, 0.24),
    inset 0 1px 0 rgba(255, 255, 255, 0.22);
  transition:
    transform 0.22s ease,
    box-shadow 0.22s ease,
    opacity 0.22s ease;
}

.submit-button::before {
  content: '';
  position: absolute;
  inset: 1px;
  border-radius: inherit;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.22), transparent 38%);
}

.submit-button span {
  position: relative;
  z-index: 1;
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-2px) scale(1.01);
  box-shadow:
    0 28px 54px rgba(14, 116, 144, 0.28),
    inset 0 1px 0 rgba(255, 255, 255, 0.22);
}

.submit-button:disabled {
  cursor: not-allowed;
  opacity: 0.76;
  box-shadow: none;
}

@media (max-width: 960px) {
  .auth-shell {
    padding: 20px;
  }

  .auth-frame {
    grid-template-columns: 1fr;
  }

  .auth-showcase,
  .auth-panel {
    padding: 34px 24px;
  }

  .showcase-stack {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .auth-showcase h1 {
    max-width: none;
    font-size: 2.6rem;
  }

  .forms-stage {
    min-height: 392px;
  }

  .panel-meta {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
