# Graph Report - iot-dashboard  (2026-11-17)

## Corpus Check
- 83 files · ~54,718 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 13 file(s) not represented in the graph (top: .css 6, (none) 3, .cmd 3)

## Summary
- 767 nodes · 1942 edges · 42 communities (30 shown, 12 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 36 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- icons.jsx / ui.jsx
- test_assistant.py / assistant.py
- create_app() / now()
- api() / demo.js
- dev.mjs / review-pages.mjs
- Current QR player flow and administrator access / MySQL-compatible schema baseline with current migr
- setup_local.py / run_browser_tests.py
- main.py / security.py
- Stack Intelligence administrator analytics / Separate background calibration and readiness
- frontend/package.json / dependencies
- Player QR scanner implementation and entry contract / Shared backend browser-write and QR entry orig
- 001_initial.sql / game_sessions
- schema.sql / game_sessions
- test_player_flow.py / uuid
- Registration.test.jsx / test-setup.js
- analytics.py / collect()
- Canonical documentation index and authority / Public Stack Moko Baby introduction and installation g
- Technology stack and architecture overview / Current local NLP architecture supersedes baseline
- main.jsx / @radix-ui/react-tooltip
- Local React and backend setup / Combined launcher starts API waits readiness then Vite
- AI system rules / Conversational policy without fabricated claims
- devDependencies / vite.config.js
- package.json / scripts
- game.py / simulated_result()
- Dependency-ordered implementation plan / Conversational milestone with targeted validation
- Backend setup and implementation guide / Single-event FastAPI database baseline
- 002_player_flow.sql / entry_grants
- scripts / build
- Project maintenance instructions / Always read canonical internal docs before project work
- assistant_staff() / assistant_query()
- Frontend startup access and design guide / Shared real analytics with explicit hardware limits
- Sourcio-adapted dashboard specification / Admin fixed chat connected to local routing and factual ev
- Local Graphify setup and freshness workflow / Graphifyy 0.9.109 isolated local package
- QR access and theme five-pass refinement log / Documented current Edge accessibility unit and produc
- .prettierrc.json / printWidth
- Pinned backend dependency manifest / Pinned Argon2 and cryptography security dependencies
- Source-backed decisions and open gates / Open hardware rules TLS provider and retention decisions
- React main.jsx module entry and root mount / Stack Moko Baby frontend HTML entry
- engines / node

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 63 edges
2. `useApp()` - 32 edges
3. `Stack Intelligence administrator analytics` - 30 edges
4. `Card()` - 29 edges
5. `Registration()` - 28 edges
6. `now()` - 26 edges
7. `Badge()` - 26 edges
8. `Assistant` - 25 edges
9. `one()` - 25 edges
10. `execute()` - 25 edges

## Surprising Connections (you probably didn't know these)
- `Single-event FastAPI database baseline` --references--> `Stack Intelligence administrator analytics`  [EXTRACTED]
  backend/README.md → docs/admin-assistant.md
- `Shared real analytics with explicit hardware limits` --references--> `Stack Intelligence administrator analytics`  [EXTRACTED]
  frontend/README.md → docs/admin-assistant.md
- `main()` --uses--> `Settings`  [INFERRED]
  scripts/export-registration-qr.py → backend/app/config.py
- `main()` --calls--> `one()`  [EXTRACTED]
  scripts/export-registration-qr.py → backend/app/database.py
- `Public guide is not internal authority` --references--> `Canonical documentation index and authority`  [EXTRACTED]
  README.md → docs/README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Curated conversation preserves typed context beside bounded factual analytics** — docs_admin_assistant_local_curated_social_replies_during_loading, docs_admin_assistant_whole_utterance_guards_and_retained_analytical_context, docs_admin_assistant_requested_metrics_and_expandable_evidence, docs_admin_assistant_privacy_normalized_intent_pipeline [EXTRACTED 1.00]
- **Separate preparation and question timing with authenticated readiness** — docs_admin_assistant_separate_background_calibration_and_readiness, docs_admin_assistant_handler_wide_twenty_second_deadline, docs_admin_assistant_protected_assistant_api_and_evidence [EXTRACTED 1.00]
- **Recorded successive targeted checks retain open release gates** — docs_admin_assistant_conversational_validation_63_checks_and_build, docs_admin_assistant_historical_cold_load_investigation_and_38_checks, docs_admin_assistant_historical_synthetic_browser_and_auth_boundaries, docs_admin_assistant_remaining_manual_and_hardware_acceptance [EXTRACTED 1.00]
- **Combined launch readiness and process ownership** — docs_local_setup_combined_launcher_starts_api_waits_readiness_then_vite, docs_local_setup_manual_xampp_and_launcher_owned_process_lifecycle, docs_local_setup_optional_api_only_and_frontend_only_npm_startup, docs_local_setup_installed_node_startup_independent_of_codex_versioned_runtime, docs_local_setup_connection_refused_reflects_missing_api_and_readiness_timeout, docs_local_setup_session401_differs_from_connectivity_and_prior200_is_time_specific [EXTRACTED 1.00]
- **Private waiting reason and explicit reservation precede a round** — docs_player_flow_and_access_server_registration_with_unused_entry_grant_and_private_identity, docs_player_flow_and_access_owner_only_persistent_ticket_across_refreshes, docs_player_flow_and_access_private_cabinetstate_and_queuestate_waiting_reasons, docs_player_flow_and_access_explicit_operator_call_followed_by_physical_button_start, docs_player_flow_and_access_ready_freshness_admission_and_active_round_queue_guards [EXTRACTED 1.00]
- **Explicit simulator controls preserve source and recovery boundaries** — docs_player_flow_and_access_explicit_queue_page_simulator_action_sequence, docs_player_flow_and_access_release_test_ticket_affects_simulator_reservations_only, docs_player_flow_and_access_simulator_evidence_replay_and_separate_device_leaderboard_cohort, docs_player_flow_and_access_durable_win_loss_alerts_with_focus_refresh_polling [EXTRACTED 1.00]
- **Origin compatibility retains scheme port Host and CSRF boundaries** — docs_qr_scanner_shared_backend_browser_write_and_qr_entry_origin_policy, docs_qr_scanner_loopback_aliases_retain_matching_scheme_and_port, docs_qr_scanner_configured_public_additional_request_host_and_development_origins, docs_qr_scanner_vite_preserves_public_host_without_rewriting_browser_origin, docs_qr_scanner_restart_both_servers_and_defer_request_origin_verification [EXTRACTED 1.00]
- **Local normalization and shared origin policy preserve token validation** — docs_qr_scanner_canonical_local_entry_url_normalization_across_encoded_hosts, docs_qr_scanner_backend_normalized_origin_registered_token_and_enabled_validation, docs_qr_scanner_qrcontent_and_camera_or_upload_method_request_contract, docs_qr_scanner_shared_backend_browser_write_and_qr_entry_origin_policy [EXTRACTED 1.00]

## Communities (42 total, 12 thin omitted)

### Community 0 - "icons.jsx / ui.jsx"
Cohesion: 0.06
Nodes (115): AdminOnly(), App(), PlayerOnly(), ActivityChart(), axis, ChartTip(), LevelChart(), OutcomesChart() (+107 more)

### Community 1 - "test_assistant.py / assistant.py"
Cohesion: 0.07
Nodes (52): Assistant, inspect(), basic_response(), compose(), Context, conversational_reply(), endpoint(), Intent (+44 more)

### Community 2 - "create_app() / now()"
Cohesion: 0.16
Nodes (38): all_rows(), execute(), one(), create_app(), active(), admin_session(), admissions(), analytics() (+30 more)

### Community 3 - "api() / demo.js"
Cohesion: 0.07
Nodes (35): AdminAssistant(), inspect(), send(), submit(), answerLabels, Evidence(), periods, statusLabels (+27 more)

### Community 4 - "dev.mjs / review-pages.mjs"
Cohesion: 0.06
Nodes (21): errors, @axe-core/playwright@4.14.0, @playwright/test@1.65.1, directory, errors, height, results, routes (+13 more)

### Community 5 - "Current QR player flow and administrator access / MySQL-compatible schema baseline with current migr"
Cohesion: 0.08
Nodes (30): Functional specification baseline, Pending physical hardware performance and recovery acceptance, Proposed classic-v1 game rules, Scoped metric denominators and local-day bounds, Authenticated synthetic-tested device integration boundary, Completed-round-only source-matched player leaderboard, Current QR player flow and administrator access, Durable win loss alerts with focus-refresh polling (+22 more)

### Community 6 - "setup_local.py / run_browser_tests.py"
Cohesion: 0.14
Nodes (6): Settings, make_engine(), migrate(), seed(), environment(), main()

### Community 7 - "main.py / security.py"
Cohesion: 0.11
Nodes (14): Admissions, Entry, Heartbeat, Login, Placement, Reason, Registration, Result (+6 more)

### Community 9 - "frontend/package.json / dependencies"
Cohesion: 0.13
Nodes (19): dependencies, @fontsource-variable/inter@5.3.0, html5-qrcode@2.3.8, qrcode.react@4.2.0, @radix-ui/react-dialog@1.3.1, @radix-ui/react-dropdown-menu@2.2.1, react@19.3.1, react-router-dom@7.18.5 (+11 more)

### Community 10 - "Player QR scanner implementation and entry contract / Shared backend browser-write and QR entry orig"
Cohesion: 0.18
Nodes (13): Backend normalized origin registered token and enabled validation, Canonical local entry URL normalization across encoded hosts, Configured public additional request-host and development origins, Current-event registration PNG export excluded from project graph, Existing html5-qrcode2.3.8 scanner APIs, Existing scanner suite descriptions and correction verification limits, Local camera and image scanning with explicit permission, Loopback aliases retain matching scheme and port (+5 more)

### Community 11 - "001_initial.sql / game_sessions"
Cohesion: 0.28
Nodes (16): ai_requests, audit_logs, auth_sessions, device_commands, device_events, events, game_sessions, machines (+8 more)

### Community 12 - "schema.sql / game_sessions"
Cohesion: 0.28
Nodes (16): ai_requests, audit_logs, auth_sessions, device_commands, device_events, events, game_sessions, machines (+8 more)

### Community 13 - "test_player_flow.py / uuid"
Cohesion: 0.28
Nodes (11): entry_payload(), join(), post(), test_access_control_csrf_and_privacy(), test_device_result_replay_and_cohort_separation(), test_fifo_concurrency_idempotency_and_results(), test_identity_encryption_and_cookie_flags(), test_leaderboard_relocks_on_next_registration() (+3 more)

### Community 14 - "Registration.test.jsx / test-setup.js"
Cohesion: 0.14
Nodes (10): @testing-library/jest-dom@7.0.1, @testing-library/react@16.3.3, @testing-library/user-event@14.6.10, vitest@5.1.0, setup(), state, @testing-library/jest-dom, @testing-library/react (+2 more)

### Community 15 - "analytics.py / collect()"
Cohesion: 0.21
Nodes (4): clean(), collect(), select(), stamp()

### Community 18 - "main.jsx / @radix-ui/react-tooltip"
Cohesion: 0.15
Nodes (6): @fortawesome/fontawesome-free@7.3.1, @radix-ui/react-tooltip@1.4.1, react-dom@19.3.1, @fortawesome/fontawesome-free, @radix-ui/react-tooltip, react-dom

### Community 19 - "Local React and backend setup / Combined launcher starts API waits readiness then Vite"
Cohesion: 0.23
Nodes (8): Combined launcher starts API waits readiness then Vite, Direct backend .venv uvicorn startup without activation, Documented user-installed Node24 npm11 and Python3.13 versions, Installed Node startup independent of Codex versioned runtime, Local React and backend setup, npm ci and Python virtual environment dependency reinstall, Optional API-only and frontend-only npm startup, Restart terminal application after user PATH setup

### Community 21 - "devDependencies / vite.config.js"
Cohesion: 0.20
Nodes (9): devDependencies, jsdom@31.0.1, prettier@3.10.1, vite@8.3.8, @vitejs/plugin-react@6.3.0, jsdom, prettier, vite (+1 more)

### Community 22 - "package.json / scripts"
Cohesion: 0.18
Nodes (10): engines, node, name, private, scripts, dev, dev:backend, dev:frontend (+2 more)

### Community 23 - "game.py / simulated_result()"
Cohesion: 0.40
Nodes (5): canonical(), replay(), simulated_result(), test_shared_scoring_vectors(), test_timeout_and_tamper_rejection()

### Community 26 - "002_player_flow.sql / entry_grants"
Cohesion: 0.32
Nodes (4): entry_grants, login_attempts, player_notifications, qr_links

### Community 27 - "scripts / build"
Cohesion: 0.25
Nodes (8): scripts, build, dev, dev:frontend, format, preview, test, test:browser

### Community 28 - "Project maintenance instructions / Always read canonical internal docs before project work"
Cohesion: 0.29
Nodes (3): Existing html5-qrcode scanner API requirement, Frontend implementation conventions, Project maintenance instructions

### Community 29 - "assistant_staff() / assistant_query()"
Cohesion: 0.33
Nodes (5): assistant_prepare(), assistant_query(), within_deadline(), assistant_staff(), assistant_status()

### Community 31 - "Sourcio-adapted dashboard specification / Admin fixed chat connected to local routing and factual ev"
Cohesion: 0.40
Nodes (4): Admin fixed chat connected to local routing and factual evidence, Player reference visual language and source limitations, Responsive and accessible dashboard behavior, Sourcio-adapted dashboard specification

### Community 32 - "Local Graphify setup and freshness workflow / Graphifyy 0.9.109 isolated local package"
Cohesion: 0.40
Nodes (3): Graphifyy 0.9.109 isolated local package, Local Graphify setup and freshness workflow, Optional structural file watcher

### Community 33 - "QR access and theme five-pass refinement log / Documented current Edge accessibility unit and produc"
Cohesion: 0.50
Nodes (4): Access flow contrast mobile and verification refinement passes, Documented current Edge accessibility unit and production checks, Historical eight-page sample review evidence, QR access and theme five-pass refinement log

### Community 34 - ".prettierrc.json / printWidth"
Cohesion: 0.40
Nodes (4): printWidth, semi, singleQuote, trailingComma

### Community 35 - "Pinned backend dependency manifest / Pinned Argon2 and cryptography security dependencies"
Cohesion: 0.67
Nodes (3): Pinned Argon2 and cryptography security dependencies, Pinned backend dependency manifest, Pinned FastAPI SQLAlchemy PyMySQL Uvicorn runtime

### Community 36 - "Source-backed decisions and open gates / Open hardware rules TLS provider and retention decisions"
Cohesion: 0.67
Nodes (3): Open hardware rules TLS provider and retention decisions, Primary-source research evidence, Source-backed decisions and open gates

## Knowledge Gaps
- **99 isolated node(s):** `request_receipts`, `login_attempts`, `request_receipts`, `semi`, `singleQuote` (+94 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 237 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Assistant` connect `test_assistant.py / assistant.py` to `create_app() / now()`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `create_app()` (e.g. with `Question` and `Settings`) actually correct?**
  _`create_app()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `request_receipts`, `login_attempts`, `request_receipts` to the rest of the system?**
  _99 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `icons.jsx / ui.jsx` be split into smaller, more focused modules?**
  _Cohesion score 0.06341212744090442 - nodes in this community are weakly interconnected._
- **Why does `create_app()` connect `create_app() / now()` to `test_assistant.py / assistant.py`, `setup_local.py / run_browser_tests.py`, `main.py / security.py`, `analytics.py / collect()`, `game.py / simulated_result()`, `assistant_staff() / assistant_query()`?**
  _High betweenness centrality (0.000) - this node is a cross-community bridge._
- **Should `test_assistant.py / assistant.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06975308641975309 - nodes in this community are weakly interconnected._
- **Should `api() / demo.js` be split into smaller, more focused modules?**
  _Cohesion score 0.07188160676532769 - nodes in this community are weakly interconnected._

Semantic extraction was performed by the host assistant. Exact token usage was not exposed; zero counters mean unreported, not zero-cost. This map covers documentation and implemented local frontend/backend sources. Graph relationships do not prove live hardware state; physical ESP32 integration remains unverified.
