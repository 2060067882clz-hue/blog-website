import { reactive } from 'vue'

export const toasts = reactive([])

export function dismissToast(id) {
  const index = toasts.findIndex((item) => item.id === id)
  if (index >= 0) {
    toasts.splice(index, 1)
  }
}

export function notify(message, tone = 'info') {
  const id = `${Date.now()}-${Math.random().toString(16).slice(2)}`
  toasts.push({ id, message, tone })
  window.setTimeout(() => dismissToast(id), 3600)
}
