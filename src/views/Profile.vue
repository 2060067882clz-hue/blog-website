<template>
  <section class="profile-shell">
    <div class="profile-card">
      <p class="profile-kicker">Personal Center</p>
      <h1 v-if="loading">正在读取你的信息...</h1>
      <h1 v-else>你好，{{ displayName }}</h1>
      <p class="profile-copy">
        已经成功连接到后端认证服务。这里展示的是 `/auth/me` 返回的当前用户信息。
      </p>

      <p v-if="errorMessage" class="profile-error">{{ errorMessage }}</p>

      <div v-if="user" class="profile-stats">
        <article>
          <span>登录状态</span>
          <strong>已连接</strong>
        </article>
        <article>
          <span>当前账号</span>
          <strong>{{ user.username }}</strong>
        </article>
        <article>
          <span>昵称</span>
          <strong>{{ user.display_name }}</strong>
        </article>
        <article>
          <span>角色</span>
          <strong>{{ user.role }}</strong>
        </article>
      </div>

      <button class="logout-button" @click="logout" :disabled="submitting">
        {{ submitting ? '退出中...' : '退出登录' }}
      </button>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import { clearAuth, getCurrentUser, getStoredUser, logoutRequest, saveUser } from '../services/auth'

const router = useRouter()
const user = ref(getStoredUser())
const loading = ref(true)
const submitting = ref(false)
const errorMessage = ref('')

const displayName = computed(() => user.value?.display_name || '用户')

const loadProfile = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    const data = await getCurrentUser()
    user.value = data.user
    saveUser(data.user)
  } catch (error) {
    errorMessage.value = error.message || '获取用户信息失败'
    clearAuth()
    router.push('/login')
  } finally {
    loading.value = false
  }
}

const logout = async () => {
  submitting.value = true

  try {
    await logoutRequest()
  } catch (error) {
    console.error(error)
  } finally {
    clearAuth()
    submitting.value = false
    router.push('/login')
  }
}

onMounted(loadProfile)
</script>

<style scoped>
.profile-shell {
  min-height: 100vh;
  padding: 32px;
  display: grid;
  place-items: center;
  background:
    radial-gradient(circle at top right, rgba(214, 161, 75, 0.24), transparent 22%),
    linear-gradient(145deg, #f5efe6 0%, #eef4f2 100%);
}

.profile-card {
  width: min(680px, 100%);
  padding: 48px;
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(98, 74, 46, 0.08);
  box-shadow: 0 30px 70px rgba(73, 54, 34, 0.12);
  backdrop-filter: blur(14px);
}

.profile-kicker {
  margin: 0 0 14px;
  color: #9a6b3c;
  font-size: 0.8rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  font-weight: 700;
}

.profile-card h1 {
  margin: 0;
  font-size: clamp(2.2rem, 5vw, 3.4rem);
  line-height: 1.05;
  color: #102a43;
}

.profile-copy {
  margin: 18px 0 0;
  color: #52606d;
  line-height: 1.8;
  font-size: 1rem;
}

.profile-error {
  margin: 18px 0 0;
  padding: 12px 14px;
  border-radius: 14px;
  background: rgba(186, 42, 42, 0.09);
  color: #a61b1b;
}

.profile-stats {
  margin-top: 32px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.profile-stats article {
  padding: 20px;
  border-radius: 18px;
  background: rgba(247, 241, 232, 0.72);
  box-shadow: inset 0 0 0 1px rgba(154, 107, 60, 0.08);
}

.profile-stats span {
  display: block;
  margin-bottom: 10px;
  font-size: 0.92rem;
  color: #7b8794;
}

.profile-stats strong {
  font-size: 1.1rem;
  color: #243b53;
}

.logout-button {
  margin-top: 32px;
  border: none;
  border-radius: 16px;
  padding: 15px 24px;
  font-size: 1rem;
  font-weight: 700;
  color: #fffdf8;
  cursor: pointer;
  background: linear-gradient(135deg, #b1412f 0%, #cf5e3d 100%);
  box-shadow: 0 18px 28px rgba(177, 65, 47, 0.24);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    opacity 0.2s ease;
}

.logout-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 22px 30px rgba(177, 65, 47, 0.28);
}

.logout-button:disabled {
  opacity: 0.75;
  cursor: not-allowed;
  box-shadow: none;
}

@media (max-width: 720px) {
  .profile-shell {
    padding: 20px;
  }

  .profile-card {
    padding: 32px 24px;
  }

  .profile-stats {
    grid-template-columns: 1fr;
  }
}
</style>
