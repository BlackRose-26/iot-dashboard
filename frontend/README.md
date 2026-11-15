# Stack Moko Baby frontend

React JavaScript/JSX and Vite, connected to FastAPI and XAMPP MariaDB. Start with [backend setup](../backend/README.md), then run `D:\iot-dashboard\scripts\start-dashboard.cmd` and open [admin login](http://127.0.0.1:5173/admin/login). The generated credentials are in the private local file `backend/.admin-credentials.txt`.

Node.js 24 and npm are installed for the local user account. Restart your terminal app once after setup so it picks up the installed commands. Normal development commands:

```powershell
cd D:\iot-dashboard\frontend
npm ci
npm run dev
```

The frontend proxies `/api` to the local backend at port 8000. XAMPP MySQL and the API must be running. Do not put database credentials, identity keys or an administrator password in frontend environment variables. `VITE_PUBLIC_BASE_URL` is an optional public event address for QR links, never a secret.

## Pages and access

The five administrator pages under `/admin` require a valid server session: overview, analytics, queue, sessions and machine. `/admin/login` is the only sign-in page. Neutral light/dark themes apply to all admin pages and portals. The toggle stores only the theme preference.

Players choose camera or QR-image upload at `/scan`, using the existing html5-qrcode API. Opening `/join/:token` alone shows the scanner; only a detected code checked by the server issues an entry grant for `/register`; successful registration opens `/ticket`, showing only that player's position and state. A completed win or loss displays a result notification and unlocks `/leaderboard/acs-day`. There are no dashboard links in player views. Direct registration, ticket guessing and direct pre-game leaderboard access do not bypass server checks.

The player keeps their place across refreshes through a private HttpOnly cookie. Student ID is required, sent only in the registration POST and cleared from the form after the attempt. It is never placed in URLs, browser storage, public ticket data or analytics. The server encrypts it at rest. Keep HTTP development testing to dummy IDs; configure a trusted HTTPS event address before real phone registration.

## Shared design system

`styles/foundation.css` defines shared tokens; `components/ui.jsx` supplies cards, fields, badges and accessible Radix dialogs/menus. `styles/access-and-themes.css` scopes neutral administrator themes; player pages retain the Sourcio-derived gray canvas, rounded white cards, lime and blue accents. Inter and Font Awesome fonts are bundled locally. All symbols use **Font Awesome Free webfonts**, with no SVG icon library. Recharts and the gauge use data graphics; QR rendering uses canvas.

Dashboard numbers come from saved database results. Unknown hardware readings stay unknown; no live timer, row progress or Wi-Fi signal is invented. Development simulator results are clearly marked and use a separate player leaderboard. AI explanations remain deterministic summaries, labelled as not AI-generated; no model provider is connected. Device firmware and live progress telemetry are not implemented.

Polling refreshes queue/ticket state every two seconds and on focus. In-page result alerts work while open. Optional browser notifications require support and user permission; closed-tab push is not implemented. Phone/LAN access, HTTPS and operational limits are described in [player flow and access](../docs/player-flow-and-access.md).

## Checks

```powershell
npm test
npm run build
npx prettier --check src scripts e2e *.js *.json index.html
```

For the real multi-browser flow and accessibility checks, run `.tools\backend-venv\Scripts\python.exe backend\run_browser_tests.py` from the project root. It uses isolated test servers and a disposable XAMPP database, not the application database. Direct `pnpm test:browser` expects those dedicated servers and test credentials to be supplied. Review screenshots are excluded from Git and Graphify.
