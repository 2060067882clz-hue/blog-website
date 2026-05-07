<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

import ArticleCard from '../components/ArticleCard.vue'
import EmptyState from '../components/EmptyState.vue'
import { apiRequest } from '../lib/api'
import { authState, isAdmin } from '../lib/auth'
import { formatDate, sortByDate } from '../lib/format'
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

onMounted(loadMyArticles)
</script>

<template>
  <section class="dashboard-hero">
    <div class="panel dashboard-profile">
      <span class="eyebrow">Workspace</span>
      <h1>{{ authState.user.nickname || authState.user.username }} 的创作工作台</h1>
      <p>
        使用后端现有的发文、改文、删文和“我的文章”接口，整理成一个更适合日常操作的内容后台。
      </p>
      <div class="dashboard-profile__meta">
        <span>角色：{{ isAdmin ? '管理员' : '普通用户' }}</span>
        <span>邮箱：{{ authState.user.email }}</span>
        <span>注册时间：{{ formatDate(authState.user.create_time) }}</span>
      </div>
      <div class="dashboard-profile__actions">
        <button class="button button--ghost" type="button" @click="resetForm">
          新建一篇文章
        </button>
        <RouterLink v-if="isAdmin" class="button" to="/admin">
          进入管理台
        </RouterLink>
      </div>
    </div>

    <form class="panel editor-panel" @submit.prevent="submitArticle">
      <div class="section-head section-head--compact">
        <div>
          <span class="eyebrow">Editor</span>
          <h2>{{ editingId ? '编辑文章' : '发布新文章' }}</h2>
        </div>
        <button
          v-if="editingId"
          class="button button--plain"
          type="button"
          @click="resetForm"
        >
          取消编辑
        </button>
      </div>

      <label class="field">
        <span>标题</span>
        <input
          v-model="form.title"
          maxlength="120"
          placeholder="写一个清晰、有辨识度的标题"
        />
      </label>

      <label class="field">
        <span>正文</span>
        <textarea
          v-model="form.content"
          rows="12"
          placeholder="这里直接对应后端文章正文 content 字段"
        />
      </label>

      <div class="editor-panel__footer">
        <span>{{ form.content.length }} 字</span>
        <button class="button" type="submit" :disabled="saving">
          {{ saving ? '保存中...' : draftLabel }}
        </button>
      </div>
    </form>
  </section>

  <section class="section-head">
    <div>
      <span class="eyebrow">My Articles</span>
      <h2>我的文章</h2>
    </div>
    <div class="badge-row">
      <span class="badge">{{ articleCount }} 篇内容</span>
      <span class="badge">接口：`GET /articles/me`</span>
    </div>
  </section>

  <section v-if="loading" class="panel panel--soft">正在加载你的文章...</section>

  <div v-else-if="sortedArticles.length" class="article-grid">
    <ArticleCard v-for="article in sortedArticles" :key="article.id" :article="article">
      <template #actions>
        <button class="button button--plain" type="button" @click="startEditing(article)">
          编辑
        </button>
        <button
          class="button button--danger"
          type="button"
          :disabled="deletingId === article.id"
          @click="removeArticle(article.id)"
        >
          {{ deletingId === article.id ? '删除中...' : '删除' }}
        </button>
      </template>
    </ArticleCard>
  </div>

  <EmptyState
    v-else
    title="你还没有发布任何文章"
    description="上面的编辑器已经准备好了，写完就可以直接调用后端发布接口。"
  />
</template>
