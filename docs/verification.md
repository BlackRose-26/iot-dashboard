# Current QR/queue/authentication verification

15 November 2026 · Canonical source: D:\iot-dashboard

- Applied both versioned migrations to the local application database on XAMPP MariaDB 10.11.16. The running API uses a restricted project account, not root. No real identities were used.
- Final frontend unit/component suite: **10 passed**. Production build and Prettier formatting pass.
- Final real-browser suite: **3 expanded scenarios passed** using headless Microsoft Edge against dedicated API/Vite servers and a disposable MariaDB database. Scenarios cover server-enforced admin login/logout, QR entry gating and canvas generation; two independent phone-sized player contexts; FIFO changes and persistence after reload; called/playing states; saved win and loss notifications; post-game leaderboard unlocking; neutral light/dark admin routes; theme persistence; mobile navigation and overflow.
- Automated accessibility: no axe WCAG A/AA violations in the 10 admin route/theme states or the two completed player leaderboard states checked. This does not claim a complete accessibility audit.
- Backend tests use disposable MariaDB databases, not SQLite or application records. They check unauthorized API access, CSRF/origin rejection, private identity handling, rate limits/session expiry, FIFO/concurrent idempotent assignment, registration replay/duplicate protection, paused admissions, cancellation/skip audit, both outcomes, terminal replay/conflict, scoring evidence, encryption/cookie attributes and leaderboard relocking for another round. Final backend result: **10 passed**, with one dependency deprecation warning from the Starlette/httpx test adapter. No runtime check failed.
- The application database was kept empty of test players and results. Browser screenshots use synthetic test names/codes only. Secrets, generated administrator credentials, database contents and screenshot/test artifacts are excluded from Graphify inputs.
- Physical ESP32 integration and phone-camera scanning were **not tested**. Device endpoint tests use synthetic authenticated HTTP requests. No live countdown, row telemetry or physical sound/LED control is claimed. The development simulator is explicitly labelled and separated from the device player leaderboard.
- Browser alerts are optional and permission dependent; on-page alerts were tested. Closed-tab push and production HTTPS/LAN access were not implemented or claimed as verified. The local in-app browser control service was unavailable; actual browser checks used installed Edge.

Earlier planning and sample-preview verification follows as historical evidence; its no-backend statements are superseded by player-flow-and-access.md.

# Project verification

15 November 2026 (Asia/Manila) · Project: `D:\iot-dashboard`

## First frontend implementation

