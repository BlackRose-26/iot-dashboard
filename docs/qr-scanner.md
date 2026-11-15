# Player QR scanner

15 November 2026. The user requires camera or uploaded-image scanning and an existing scanner API. The implementation uses **html5-qrcode 2.3.8**, installed through npm and loaded only when scanning begins. It uses the documented `Html5Qrcode.start()`, `stop()`, `clear()` and `scanFile()` APIs. There is no custom QR decoder or external image-upload service. [Official scanner API](https://scanapp.org/html5-qrcode-docs/docs/apis/classes/Html5Qrcode).

## Player flow

1. Open `/` or `/scan` on the event website. Choose **Use camera** or **Upload QR image**.
2. The scanner API reads the QR code locally. Camera permission is requested only after a click. Uploads accept PNG, JPG or WebP images up to 8 MB. Images and video are not sent to the application server or any third-party service.
3. The app checks that detected content is a complete HTTP(S) game-entry URL with the expected `/join/{token}` shape. It normalizes that path to the website currently open, so codes printed with localhost, 127.0.0.1, a LAN address or another hostname can carry the same registered game token. It never follows or requests the decoded host.
4. The backend checks the URL origin and active registered QR token, then issues a two-hour private entry grant. The existing registration, private queue, physical-button game and post-result leaderboard flow continues.

Opening or pasting `/join/:token` now opens the scanner rather than granting entry. This intentionally supersedes the previous link-only exchange. A native phone camera may first open that URL; the in-app scanner/image workflow is still required before registration is unlocked. An existing authenticated player may return directly to their own ticket.

The scanner reads **QR_CODE only**, not arbitrary barcode formats. Invalid images, unrelated codes, inactive/unregistered game tokens do not unlock registration. Camera permission failures leave image upload available. Camera scanning stops after detection, when explicitly stopped, when switching to a file or when leaving the page. Camera/video content is never logged or persisted by the app.

Camera access needs a secure browser context: HTTPS for phones, with localhost available for desktop development. HTTP LAN addresses may serve the page and support image selection but cannot provide browser camera access. Permission and physical camera behavior still require testing on the actual phones and trusted event hostname. [Browser camera requirements](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia).

## Entry contract and limits

`POST /api/player/entry` takes JSON:

```json
{
  "qrContent": "https://event.example/join/{registered43CharacterToken}",
  "method": "camera"
}
```

`method` is `camera` or `upload`; the old token-only request is rejected. The server independently validates the content and checks `qr_links.enabled` before issuing the grant cookie. There is no direct manual-token or pasted-URL input in the scanner UI. Uploaded images remain in the browser; only the decoded content and method are posted.

This is validated scan-driven navigation, not camera attestation. The method is a client report; someone who already knows a valid public QR's contents could reproduce its entry request. Scanning does not start a physical round or award a score. Queue assignment remains an authenticated server transaction and the ESP32 remains responsible for physical game timing and button presses. All student-ID and admin access protections remain unchanged.

## Verification

The browser suite generates actual QR PNGs from the admin's QR canvas and feeds them through `scanFile()`. It checks rejection of unrelated files and normalization of a registered QR printed with a different hostname, verifies that merely opening the QR URL grants nothing, and confirms the subsequent registration/queue/result flow. Camera tests feed a synthetic `MediaStream` through the real scanner API, check detection and track release, and test permission denial. This does not claim that a physical phone camera was tested. Scanner layout is reviewed at desktop and phone widths, with Font Awesome webfont symbols and no SVG icon assets.


## Hostname compatibility correction

The strict frontend origin equality check was removed because a valid QR printed with 127.0.0.1 was rejected when the player opened localhost (and similarly for LAN addresses). Only the /join token path is reused on the current website; the backend still checks that the token is registered and enabled. A fresh current-event PNG is saved at frontend/public/stack-moko-baby-registration-qr.png by scripts/export-registration-qr.py. This machine-specific public QR artifact is excluded from Git and Graphify inputs. Regression expectations were updated, but no tests, browser checks or build verification were run for this correction, as requested by the user.

## Request-origin compatibility correction — 16 November 2026

The backend now shares one origin policy between browser-write protection and QR entry. It recognizes localhost, 127.0.0.1 and IPv6 loopback as explicitly permitted aliases at the same scheme and port. It accepts the configured public website, any explicit comma-separated `STACK_ALLOWED_ORIGINS`, and the current request host. Development mode additionally permits the normal local frontend ports 5173 and 4173. The Vite development/preview proxy explicitly preserves the browser-facing Host header so LAN addresses remain usable. Browser Origin headers are not rewritten, unrelated origins are still rejected, and authenticated writes still require their CSRF token. A production reverse proxy must preserve the public host or use an explicitly configured frontend origin.

Restart the backend and frontend after this configuration change. No tests, browser requests or build checks were run for this correction, following the user's instruction to test it themselves.
