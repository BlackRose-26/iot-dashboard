import { describe, expect, it } from 'vitest'
import { ClockMap, parseLine } from './button'

describe('button bridge lines', () => {
  it('parses READY and PRESS lines only', () => {
    expect(parseLine('READY\r')).toEqual({ type: 'ready' })
    expect(parseLine('PRESS 12345')).toEqual({ type: 'press', espMs: 12345 })
    expect(parseLine('PRESS -1')).toBeNull()
    expect(parseLine('Cabinet ready')).toBeNull()
  })

  it('keeps the lowest-delay offset and resets after an ESP32 restart', () => {
    const map = new ClockMap()
    expect(map.toPage(1000, 5008)).toBe(5008)
    expect(map.toPage(2000, 6003)).toBe(6003) // less USB delay: better offset
    expect(map.toPage(3000, 7010)).toBe(7003) // late delivery keeps the edge time
    expect(map.toPage(5, 9000)).toBe(9000) // clock went back to zero: new offset
  })
})