- React JavaScript/JSX + Vite; eight implemented pages: overview, analytics, queue, sessions, machine, leaderboard, registration and player ticket.
- Standard Font Awesome Free **webfont** symbols throughout; no SVG icon library. QR is rendered on canvas. SVG is used for chart/data graphics only.
- Shared Radix primitives, CSS foundation variables, consistent components and locally hosted fonts.
- Five review/refinement passes for every page, recorded in [ui-iteration-log.md](ui-iteration-log.md). Screenshots are in `ui-review/` at 1440, 1024, 390, 1600 and 360 pixel widths.
- Final screenshot sweeps: all eight pages have no page overflow, no broken images and no JavaScript page errors at 1600 and 360 pixels; the corrected 390-pixel sweep also passes.
- Unit/component tests: **10 passed**. Covers ID format/leading zeros, registration validation and privacy, empty ratios, pooled accuracy, ranking and scoring fixtures.
- Browser checks: **15 passed** using installed Microsoft Edge. Covers mobile navigation, ticket creation/cancellation, cabinet guards, offline unknown readings, analytics empty state, queue controls, session details/export, QR/font icons and accessibility on all eight pages.
- Automated accessibility: no violations detected by axe for its WCAG A/AA rule set on the checked page states. This is not a full accessibility certification.
- Production build and formatting checks passed. Dependency versions are pinned with a lockfile.
- Local preview: [dashboard](http://127.0.0.1:5173/admin/overview), [registration](http://127.0.0.1:5173/register/acs-day/cabinet-01). Restart with `scripts/start-dashboard.cmd`.

## Scope boundaries

The frontend uses clearly labeled synthetic data and in-memory UI preview actions. Registration accepts a dummy ID for design testing and does not send it to a server or persist it in browser storage. There is no real staff authentication, database registration, ranked device reservation, external AI call or ESP32 connection yet. Preview tickets reset after a full page reload.

The in-app browser control service was unavailable during this task. Browser automation and screenshots used a local headless Edge session instead; the desktop preview-opening action was requested separately.

## Database evidence retained from planning

The installed XAMPP database binary reports **MariaDB 10.11.16**, with port **3306** in its inspected configuration. The candidate `schema.sql` uses `utf8mb4_unicode_ci`. All **16 tables** were created successfully in a fresh isolated MariaDB instance using that binary; the SQL parser also accepted all 19 statements. Existing XAMPP databases and accounts were untouched. Concurrency, migrations and application integration still require their build-phase checks.

## Project map

Local Graphify 0.9.109 is installed. Source extraction excludes dependencies, build output, private files and screenshot artifacts. The map is refreshed after source changes; document semantics are refreshed separately. See [graphify-setup.md](graphify-setup.md). Graph integrity and map size are recorded in `graphify-out/build-summary.json`.


## Current implementation map verification

The code map now contains 339 nodes and 959 edges. A registration query returned actual frontend source references. Graphify reports limited CSS/import/test relationship extraction: three raw CSS targets are unresolved and two repeated endpoint pairs can collapse. Source files remain authoritative. Exact semantic token usage is not exposed by the host tool; any zero counters mean unreported.

## Final project-map refresh for QR and access implementation

Graphify structural update completed after the code changes, and document semantics were re-extracted with complete coverage of the 13 changed document inputs. The final map contains 501 nodes, 1,420 relationships and 29 communities. Both `query` and `explain` located current QR registration, private player context and administrator route guards. Private credential/environment files are absent from node source references.

Raw extraction diagnostics retain 79 dangling candidate references, three external stylesheet references and 11 same-endpoint relationship groups before reference resolution/edge collapse; these are map-model limitations, not evidence of failed application checks. Eight code/config/test files yielded no symbols and CSS is not structurally classified. Community names were preserved or derived from hubs after the update. Graph output is navigation evidence and does not establish hardware connectivity.
## Standard local toolchain setup

Node.js 24.22.3 and npm 11.19.1 were installed for the user account from the official Node.js distribution with SHA256 verification. Python 3.13.17 was installed per-user using the Python Software Foundation installer verified by winget. User PATH entries were added; PowerShell script execution policy was not changed. npm uses its Windows command entry point. Restart the terminal application to inherit the new PATH.

A clean npm lockfile and dependency installation replaced the previous pnpm-linked dependency layout. The previous dependency folder was partially preserved under the ignored `.tools` directory during migration. A regular `backend/.venv` was created and all pinned Python requirements installed successfully. The normal `npm run dev` command started Vite and returned HTTP 200. `npm run build` and all 10 frontend tests passed. All 10 backend tests passed under the new Python 3.13 environment; pip reported no broken requirements. The new backend environment started successfully and its health endpoint connected to XAMPP MariaDB. Test servers were stopped after verification.
## Camera and QR-image scanner implementation

The player scanner at `/` and `/scan` uses the existing html5-qrcode 2.3.8 API for camera permission, camera start/stop and image decoding. No custom decoder or remote image service was created. The token-only entry request was replaced by validated `qrContent` plus `method`; merely opening `/join/:token` no longer grants registration. QR exports now have a 480px source canvas displayed at the original 240px size to improve image reads. Video preserves its natural aspect ratio so the SDK receives an undistorted camera view.

Verification: 20 frontend tests and 11 backend tests passed, with a successful production build and formatting checks. The full seven-scenario Edge suite passed for scan-to-registration-to-queue/results, actual image decoding, invalid-code rejection, permission denial and synthetic camera streams. A later strict check exposed the SDK's handling of a permission request finishing after navigation; the final implementation uses its getCameras permission probe and handles late stream cleanup. The three camera regression scenarios then passed with the explicit no-page-error assertion, including cancellation followed by image upload. Desktop and phone scanner screenshots are in the excluded `ui-review` folder. Physical phone cameras and production HTTPS were not tested. Only disposable test database records and synthetic stream/image fixtures were used. User-started frontend/backend servers were preserved.

Five scanner review passes covered the shared player layout, SDK/API integration, server entry validation, responsive/accessibility refinements and camera/image lifecycle regressions. Six changed documentation inputs were semantically re-extracted for Graphify, followed by the structural code update. Camera frames, uploaded files, credentials and real identities were not indexed.

## QR hostname correction — 16 November 2026

Removed the frontend's strict comparison of the printed QR hostname with the open website. Valid /join token paths are normalized to the current origin before submission; backend active/registered-token validation remains enabled. Exported the current event QR to frontend/public/stack-moko-baby-registration-qr.png, excluded from Git and Graphify. No tests, browser checks, image decoding or build verification were run for this change, at the user's request. Graphify document semantics and the code map were refreshed.


## Backend request-origin compatibility — 16 November 2026

Changed browser-write and QR-entry checks to a shared origin policy. Localhost, 127.0.0.1 and IPv6 loopback are treated as permitted aliases at the same scheme/port; configured public/additional origins and the browser-facing request host are accepted. Development mode permits the standard local frontend ports. Vite explicitly preserves the browser-facing Host header without rewriting Origin. CSRF, authentication and registered/enabled QR token checks remain active. No tests, application requests, browser checks or builds were run, per user instruction. Restart backend/frontend to load the changes. Graphify documentation and code maps were refreshed.
