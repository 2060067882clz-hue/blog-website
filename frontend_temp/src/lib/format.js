export function formatDate(value) {
  if (!value) {
    return '--'
  }

  // normalize common timestamp formats: numeric seconds -> ms
  let ts = value
  if (typeof ts === 'number') {
    if (ts > 0 && ts < 1e12) ts = ts * 1000
  } else if (/^\d+$/.test(String(ts))) {
    const n = Number(ts)
    if (n > 0 && n < 1e12) ts = n * 1000
    else ts = n
  }

  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(ts))
}

export function getExcerpt(content, length = 140) {
  const plain = (content || '').replace(/\s+/g, ' ').trim()
  if (plain.length <= length) {
    return plain
  }
  return `${plain.slice(0, length).trim()}...`
}

export function sortByDate(items, key = 'update_time') {
  return [...items].sort((left, right) => new Date(right[key]) - new Date(left[key]))
}
