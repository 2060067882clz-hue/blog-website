import { computed, reactive } from 'vue'

import { apiRequest, getStoredToken } from './api'

export const authState = reactive({
  token: getStoredToken(),
  user: null,
  ready: false,
})

export const isLoggedIn = computed(() => Boolean(authState.token && authState.user))
export const isAdmin = computed(() => authState.user?.role === 1)

function persistAuth() {
  if (authState.token) {
    localStorage.setItem('token', authState.token)
  } else {
    localStorage.removeItem('token')
  }

  if (authState.user) {
    localStorage.setItem('user', JSON.stringify(authState.user))
  } else {
    localStorage.removeItem('user')
  }
}

function restoreCachedUser() {
  const rawUser = localStorage.getItem('user')
  if (!rawUser) {
    return null
  }

  try {
    return JSON.parse(rawUser)
  } catch {
    localStorage.removeItem('user')
    return null
  }
}

export function setSession(token, user) {
  authState.token = token
  authState.user = user
  persistAuth()
}

export function clearSession() {
  authState.token = null
  authState.user = null
  persistAuth()
}

export async function hydrateAuth() {
  if (authState.ready) {
    return
  }

  authState.user = restoreCachedUser()

  if (!authState.token) {
    authState.ready = true
    return
  }

  try {
    const response = await apiRequest('/auth/me')
    authState.user = response.data
    persistAuth()
  } catch {
    clearSession()
  } finally {
    authState.ready = true
  }
}

export async function login(payload) {
  const response = await apiRequest('/auth/login', {
    method: 'POST',
    body: payload,
    token: null,
  })
  setSession(response.data.token, response.data.user)
  return response
}

export async function register(payload) {
  const response = await apiRequest('/auth/register', {
    method: 'POST',
    body: payload,
    token: null,
  })
  setSession(response.data.token, response.data.user)
  return response
}

export async function logout() {
  try {
    if (authState.token) {
      await apiRequest('/auth/logout', { method: 'POST' })
    }
  } finally {
    clearSession()
  }
}
