<template>
  <section class="center-shell">
    <div class="ambient ambient-one"></div>
    <div class="ambient ambient-two"></div>
    <div class="ambient ambient-grid"></div>
    <div class="ambient ambient-rings"></div>

    <div class="center-frame">
      <aside class="center-sidebar">
        <div class="sidebar-copy">
          <p class="eyebrow">Personal Space</p>
          <h1>个人空间</h1>
          <p class="sidebar-description">
            延续登录页的玻璃质感和柔和光效，让个人信息、文章与收藏都保持同一套节奏和氛围。
          </p>
        </div>

        <div class="profile-card glass-card">
          <div class="profile-avatar">{{ avatarText }}</div>
          <div class="profile-meta">
            <strong>{{ userInfo.nickname }}</strong>
            <span>{{ userInfo.account }}</span>
          </div>
          <div class="profile-stats">
            <article>
              <small>文章</small>
              <strong>{{ posts.length }}</strong>
            </article>
            <article>
              <small>收藏</small>
              <strong>{{ favorites.length }}</strong>
            </article>
            <article>
              <small>状态</small>
              <strong>{{ loadingUser ? '同步中' : '在线' }}</strong>
            </article>
          </div>
        </div>

        <nav class="nav-card glass-card" aria-label="个人空间导航">
          <button
            v-for="item in navItems"
            :key="item.key"
            type="button"
            class="nav-item"
            :class="{ active: selected === item.key }"
            @click="selected = item.key"
          >
            <span class="nav-item-text">
              <small>{{ item.en }}</small>
              <strong>{{ item.label }}</strong>
            </span>
            <span class="nav-item-count">{{ item.count }}</span>
          </button>
        </nav>

        <div class="sidebar-actions">
          <button type="button" class="ghost-button" @click="goBack">返回上一页</button>
          <button type="button" class="warm-button" @click="handleLogout">退出登录</button>
        </div>
      </aside>

      <main class="center-panel">
        <header class="panel-header">
          <div>
            <p class="panel-kicker">{{ activeSection.en }}</p>
            <h2>{{ activeSection.title }}</h2>
            <p class="panel-copy">{{ activeSection.description }}</p>
          </div>
          <span class="status-chip" :class="{ pending: loadingUser }">
            {{ loadingUser ? 'Syncing' : 'Ready' }}
          </span>
        </header>

        <div v-if="feedbackMessage" class="message-stage">
          <p class="success-message">{{ feedbackMessage }}</p>
        </div>

        <Transition name="panel-switch" mode="out-in">
          <section :key="selected" class="panel-body glass-panel">
            <div v-if="selected === 'info'" class="info-grid">
              <article
                v-for="item in infoItems"
                :key="item.label"
                class="info-card"
              >
                <small>{{ item.label }}</small>
                <strong>{{ item.value }}</strong>
              </article>
            </div>

            <div v-else class="content-stack">
              <div class="section-summary">
                <p>{{ activeSection.summary }}</p>
                <span>{{ activeSection.totalLabel }}</span>
              </div>

              <ul class="content-list">
                <li
                  v-for="entry in activeEntries"
                  :key="entry.id"
                  class="content-item"
                >
                  <div class="content-main">
                    <h3>{{ entry.title }}</h3>
                    <p>{{ entry.description }}</p>
                  </div>
                  <div class="content-meta">
                    <span>{{ entry.date }}</span>
                    <strong>{{ entry.meta }}</strong>
                  </div>
                </li>
              </ul>

              <div v-if="!activeEntries.length" class="empty-state">
                <strong>这里还没有内容</strong>
                <p>后续发布文章或收藏内容后，会在这里平滑展示出来。</p>
              </div>

              <div v-if="activeTotalPages > 1" class="pagination">
                <button
                  type="button"
                  class="page-btn"
                  :disabled="activePage === 1"
                  @click="changePage(activePage - 1)"
                >
                  上一页
                </button>
                <button
                  v-for="page in activeTotalPages"
                  :key="page"
                  type="button"
                  class="page-btn"
                  :class="{ active: activePage === page }"
                  @click="changePage(page)"
                >
                  {{ page }}
                </button>
                <button
                  type="button"
                  class="page-btn"
                  :disabled="activePage === activeTotalPages"
                  @click="changePage(activePage + 1)"
                >
                  下一页
                </button>
              </div>
            </div>
          </section>
        </Transition>
      </main>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'

