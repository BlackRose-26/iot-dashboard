import { useEffect, useId, useRef, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Badge, Button, Card } from '../components/ui'
import { PublicHeader } from './Leaderboard'
import RobotIcon from '../components/RobotIcon'
import { GameBand, LiveTiles, TodayStrip, openRobotChat, steps } from '../components/SiteSections'
import * as ui from '../components/siteStyles'
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
      <main id="main-content">
        <div className="tw:grid tw:grid-cols-[minmax(0,1fr)_minmax(0,500px)] tw:max-[1000px]:grid-cols-[minmax(0,1fr)_minmax(0,420px)] tw:max-[760px]:grid-cols-1 tw:gap-x-16 tw:max-[1000px]:gap-x-9 tw:gap-y-5 tw:max-[760px]:gap-y-3.5 tw:items-center tw:pt-12 tw:pb-8 tw:max-[760px]:pt-5 tw:max-[760px]:pb-4">
          <section className="tw:flex tw:flex-col tw:gap-5">
            <span className={`${ui.pill} ${ui.enter}`}>ACS CARNIVAL · CABINET 01</span>
            <h1
              className={`tw:mt-[22px] tw:mb-4 tw:max-[760px]:mt-4 tw:max-[760px]:mb-2.5 tw:text-[clamp(40px,4.6vw,64px)] tw:max-[760px]:text-[36px] tw:font-extrabold tw:tracking-[-2.4px] tw:max-[760px]:tracking-[-1.4px] tw:leading-[1.02] ${ui.enter} ${ui.delays[1]}`}
              aria-label="Your game starts with a scan."
            >
              Your game starts
              <br />
              with a scan.
            </h1>
            <p
              className={`tw:m-0 tw:max-w-[460px] tw:text-[16px] tw:max-[760px]:text-[15px] tw:leading-[1.6] tw:text-note ${ui.enter} ${ui.delays[2]}`}
            >
              {message ||
                'Scan the QR beside the cabinet, pick a nickname and keep your place in line. Your phone tells you when it’s your turn.'}
            </p>
            <LiveTiles />
            <div className={`tw:flex tw:flex-wrap tw:gap-3 ${ui.enter} ${ui.delays[4]}`}>
              <a href="#how" className={ui.button}>
                How it works
                <i className="fa-solid fa-arrow-down" aria-hidden="true" />
              </a>
              <button type="button" className={ui.buttonDark} onClick={openRobotChat}>
                <span className={ui.robotChip}>
                  <RobotIcon size={26} tone="ink" />
                </span>
                Ask the robot
              </button>
            </div>
          </section>
          <Card
            className={`sp-card tw:bg-night tw:text-cloud tw:border-0 tw:rounded-[40px] tw:p-7 tw:max-[760px]:p-[22px] ${ui.enter} ${ui.delays[2]}`}
          >
            <div className="tw:flex tw:items-center tw:justify-between tw:gap-3 tw:mb-[18px]">
              <span className="tw:text-[13px] tw:font-extrabold tw:tracking-[1px] tw:uppercase tw:text-cloud">
                Scan to join
              </span>
              <Badge tone="soft" className="tw:bg-cloud/12 tw:text-cloud">
                Cabinet 01
              </Badge>
            </div>
            <div
              className={`tw:relative tw:min-h-[300px] tw:max-[760px]:min-h-[260px] tw:rounded-[30px] tw:bg-cloud/4 tw:border-[1.5px] tw:border-solid tw:border-cloud/18 tw:overflow-hidden tw:[&_.camera-reader_video]:rounded-[30px] tw:[&_.scan-overlay]:rounded-[30px] tw:[&_.scan-overlay]:bg-night/88 tw:[&_.scan-overlay]:text-cloud ${mode === 'camera' ? 'active' : ''}`}
            >
              <div
                id={cameraId}
                className="camera-reader"
                role="region"
                aria-label="Camera QR scanner"
              />
              {!['camera', 'requesting', 'verifying'].includes(mode) && (
                <button
                  type="button"
                  className="tw:group tw:absolute tw:inset-0 tw:w-full tw:border-0 tw:p-0 tw:bg-transparent tw:text-white tw:cursor-pointer tw:flex tw:items-center tw:justify-center tw:disabled:cursor-default tw:disabled:opacity-70 tw:focus-visible:outline-4 tw:focus-visible:outline-solid tw:focus-visible:outline-lime tw:focus-visible:-outline-offset-8 tw:focus-visible:rounded-[30px]"
                  onClick={startCamera}
                  disabled={busy}
                  aria-label="Use camera"
                >
                  <span
                    className="tw:absolute tw:w-10 tw:h-10 tw:border-0 tw:border-solid tw:border-lime tw:left-[22%] tw:max-[760px]:left-[18%] tw:top-[34px] tw:border-l-4 tw:border-t-4 tw:rounded-tl-[12px]"
                    aria-hidden="true"
                  />
                  <span
                    className="tw:absolute tw:w-10 tw:h-10 tw:border-0 tw:border-solid tw:border-lime tw:right-[22%] tw:max-[760px]:right-[18%] tw:top-[34px] tw:border-r-4 tw:border-t-4 tw:rounded-tr-[12px]"
                    aria-hidden="true"
                  />
                  <span
                    className="tw:absolute tw:w-10 tw:h-10 tw:border-0 tw:border-solid tw:border-lime tw:left-[22%] tw:max-[760px]:left-[18%] tw:bottom-24 tw:border-l-4 tw:border-b-4 tw:rounded-bl-[12px]"
                    aria-hidden="true"
                  />
                  <span
                    className="tw:absolute tw:w-10 tw:h-10 tw:border-0 tw:border-solid tw:border-lime tw:right-[22%] tw:max-[760px]:right-[18%] tw:bottom-24 tw:border-r-4 tw:border-b-4 tw:rounded-br-[12px]"
                    aria-hidden="true"
                  />
                  <span
                    className="tw:absolute tw:left-[24%] tw:right-[24%] tw:top-[22%] tw:h-[3px] tw:rounded-full tw:bg-lime tw:shadow-[0_0_12px_#dfff00] tw:motion-safe:animate-scan-line tw:motion-reduce:hidden"
                    aria-hidden="true"
                  />
                  <i
                    className="fa-solid fa-qrcode tw:text-[64px] tw:opacity-90 tw:-mt-11"
                    aria-hidden="true"
                  />
                  <span
                    className="tw:absolute tw:bottom-6 tw:flex tw:items-center tw:gap-2.5 tw:bg-lime tw:text-night tw:rounded-full tw:px-[26px] tw:py-[13px] tw:text-[16px] tw:font-extrabold tw:group-hover:bg-white tw:motion-safe:transition-colors tw:motion-safe:duration-[120ms]"
                    aria-hidden="true"
                  >
                    <i className="fa-solid fa-camera" />
                    Tap to scan
                  </span>
                </button>
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
            <div
              className="scanner-status tw:text-[13px] tw:text-cloud/75 tw:min-h-0 tw:mt-[14px] tw:mx-1 tw:mb-4"
              role="status"
              aria-live="polite"
            >
              {mode === 'camera'
                ? 'Camera is on. Looking for the cabinet QR code…'
                : mode === 'image'
                  ? 'Reading your QR image…'
                  : 'Your camera stays off until you choose to use it.'}
            </div>
            {error && (
              <p className="field-error scan-error tw:bg-lime tw:text-night" role="alert">
                {error}
              </p>
            )}
            {['camera', 'requesting'].includes(mode) && (
              <Button tone="light" className="full-width" onClick={stopCamera}>
                <i className="fa-solid fa-stop" aria-hidden="true" />
                {mode === 'requesting' ? 'Cancel camera' : 'Stop camera'}
              </Button>
            )}
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
              className="full-width tw:bg-transparent tw:text-cloud tw:border-[1.5px] tw:border-solid tw:border-cloud/55 tw:min-h-[52px] tw:text-[15px] tw:hover:bg-cloud/10"
              onClick={() => fileInput.current?.click()}
              disabled={busy}
            >
              <i className="fa-solid fa-image" aria-hidden="true" />
              Upload QR image
            </Button>
            <p className="tw:flex tw:gap-2.5 tw:items-start tw:mt-[14px] tw:mx-1 tw:mb-0 tw:text-[12px] tw:leading-[1.55] tw:text-cloud/75">
              <i className="fa-solid fa-shield-halved tw:pt-0.5" aria-hidden="true" />
              PNG, JPG or WebP up to 8 MB. Images stay on this device; only the game code is
              checked.
            </p>
            <div id={fileId} className="file-reader" aria-hidden="true" />
            {ticket && (
              <Link
                to="/ticket"
                className="text-button scan-ticket-link tw:text-lime tw:text-[14px]"
              >
                Already joined? Open my ticket
                <i className="fa-solid fa-arrow-right" aria-hidden="true" />
              </Link>
            )}
          </Card>
        </div>
        <section className={ui.section} aria-labelledby="how">
          <h2 id="how" className={ui.h2}>
            How it works
          </h2>
          <ol className={ui.grid}>
            {steps.map(([title, text], index) => (
              <li key={title} className={`${ui.box} ${ui.enter} ${ui.delays[index]}`}>
                <span className={ui.num}>{index + 1}</span>
                <h3 className={ui.boxTitle}>{title}</h3>
                <p className={ui.boxText}>{text}</p>
              </li>
            ))}
          </ol>
        </section>
        <section className={ui.section} aria-label="Today at the cabinet">
          <TodayStrip />
        </section>
        <section className={ui.section} aria-labelledby="rules">
          <GameBand />
        </section>
      </main>
      <footer className="public-footer">Stack Moko Baby · Scan. Register. Stack.</footer>
    </div>
  )
}
