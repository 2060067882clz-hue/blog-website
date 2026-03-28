import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Profile from '../views/Profile.vue'
import Center from '../views/center.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/profile', component: Profile },
  { path: '/center', name: 'Center', component: Center },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  if (to.path === '/profile' && !token) {
    next('/login')
    return
  }

  if (to.path === '/login' && token) {
    next('/profile')
    return
  }

  next()
})

export default router
