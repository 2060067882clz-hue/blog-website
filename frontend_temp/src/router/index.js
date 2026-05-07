import { createRouter, createWebHistory } from 'vue-router'

import { authState, hydrateAuth, isAdmin, isLoggedIn } from '../lib/auth'
import AdminView from '../views/AdminView.vue'
import ArticleView from '../views/ArticleView.vue'
import AuthView from '../views/AuthView.vue'
import DashboardView from '../views/DashboardView.vue'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { title: '博客首页' },
  },
  {
    path: '/article/:id',
    name: 'article',
    component: ArticleView,
    meta: { title: '文章详情' },
  },
  {
    path: '/auth',
    name: 'auth',
    component: AuthView,
    meta: { title: '登录与注册', guestOnly: true },
  },
  {
    path: '/login',
    redirect: '/auth',
  },
  {
    path: '/register',
    redirect: '/auth',
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: { title: '创作工作台', requiresAuth: true },
  },
  {
    path: '/profile',
    redirect: '/dashboard',
  },
  {
    path: '/admin',
    name: 'admin',
    component: AdminView,
    meta: { title: '管理员后台', requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach(async (to) => {
  if (!authState.ready) {
    await hydrateAuth()
  }

  if (to.meta.requiresAuth && !isLoggedIn.value) {
    return {
      path: '/auth',
      query: { redirect: to.fullPath },
    }
  }

  if (to.meta.requiresAdmin && !isAdmin.value) {
    return isLoggedIn.value ? '/dashboard' : '/auth'
  }

  if (to.meta.guestOnly && isLoggedIn.value) {
    return typeof to.query.redirect === 'string' ? to.query.redirect : '/dashboard'
  }

  return true
})

router.afterEach((to) => {
  document.title = `Blog Atelier | ${to.meta.title || '内容空间'}`
})

export default router
