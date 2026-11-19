import { useEffect, useId, useRef, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Badge, Button, Card } from '../components/ui'
import { PublicHeader } from './Leaderboard'
import { useApp } from '../state/AppContext'
import { api } from '../state/api'
import { registrationQrContent } from '../state/qr-entry'

let scannerApi
function loadScannerApi() {
  scannerApi ||= import('html5-qrcode').catch((error) => {
    scannerApi = null
    throw error
  })
  return scannerApi
}
async function release(session) {
  if (!session || session.finished) return
  // The SDK may finish opening a camera after React has removed this page.
  // Keep its owned media host attached until start/stop settles, then remove it.
  if (session.starting && !session.element.isConnected && !session.parked) {
    session.parked = true
    session.element.setAttribute('aria-hidden', 'true')
    Object.assign(session.element.style, {
      position: 'fixed',
      left: '-10000px',
      top: '0',
      width: '320px',
      height: '320px',
      opacity: '0',
      pointerEvents: 'none',
    })
    document.body.appendChild(session.element)
  }
  if (session.releasing) return session.releasing
  session.cancelled = true
  session.releasing = (async () => {
    await session.starting?.catch(() => {})
    // Let the browser settle the SDK's video.play() promise before removing it.
    if (session.starting) await new Promise((resolve) => setTimeout(resolve, 0))
    const stream = session.element?.querySelector('video')?.srcObject
    try {
      if (session.scanner.isScanning) await session.scanner.stop()
    } catch {}
    stream?.getTracks().forEach((track) => {
      if (track.readyState !== 'ended') track.stop()
    })
    try {
      session.scanner.clear()
    } catch {}
    if (session.parked) session.element.remove()
    session.finished = true
  })()
  return session.releasing
}
export default function Scanner({ message }) {
  const id = useId().replaceAll(':', '')
  const cameraId = `qr-camera-${id}`
  const fileId = `qr-file-${id}`
  const { refreshPlayer, ticket } = useApp()
  const navigate = useNavigate()
  const [mode, setMode] = useState('idle')
  const [error, setError] = useState('')
  const camera = useRef(null)
  const imageScanner = useRef(null)
  const fileInput = useRef(null)
  const mounted = useRef(true)
  const validating = useRef(false)
  const uploading = useRef(false)
  const cameraRequest = useRef(0)
  const request = useRef(null)
  const busy = ['requesting', 'image', 'verifying'].includes(mode)
  useEffect(() => {
    mounted.current = true
    return () => {
      mounted.current = false
      cameraRequest.current++
      request.current?.abort()
      void release(camera.current)
      void release(imageScanner.current)
    }
  }, [])

  async function detected(text, method, session) {
    if (!mounted.current || validating.current || session.cancelled) return
    let qrContent
    try {
      qrContent = registrationQrContent(text)
    } catch (e) {
      setError(e.message)
      return
    }
    validating.current = true
    setError('')
    setMode('verifying')
    if (camera.current?.scanner.isScanning) await release(camera.current)
    else void release(camera.current)
    if (!mounted.current) return
    request.current = new AbortController()
    try {
      await api('/player/entry', {
        method: 'POST',
        body: { qrContent, method },
        signal: request.current.signal,
      })
      const context = await refreshPlayer()
      if (!mounted.current) return
      navigate(
        context.ticket && ['waiting', 'called', 'playing', 'review'].includes(context.ticket.status)
          ? '/ticket'
          : '/register',
        { replace: true },
      )
    } catch (e) {
      if (mounted.current && e.name !== 'AbortError') {
        setError(e.message)
        setMode('idle')
      }
    } finally {
      validating.current = false
    }
  }
  async function startCamera() {
    if (busy || mode === 'camera') return
    if (!window.isSecureContext || !navigator.mediaDevices?.getUserMedia) {
      setError('Camera scanning needs HTTPS or localhost. You can upload a QR image instead.')
      return
    }
    const sequence = ++cameraRequest.current
    setError('')
    setMode('requesting')
    try {
      await release(camera.current)
      const { Html5Qrcode, Html5QrcodeSupportedFormats } = await loadScannerApi()
      // The SDK's permission probe closes its temporary stream itself. Check
      // cancellation before creating a video preview or starting a scanner.
      await Html5Qrcode.getCameras()
      if (!mounted.current || sequence !== cameraRequest.current) return
      const session = {
        scanner: new Html5Qrcode(cameraId, {
          formatsToSupport: [Html5QrcodeSupportedFormats.QR_CODE],
          verbose: false,
        }),
        element: document.getElementById(cameraId),
        cancelled: false,
      }
      camera.current = session
      session.starting = session.scanner.start(
        { facingMode: 'environment' },
        { fps: 8 },
        (text) => {
          void detected(text, 'camera', session)
        },
        () => {},
      )
      await session.starting
      if (!mounted.current || sequence !== cameraRequest.current || session.cancelled) {
        await release(session)
        return
      }
      if (!validating.current) setMode('camera')
    } catch {
      if (mounted.current && sequence === cameraRequest.current) {
        await release(camera.current)
        setMode('idle')
        setError(
          'The camera could not open. Allow camera access, check that it is not in use, or upload a QR image instead.',
        )
      }
    }
  }
  async function stopCamera() {
    cameraRequest.current++
    setMode('idle')
    setError('')
    await release(camera.current)
  }
  async function upload(event) {
    const file = event.target.files?.[0]
    event.target.value = ''
    if (!file || busy || uploading.current || validating.current) return
    if (
      !['image/png', 'image/jpeg', 'image/webp'].includes(file.type) ||
      file.size > 8 * 1024 * 1024 ||
      !file.size
    ) {
      setError('Choose a PNG, JPG or WebP image smaller than 8 MB.')
      return
    }
    cameraRequest.current++
    uploading.current = true
    let session
    setError('')
    setMode('image')
    try {
      if (camera.current?.scanner.isScanning) await release(camera.current)
      else void release(camera.current)
      await release(imageScanner.current)
      const { Html5Qrcode, Html5QrcodeSupportedFormats } = await loadScannerApi()
      if (!mounted.current) return
      session = {
        scanner: new Html5Qrcode(fileId, {
          formatsToSupport: [Html5QrcodeSupportedFormats.QR_CODE],
          verbose: false,
        }),
        element: document.getElementById(fileId),
        cancelled: false,
      }
      imageScanner.current = session
      let text
      try {
        text = await session.scanner.scanFile(file, false)
      } catch {
        if (!mounted.current || session.cancelled) return
        // A second maintained local API handles QR patterns the primary SDK
        // cannot read. Images never leave the browser; no decoder is hand-built.
        const { default: QrScanner } = await import('qr-scanner')
        text = (await QrScanner.scanImage(file, { returnDetailedScanResult: true })).data
      }
      await detected(text, 'upload', session)
      if (mounted.current && !validating.current) setMode('idle')
    } catch {
      if (mounted.current) {
        setError(
          'No readable QR code was found. Upload a clear image of the full code, including its white border.',
        )
        setMode('idle')
      }
    } finally {
      await release(session)
      uploading.current = false
    }
  }
  return (
    <div className="public-shell scanner-shell">
      <PublicHeader />
      <main id="main-content" className="scanner-layout">
        <section className="scanner-story">
          <Badge tone="lime">
            <i className="fa-solid fa-qrcode" aria-hidden="true" />
            START HERE
          </Badge>
          <h1 aria-label="Your game starts with a scan.">
            Your game starts
            <br />
            with a scan.
          </h1>
          <p>
            {message ||
              'One code. Your place in line. Scan the QR at Cabinet 01 to join the carnival.'}
          </p>
          <div className="scan-journey" role="list" aria-label="Player journey">
            <span role="listitem">
              <b>01</b>Scan the code
            </span>
            <span role="listitem">
              <b>02</b>Save your spot
            </span>
            <span role="listitem">
              <b>03</b>Make your stack
            </span>
          </div>
          <div className="scan-art" aria-hidden="true">
            <i className="fa-solid fa-qrcode" />
            <span className="scan-corner tl" />
            <span className="scan-corner tr" />
            <span className="scan-corner bl" />
            <span className="scan-corner br" />
            <span className="scan-art-pill">
              <i className="fa-solid fa-layer-group" />
              ONE MORE LEVEL.
            </span>
          </div>
        </section>
        <Card className="scanner-card">
          <div className="scanner-card-heading">
            <span className="eyebrow">YOUR WAY INTO THE GAME</span>
            <Badge tone="soft">Cabinet 01</Badge>
          </div>
          <h2>Ready when you are.</h2>
          <p>Use your camera or choose a saved QR image.</p>
          <div className={`scanner-view ${mode === 'camera' ? 'active' : ''}`}>
            <div
              id={cameraId}
              className="camera-reader"
              role="region"
              aria-label="Camera QR scanner"
            />
            {!['camera', 'requesting', 'verifying'].includes(mode) && (
              <div className="scan-placeholder">
                <span>
                  <i className="fa-solid fa-camera" aria-hidden="true" />
                </span>
                <strong>Point. Scan. You’re in.</strong>
                <p>Keep the full QR code inside the camera view.</p>
              </div>
            )}
            {mode === 'requesting' && (
              <div className="scan-overlay">
                <i className="fa-solid fa-spinner spin" aria-hidden="true" />
                <span>Allow camera access to begin.</span>
              </div>
            )}
            {mode === 'verifying' && (
              <div className="scan-overlay">
                <i className="fa-solid fa-spinner spin" aria-hidden="true" />
                <span>Checking your game QR…</span>
              </div>
            )}
          </div>
          <div className="scanner-status" role="status" aria-live="polite">
            {mode === 'camera'
              ? 'Camera is on. Looking for the cabinet QR code…'
              : mode === 'image'
                ? 'Reading your QR image…'
                : 'Your camera stays off until you choose to use it.'}
          </div>
          {error && (
            <p className="field-error scan-error" role="alert">
              {error}
            </p>
          )}
          {['camera', 'requesting'].includes(mode) ? (
            <Button tone="light" className="full-width" onClick={stopCamera}>
              <i className="fa-solid fa-stop" aria-hidden="true" />
              {mode === 'requesting' ? 'Cancel camera' : 'Stop camera'}
            </Button>
          ) : (
            <Button tone="lime" className="full-width" onClick={startCamera} disabled={busy}>
              <i className="fa-solid fa-camera" aria-hidden="true" />
              Use camera
            </Button>
          )}
          <div className="scan-divider">
            <span>or use an image</span>
          </div>
          <input
            ref={fileInput}
            type="file"
            id={`qr-upload-${id}`}
            className="sr-only"
            aria-label="QR code image"
            accept="image/png,image/jpeg,image/webp"
            disabled={busy}
            onChange={upload}
          />
          <Button
            tone="light"
            className="full-width scan-upload"
            onClick={() => fileInput.current?.click()}
            disabled={busy}
          >
            <i className="fa-solid fa-image" aria-hidden="true" />
            Upload QR image
          </Button>
          <p className="field-help scan-file-help">PNG, JPG or WebP · up to 8 MB</p>
          <div id={fileId} className="file-reader" aria-hidden="true" />
          <div className="scan-privacy">
            <i className="fa-solid fa-shield-halved" aria-hidden="true" />
            <p>
              Your images stay on this device. Only the detected game code is checked by the event
              server.
            </p>
          </div>
          {ticket && (
            <Link to="/ticket" className="text-button scan-ticket-link">
              Already joined? Open my ticket
              <i className="fa-solid fa-arrow-right" aria-hidden="true" />
            </Link>
          )}
        </Card>
      </main>
      <footer className="public-footer">Stack Moko Baby · Scan. Register. Stack.</footer>
    </div>
  )
}
