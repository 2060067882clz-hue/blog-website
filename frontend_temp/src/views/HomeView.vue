<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

import ArticleCard from '../components/ArticleCard.vue'
import EmptyState from '../components/EmptyState.vue'
import { apiRequest } from '../lib/api'
import { isLoggedIn } from '../lib/auth'
import { sortByDate } from '../lib/format'
import { notify } from '../lib/notify'

const loading = ref(true)
const search = ref('')
const articles = ref([])

const visibleArticles = computed(() => {
  const keyword = search.value.trim().toLowerCase()
  const sorted = sortByDate(articles.value)

  if (!keyword) {
    return sorted
  }

  return sorted.filter((article) =>
    `${article.title} ${article.content} ${article.author.nickname} ${article.author.username}`
      .toLowerCase()
      .includes(keyword),
  )
})

const featuredArticle = computed(() => visibleArticles.value[0] || null)
const remainingArticles = computed(() => visibleArticles.value.slice(1))
const authorCount = computed(() => new Set(articles.value.map((item) => item.author.id)).size)

async function loadArticles() {
  loading.value = true
  try {
    const response = await apiRequest('/articles')
    articles.value = response.data
  } catch (error) {
    notify(error.message || '文章加载失败', 'danger')
  } finally {
    loading.value = false
  }
}

onMounted(loadArticles)
</script>

<template>
  <section class="hero-panel">
    <div class="hero-panel__content">
      <span class="eyebrow">Blog Experience</span>
      <h1>把后端已经实现的博客能力，变成一套完整且精致的前端界面。</h1>
      <p>
        页面严格对应现有接口：游客可浏览文章，登录后可评论与创作，管理员可进入管理台巡检用户和内容。
      </p>
      <div class="hero-panel__actions">
        <RouterLink class="button" :to="isLoggedIn ? '/dashboard' : '/auth'">
          {{ isLoggedIn ? '进入创作工作台' : '立即登录开始使用' }}
        </RouterLink>
        <a class="button button--ghost" href="#article-list">浏览最新文章</a>
      </div>
    </div>

    <div class="hero-panel__stats">
      <div class="stat-card">
        <span>文章总量</span>
        <strong>{{ articles.length }}</strong>
      </div>
      <div class="stat-card">
        <span>作者数量</span>
        <strong>{{ authorCount }}</strong>
      </div>
      <div class="stat-card">
        <span>权限场景</span>
        <strong>游客 / 用户 / 管理员</strong>
      </div>
    </div>
  </section>

  <section class="section-head">
    <div>
      <span class="eyebrow">Article Feed</span>
      <h2>内容广场</h2>
    </div>
    <label class="search-box">
      <span>搜索</span>
      <input v-model="search" type="search" placeholder="按标题、内容、作者筛选" />
    </label>
  </section>

  <section v-if="loading" class="panel panel--soft">正在加载文章列表...</section>

  <section
    v-else-if="featuredArticle"
    id="article-list"
    class="content-grid"
  >
    <RouterLink class="feature-story" :to="`/article/${featuredArticle.id}`">
      <div class="feature-story__meta">
        <span>Featured</span>
        <span>{{ featuredArticle.author.nickname || featuredArticle.author.username }}</span>
      </div>
      <h2>{{ featuredArticle.title }}</h2>
      <p>{{ featuredArticle.content }}</p>
    </RouterLink>

    <div class="article-grid">
      <ArticleCard
        v-for="article in remainingArticles"
        :key="article.id"
        :article="article"
      />
    </div>
  </section>

  <EmptyState
    v-else
    title="还没有可展示的文章"
    description="等后端初始化数据就位后，这里会自动展示内容。"
  />
</template>
