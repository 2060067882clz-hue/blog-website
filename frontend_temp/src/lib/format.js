export function formatDate(value) {
  if (!value) {
    return '--'
  }

  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value))
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
