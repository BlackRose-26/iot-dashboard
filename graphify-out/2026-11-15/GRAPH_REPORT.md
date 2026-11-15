# Graph Report - iot-dashboard  (2026-11-15)

## Corpus Check
- 69 files · ~38,865 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: .css 5, (none) 3, .cmd 3)

## Summary
- 547 nodes · 1499 edges · 29 communities (25 shown, 4 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- icons.jsx / ui.jsx
- create_app() / main.py
- Current QR player flow and administrator access / Scanner detection checked before two-hour HttpOnly
- package.json / dependencies
- Implemented FastAPI XAMPP development backend / Connected React JavaScript frontend and access journ
- Scanner.jsx / Scanner()
- devDependencies / Registration.test.jsx
- 001_initial.sql / game_sessions
- schema.sql / game_sessions
- review-pages.mjs / @playwright/test
- Player QR scanner implementation and entry contract / Local camera and image scanning with explicit 
- main.jsx / @radix-ui/react-tooltip
- Documentation index and authority
- demo.js / demo.test.js
- Local React and backend setup / Start XAMPP MySQL before application servers
- 002_player_flow.sql / entry_grants
- Project maintenance instructions / Private-data exclusion from project graph
- flows.spec.js / @axe-core/playwright
- scripts / build
- MySQL-compatible schema baseline with current migration override / Atomic result transaction and non
- Architecture baseline with current implementation override / Confirmed React JavaScript JSX Vite fro
- vite.config.js / vite
- QR access and theme five-pass refinement log / Documented current Edge accessibility unit and produc
- .prettierrc.json / printWidth
- Pinned backend dependency manifest / Pinned Argon2 and cryptography security dependencies
- React main.jsx module entry and root mount / Stack Moko Baby frontend HTML entry

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 52 edges
2. `useApp()` - 32 edges
3. `Card()` - 29 edges
4. `Badge()` - 28 edges
5. `Registration()` - 28 edges
6. `Current QR player flow and administrator access` - 28 edges
7. `execute()` - 23 edges
8. `one()` - 22 edges
9. `now()` - 22 edges
10. `Button()` - 20 edges

## Surprising Connections (you probably didn't know these)
- `Private-data exclusion from project graph` --semantically_similar_to--> `Local camera and image scanning with explicit permission`  [INFERRED] [semantically similar]
  AGENTS.md → docs/qr-scanner.md
- `Exclude student identity and nicknames from provider context` --semantically_similar_to--> `Private-data exclusion from project graph`  [INFERRED] [semantically similar]
  docs/ai-system-rules.md → AGENTS.md
- `Implemented auth queue and simulator truth boundaries` --references--> `Current QR player flow and administrator access`  [EXTRACTED]
  AGENTS.md → docs/player-flow-and-access.md
- `Existing html5-qrcode scanner API requirement` --references--> `Player QR scanner implementation and entry contract`  [EXTRACTED]
  AGENTS.md → docs/qr-scanner.md
- `Documentation index and authority` --references--> `Implemented FastAPI XAMPP development backend`  [EXTRACTED]
  docs/README.md → backend/README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Daily XAMPP React and Python startup workflow** — docs_local_setup_start_xampp_mysql_before_application_servers, docs_local_setup_primary_react_npm_development_command, docs_local_setup_direct_backend__venv_uvicorn_startup_without_activation, docs_local_setup_local_admin_login_and_explicit_server_shutdown [EXTRACTED 1.00]
- **Local camera lifecycle with explicit support and attestation limits** — docs_qr_scanner_local_camera_and_image_scanning_with_explicit_permission, docs_qr_scanner_qr_only_scanning_errors_and_camera_cleanup, docs_qr_scanner_phone_camera_https_and_physical_testing_limits, docs_qr_scanner_client_reported_method_is_not_physical_camera_attestation, docs_qr_scanner_documented_real_decoder_image_and_synthetic_camera_checks [EXTRACTED 1.00]
- **Existing scanner API to validated private entry grant** — docs_qr_scanner_existing_html5_qrcode2_3_8_scanner_apis, docs_qr_scanner_local_camera_and_image_scanning_with_explicit_permission, docs_qr_scanner_complete_same_event_game_entry_url_validation, docs_qr_scanner_backend_origin_registered_token_and_enabled_state_validation, docs_qr_scanner_qrcontent_and_camera_or_upload_method_request_contract, docs_player_flow_and_access_scanner_detection_checked_before_two_hour_httponly_entry_grant [EXTRACTED 1.00]
- **Private identity boundaries across runtime and development** — docs_ai_system_rules_exclude_student_identity_and_nicknames_from_provider_context, agents_private_data_exclusion_from_project_graph [INFERRED 0.85]

## Communities (29 total, 4 thin omitted)

### Community 0 - "icons.jsx / ui.jsx"
Cohesion: 0.07
Nodes (111): AdminOnly(), App(), PlayerOnly(), ActivityChart(), axis, ChartTip(), LevelChart(), OutcomesChart() (+103 more)

### Community 1 - "create_app() / main.py"
Cohesion: 0.05
Nodes (70): Settings, all_rows(), execute(), make_engine(), one(), canonical(), replay(), simulated_result() (+62 more)

### Community 2 - "Current QR player flow and administrator access / Scanner detection checked before two-hour HttpOnly"
Cohesion: 0.17
Nodes (15): Atomic replayed results notification and outbox, Completed-round-only source-matched player leaderboard, Current QR player flow and administrator access, Durable win loss alerts with focus-refresh polling, Owner-only persistent ticket across refreshes, Preserved Sourcio-derived player styling and font symbols, Recorded retention deadline with future deletion and recovery operations, Scanner detection checked before two-hour HttpOnly entry grant (+7 more)

### Community 3 - "package.json / dependencies"
Cohesion: 0.12
Nodes (21): dependencies, @fontsource-variable/inter@5.3.0, html5-qrcode@2.3.8, qrcode.react@4.2.0, @radix-ui/react-dialog@1.3.1, @radix-ui/react-dropdown-menu@2.2.1, react@19.3.1, react-router-dom@7.18.5 (+13 more)

### Community 4 - "Implemented FastAPI XAMPP development backend / Connected React JavaScript frontend and access journ"
Cohesion: 0.12
Nodes (15): Administrator password cookie and CSRF defenses, Authorized development simulator with source-separated ranking, Disposable MariaDB synthetic integration test boundary, Implemented FastAPI XAMPP development backend, Implemented FIFO locking and duplicate protection, Implemented keyed encrypted private student identity, Primary Python3.13 backend .venv environment, Repeatable local database provisioning and runtime account (+7 more)

### Community 5 - "Scanner.jsx / Scanner()"
Cohesion: 0.20
Nodes (16): submit(), loadScannerApi(), release(), Scanner(), detected(), startCamera(), stopCamera(), upload() (+8 more)

### Community 6 - "devDependencies / Registration.test.jsx"
Cohesion: 0.12
Nodes (15): devDependencies, jsdom@31.0.1, prettier@3.10.1, @testing-library/jest-dom@7.0.1, @testing-library/react@16.3.3, @testing-library/user-event@14.6.10, vitest@5.1.0, setup() (+7 more)

### Community 7 - "001_initial.sql / game_sessions"
Cohesion: 0.28
Nodes (16): ai_requests, audit_logs, auth_sessions, device_commands, device_events, events, game_sessions, machines (+8 more)

### Community 8 - "schema.sql / game_sessions"
Cohesion: 0.28
Nodes (16): ai_requests, audit_logs, auth_sessions, device_commands, device_events, events, game_sessions, machines (+8 more)

### Community 9 - "review-pages.mjs / @playwright/test"
Cohesion: 0.14
Nodes (8): @playwright/test@1.65.1, directory, errors, height, results, routes, width, @playwright/test

### Community 10 - "Player QR scanner implementation and entry contract / Local camera and image scanning with explicit "
Cohesion: 0.24
Nodes (11): Phone networking TLS and operational readiness gaps, Authenticated synthetic-tested device integration boundary, Ready freshness admission and active-round queue guards, Backend origin registered token and enabled-state validation, Complete same-event game-entry URL validation, Documented real decoder image and synthetic camera checks, Existing html5-qrcode2.3.8 scanner APIs, Local camera and image scanning with explicit permission (+3 more)

### Community 11 - "main.jsx / @radix-ui/react-tooltip"
Cohesion: 0.17
Nodes (6): @fortawesome/fontawesome-free@7.3.1, @radix-ui/react-tooltip@1.4.1, react-dom@19.3.1, @fortawesome/fontawesome-free, @radix-ui/react-tooltip, react-dom

### Community 12 - "Documentation index and authority"
Cohesion: 0.10
Nodes (18): Pending AI privacy injection and failure evaluations, Proposed AI deadlines rate and budget limits, Proposed analytics-v1 system policy, Server-scoped allowlisted analytics tools, Player reference visual language and source limitations, Sourcio-adapted dashboard specification, Functional specification baseline, Pending physical hardware performance and recovery acceptance (+10 more)

### Community 13 - "demo.js / demo.test.js"
Cohesion: 0.25
Nodes (9): activity, EVENT, initialQueue, levelStatistics(), names, players, rankPlayers(), rounds (+1 more)

### Community 14 - "Local React and backend setup / Start XAMPP MySQL before application servers"
Cohesion: 0.27
Nodes (10): Direct backend .venv uvicorn startup without activation, Documented user-installed Node24 npm11 and Python3.13 versions, Independent Node install and Windows npm cmd entrypoint, Keep backend environment credentials and database private, Local admin login and explicit server shutdown, Local React and backend setup, npm ci and Python virtual environment dependency reinstall, Primary React npm development command (+2 more)

### Community 15 - "002_player_flow.sql / entry_grants"
Cohesion: 0.32
Nodes (4): entry_grants, login_attempts, player_notifications, qr_links

### Community 16 - "Project maintenance instructions / Private-data exclusion from project graph"
Cohesion: 0.29
Nodes (3): Frontend implementation conventions, Implemented auth queue and simulator truth boundaries, Project maintenance instructions

### Community 17 - "flows.spec.js / @axe-core/playwright"
Cohesion: 0.29
Nodes (3): errors, @axe-core/playwright@4.14.0, @axe-core/playwright

### Community 18 - "scripts / build"
Cohesion: 0.29
Nodes (7): scripts, build, dev, format, preview, test, test:browser

### Community 19 - "MySQL-compatible schema baseline with current migration override / Atomic result transaction and non"
Cohesion: 0.33
Nodes (6): Atomic result transaction and non-destructive invalidation design, Composite event machine queue player bindings, Generated active-session and live-ticket uniqueness, MariaDB10.11 XAMPP utf8mb4_unicode_ci compatibility, MySQL-compatible schema baseline with current migration override, Private identity and retention schema design

### Community 20 - "Architecture baseline with current implementation override / Confirmed React JavaScript JSX Vite fro"
Cohesion: 0.18
Nodes (8): Graphifyy 0.9.109 isolated local package, Local Graphify setup and freshness workflow, Optional structural file watcher, Architecture baseline with current implementation override, Confirmed React JavaScript JSX Vite frontend, FastAPI Python SQLAlchemy and XAMPP runtime architecture, Proposed ESP32 firmware remains physically unconnected, Shared CSS Radix Font Awesome and Recharts foundations

### Community 21 - "vite.config.js / vite"
Cohesion: 0.33
Nodes (4): vite@8.3.8, @vitejs/plugin-react@6.3.0, vite, @vitejs/plugin-react

### Community 23 - "QR access and theme five-pass refinement log / Documented current Edge accessibility unit and produc"
Cohesion: 0.25
Nodes (7): Access flow contrast mobile and verification refinement passes, Documented current Edge accessibility unit and production checks, Historical eight-page sample review evidence, QR access and theme five-pass refinement log, Admin neutral-theme and current-access research update, Dashboard and registration design research, Primary dashboard form and custom framework research

### Community 24 - ".prettierrc.json / printWidth"
Cohesion: 0.40
Nodes (4): printWidth, semi, singleQuote, trailingComma

### Community 25 - "Pinned backend dependency manifest / Pinned Argon2 and cryptography security dependencies"
Cohesion: 0.67
Nodes (3): Pinned Argon2 and cryptography security dependencies, Pinned backend dependency manifest, Pinned FastAPI SQLAlchemy PyMySQL Uvicorn runtime

## Knowledge Gaps
- **93 isolated node(s):** `request_receipts`, `login_attempts`, `request_receipts`, `semi`, `singleQuote` (+88 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 159 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Current QR player flow and administrator access` connect `Current QR player flow and administrator access / Scanner detection checked before two-hour HttpOnly` to `Player QR scanner implementation and entry contract / Local camera and image scanning with explicit `, `Implemented FastAPI XAMPP development backend / Connected React JavaScript frontend and access journ`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **What connects `request_receipts`, `login_attempts`, `request_receipts` to the rest of the system?**
  _93 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `icons.jsx / ui.jsx` be split into smaller, more focused modules?**
  _Cohesion score 0.06949191159717476 - nodes in this community are weakly interconnected._
- **Why does `Implemented FastAPI XAMPP development backend` connect `Implemented FastAPI XAMPP development backend / Connected React JavaScript frontend and access journ` to `Current QR player flow and administrator access / Scanner detection checked before two-hour HttpOnly`, `Player QR scanner implementation and entry contract / Local camera and image scanning with explicit `, `Local React and backend setup / Start XAMPP MySQL before application servers`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **Should `create_app() / main.py` be split into smaller, more focused modules?**
  _Cohesion score 0.052296436797181954 - nodes in this community are weakly interconnected._
- **Why does `Player QR scanner implementation and entry contract` connect `Player QR scanner implementation and entry contract / Local camera and image scanning with explicit ` to `Current QR player flow and administrator access / Scanner detection checked before two-hour HttpOnly`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **Should `package.json / dependencies` be split into smaller, more focused modules?**
  _Cohesion score 0.11688311688311688 - nodes in this community are weakly interconnected._