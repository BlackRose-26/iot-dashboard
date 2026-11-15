# Stack Moko Baby backend

FastAPI, SQLAlchemy Core and the local XAMPP MariaDB service. This first implementation supports one event (`acs-day`), one cabinet (`cabinet-01`) and the proposed Classic v1 ruleset. It does not implement ESP32 firmware or AI analytics.

## Local startup

The project now uses a normal Python 3.13 environment at `D:\iot-dashboard\backend\.venv`. See [local setup and daily commands](../docs/local-setup.md). The earlier `.tools/backend-venv` remains a compatibility fallback.

1. Start MySQL in XAMPP (the installed server is MariaDB 10.11.16).
2. Run `backend\.venv\Scripts\python.exe backend\setup_local.py` from the project root. This creates only the named project database, applies versioned migrations, grants a restricted application account and generates local secrets. Reruns preserve data and passwords. If your local root account has a password, supply `STACK_DB_ROOT_PASSWORD` privately through the environment.
3. Start the complete app with `scripts\start-dashboard.cmd`, or start the API with `backend\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --no-access-log` and the Vite frontend separately.
4. Open `/admin/login`. The generated administrator username and password are in `backend/.admin-credentials.txt`. That file and `backend/.env` are excluded from Git and Graphify. Do not share them.

For a new environment, create a Python 3.13 virtual environment and install `backend/requirements.txt`. The setup command uses a local root account only for provisioning. The running API uses the restricted account, never root. Browser tests use root solely to create and remove a uniquely named disposable test database.

## Player journey and verification

Admin → Registration QR → scan on a separate browser/phone → register → private ticket → called → playing → win/loss notification → unlocked leaderboard. Refreshing the page preserves the ticket through an HttpOnly cookie. Players now use the camera/image scanner API at /scan; opening a copied QR URL alone does not grant entry. See docs/qr-scanner.md for the entry contract and its attestation limits. Registration is unavailable without a valid, unexpired entry grant. Players have no dashboard links or administrative API access.

The admin Machine page contains a **development simulator**: set it ready, call the next player on Queue, start the test round, then choose win or loss. Simulator results are stored with their source and use a separate player leaderboard from device results. Set `STACK_SIMULATOR_ENABLED=false` for real events. An ESP32 must implement the documented authenticated heartbeat/start/result contract before physical rounds work.

On-page status and result alerts work while the ticket is open. Browser notifications are optional, requested by a button, require browser support/permission and usually HTTPS. Closed-tab push, SMS and email notifications are not implemented. Background browser polling may be throttled; returning to the page refreshes its state. Tickets and notifications are fetched every two seconds; no WebSocket server is claimed.

For phones, set `STACK_PUBLIC_URL` and optional frontend `VITE_PUBLIC_BASE_URL` to a reachable event address and restart services. The QR dialog also lets an operator select that public base address. Both phone and computer must reach the same service; `127.0.0.1` points to each device itself. Use a trusted HTTPS reverse proxy and `STACK_COOKIE_SECURE=true` before collecting real IDs over the network. Local HTTP is for development with dummy identities. Firewall and router configuration are not automatically changed.

## Security and operations

- Argon2id administrator password hashes; separate admin/player opaque cookies, server expiry, logout revocation, HttpOnly, SameSite Strict, CSRF header and same-origin write checks. Login throttles eight failures per username/client address per 15 minutes. There is no public admin signup.
- Student IDs are trimmed without dropping leading zeros, looked up using a keyed HMAC, and encrypted with AES-256-GCM and a per-record nonce. Neither the original ID nor the hash/ciphertext is returned through player/admin dashboard APIs. Validation errors do not echo request values. SQL parameters are hidden in diagnostic exceptions. Do not enable request-body logging.
- FIFO order is `(joined_at, id)`. Mutations acquire the event then cabinet lock. READ COMMITTED prevents an earlier authorization read from hiding another transaction’s committed reservation. The database also enforces one live ticket per player/event and one active session per cabinet. Call-next has an idempotency receipt; registration retries cannot add a second ticket. Skip requires a reason and records an audit entry.
- Scores are recomputed from placement evidence and proposed movement rules. A terminal result, placements, queue completion, notification and outbox entry commit together. Identical terminal retries return the original acknowledgement; conflicting terminal results fail. Physical game timing remains on the device.
- Keep encryption/HMAC keys backed up privately. `purge_after` is recorded; an automated retention job is not implemented yet. A lost browser session requires an operator recovery process; entering an existing student ID in another browser does not grant access to that player’s ticket.
- This is a local development implementation. Production HTTPS, credential rotation, event scheduling, identity retention/recovery operations, real device reconciliation/no-show handling and deployment hardening still need operational validation.

## Checks

From the project root:

```powershell
backend\.venv\Scripts\python.exe -m pytest backend\tests -q
backend\.venv\Scripts\python.exe backend\run_browser_tests.py
```

For pytest, run from `backend` instead if the project root does not provide the package import path. Browser checks create dedicated API/Vite servers on 8001/5174 and a disposable MariaDB database; application data is not used. The test account and IDs are synthetic. Screenshots are written to `docs/ui-review` and excluded from Git and Graphify.
