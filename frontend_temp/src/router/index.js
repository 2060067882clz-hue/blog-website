import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Profile from '../views/Profile.vue'

const routes = [
    { path: '/', redirect: '/login' },
    { path: '/login', component: Login },
    { path: '/profile', component: Profile }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// 路由守卫：未登录不能访问个人页
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token')
    if (to.path === '/profile' && !token) {
        next('/login')
    } else {
        next()
    }
})

export default router