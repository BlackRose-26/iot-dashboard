// Square-wave beeps for the web game screen, ported from firmware/stack_moko_baby/sounds.h.
// Each note is [hz, ms]; hz 0 is a rest. The firmware adds a 10 ms gap after every note.
export const SOUNDS = {
  countdown: [
    [880, 120],
    [0, 360],
    [880, 120],
    [0, 360],
    [880, 120],
    [0, 360],
    [1760, 250],
  ],
  loss: [
    [392, 160],
    [330, 160],
    [262, 420],
  ],
  win: [
    [523, 120],
    [659, 120],
    [784, 120],
    [1047, 380],
  ],
  place: [[1200, 30]],
}

let context = null

// Browsers allow audio only after a click or key press; call this from one.
export function unlockAudio() {
  const Audio = window.AudioContext || window.webkitAudioContext
  if (!Audio) return
  context ??= new Audio()
  if (context.state === 'suspended') void context.resume()
}

export function playSound(name, volume = 0.12) {
  if (!context || context.state !== 'running') return
  let at = context.currentTime + 0.01
  for (const [hz, ms] of SOUNDS[name]) {
    if (hz) {
      const oscillator = context.createOscillator()
      const gain = context.createGain()
      oscillator.type = 'square'
      oscillator.frequency.value = hz
      gain.gain.setValueAtTime(volume, at)
      gain.gain.setValueAtTime(0, at + ms / 1000)
      oscillator.connect(gain).connect(context.destination)
      oscillator.start(at)
      oscillator.stop(at + ms / 1000 + 0.01)
    }
    at += (ms + 10) / 1000
  }
}
