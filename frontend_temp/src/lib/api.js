const DEFAULT_API_BASE_URL = 'http://127.0.0.1:8000/api/v1'

export class ApiError extends Error {
  constructor(message, status, code, payload) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.code = code
    this.payload = payload
  }
}

const trimTrailingSlash = (value) => value.replace(/\/+$/, '')

export const API_BASE_URL = trimTrailingSlash(
  import.meta.env.VITE_API_BASE_URL || DEFAULT_API_BASE_URL,
)

export function getStoredToken() {
  return localStorage.getItem('token')
}

export async function apiRequest(path, options = {}) {
  const {
    method = 'GET',
    body,
    headers = {},
    token = undefined,
  } = options

  const requestHeaders = new Headers(headers)
  const activeToken = token === undefined ? getStoredToken() : token

  if (body !== undefined && !requestHeaders.has('Content-Type')) {
    requestHeaders.set('Content-Type', 'application/json')
  }

  if (activeToken && !requestHeaders.has('Authorization')) {
    requestHeaders.set('Authorization', `Bearer ${activeToken}`)
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers: requestHeaders,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  })

  const contentType = response.headers.get('content-type') || ''
  let payload = null

  if (contentType.includes('application/json')) {
    payload = await response.json()
  } else {
    const text = await response.text()
    payload = text ? { message: text } : null
  }

  if (!response.ok || payload?.success === false) {
    throw new ApiError(
      payload?.error?.message || payload?.message || `Request failed: ${response.status}`,
      response.status,
      payload?.error?.code || 'REQUEST_FAILED',
      payload,
    )
  }

  return payload
}
