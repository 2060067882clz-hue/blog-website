<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { watch } from 'vue'

import { apiRequest } from '../lib/api'
import { notify } from '../lib/notify'

const router = useRouter()
const route = useRoute()
const saving = ref(false)
const form = ref({ title: '', content: '' })
const editId = ref(null)

function fillFormFromResponse(response) {
	const article = response?.data?.article || response?.data || {}
	form.value.title = article.title || ''
	form.value.content = article.content || ''
}

onMounted(async () => {
	const q = route.query.edit
	if (q) {
		const id = Number(q)
		if (id) {
			editId.value = id
			try {
				const res = await apiRequest(`/articles/${id}`)
				fillFormFromResponse(res)
			} catch (e) {
				notify('加载文章失败', 'danger')
			}
		}
	}
})

// also handle query changes so opening the editor with ?edit=... dynamically fills content
watch(
	() => route.query.edit,
	async (q) => {
		if (!q) {
			editId.value = null
			form.value.title = ''
			form.value.content = ''
			return
		}
		const id = Number(q)
		if (!id) return
		editId.value = id
		try {
			const res = await apiRequest(`/articles/${id}`)
			fillFormFromResponse(res)
		} catch (e) {
			notify('加载文章失败', 'danger')
		}
	},
)

function goBack() {
	if (window.history.length > 1) {
		window.history.back()
		return
	}
	try {
		const ref = document.referrer
		if (ref) {
			const refUrl = new URL(ref)
			if (refUrl.origin === window.location.origin) {
				const path = refUrl.pathname + (refUrl.search || '')
				router.push(path)
				return
			}
		}
	} catch (e) {}
	router.push('/dashboard')
}

async function submitArticle() {
	if (!form.value.title.trim() || !form.value.content.trim()) {
		notify('标题和正文不能为空', 'warning')
		return
	}

	saving.value = true
	try {
		if (editId.value) {
			const response = await apiRequest(`/articles/${editId.value}`, {
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
		router.push('/dashboard')
	} catch (error) {
		notify(error.message || '文章发布失败', 'danger')
	} finally {
		saving.value = false
	}
}
</script>

<template>
	<section class="panel create-article">
		<button class="create-article__back button button--plain" type="button" @click="goBack">返回</button>
		<div class="section-head">
			<div>
				<h2>{{ editId ? '编辑文章' : '发布新文章' }}</h2>
			</div>
		</div>

		<form class="panel editor-panel" @submit.prevent="submitArticle">
			<label class="field">
				<span>标题</span>
				<input v-model="form.title" maxlength="120" placeholder="写一个清晰、有辨识度的标题" />
			</label>

			<label class="field">
				<span>正文</span>
				<textarea v-model="form.content" rows="16" placeholder="这里直接对应后端文章正文 content 字段" />
			</label>

			<div class="editor-panel__footer">
				<span>{{ form.content.length }} 字</span>
				<button class="button" type="submit" :disabled="saving">
					{{ saving ? '保存中...' : (editId ? '更新文章' : '发布文章') }}
				</button>
			</div>
		</form>
	</section>
</template>

