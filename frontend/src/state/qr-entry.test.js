import { describe, expect, it } from 'vitest'
import { registrationQrContent } from './qr-entry'

const origin = 'https://carnival.example'
const code = `${origin}/join/${'a'.repeat(43)}`
describe('game QR validation after scanner API detection', () => {
  it('accepts the complete game URL for the current event website', () => {
    expect(registrationQrContent(code, origin)).toBe(code)
  })
  it.each([
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://192.168.1.10:5173',
    'https://other.example',
  ])('uses the current website for a scanned game link from %s', (address) => {
    expect(registrationQrContent(`${address}/join/${'a'.repeat(43)}`, origin)).toBe(code)
  })
  it.each([
    'javascript:alert(1)',
    'hello',
    '/join/' + 'a'.repeat(43),
    `${code}?redirect=admin`,
    `${code}#admin`,
    `${origin}/admin/login`,
    `${origin}/join/short`,
    `https://user:password@carnival.example/join/${'a'.repeat(43)}`,
  ])('rejects unrelated or altered QR content: %s', (value) => {
    expect(() => registrationQrContent(value, origin)).toThrow('not a Stack Moko Baby QR')
  })
})
