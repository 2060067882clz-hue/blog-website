<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

import EmptyState from '../components/EmptyState.vue'
import { apiRequest } from '../lib/api'
import { authState } from '../lib/auth'
import { formatDate, sortByDate } from '../lib/format'
import { notify } from '../lib/notify'

const loading = ref(true)
const users = ref([])
const articles = ref([])
const busyKey = ref('')

const sortedUsers = computed(() => sortByDate(users.value, 'create_time'))
const sortedArticles = computed(() => sortByDate(articles.value))

async function loadAdminData() {
  loading.value = true
  try {
    const [userResponse, articleResponse] = await Promise.all([
      apiRequest('/admin/users'),
      apiRequest('/admin/articles'),
    ])

    users.value = userResponse.data
    articles.value = articleResponse.data
  } catch (error) {
    notify(error.message || '管理数据加载失败', 'danger')
  } finally {
    loading.value = false
  }
}

async function removeUser(userId) {
  if (!window.confirm('确认删除该用户吗？该用户的文章和评论也会被一起清理。')) {
    return
  }

  busyKey.value = `user-${userId}`
  try {
    const response = await apiRequest(`/admin/users/${userId}`, { method: 'DELETE' })
    users.value = users.value.filter((item) => item.id !== userId)
    articles.value = articles.value.filter((item) => item.author.id !== userId)
    notify(response.message || '用户已删除', 'success')
  } catch (error) {
    notify(error.message || '用户删除失败', 'danger')
  } finally {
    busyKey.value = ''
  }
}

async function removeArticle(articleId) {
  if (!window.confirm('确认以管理员身份删除这篇文章吗？')) {
    return
  }

  busyKey.value = `article-${articleId}`
  try {
    const response = await apiRequest(`/admin/articles/${articleId}`, { method: 'DELETE' })
    articles.value = articles.value.filter((item) => item.id !== articleId)
    notify(response.message || '文章已删除', 'success')
  } catch (error) {
    notify(error.message || '文章删除失败', 'danger')
  } finally {
    busyKey.value = ''
  }
}

onMounted(loadAdminData)
</script>

<template>
  <section class="admin-hero">
    <div class="panel">
      <span class="eyebrow">Admin Console</span>
      <h1>全站巡检与内容治理</h1>
      <p>
        管理页面只使用后端已经实现的 4 个管理员接口：查看用户、查看文章、删除用户、删除文章。
      </p>
      <div class="badge-row">
        <span class="badge">用户 {{ users.length }}</span>
        <span class="badge">文章 {{ articles.length }}</span>
        <span class="badge">当前管理员 {{ authState.user.username }}</span>
      </div>
    </div>
  </section>

  <section v-if="loading" class="panel panel--soft">正在加载管理台数据...</section>

  <template v-else>
    <section class="section-head">
      <div>
        <span class="eyebrow">Users</span>
        <h2>用户列表</h2>
      </div>
    </section>

    <div v-if="sortedUsers.length" class="admin-list">
      <article v-for="user in sortedUsers" :key="user.id" class="admin-card">
        <div>
          <h3>{{ user.nickname || user.username }}</h3>
          <p>{{ user.email }}</p>
        </div>
        <div class="admin-card__meta">
          <span>{{ user.role === 1 ? '管理员' : '普通用户' }}</span>
          <span>{{ formatDate(user.create_time) }}</span>
        </div>
        <button
          class="button button--danger"
          type="button"
          :disabled="busyKey === `user-${user.id}` || user.id === authState.user.id"
          @click="removeUser(user.id)"
        >
          {{
            user.id === authState.user.id
              ? '不能删除自己'
              : busyKey === `user-${user.id}`
                ? '删除中...'
                : '删除用户'
          }}
        </button>
      </article>
    </div>

    <EmptyState
      v-else
      title="暂无用户数据"
      description="如果后端还没有初始化演示数据，这里会暂时为空。"
    />

    <section class="section-head">
      <div>
        <span class="eyebrow">Articles</span>
        <h2>全站文章</h2>
      </div>
    </section>

    <div v-if="sortedArticles.length" class="admin-list">
      <article v-for="article in sortedArticles" :key="article.id" class="admin-card">
        <div>
          <h3>{{ article.title }}</h3>
          <p>作者：{{ article.author.nickname || article.author.username }}</p>
        </div>
        <div class="admin-card__meta">
          <span>{{ formatDate(article.update_time) }}</span>
          <RouterLink class="button button--plain" :to="`/article/${article.id}`">
            查看详情
          </RouterLink>
        </div>
        <button
          class="button button--danger"
          type="button"
          :disabled="busyKey === `article-${article.id}`"
          @click="removeArticle(article.id)"
        >
          {{ busyKey === `article-${article.id}` ? '删除中...' : '删除文章' }}
        </button>
      </article>
    </div>

    <EmptyState
      v-else
      title="暂无文章数据"
      description="当站内还没有内容时，这里会自动显示空状态。"
    />
  </template>
</template>
