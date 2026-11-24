// Arcade button input for the web game screen.
// The ESP32 runs firmware/button_bridge and prints one line per press over USB:
//   READY            at boot and every 5 s (the bridge is alive)
//   PRESS <millis>   the ESP32's own time of the button's falling edge
// Chrome/Edge read it with Web Serial (HTTPS or localhost only).

export const BAUD_RATE = 115200

export function parseLine(line) {
  const text = line.trim()
  if (text === 'READY') return { type: 'ready' }
  const match = /^PRESS (\d{1,12})$/.exec(text)
  return match ? { type: 'press', espMs: Number(match[1]) } : null
}

// Maps ESP32 milliseconds to page time. The smallest (page - esp) gap seen is the
// closest to zero USB delay, so presses keep the button's own timing.
export class ClockMap {
  constructor() {
    this.offset = null
  }

  reset() {
    this.offset = null
  }

  toPage(espMs, receivedAt) {
    const candidate = receivedAt - espMs
    // A much larger gap means the ESP32 restarted (its clock went back to zero).
    if (this.offset == null || candidate < this.offset || candidate - this.offset > 2000)
      this.offset = candidate
    return espMs + this.offset
  }
}

export function serialSupported() {
  return typeof navigator !== 'undefined' && 'serial' in navigator
}

// Reads lines from one serial port and reconnects to an already-allowed port.
export class SerialButton {
  constructor({ onPress, onStatus, clock }) {
    this.onPress = onPress
    this.onStatus = onStatus
    this.clock = clock
    this.map = new ClockMap()
    this.port = null
    this.reader = null
    this.stopped = false
    this.onConnect = () => this.reconnect()
    if (serialSupported()) navigator.serial.addEventListener('connect', this.onConnect)
  }

  status(state, detail = '') {
    this.onStatus?.({ state, detail })
  }

  // Needs a click (browser rule) the first time; later visits use reconnect().
  async choose() {
    if (!serialSupported()) throw new Error('This browser has no Web Serial. Use Chrome or Edge.')
    const port = await navigator.serial.requestPort()
    await this.open(port)
  }

  async reconnect() {
    if (!serialSupported() || this.port) return false
    const [port] = await navigator.serial.getPorts()
    if (!port) {
      this.status('none')
      return false
    }
    await this.open(port)
    return true
  }

  async open(port) {
    try {
      await port.open({ baudRate: BAUD_RATE })
    } catch (error) {
      // Already open (for example after a hot reload) is fine; anything else is not.
      if (!String(error?.message).includes('already open')) {
        this.status('error', 'The button port is busy. Close the Arduino serial monitor and retry.')
        throw error
      }
    }
    this.port = port
    this.map.reset()
    this.status('connected')
    void this.read(port)
  }

  async read(port) {
    const decoder = new TextDecoder()
    let buffer = ''
    while (port.readable && !this.stopped) {
      this.reader = port.readable.getReader()
      try {
        for (;;) {
          const { value, done } = await this.reader.read()
          if (done) break
          const receivedAt = this.clock()
          buffer += decoder.decode(value, { stream: true })
          let newline
          while ((newline = buffer.search(/\r?\n/)) >= 0) {
            const message = parseLine(buffer.slice(0, newline))
            buffer = buffer.slice(buffer[newline] === '\r' ? newline + 2 : newline + 1)
            if (message?.type === 'ready') this.status('connected')
            if (message?.type === 'press') this.onPress(this.map.toPage(message.espMs, receivedAt))
          }
          if (buffer.length > 256) buffer = ''
        }
      } catch {
        break // unplugged or reset; the 'connect' event brings it back
      } finally {
        this.reader.releaseLock()
      }
    }
    this.port = null
    if (!this.stopped) this.status('lost', 'Button unplugged. Plug the ESP32 back in.')
    try {
      await port.close()
    } catch {
      /* already closed */
    }
  }

  async stop() {
    this.stopped = true
    if (serialSupported()) navigator.serial.removeEventListener('connect', this.onConnect)
    try {
      await this.reader?.cancel()
    } catch {
      /* ignore */
    }
  }
}
