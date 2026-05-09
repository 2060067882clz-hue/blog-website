<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

import { formatDate, getExcerpt } from '../lib/format'

const props = defineProps({
  article: {
    type: Object,
    required: true,
  },
})

const excerpt = computed(() => getExcerpt(props.article.content, 150))
</script>

<template>
  <article class="article-card">
    <div class="article-card__meta">
      <span>{{ props.article.author.nickname || props.article.author.username }}</span>
      <span>{{ formatDate(props.article.update_time) }}</span>
    </div>
    <h3>{{ props.article.title }}</h3>
    <p>{{ excerpt }}</p>
    <div class="article-card__footer">
      <RouterLink class="button button--plain" :to="`/article/${props.article.id}`">
        阅读全文
      </RouterLink>
      <div class="article-card__actions">
        <slot name="actions" />
      </div>
    </div>
  </article>
</template>
