<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'

import { authState, isAdmin, isLoggedIn, logout } from '../lib/auth'
import { notify } from '../lib/notify'

const route = useRoute()
const router = useRouter()

const primaryAction = computed(() => {
  if (isLoggedIn.value) {
    return { to: '/dashboard', label: '进入工作台' }
  }
  return { to: '/auth', label: '登录 / 注册' }
})

async function handleLogout() {
  try {
    await logout()
    notify('已退出登录', 'success')
    if (route.meta.requiresAuth) {
      router.push('/')
    }
  } catch (error) {
    notify(error.message || '退出登录失败', 'danger')
  }
}
</script>

<template>
  <div class="shell">
    <div class="shell__orb shell__orb--one" />
    <div class="shell__orb shell__orb--two" />
    <div class="shell__grid" />

    <header class="topbar">
      <RouterLink class="brand" to="/">
        <span class="brand__mark">B</span>
        <div>
          <strong>Blog Atelier</strong>
          <span>为现有后端量身定制的前端工作台</span>
        </div>
      </RouterLink>

      <nav class="topbar__nav">
        <RouterLink to="/" class="button button--ghost">首页</RouterLink>
        <RouterLink v-if="isAdmin" to="/admin">管理台</RouterLink>
        <RouterLink :to="primaryAction.to" class="button button--ghost">
          {{ primaryAction.label }}
        </RouterLink>
      </nav>

      <div class="topbar__user">
        <template v-if="isLoggedIn">
          <div class="identity">
            <span class="identity__name">
              {{ authState.user.nickname || authState.user.username }}
            </span>
            <span class="identity__meta">
              {{ isAdmin ? '管理员' : '创作者' }}
            </span>
          </div>
          <button class="button button--plain" type="button" @click="handleLogout">
            退出
          </button>
        </template>
      </div>
    </header>

    <main class="page-wrap">
      <slot />
    </main>
  </div>
</template>
