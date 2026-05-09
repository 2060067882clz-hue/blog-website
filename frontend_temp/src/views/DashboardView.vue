<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

import ArticleCard from '../components/ArticleCard.vue'
import EmptyState from '../components/EmptyState.vue'
import { apiRequest } from '../lib/api'
import { authState, isAdmin, hydrateAuth } from '../lib/auth'
import { sortByDate, formatDate } from '../lib/format'
import { notify } from '../lib/notify'

const route = useRoute()

const loading = ref(true)
const saving = ref(false)
const deletingId = ref(null)
const editingId = ref(null)
const articles = ref([])
const form = ref({
  title: '',
  content: '',
})

const sortedArticles = computed(() => sortByDate(articles.value))
const articleCount = computed(() => articles.value.length)
const draftLabel = computed(() => (editingId.value ? '更新文章' : '发布文章'))
const currentUser = computed(() => authState.user || {})
const displayName = computed(() => currentUser.value.nickname || currentUser.value.username || '')
const avatarInitial = computed(() => (displayName.value || '?').charAt(0).toUpperCase())

function resetForm() {
  editingId.value = null
  form.value = {
    title: '',
    content: '',
  }
}

function startEditing(article) {
  editingId.value = article.id
  form.value = {
    title: article.title,
    content: article.content,
  }
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

async function loadMyArticles() {
  loading.value = true
  try {
    const response = await apiRequest('/articles/me')
    articles.value = response.data

    const queryId = Number(route.query.edit)
    if (queryId) {
      const target = response.data.find((item) => item.id === queryId)
      if (target) {
        startEditing(target)
      }
    }
  } catch (error) {
    notify(error.message || '我的文章加载失败', 'danger')
  } finally {
    loading.value = false
  }
}

async function submitArticle() {
  if (!form.value.title.trim() || !form.value.content.trim()) {
    notify('标题和正文不能为空', 'warning')
    return
  }

  saving.value = true
  try {
    if (editingId.value) {
      const response = await apiRequest(`/articles/${editingId.value}`, {
        method: 'PATCH',
        body: form.value,
      })
      notify(response.message || '文章更新成功', 'success')
    } else {
      const response = await apiRequest('/articles', {
        method: 'POST',
        body: form.value,
      })
      notify(response.message || '文章发布成功', 'success')
    }

    resetForm()
    await loadMyArticles()
  } catch (error) {
    notify(error.message || '文章保存失败', 'danger')
  } finally {
    saving.value = false
  }
}

async function removeArticle(articleId) {
  if (!window.confirm('确认删除这篇文章吗？')) {
    return
  }

  deletingId.value = articleId
  try {
    const response = await apiRequest(`/articles/${articleId}`, { method: 'DELETE' })
    articles.value = articles.value.filter((item) => item.id !== articleId)
    if (editingId.value === articleId) {
      resetForm()
    }
    notify(response.message || '文章已删除', 'success')
  } catch (error) {
    notify(error.message || '文章删除失败', 'danger')
  } finally {
    deletingId.value = null
  }
}

onMounted(async () => {
  await hydrateAuth()
  await loadMyArticles()
})

// change password modal state
const showChangePassword = ref(false)
const changeSaving = ref(false)
const changeForm = ref({
  current_password: '',
  new_password: '',
  confirm_password: '',
})
const changeError = ref('')

function openChangePassword() {
  changeForm.value.current_password = ''
  changeForm.value.new_password = ''
  changeForm.value.confirm_password = ''
  changeError.value = ''
  showChangePassword.value = true
}

function closeChangePassword() {
  showChangePassword.value = false
}

async function submitChangePassword() {
  if (!changeForm.value.current_password) {
    notify('请填写当前密码', 'warning')
    return
  }
  if (!changeForm.value.new_password) {
    changeError.value = '请输入新的密码'
    return
  }
  if (changeForm.value.new_password !== changeForm.value.confirm_password) {
    notify('两次输入的新密码不一致', 'warning')
    return
  }

  changeSaving.value = true
  try {
    // try common endpoint; backend may need adjustment if different
    const resp = await apiRequest('/auth/change-password', {
      method: 'POST',
      body: {
        current_password: changeForm.value.current_password,
        new_password: changeForm.value.new_password,
      },
    })
    notify(resp.message || '密码修改成功，请重新登录', 'success')
    closeChangePassword()
  } catch (err) {
    // Map common failure cases to user-friendly messages shown in modal top-right
    const payload = err?.payload || {}
    let errMsg = '密码修改失败'

    // prefer server-provided message when meaningful
    const serverMsg = payload?.message || payload?.error?.message || err?.message

    // If backend returned 404 (common in some backends for 'not found' current password), treat as current password wrong
    if (err?.status === 404 || String(serverMsg).includes('404')) {
      errMsg = '当前密码错误'
    } else if (serverMsg) {
      const s = String(serverMsg).toLowerCase()
      if (s.includes('current') || s.includes('当前') || s.includes('incorrect') || s.includes('password') || s.includes('密码')) {
        // likely indicates current password incorrect
        errMsg = '当前密码不正确'
      } else {
        errMsg = String(serverMsg)
      }
    } else if (err?.status === 401) {
      errMsg = '当前密码不正确或会话已过期'
    } else if (err?.status === 422 || err?.status === 400) {
      if (payload?.errors) {
        errMsg = Object.values(payload.errors).flat().join('；')
      } else {
        errMsg = payload?.message || '参数校验失败'
      }
    } else if (err?.status >= 500) {
      errMsg = '服务器错误，请稍后重试'
    }

    changeError.value = errMsg
    notify(serverMsg || '密码修改失败', 'danger')
  } finally {
    changeSaving.value = false
  }
}
</script>

<template>
  <section class="dashboard-hero">
    <div class="panel dashboard-profile">
      <span class="eyebrow">创作工作台</span>
      <h1>{{ displayName }} 的创作工作台</h1>
      
      
      <div class="dashboard-profile__actions">
        <RouterLink class="button button--ghost" to="/article/new">
          新建一篇文章
        </RouterLink>
        <RouterLink class="button button--ghost" to="/my-articles">我的文章</RouterLink>
        <RouterLink v-if="isAdmin" class="button" to="/admin">
          进入管理台
        </RouterLink>
      </div>
    </div>

    <aside class="panel profile-sidebar">
      <div class="profile-card">
          <div class="profile-badge">
            <span class="eyebrow">个人中心</span>
            <button class="button button--ghost button--profile-right" @click="openChangePassword">修改密码</button>
          </div>
        <div class="profile-head">
          <div class="avatar">{{ avatarInitial }}</div>
          <div class="identity">
            <span class="identity__name">用户名：{{ displayName }}</span>
            <span class="identity__name">ID：{{ currentUser.id || '--' }}</span>
          </div>
        </div>

        <div class="profile-stats">
          <div class="stat-item">
            <span class="eyebrow">邮箱</span>
            <strong>{{ currentUser.email || '--' }}</strong>
          </div>
          <div class="stat-item">
            <span class="eyebrow">文章数</span>
            <strong>{{ articleCount }}</strong>
          </div>
          <div class="stat-item">
            <span class="eyebrow">账号类型</span>
            <strong>{{ isAdmin ? '管理员' : '普通用户' }}</strong>
          </div>
          <div class="stat-item">
            <span class="eyebrow">注册日期</span>
            <strong>{{ formatDate(currentUser.create_time || currentUser.created_at || currentUser.createdAt || currentUser.registered_at || currentUser.registeredAt || currentUser.created) }}</strong>
          </div>
        </div>

        <div class="profile-actions">
        </div>
      </div>
    </aside>
    <!-- Change Password Modal -->
    <div v-if="showChangePassword" class="modal-backdrop" @click.self="closeChangePassword">
      <div class="modal-box" role="dialog" aria-modal="true">
        <div class="modal-head">
          <h3>修改密码</h3>
        </div>
        <div v-if="changeError" class="modal-error">{{ changeError }}</div>
        <div class="modal-body">
          <div class="field">
            <label>当前密码</label>
            <input type="password" v-model="changeForm.current_password" placeholder="输入当前密码" />
          </div>
          <div class="field">
            <label>新密码</label>
            <input type="password" v-model="changeForm.new_password" placeholder="输入新密码" @input="changeError = ''" />
          </div>
          <div class="field">
            <label>确认新密码</label>
            <input type="password" v-model="changeForm.confirm_password" placeholder="再次输入新密码" @input="changeError = ''" />
          </div>
          <div style="margin-top:16px;text-align:right;">
            <button class="button button--ghost" @click="closeChangePassword">取消</button>
            <button class="button" :disabled="changeSaving" style="margin-left:8px;" @click="submitChangePassword">{{ changeSaving ? '保存中…' : '保存' }}</button>
          </div>
        </div>
      </div>
    </div>
  </section>


  <!-- 已移除底部“我的文章”板块；保留顶部创作工作台信息 -->
</template>