import { clearAuth, getCurrentUser, getStoredUser, logoutRequest } from '../services/auth'

const router = useRouter()

const selected = ref('info')
const loadingUser = ref(false)
const feedbackMessage = ref('')
const postsPage = ref(1)
const favoritesPage = ref(1)
const pageSize = 3

const posts = ref([
  {
    id: 1,
    title: '我的第一篇博客',
    date: '2024-02-01',
    views: 120,
    description: '记录从搭建项目到页面落地的完整过程，适合作为个人写作的起点。',
  },
  {
    id: 2,
    title: '如何写好一篇技术文章',
    date: '2024-03-12',
    views: 85,
    description: '从结构组织、案例切入和节奏控制三个角度，整理更适合阅读的表达方式。',
  },
  {
    id: 3,
    title: 'Vue 实战总结',
    date: '2024-05-05',
    views: 230,
    description: '总结组件拆分、状态同步与页面动效的常见经验，方便后续项目复用。',
  },
  {
    id: 4,
    title: '前端动画如何做到不生硬',
    date: '2024-08-18',
    views: 164,
    description: '整理常用缓动曲线、位移动画与层次反馈，让交互动起来更轻盈。',
  },
])

const favorites = ref([
  {
    id: 1,
    title: '优秀的前端工程实践',
    date: '2024-06-10',
    description: '关于组件规范、状态管理和目录组织的一次高质量总结。',
  },
  {
    id: 2,
    title: '性能优化技巧汇总',
    date: '2024-07-02',
    description: '从资源加载、渲染阻塞到运行时优化，适合作为排查清单。',
  },
  {
    id: 3,
    title: 'UI 过渡动画设计指南',
    date: '2024-09-21',
    description: '把视觉层级、反馈力度与过渡时长统一起来，页面会明显更顺。',
  },
])

const defaultUserInfo = {
  nickname: '用户昵称',
  account: 'user@example.com',
  gender: '未设置',
  registrationDate: '2024-01-15',
}

const userInfo = ref({ ...defaultUserInfo })

const navItems = computed(() => [
  { key: 'info', label: '个人信息', en: 'Profile', count: '01' },
  { key: 'posts', label: '我的文章', en: 'Posts', count: String(posts.value.length).padStart(2, '0') },
  { key: 'favorites', label: '我的收藏', en: 'Saved', count: String(favorites.value.length).padStart(2, '0') },
])

const sectionMap = computed(() => ({
  info: {
    en: 'Profile Overview',
    title: '基础资料',
    description: '展示当前账号的基础信息与账号状态。',
  },
  posts: {
    en: 'Published Posts',
    title: '我发表的博客',
    description: '按更清晰的卡片节奏展示文章信息与阅读数据。',
    summary: '这里集中展示你已经发布的文章，信息层级与间距做了统一处理。',
    totalLabel: `共 ${posts.value.length} 篇文章`,
  },
  favorites: {
    en: 'Saved Collection',
    title: '我收藏的博客',
    description: '保留更轻的阅读感，让收藏列表在视觉上更干净。',
    summary: '收藏内容会按照同样的布局展示，浏览时不会出现风格跳变。',
    totalLabel: `共 ${favorites.value.length} 条收藏`,
  },
}))

const activeSection = computed(() => sectionMap.value[selected.value])

const avatarText = computed(() => userInfo.value.nickname?.slice(0, 1) || 'U')

const infoItems = computed(() => [
  { label: '昵称', value: userInfo.value.nickname },
  { label: '账号', value: userInfo.value.account },
  { label: '性别', value: userInfo.value.gender },
  { label: '注册日期', value: userInfo.value.registrationDate },
])

const postsTotalPages = computed(() => Math.max(1, Math.ceil(posts.value.length / pageSize)))
const favoritesTotalPages = computed(() => Math.max(1, Math.ceil(favorites.value.length / pageSize)))

const pagedPosts = computed(() => {
  const start = (postsPage.value - 1) * pageSize
  return posts.value.slice(start, start + pageSize).map((post) => ({
    ...post,
    meta: `${post.views} 阅读`,
  }))
})

