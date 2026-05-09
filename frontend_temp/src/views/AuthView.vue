<script setup>
import { computed, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { isLoggedIn, login, register } from '../lib/auth'
import { notify } from '../lib/notify'

const route = useRoute()
const router = useRouter()

const mode = ref('login')
const submitting = ref(false)
const loginPasswordVisible = ref(false)
const registerPasswordVisible = ref(false)
const registerConfirmVisible = ref(false)
const formError = ref('')

const loginForm = reactive({
  username: '',
  password: '',
})

const registerForm = reactive({
  username: '',
  email: '',
  nickname: '',
  password: '',
  confirmPassword: '',
})

const redirectTarget = computed(() => {
  const target = route.query.redirect
  return typeof target === 'string' && target.startsWith('/') ? target : '/dashboard'
})

const registerPasswordMismatch = computed(() => {
  if (!registerForm.confirmPassword) {
    return false
  }
  return registerForm.password !== registerForm.confirmPassword
})

const registerButtonDisabled = computed(() => {
  return submitting.value || registerPasswordMismatch.value
})

if (isLoggedIn.value) {
  router.replace(redirectTarget.value)
}

function switchMode(nextMode) {
  mode.value = nextMode
  formError.value = ''
}

function fillDemoAccount(type) {
  switchMode('login')

  if (type === 'admin') {
    loginForm.username = 'admin'
    loginForm.password = 'Admin123456'
    return
  }

  loginForm.username = 'tester01'
  loginForm.password = 'Tester123'
}

function validateLogin() {
  if (!loginForm.username.trim()) {
    return '请输入用户名。'
  }

  if (!loginForm.password.trim()) {
    return '请输入密码。'
  }

  return ''
}

function validateRegister() {
  if (!registerForm.username.trim()) {
    return '请输入用户名。'
  }

  if (!registerForm.email.trim()) {
    return '请输入邮箱地址。'
  }

  if (!registerForm.password.trim()) {
    return '请设置密码。'
  }

  if (!registerForm.confirmPassword.trim()) {
    return '请确认密码。'
  }

  if (registerForm.password !== registerForm.confirmPassword) {
    return '两次输入的密码不一致。'
  }

  return ''
}

async function handleLogin() {
  formError.value = validateLogin()
  if (formError.value) {
    notify(formError.value, 'warning')
    return
  }

  submitting.value = true

  try {
    const response = await login({
      username: loginForm.username.trim(),
      password: loginForm.password,
    })

    notify(response.message || '登录成功。', 'success')
    router.push(redirectTarget.value)
  } catch (error) {
    formError.value = error.message || '登录失败。'
    notify(formError.value, 'danger')
  } finally {
    submitting.value = false
  }
}

async function handleRegister() {
  formError.value = validateRegister()
  if (formError.value) {
    notify(formError.value, 'warning')
    return
  }

  submitting.value = true

  try {
    const response = await register({
      username: registerForm.username.trim(),
      email: registerForm.email.trim(),
      nickname: registerForm.nickname.trim(),
      password: registerForm.password,
    })

    notify(response.message || '注册成功。', 'success')
    router.push('/dashboard')
  } catch (error) {
    formError.value = error.message || '注册失败。'
    notify(formError.value, 'danger')
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <section class="auth-page">
    <div class="auth-page__intro">
      <span class="eyebrow">登录入口</span>
      <h1>为博客平台提供完整的登录与注册流程。</h1>
      <p>
        这个页面已对接后端认证接口：登录、注册、自动保持会话，并可跳回受保护页面。
      </p>

      <div class="auth-highlights">
        <article class="auth-highlight">
          <strong>登录</strong>
          <p>用户名和密码直接对应 `POST /api/v1/auth/login`。</p>
        </article>
        <article class="auth-highlight">
          <strong>注册</strong>
          <p>用户名、邮箱、昵称和密码对应后端注册接口。</p>
        </article>
        <article class="auth-highlight">
          <strong>权限</strong>
          <p>登录后，普通用户和管理员会自动跳转到对应工作区。</p>
        </article>
      </div>

      <div class="auth-demo">
        <div>
          <span class="eyebrow">演示账号</span>
          <h2>一键填充用于测试</h2>
        </div>

        <div class="auth-demo__buttons">
          <button class="button" type="button" @click="fillDemoAccount('admin')">
            填充管理员账号
          </button>
          <button class="button button--ghost" type="button" @click="fillDemoAccount('tester')">
            填充测试用户
          </button>
        </div>

        <div class="auth-demo__list">
          <div class="auth-demo__item">
            <span>管理员</span>
            <strong>admin / Admin123456</strong>
          </div>
          <div class="auth-demo__item">
            <span>测试用户</span>
            <strong>tester01 / Tester123</strong>
          </div>
        </div>
      </div>
    </div>

    <div class="auth-panel">
      <div class="auth-switch">
        <button
          type="button"
          :class="{ active: mode === 'login' }"
          @click="switchMode('login')"
        >
          登录
        </button>
        <button
          type="button"
          :class="{ active: mode === 'register' }"
          @click="switchMode('register')"
        >
          注册
        </button>
      </div>

      <p class="auth-caption">
        {{
          mode === 'login'
            ? '使用已有账号发表评论、发布文章并进入工作台。'
            : '创建新账号后，后端会自动让你登录。'
        }}
      </p>

      <form v-if="mode === 'login'" class="auth-form" @submit.prevent="handleLogin">
        <label class="auth-field">
          <span>用户名</span>
          <input
            v-model="loginForm.username"
            autocomplete="username"
            maxlength="32"
            placeholder="请输入用户名"
            required
          />
        </label>

        <label class="auth-field">
          <span>密码</span>
          <div class="auth-password">
            <input
              v-model="loginForm.password"
              :type="loginPasswordVisible ? 'text' : 'password'"
              autocomplete="current-password"
              maxlength="128"
              placeholder="请输入密码"
              required
            />
            <button
              class="auth-password__toggle"
              type="button"
              @click="loginPasswordVisible = !loginPasswordVisible"
            >
              {{ loginPasswordVisible ? '隐藏' : '显示' }}
            </button>
          </div>
        </label>

        <div v-if="formError" class="auth-error">
          {{ formError }}
        </div>

        <button class="button auth-submit" type="submit" :disabled="submitting">
          {{ submitting ? '登录中...' : '登录并进入工作台' }}
        </button>
      </form>

      <form v-else class="auth-form" @submit.prevent="handleRegister">
        <div class="auth-form__split">
          <label class="auth-field">
            <span>用户名</span>
            <input
              v-model="registerForm.username"
              autocomplete="username"
              maxlength="32"
              placeholder="请输入用户名"
              required
            />
          </label>

          <label class="auth-field">
            <span>昵称</span>
            <input
              v-model="registerForm.nickname"
              autocomplete="nickname"
              maxlength="32"
              placeholder="可选填写昵称"
            />
          </label>
        </div>

        <label class="auth-field">
          <span>邮箱</span>
          <input
            v-model="registerForm.email"
            type="email"
            autocomplete="email"
            placeholder="name@example.com"
            required
          />
        </label>

        <div class="auth-form__split">
          <label class="auth-field">
            <span>密码</span>
            <div class="auth-password">
              <input
                v-model="registerForm.password"
                :type="registerPasswordVisible ? 'text' : 'password'"
                autocomplete="new-password"
                maxlength="128"
                placeholder="至少 6 个字符"
                required
              />
              <button
                class="auth-password__toggle"
                type="button"
                @click="registerPasswordVisible = !registerPasswordVisible"
              >
                {{ registerPasswordVisible ? '隐藏' : '显示' }}
              </button>
            </div>
          </label>

          <label class="auth-field">
            <span>确认密码</span>
            <div class="auth-password">
              <input
                v-model="registerForm.confirmPassword"
                :type="registerConfirmVisible ? 'text' : 'password'"
                autocomplete="new-password"
                maxlength="128"
                placeholder="再次输入密码"
                required
              />
              <button
                class="auth-password__toggle"
                type="button"
                @click="registerConfirmVisible = !registerConfirmVisible"
              >
                {{ registerConfirmVisible ? '隐藏' : '显示' }}
              </button>
            </div>
          </label>
        </div>

        <p class="auth-tip">
          用户名：3-32 个字符。密码：6-128 个字符。昵称可选。
        </p>

        <div v-if="formError" class="auth-error">
          {{ formError }}
        </div>

        <button class="button auth-submit" type="submit" :disabled="registerButtonDisabled">
          {{ submitting ? '注册中...' : '注册并登录' }}
        </button>
      </form>
    </div>
  </section>
</template>
