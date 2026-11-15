export async function api(path, { method = 'GET', body, csrf, key, signal } = {}) {
  let response
  try {
    response = await fetch(`/api${path}`, {
      method,
      credentials: 'same-origin',
      signal,
      headers: {
        ...(body ? { 'Content-Type': 'application/json' } : {}),
        ...(csrf ? { 'X-CSRF-Token': csrf } : {}),
        ...(key ? { 'Idempotency-Key': key } : {}),
      },
      ...(body ? { body: JSON.stringify(body) } : {}),
    })
  } catch (error) {
    if (error.name === 'AbortError') throw error
    throw new Error('Connection lost. Keep this page open; we will reconnect.')
  }
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    const error = new Error(
      typeof data.detail === 'string' ? data.detail : 'Something went wrong. Please try again.',
    )
    error.status = response.status
    throw error
  }
  return data
}