const pagedFavorites = computed(() => {
  const start = (favoritesPage.value - 1) * pageSize
  return favorites.value.slice(start, start + pageSize).map((favorite) => ({
    ...favorite,
    meta: '已收藏',
  }))
})

const activeEntries = computed(() => (selected.value === 'posts' ? pagedPosts.value : pagedFavorites.value))
const activePage = computed(() => (selected.value === 'posts' ? postsPage.value : favoritesPage.value))
const activeTotalPages = computed(() =>
  selected.value === 'posts' ? postsTotalPages.value : favoritesTotalPages.value,
)

const syncUserInfo = (sourceUser) => {
  if (!sourceUser) {
    userInfo.value = { ...defaultUserInfo }
    return
  }

  userInfo.value = {
    nickname: sourceUser.display_name || sourceUser.nickname || defaultUserInfo.nickname,
    account: sourceUser.username || sourceUser.email || defaultUserInfo.account,
    gender: sourceUser.gender || defaultUserInfo.gender,
    registrationDate:
      sourceUser.created_at?.slice(0, 10) ||
      sourceUser.registration_date ||
      defaultUserInfo.registrationDate,
  }
}

const loadUser = async () => {
  syncUserInfo(getStoredUser())
  loadingUser.value = true

  try {
    const latestUser = await getCurrentUser()
    syncUserInfo(latestUser)
  } catch {
    feedbackMessage.value = '当前展示的是本地缓存资料，后端信息同步失败。'
  } finally {
    loadingUser.value = false
  }
}

const changePage = (page) => {
  if (selected.value === 'posts') {
    postsPage.value = Math.min(Math.max(page, 1), postsTotalPages.value)
    return
  }

  favoritesPage.value = Math.min(Math.max(page, 1), favoritesTotalPages.value)
}

const goBack = () => {
  router.push('/profile')
}

const handleLogout = async () => {
  try {
    await logoutRequest()
  } catch {
    // Allow local logout even when the request fails.
  } finally {
    clearAuth()
    router.push('/login')
  }
}

watch(selected, () => {
  feedbackMessage.value = ''
})

onMounted(() => {
  loadUser()
})
</script>

<style scoped>
.center-shell {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  padding: 28px;
  background:
    radial-gradient(circle at 14% 18%, rgba(255, 178, 36, 0.18), transparent 24%),
    radial-gradient(circle at 82% 20%, rgba(70, 230, 255, 0.14), transparent 24%),
    linear-gradient(135deg, #08111f 0%, #12233a 48%, #1f2e45 100%);
}

.ambient {
  position: absolute;
  pointer-events: none;
}

.ambient-one,
.ambient-two {
  border-radius: 999px;
  filter: blur(54px);
  opacity: 0.55;
}

.ambient-one {
  width: 320px;
  height: 320px;
  top: -82px;
  left: -44px;
  background: rgba(251, 191, 36, 0.28);
}

.ambient-two {
  width: 420px;
  height: 420px;
  right: -120px;
  bottom: -150px;
  background: rgba(34, 211, 238, 0.22);
}

.ambient-grid {
  inset: 0;
  background-image:
    linear-gradient(rgba(148, 163, 184, 0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(148, 163, 184, 0.08) 1px, transparent 1px);
  background-size: 42px 42px;
  mask-image: radial-gradient(circle at center, black 36%, transparent 86%);
  opacity: 0.28;
}

.ambient-rings {
  inset: auto auto 10% 7%;
  width: 260px;
  height: 260px;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow:
    0 0 0 28px rgba(255, 255, 255, 0.03),
    0 0 0 56px rgba(255, 255, 255, 0.02);
  opacity: 0.5;
}

.center-frame {
  position: relative;
  z-index: 1;
  width: min(1240px, 100%);
  min-height: calc(100vh - 56px);
  margin: 0 auto;
  display: grid;
  grid-template-columns: 360px minmax(0, 1fr);
  gap: 22px;
}

.center-sidebar,
.center-panel {
  border-radius: 34px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.08),
    0 36px 120px rgba(0, 0, 0, 0.32);
  backdrop-filter: blur(24px) saturate(132%);
}

.center-sidebar {
  padding: 34px 28px 28px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  color: #e7eff8;
  background:
    radial-gradient(circle at top left, rgba(250, 204, 21, 0.14), transparent 30%),
    linear-gradient(160deg, rgba(255, 255, 255, 0.055), rgba(255, 255, 255, 0.018));
}

.sidebar-copy h1,
.panel-header h2 {
  margin: 0;
  letter-spacing: -0.05em;
}

.eyebrow,
.panel-kicker {
  margin: 0 0 14px;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.24em;
  text-transform: uppercase;
}

.eyebrow {
  color: #fbbf24;
}

.sidebar-copy h1 {
  font-size: clamp(2.4rem, 4vw, 3.6rem);
  line-height: 0.96;
}

.sidebar-description {
  margin: 18px 0 0;
  color: rgba(226, 232, 240, 0.76);
  line-height: 1.8;
}

.glass-card,
.glass-panel,
.info-card,
.content-item,
.empty-state,
.page-btn,
.ghost-button,
.warm-button {
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.08),
    0 20px 44px rgba(0, 0, 0, 0.12);
}

