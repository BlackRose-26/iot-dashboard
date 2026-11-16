# Graph Report - iot-dashboard  (2026-11-16)

## Corpus Check
- 76 files · ~43,575 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 13 file(s) not represented in the graph (top: .css 6, (none) 3, .cmd 3)

## Summary
- 647 nodes · 1676 edges · 37 communities (31 shown, 6 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 7 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `36f112b5`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- icons.jsx / ui.jsx
- Local React and backend setup
- Stack Intelligence administrator chat / Proposed analytics-v1 system policy
- Current QR player flow and administrator access
- create_app() / execute()
- dev.mjs / review-pages.mjs
- setup_local.py / run_browser_tests.py
- main.py / security.py
- devDependencies
- Player QR scanner implementation and entry contract / Shared backend browser-write and QR entry orig
- 001_initial.sql / game_sessions
- schema.sql / game_sessions
- Scanner() / api()
- test_player_flow.py / join()
- main.jsx / @radix-ui/react-tooltip
- dependencies / html5-qrcode
- game.py / simulated_result()
- Registration.test.jsx / test-setup.js
- package.json / scripts
- Documentation index and authority
- 002_player_flow.sql / entry_grants
- scripts / build
- AdminAssistant() / AdminAssistant.jsx
- Architecture baseline with current implementation override
- QR access and theme five-pass refinement log / Documented current Edge accessibility unit and produc
- .prettierrc.json / printWidth
- Pinned backend dependency manifest / Pinned Argon2 and cryptography security dependencies
- Dependency-ordered implementation baseline and current overrides
- React main.jsx module entry and root mount / Stack Moko Baby frontend HTML entry
- Implemented FastAPI XAMPP development backend
- Sourcio-adapted dashboard specification
- Connected React JavaScript frontend and access journey
- MySQL-compatible schema baseline with current migration override
- engines

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 53 edges
2. `useApp()` - 32 edges
3. `Current QR player flow and administrator access` - 32 edges
4. `Card()` - 29 edges
5. `Badge()` - 28 edges
6. `Registration()` - 28 edges
7. `Stack Intelligence administrator chat` - 24 edges
8. `one()` - 23 edges
9. `execute()` - 23 edges
10. `now()` - 22 edges

## Surprising Connections (you probably didn't know these)
- `main()` --uses--> `Settings`  [INFERRED]
  scripts/export-registration-qr.py → backend/app/config.py
- `main()` --calls--> `one()`  [EXTRACTED]
  scripts/export-registration-qr.py → backend/app/database.py
- `Combined startup waits readiness without repeated database setup` --references--> `Combined launcher starts API waits readiness then Vite`  [EXTRACTED]
  backend/README.md → docs/local-setup.md
- `Combined dev supersedes older frontend-only startup` --references--> `Combined launcher starts API waits readiness then Vite`  [EXTRACTED]
  frontend/README.md → docs/local-setup.md
- `Implemented FastAPI XAMPP development backend` --references--> `Local React and backend setup`  [EXTRACTED]
  backend/README.md → docs/local-setup.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Future whole-event read-only analytical coverage** — docs_admin_assistant_future_iot_cabinet_analytical_coverage, docs_admin_assistant_future_dashboard_metric_definition_analytical_coverage, docs_admin_assistant_future_aggregate_player_analytical_coverage_without_identity_access, docs_admin_assistant_future_read_only_queue_and_admissions_analytical_coverage, docs_admin_assistant_future_source_separated_scores_results_and_level_analysis, docs_admin_assistant_future_bounded_event_trends_and_cautious_comparisons, docs_admin_assistant_whole_authorized_event_means_analytical_coverage_not_control [EXTRACTED 1.00]
- **Implemented chat preview separated from deferred analysis service** — docs_admin_assistant_admin_only_fixed_bottom_shared_chat_dock, docs_admin_assistant_memory_only_draft_and_conversation_lifecycle, docs_admin_assistant_explicit_placeholder_replies_without_live_analysis_or_backend_calls, docs_admin_assistant_deferred_staff_authenticated_conversation_endpoint, docs_admin_assistant_deferred_normalized_intent_and_prewritten_aggregate_tools, docs_admin_assistant_deferred_provider_model_limits_and_separate_retention_decision [EXTRACTED 1.00]
- **Combined launch readiness and process ownership** — docs_local_setup_combined_launcher_starts_api_waits_readiness_then_vite, docs_local_setup_manual_xampp_and_launcher_owned_process_lifecycle, docs_local_setup_optional_api_only_and_frontend_only_npm_startup, docs_local_setup_installed_node_startup_independent_of_codex_versioned_runtime, docs_local_setup_connection_refused_reflects_missing_api_and_readiness_timeout, docs_local_setup_session401_differs_from_connectivity_and_prior200_is_time_specific [EXTRACTED 1.00]
- **Private waiting reason and explicit reservation precede a round** — docs_player_flow_and_access_server_registration_with_unused_entry_grant_and_private_identity, docs_player_flow_and_access_owner_only_persistent_ticket_across_refreshes, docs_player_flow_and_access_private_cabinetstate_and_queuestate_waiting_reasons, docs_player_flow_and_access_explicit_operator_call_followed_by_physical_button_start, docs_player_flow_and_access_ready_freshness_admission_and_active_round_queue_guards [EXTRACTED 1.00]
- **Explicit simulator controls preserve source and recovery boundaries** — docs_player_flow_and_access_explicit_queue_page_simulator_action_sequence, docs_player_flow_and_access_release_test_ticket_affects_simulator_reservations_only, docs_player_flow_and_access_simulator_evidence_replay_and_separate_device_leaderboard_cohort, docs_player_flow_and_access_durable_win_loss_alerts_with_focus_refresh_polling [EXTRACTED 1.00]
- **Origin compatibility retains scheme port Host and CSRF boundaries** — docs_qr_scanner_shared_backend_browser_write_and_qr_entry_origin_policy, docs_qr_scanner_loopback_aliases_retain_matching_scheme_and_port, docs_qr_scanner_configured_public_additional_request_host_and_development_origins, docs_qr_scanner_vite_preserves_public_host_without_rewriting_browser_origin, docs_qr_scanner_restart_both_servers_and_defer_request_origin_verification [EXTRACTED 1.00]
- **Local normalization and shared origin policy preserve token validation** — docs_qr_scanner_canonical_local_entry_url_normalization_across_encoded_hosts, docs_qr_scanner_backend_normalized_origin_registered_token_and_enabled_validation, docs_qr_scanner_qrcontent_and_camera_or_upload_method_request_contract, docs_qr_scanner_shared_backend_browser_write_and_qr_entry_origin_policy [EXTRACTED 1.00]
- **Public installation guide preserves canonical internal instructions** — readme_public_stack_moko_baby_introduction_and_installation_guide, readme_public_onboarding_defers_to_internal_project_guide, docs_readme_documentation_index_and_authority, docs_readme_canonical_internal_guide_distinct_from_root_public_readme, agents_always_read_canonical_internal_docs_before_project_work [EXTRACTED 1.00]

## Communities (37 total, 6 thin omitted)

### Community 0 - "icons.jsx / ui.jsx"
Cohesion: 0.06
Nodes (122): AdminOnly(), App(), PlayerOnly(), ActivityChart(), axis, ChartTip(), LevelChart(), OutcomesChart() (+114 more)

### Community 1 - "Local React and backend setup"
Cohesion: 0.15
Nodes (14): Combined startup waits readiness without repeated database setup, Combined launcher starts API waits readiness then Vite, Direct backend .venv uvicorn startup without activation, Documented user-installed Node24 npm11 and Python3.13 versions, Installed Node startup independent of Codex versioned runtime, Local React and backend setup, npm ci and Python virtual environment dependency reinstall, Optional API-only and frontend-only npm startup (+6 more)

### Community 2 - "Stack Intelligence administrator chat / Proposed analytics-v1 system policy"
Cohesion: 0.09
Nodes (24): Accessible preview composer focus overlay and mobile behavior, Admin-only fixed bottom shared chat dock, Deferred evidence-backed scoped answer and failure states, Deferred normalized intent and prewritten aggregate tools, Deferred provider model limits and separate retention decision, Deferred staff-authenticated conversation endpoint, Future aggregate player analytical coverage without identity access, Future bounded event trends and cautious comparisons (+16 more)

### Community 3 - "Current QR player flow and administrator access"
Cohesion: 0.17
Nodes (17): Authenticated synthetic-tested device integration boundary, Completed-round-only source-matched player leaderboard, Current QR player flow and administrator access, Durable win loss alerts with focus-refresh polling, Explicit Queue-page simulator action sequence, Owner-only persistent ticket across refreshes, Preserved Sourcio-derived player styling and font symbols, Private cabinetState and queueState waiting reasons (+9 more)

### Community 4 - "create_app() / execute()"
Cohesion: 0.19
Nodes (36): all_rows(), execute(), one(), create_app(), active(), admin_session(), admissions(), audit() (+28 more)

### Community 5 - "dev.mjs / review-pages.mjs"
Cohesion: 0.06
Nodes (21): errors, @axe-core/playwright@4.14.0, @playwright/test@1.65.1, directory, errors, height, results, routes (+13 more)

### Community 6 - "setup_local.py / run_browser_tests.py"
Cohesion: 0.11
Nodes (7): Settings, make_engine(), encrypt_identity(), migrate(), seed(), environment(), main()

### Community 7 - "main.py / security.py"
Cohesion: 0.11
Nodes (14): Admissions, boundaries(), Entry, Heartbeat, Login, Placement, Reason, Registration (+6 more)

### Community 8 - "devDependencies"
Cohesion: 0.20
Nodes (9): devDependencies, jsdom@31.0.1, prettier@3.10.1, vite@8.3.8, @vitejs/plugin-react@6.3.0, jsdom, prettier, vite (+1 more)

### Community 9 - "Player QR scanner implementation and entry contract / Shared backend browser-write and QR entry orig"
Cohesion: 0.18
Nodes (13): Backend normalized origin registered token and enabled validation, Canonical local entry URL normalization across encoded hosts, Configured public additional request-host and development origins, Current-event registration PNG export excluded from project graph, Existing html5-qrcode2.3.8 scanner APIs, Existing scanner suite descriptions and correction verification limits, Local camera and image scanning with explicit permission, Loopback aliases retain matching scheme and port (+5 more)

### Community 10 - "001_initial.sql / game_sessions"
Cohesion: 0.28
Nodes (16): ai_requests, audit_logs, auth_sessions, device_commands, device_events, events, game_sessions, machines (+8 more)

### Community 11 - "schema.sql / game_sessions"
Cohesion: 0.28
Nodes (16): ai_requests, audit_logs, auth_sessions, device_commands, device_events, events, game_sessions, machines (+8 more)

### Community 12 - "Scanner() / api()"
Cohesion: 0.23
Nodes (15): loadScannerApi(), release(), Scanner(), detected(), startCamera(), stopCamera(), upload(), api() (+7 more)

### Community 13 - "test_player_flow.py / join()"
Cohesion: 0.31
Nodes (11): entry_payload(), join(), post(), test_access_control_csrf_and_privacy(), test_device_result_replay_and_cohort_separation(), test_fifo_concurrency_idempotency_and_results(), test_identity_encryption_and_cookie_flags(), test_leaderboard_relocks_on_next_registration() (+3 more)

### Community 14 - "main.jsx / @radix-ui/react-tooltip"
Cohesion: 0.15
Nodes (6): @fortawesome/fontawesome-free@7.3.1, @radix-ui/react-tooltip@1.4.1, react-dom@19.3.1, @fortawesome/fontawesome-free, @radix-ui/react-tooltip, react-dom

### Community 15 - "dependencies / html5-qrcode"
Cohesion: 0.13
Nodes (19): dependencies, @fontsource-variable/inter@5.3.0, html5-qrcode@2.3.8, qrcode.react@4.2.0, @radix-ui/react-dialog@1.3.1, @radix-ui/react-dropdown-menu@2.2.1, react@19.3.1, react-router-dom@7.18.5 (+11 more)

### Community 16 - "game.py / simulated_result()"
Cohesion: 0.35
Nodes (5): canonical(), replay(), simulated_result(), test_shared_scoring_vectors(), test_timeout_and_tamper_rejection()

### Community 17 - "Registration.test.jsx / test-setup.js"
Cohesion: 0.14
Nodes (10): @testing-library/jest-dom@7.0.1, @testing-library/react@16.3.3, @testing-library/user-event@14.6.10, vitest@5.1.0, setup(), state, @testing-library/jest-dom, @testing-library/react (+2 more)

### Community 18 - "package.json / scripts"
Cohesion: 0.18
Nodes (10): engines, node, name, private, scripts, dev, dev:backend, dev:frontend (+2 more)

### Community 19 - "Documentation index and authority"
Cohesion: 0.15
Nodes (9): Existing html5-qrcode scanner API requirement, Frontend implementation conventions, Project maintenance instructions, Confirmed Stack Moko Baby baseline, Current implementation update supersedes preview assumptions, Documentation index and authority, Current player admin backend simulator and chat implementation status, Public Stack Moko Baby introduction and installation guide (+1 more)

### Community 20 - "002_player_flow.sql / entry_grants"
Cohesion: 0.32
Nodes (4): entry_grants, login_attempts, player_notifications, qr_links

### Community 21 - "scripts / build"
Cohesion: 0.25
Nodes (8): scripts, build, dev, dev:frontend, format, preview, test, test:browser

### Community 23 - "Architecture baseline with current implementation override"
Cohesion: 0.18
Nodes (8): Graphifyy 0.9.109 isolated local package, Local Graphify setup and freshness workflow, Optional structural file watcher, Architecture baseline with current implementation override, Confirmed React JavaScript JSX Vite frontend, FastAPI Python SQLAlchemy and XAMPP runtime architecture, Proposed ESP32 firmware remains physically unconnected, Shared CSS Radix Font Awesome and Recharts foundations

### Community 24 - "QR access and theme five-pass refinement log / Documented current Edge accessibility unit and produc"
Cohesion: 0.25
Nodes (7): Access flow contrast mobile and verification refinement passes, Documented current Edge accessibility unit and production checks, Historical eight-page sample review evidence, QR access and theme five-pass refinement log, Admin neutral-theme and current-access research update, Dashboard and registration design research, Primary dashboard form and custom framework research

### Community 25 - ".prettierrc.json / printWidth"
Cohesion: 0.40
Nodes (4): printWidth, semi, singleQuote, trailingComma

### Community 26 - "Pinned backend dependency manifest / Pinned Argon2 and cryptography security dependencies"
Cohesion: 0.67
Nodes (3): Pinned Argon2 and cryptography security dependencies, Pinned backend dependency manifest, Pinned FastAPI SQLAlchemy PyMySQL Uvicorn runtime

### Community 27 - "Dependency-ordered implementation baseline and current overrides"
Cohesion: 0.25
Nodes (7): Dependency-ordered implementation baseline and current overrides, Future constrained AI backend aggregate and provider work, Pending physical hardware performance and recovery acceptance, Remaining hardware AI deployment and event readiness gates, Open hardware rules TLS provider and retention decisions, Primary-source research evidence, Source-backed decisions and open gates

### Community 32 - "Implemented FastAPI XAMPP development backend"
Cohesion: 0.18
Nodes (11): Administrator password cookie and CSRF defenses, Atomic replayed results notification and outbox, Documented isolated backend checks not run by this refresh, Implemented FastAPI XAMPP development backend, Implemented FIFO locking and duplicate protection, Implemented keyed encrypted private student identity, Polling simulator privacy and operational limits remain, Primary Python3.13 backend .venv environment (+3 more)

### Community 33 - "Sourcio-adapted dashboard specification"
Cohesion: 0.20
Nodes (8): Player reference visual language and source limitations, Responsive and accessible dashboard behavior, Rounded cards pill rows and selective accent design tokens, Sourcio-adapted dashboard specification, Functional specification baseline, Pending physical hardware performance and recovery acceptance, Proposed classic-v1 game rules, Scoped metric denominators and local-day bounds

### Community 34 - "Connected React JavaScript frontend and access journey"
Cohesion: 0.29
Nodes (7): Connected React JavaScript frontend and access journey, Dashboard saved results with unknown physical readings, Frontend API proxy and secret-free public base configuration, Required student ID POST only and private persistent cookie, Server-protected admin and QR player route separation, Shared foundations neutral admin scope and preserved player palette, Standard npm project workflow

### Community 35 - "MySQL-compatible schema baseline with current migration override"
Cohesion: 0.33
Nodes (6): Atomic result transaction and non-destructive invalidation design, Composite event machine queue player bindings, Generated active-session and live-ticket uniqueness, MariaDB10.11 XAMPP utf8mb4_unicode_ci compatibility, MySQL-compatible schema baseline with current migration override, Private identity and retention schema design

## Knowledge Gaps
- **122 isolated node(s):** `request_receipts`, `login_attempts`, `request_receipts`, `semi`, `singleQuote` (+117 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 198 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Current QR player flow and administrator access` connect `Current QR player flow and administrator access` to `Implemented FastAPI XAMPP development backend`, `Player QR scanner implementation and entry contract / Shared backend browser-write and QR entry orig`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **What connects `request_receipts`, `login_attempts`, `request_receipts` to the rest of the system?**
  _122 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `icons.jsx / ui.jsx` be split into smaller, more focused modules?**
  _Cohesion score 0.06003990567748957 - nodes in this community are weakly interconnected._
- **Why does `Documentation index and authority` connect `Documentation index and authority` to `Implemented FastAPI XAMPP development backend`, `Sourcio-adapted dashboard specification`, `Stack Intelligence administrator chat / Proposed analytics-v1 system policy`, `Local React and backend setup`, `Current QR player flow and administrator access`, `MySQL-compatible schema baseline with current migration override`, `Player QR scanner implementation and entry contract / Shared backend browser-write and QR entry orig`, `Architecture baseline with current implementation override`, `QR access and theme five-pass refinement log / Documented current Edge accessibility unit and produc`, `Dependency-ordered implementation baseline and current overrides`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **Should `Stack Intelligence administrator chat / Proposed analytics-v1 system policy` be split into smaller, more focused modules?**
  _Cohesion score 0.0944741532976827 - nodes in this community are weakly interconnected._
- **Why does `Public Stack Moko Baby introduction and installation guide` connect `Documentation index and authority` to `Implemented FastAPI XAMPP development backend`, `Sourcio-adapted dashboard specification`, `Stack Intelligence administrator chat / Proposed analytics-v1 system policy`, `Local React and backend setup`, `Current QR player flow and administrator access`, `MySQL-compatible schema baseline with current migration override`, `Player QR scanner implementation and entry contract / Shared backend browser-write and QR entry orig`, `Architecture baseline with current implementation override`, `Dependency-ordered implementation baseline and current overrides`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **Should `dev.mjs / review-pages.mjs` be split into smaller, more focused modules?**
  _Cohesion score 0.06401137980085349 - nodes in this community are weakly interconnected._