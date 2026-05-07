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
    return 'Please enter your username.'
  }

  if (!loginForm.password.trim()) {
    return 'Please enter your password.'
  }

  return ''
}

function validateRegister() {
  if (!registerForm.username.trim()) {
    return 'Please enter a username.'
  }

  if (!registerForm.email.trim()) {
    return 'Please enter an email address.'
  }

  if (!registerForm.password.trim()) {
    return 'Please create a password.'
  }

  if (!registerForm.confirmPassword.trim()) {
    return 'Please confirm your password.'
  }

  if (registerForm.password !== registerForm.confirmPassword) {
    return 'The two passwords do not match.'
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

    notify(response.message || 'Login successful.', 'success')
    router.push(redirectTarget.value)
  } catch (error) {
    formError.value = error.message || 'Login failed.'
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

    notify(response.message || 'Registration successful.', 'success')
    router.push('/dashboard')
  } catch (error) {
    formError.value = error.message || 'Registration failed.'
    notify(formError.value, 'danger')
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <section class="auth-page">
    <div class="auth-page__intro">
      <span class="eyebrow">Access Portal</span>
      <h1>Complete sign in and sign up flow for the blog platform.</h1>
      <p>
        This screen is now aligned with the backend auth API: login, register,
        automatic session persistence, and redirect back to protected pages.
      </p>

      <div class="auth-highlights">
        <article class="auth-highlight">
          <strong>Login</strong>
          <p>Username and password map directly to `POST /api/v1/auth/login`.</p>
        </article>
        <article class="auth-highlight">
          <strong>Register</strong>
          <p>Username, email, nickname, and password map to the backend register API.</p>
        </article>
        <article class="auth-highlight">
          <strong>Roles</strong>
          <p>After login, regular users and admins are redirected to the right workspace.</p>
        </article>
      </div>

      <div class="auth-demo">
        <div>
          <span class="eyebrow">Demo Account</span>
          <h2>Quick fill for testing</h2>
        </div>

        <div class="auth-demo__buttons">
          <button class="button" type="button" @click="fillDemoAccount('admin')">
            Fill Admin Account
          </button>
          <button class="button button--ghost" type="button" @click="fillDemoAccount('tester')">
            Fill Test User
          </button>
        </div>

        <div class="auth-demo__list">
          <div class="auth-demo__item">
            <span>Admin</span>
            <strong>admin / Admin123456</strong>
          </div>
          <div class="auth-demo__item">
            <span>Test User</span>
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
          Sign In
        </button>
        <button
          type="button"
          :class="{ active: mode === 'register' }"
          @click="switchMode('register')"
        >
          Create Account
        </button>
      </div>

      <p class="auth-caption">
        {{
          mode === 'login'
            ? 'Use an existing account to comment, publish articles, and access your dashboard.'
            : 'Create a new account and the backend will automatically sign you in after registration.'
        }}
      </p>

      <form v-if="mode === 'login'" class="auth-form" @submit.prevent="handleLogin">
        <label class="auth-field">
          <span>Username</span>
          <input
            v-model="loginForm.username"
            autocomplete="username"
            maxlength="32"
            placeholder="Enter your username"
            required
          />
        </label>

        <label class="auth-field">
          <span>Password</span>
          <div class="auth-password">
            <input
              v-model="loginForm.password"
              :type="loginPasswordVisible ? 'text' : 'password'"
              autocomplete="current-password"
              maxlength="128"
              placeholder="Enter your password"
              required
            />
            <button
              class="auth-password__toggle"
              type="button"
              @click="loginPasswordVisible = !loginPasswordVisible"
            >
              {{ loginPasswordVisible ? 'Hide' : 'Show' }}
            </button>
          </div>
        </label>

        <div v-if="formError" class="auth-error">
          {{ formError }}
        </div>

        <button class="button auth-submit" type="submit" :disabled="submitting">
          {{ submitting ? 'Signing In...' : 'Sign In to Dashboard' }}
        </button>
      </form>

      <form v-else class="auth-form" @submit.prevent="handleRegister">
        <div class="auth-form__split">
          <label class="auth-field">
            <span>Username</span>
            <input
              v-model="registerForm.username"
              autocomplete="username"
              maxlength="32"
              placeholder="Choose a username"
              required
            />
          </label>

          <label class="auth-field">
            <span>Nickname</span>
            <input
              v-model="registerForm.nickname"
              autocomplete="nickname"
              maxlength="32"
              placeholder="Optional display name"
            />
          </label>
        </div>

        <label class="auth-field">
          <span>Email</span>
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
            <span>Password</span>
            <div class="auth-password">
              <input
                v-model="registerForm.password"
                :type="registerPasswordVisible ? 'text' : 'password'"
                autocomplete="new-password"
                maxlength="128"
                placeholder="At least 6 characters"
                required
              />
              <button
                class="auth-password__toggle"
                type="button"
                @click="registerPasswordVisible = !registerPasswordVisible"
              >
                {{ registerPasswordVisible ? 'Hide' : 'Show' }}
              </button>
            </div>
          </label>

          <label class="auth-field">
            <span>Confirm Password</span>
            <div class="auth-password">
              <input
                v-model="registerForm.confirmPassword"
                :type="registerConfirmVisible ? 'text' : 'password'"
                autocomplete="new-password"
                maxlength="128"
                placeholder="Repeat the password"
                required
              />
              <button
                class="auth-password__toggle"
                type="button"
                @click="registerConfirmVisible = !registerConfirmVisible"
              >
                {{ registerConfirmVisible ? 'Hide' : 'Show' }}
              </button>
            </div>
          </label>
        </div>

        <p class="auth-tip">
          Username: 3-32 chars. Password: 6-128 chars. Nickname is optional.
        </p>

        <div v-if="formError" class="auth-error">
          {{ formError }}
        </div>

        <button class="button auth-submit" type="submit" :disabled="registerButtonDisabled">
          {{ submitting ? 'Creating Account...' : 'Register and Sign In' }}
        </button>
      </form>
    </div>
  </section>
</template>