.profile-card,
.nav-card,
.panel-body,
.info-card,
.content-item,
.empty-state,
.page-btn {
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.03));
  backdrop-filter: blur(22px) saturate(130%);
}

.profile-card {
  border-radius: 28px;
  padding: 24px;
}

.profile-avatar {
  width: 74px;
  height: 74px;
  border-radius: 24px;
  display: grid;
  place-items: center;
  font-size: 1.7rem;
  font-weight: 700;
  color: #fff;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.96), rgba(8, 145, 178, 0.82));
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.4),
    0 20px 34px rgba(8, 145, 178, 0.26);
}

.profile-meta {
  margin-top: 18px;
  display: grid;
  gap: 6px;
}

.profile-meta strong {
  font-size: 1.35rem;
  color: #f8fafc;
}

.profile-meta span,
.profile-stats small,
.nav-item small {
  color: rgba(226, 232, 240, 0.72);
}

.profile-stats {
  margin-top: 20px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.profile-stats article {
  padding: 14px 12px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.05);
}

.profile-stats strong {
  display: block;
  margin-top: 6px;
  color: #f8fafc;
  font-size: 1.02rem;
}

.nav-card {
  border-radius: 28px;
  padding: 12px;
  display: grid;
  gap: 10px;
}

.nav-item {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  border: 0;
  border-radius: 20px;
  padding: 16px 18px;
  color: #e2e8f0;
  cursor: pointer;
  background: transparent;
  transition:
    transform 0.22s ease,
    background 0.28s ease,
    box-shadow 0.28s ease,
    color 0.28s ease;
}

.nav-item:hover {
  transform: translateX(4px);
  background: rgba(255, 255, 255, 0.06);
}

.nav-item.active {
  color: #fff;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.28), rgba(8, 145, 178, 0.22));
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.16),
    0 22px 36px rgba(8, 145, 178, 0.18);
}

.nav-item-text {
  display: grid;
  gap: 4px;
  text-align: left;
}

.nav-item-text strong {
  font-size: 1rem;
}

.nav-item-count {
  min-width: 38px;
  padding: 8px 10px;
  border-radius: 999px;
  text-align: center;
  font-size: 0.82rem;
  font-weight: 700;
  color: #f8fafc;
  background: rgba(255, 255, 255, 0.1);
}

.sidebar-actions {
  margin-top: auto;
  display: grid;
  gap: 12px;
}

.ghost-button,
.warm-button {
  min-height: 54px;
  border-radius: 18px;
  font-size: 0.96rem;
  font-weight: 700;
  cursor: pointer;
  transition:
    transform 0.22s ease,
    box-shadow 0.22s ease,
    opacity 0.22s ease;
}

.ghost-button {
  color: #e2e8f0;
  background: rgba(255, 255, 255, 0.08);
}

.warm-button {
  color: #fff;
  background: linear-gradient(135deg, #f59e0b 0%, #ea580c 45%, #0891b2 100%);
}

.ghost-button:hover,
.warm-button:hover {
  transform: translateY(-2px);
}

.center-panel {
  padding: 34px;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.76), rgba(255, 255, 255, 0.58));
}

.panel-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 18px;
}

