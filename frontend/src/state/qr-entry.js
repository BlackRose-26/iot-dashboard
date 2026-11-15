// URL validation only. Camera and image decoding belong to html5-qrcode.
export function registrationQrContent(value, origin = window.location.origin) {
  try {
    if (typeof value !== 'string' || value.length > 1024) throw new Error()
    const url = new URL(value.trim())
    if (
      !['http:', 'https:'].includes(url.protocol) ||
      url.username ||
      url.password ||
      url.search ||
      url.hash ||
      !/^\/join\/[A-Za-z0-9_-]{43}$/.test(url.pathname)
    )
      throw new Error()
    // The printed code may use localhost, a LAN IP or the event hostname.
    // Never navigate to that host: submit its token to this site's backend,
    // which checks that it is an active QR registered for the current event.
    return new URL(url.pathname, new URL(origin).origin).href
  } catch {
    throw new Error('This is not a Stack Moko Baby QR. Scan the code displayed by the operator.')
  }
}
