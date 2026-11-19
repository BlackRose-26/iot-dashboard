export async function api(
  path,
  {
    method = 'GET',
    body,
    csrf,
    key,
    signal,
    timeoutMs = path === '/admin/assistant/query' ? 25000 : 15000,
  } = {},
) {
  const controller = new AbortController()
  let timedOut = false
  const cancel = () => controller.abort()
  if (signal?.aborted) cancel()
  else signal?.addEventListener('abort', cancel, { once: true })
  const timer = setTimeout(() => {
    timedOut = true
    controller.abort()
  }, timeoutMs)
  try {
    let response
    try {
      response = await fetch(`/api${path}`, {
        method,
        credentials: 'same-origin',
        signal: controller.signal,
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
    let data
    try {
      data = await response.json()
    } catch (error) {
      if (error.name === 'AbortError') throw error
      const failure = new Error(
        'The event API returned an invalid response. Check the server connection and retry.',
      )
      failure.status = response.status
      throw failure
    }
    if (!response.ok) {
      const error = new Error(
        typeof data?.detail === 'string' ? data.detail : 'Something went wrong. Please try again.',
      )
      error.status = response.status
      throw error
    }
    if (!data || typeof data !== 'object' || Array.isArray(data))
      throw new Error(
        'The event API returned an invalid response. Check the server connection and retry.',
      )
    return data
  } catch (error) {
    if (timedOut)
      throw new Error('The request timed out. Check the latest status before retrying an action.')
    throw error
  } finally {
    clearTimeout(timer)
    signal?.removeEventListener('abort', cancel)
  }
}