.panel-kicker {
  color: #b45309;
}

.panel-header h2 {
  font-size: clamp(2rem, 3vw, 2.8rem);
  color: #0f172a;
}

.panel-copy {
  margin: 14px 0 0;
  max-width: 40rem;
  line-height: 1.78;
  color: #64748b;
}

.status-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 12px;
  border-radius: 999px;
  font-size: 0.82rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #0f766e;
  background: rgba(20, 184, 166, 0.12);
}

.status-chip::before {
  content: '';
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: currentColor;
}

.status-chip.pending {
  color: #b45309;
  background: rgba(245, 158, 11, 0.14);
}

.message-stage {
  margin-top: 18px;
}

.success-message {
  margin: 0;
  padding: 13px 15px;
  border-radius: 16px;
  color: #047857;
  background: rgba(16, 185, 129, 0.12);
  backdrop-filter: blur(18px);
}

.panel-body {
  margin-top: 24px;
  min-height: 560px;
  border-radius: 30px;
  padding: 26px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.info-card {
  border-radius: 24px;
  padding: 24px;
  display: grid;
  gap: 10px;
}

.info-card small,
.section-summary p,
.content-item p,
.empty-state p {
  color: #64748b;
}

.info-card strong {
  color: #0f172a;
  font-size: 1.2rem;
}

.content-stack {
  display: grid;
  gap: 18px;
}

.section-summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 0 4px;
}

.section-summary p {
  margin: 0;
  line-height: 1.74;
}

.section-summary span {
  flex-shrink: 0;
  color: #b45309;
  font-weight: 700;
}

.content-list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 16px;
}

.content-item {
  border-radius: 24px;
  padding: 20px 22px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
  transition:
    transform 0.24s ease,
    box-shadow 0.24s ease,
    border-color 0.24s ease;
}

.content-item:hover {
  transform: translateY(-3px);
  border-color: rgba(14, 165, 233, 0.18);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.12),
    0 24px 42px rgba(14, 116, 144, 0.12);
}

.content-main h3,
.content-main p,
.content-meta span,
.content-meta strong,
.empty-state strong {
  margin: 0;
}

.content-main {
  display: grid;
  gap: 8px;
}

.content-main h3,
.content-meta strong,
.empty-state strong {
  color: #0f172a;
}

.content-main p {
  line-height: 1.72;
}

.content-meta {
  min-width: 112px;
  display: grid;
  gap: 8px;
  justify-items: end;
  text-align: right;
}

.content-meta span {
  color: #94a3b8;
}

.empty-state {
  border-radius: 24px;
  padding: 36px 20px;
  text-align: center;
}

.empty-state p {
  margin-top: 10px;
}

.pagination {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.page-btn {
  min-width: 48px;
  min-height: 46px;
  padding: 0 16px;
  border-radius: 16px;
  color: #475569;
  cursor: pointer;
  transition:
    transform 0.2s ease,
    background 0.2s ease,
    color 0.2s ease,
    opacity 0.2s ease;
}

.page-btn:hover:not(:disabled) {
  transform: translateY(-1px);
}

.page-btn.active {
  color: #fff;
  background: linear-gradient(135deg, #f59e0b, #0891b2);
}

.page-btn:disabled {
  cursor: not-allowed;
  opacity: 0.48;
}

.panel-switch-enter-active,
.panel-switch-leave-active {
  transition:
    opacity 0.32s ease,
    transform 0.32s ease,
    filter 0.32s ease;
}

.panel-switch-enter-from,
.panel-switch-leave-to {
  opacity: 0;
  transform: translateY(12px) scale(0.985);
  filter: blur(10px);
}

@media (max-width: 1080px) {
  .center-frame {
    grid-template-columns: 1fr;
  }

  .center-sidebar,
  .center-panel {
    padding: 28px 24px;
  }
}

@media (max-width: 720px) {
  .center-shell {
    padding: 18px;
  }

  .profile-stats,
  .info-grid {
    grid-template-columns: 1fr;
  }

  .panel-header,
  .section-summary,
  .content-item {
    flex-direction: column;
  }

  .content-meta {
    justify-items: start;
    text-align: left;
  }

  .panel-body {
    padding: 20px;
  }
}
</style>
