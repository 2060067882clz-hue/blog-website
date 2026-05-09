<script setup>
import { computed, ref, watch } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'

import EmptyState from '../components/EmptyState.vue'
import { apiRequest } from '../lib/api'
import { authState, isLoggedIn } from '../lib/auth'
import { formatDate } from '../lib/format'
import { notify } from '../lib/notify'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const article = ref(null)
const commentCount = ref(0)
const comments = ref([])
const commentDraft = ref('')
const deleting = ref(false)
const submittingComment = ref(false)

const canManageArticle = computed(() => {
  if (!authState.user || !article.value) {
    return false
  }
  return authState.user.role === 1 || authState.user.id === article.value.author.id
})

function goBack() {
  if (window.history.length > 1) {
    window.history.back()
    return
  }
  router.push('/dashboard')
}

function canDeleteComment(comment) {
  if (!authState.user) {
    return false
  }
  return authState.user.role === 1 || authState.user.id === comment.author.id
}

async function loadPage() {
  loading.value = true

  try {
    const id = route.params.id
    const [articleResponse, commentResponse] = await Promise.all([
      apiRequest(`/articles/${id}`),
      apiRequest(`/articles/${id}/comments`),
    ])

    article.value = articleResponse.data.article
    commentCount.value = articleResponse.data.comment_count
    comments.value = commentResponse.data.comments
  } catch (error) {
    article.value = null
    notify(error.message || '文章详情加载失败', 'danger')
  } finally {
    loading.value = false
  }
}

async function submitComment() {
  if (!commentDraft.value.trim()) {
    notify('评论内容不能为空', 'warning')
    return
  }

  submittingComment.value = true
  try {
    const response = await apiRequest(`/articles/${route.params.id}/comments`, {
      method: 'POST',
      body: { content: commentDraft.value },
    })
    comments.value = response.data.comments
    commentCount.value = comments.value.length
    commentDraft.value = ''
    notify(response.message || '评论发布成功', 'success')
  } catch (error) {
    notify(error.message || '评论发布失败', 'danger')
  } finally {
    submittingComment.value = false
  }
}

async function removeComment(commentId) {
  try {
    const response = await apiRequest(`/comments/${commentId}`, { method: 'DELETE' })
    comments.value = comments.value.filter((item) => item.id !== commentId)
    commentCount.value = comments.value.length
    notify(response.message || '评论已删除', 'success')
  } catch (error) {
    notify(error.message || '评论删除失败', 'danger')
  }
}

async function removeArticle() {
  if (!window.confirm('确认删除这篇文章吗？相关评论也会一起删除。')) {
    return
  }

  deleting.value = true
  try {
    const response = await apiRequest(`/articles/${route.params.id}`, { method: 'DELETE' })
    notify(response.message || '文章已删除', 'success')
    router.push('/dashboard')
  } catch (error) {
    notify(error.message || '文章删除失败', 'danger')
  } finally {
    deleting.value = false
  }
}

watch(() => route.params.id, loadPage, { immediate: true })
</script>

<template>
  <section v-if="loading" class="panel panel--soft">正在加载文章详情...</section>

  <EmptyState
    v-else-if="!article"
    title="这篇文章暂时不可用"
    description="可能已经被删除，或者后端服务还没有启动。"
  >
    <RouterLink class="button" to="/">返回首页</RouterLink>
  </EmptyState>

  <template v-else>
    <article class="article-detail">
      <button class="button button--plain article-detail__back" type="button" @click="goBack">返回</button>
      <button
        v-if="canManageArticle"
        class="button button--danger article-detail__delete"
        type="button"
        :disabled="deleting"
        @click="removeArticle"
      >
        {{ deleting ? '删除中...' : '删除文章' }}
      </button>
      <div class="article-detail__head">
        <div>
          <span class="eyebrow">文章详情</span>
          <h1>{{ article.title }}</h1>
        </div>
        <div class="article-detail__tools"></div>
      </div>

      <div class="article-detail__meta">
        <span>作者：{{ article.author.nickname || article.author.username }}</span>
        <span>更新于：{{ formatDate(article.update_time) }}</span>
        <span>评论数：{{ commentCount }}</span>
      </div>

      <div class="article-detail__body">
        {{ article.content }}
      </div>
    </article>

    <section class="comment-board">
      <div class="section-head section-head--compact">
        <div>
          <span class="eyebrow">评论区</span>
          <h2>评论区</h2>
        </div>
      </div>

      <form v-if="isLoggedIn" class="comment-form" @submit.prevent="submitComment">
        <textarea
          v-model="commentDraft"
          rows="4"
          maxlength="500"
          placeholder="写下你对这篇文章的想法"
        />
        <div class="comment-form__footer">
          <span>{{ commentDraft.length }}/500</span>
          <button class="button" type="submit" :disabled="submittingComment">
            {{ submittingComment ? '发布中...' : '发表评论' }}
          </button>
        </div>
      </form>

      <div v-else class="panel panel--soft">
        登录后即可参与评论与互动。
        <RouterLink class="inline-link" to="/auth">去登录</RouterLink>
      </div>

      <div v-if="comments.length" class="comment-list">
        <article v-for="comment in comments" :key="comment.id" class="comment-card">
          <div class="comment-card__head">
            <div>
              <strong>{{ comment.author.nickname || comment.author.username }}</strong>
              <span>{{ formatDate(comment.create_time) }}</span>
            </div>
            <button
              v-if="canDeleteComment(comment)"
              class="button button--plain"
              type="button"
              @click="removeComment(comment.id)"
            >
              删除
            </button>
          </div>
          <p>{{ comment.content }}</p>
        </article>
      </div>

      <EmptyState
        v-else
        title="还没有评论"
        description="这篇文章正在等待第一条互动。"
      />
    </section>
  </template>
</template>
