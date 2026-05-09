<script setup>
import { ref, onMounted, computed } from 'vue'
import { RouterLink, useRouter } from 'vue-router'

import ArticleCard from '../components/ArticleCard.vue'
import EmptyState from '../components/EmptyState.vue'
import { apiRequest } from '../lib/api'
import { notify } from '../lib/notify'
import { sortByDate } from '../lib/format'

const router = useRouter()
const loading = ref(true)
const deletingId = ref(null)
const articles = ref([])

const sortedArticles = computed(() => sortByDate(articles.value))
const articleCount = computed(() => sortedArticles.value.length)

async function loadMyArticles() {
  loading.value = true
  try {
    const response = await apiRequest('/articles/me')
    articles.value = response.data
  } catch (error) {
    notify(error.message || '我的文章加载失败', 'danger')
  } finally {
    loading.value = false
  }
}

async function removeArticle(articleId) {
  if (!window.confirm('确认删除这篇文章吗？')) return

  deletingId.value = articleId
  try {
    const response = await apiRequest(`/articles/${articleId}`, { method: 'DELETE' })
    articles.value = articles.value.filter((item) => item.id !== articleId)
    notify(response.message || '文章已删除', 'success')
  } catch (error) {
    notify(error.message || '文章删除失败', 'danger')
  } finally {
    deletingId.value = null
  }
}

function goBack() {
  try {
    if (router && typeof router.go === 'function') {
      // try router history step back
      router.go(-1)
      // give browser a moment; if still on same path, fallback
      setTimeout(() => {
        if (window.location.pathname === '/my-articles') {
          router.push('/dashboard')
        }
      }, 250)
      return
    }

    if (window.history && window.history.length > 1) {
      window.history.back()
      setTimeout(() => {
        if (window.location.pathname === '/my-articles') {
          router.push('/dashboard')
        }
      }, 250)
      return
    }

    const ref = document.referrer
    if (ref) {
      try {
        const u = new URL(ref)
        if (u.origin === window.location.origin) {
          router.push(u.pathname + (u.search || ''))
          return
        }
      } catch (e) {}
    }

    router.push('/dashboard')
  } catch (e) {
    router.push('/dashboard')
  }
}

onMounted(loadMyArticles)
</script>

<template>
  <section class="section-head my-articles-head">
    <div class="section-head__left">
      <button class="button button--plain back-button" type="button" @click="goBack">返回</button>
      <div>
        <span class="eyebrow">我的文章</span>
        <h2>我的文章</h2>
      </div>
    </div>
    <div class="section-head__right">
      <span class="my-articles-count">文章总数：{{ articleCount }}</span>
    </div>
  </section>

  <section v-if="loading" class="panel panel--soft">正在加载你的文章...</section>

  <div v-else-if="sortedArticles.length" class="article-grid">
    <ArticleCard v-for="article in sortedArticles" :key="article.id" :article="article">
      <template #actions>
        <RouterLink class="button button--plain" :to="`/article/new?edit=${article.id}`">编辑</RouterLink>
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

  <EmptyState v-else title="你还没有发布任何文章" description="点击新建开始创作。" />
</template>
