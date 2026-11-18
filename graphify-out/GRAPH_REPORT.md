# Graph Report - iot-dashboard  (2026-11-18)

## Corpus Check
- 107 files · ~77,325 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: .css 7, (none) 3, .cmd 3)

## Summary
- 1070 nodes · 2915 edges · 58 communities (40 shown, 18 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 89 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5289b499`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- create_app() / execute()
- icons.jsx / Registration.jsx
- Overview.jsx / Card()
- Assistant / Question
- Stack Intelligence learning and clarification / Conversational behavior expansion
- ui.jsx / useApp()
- setup_local.py / database.py
- normalize() / test_assistant.py
- Current QR player flow and administrator access / Functional specification baseline
- api() / AdminAssistant()
- Leaderboard.jsx / Queue.jsx
- assistant.py / test_assistant_memory.py
- main.py / security.py
- test_player_flow.py / test_assistant_scope.py
- test_assistant_training.py
- Stack Intelligence administrator analytics / Memory controls and stale-write resistance
- NLP request grounding research implementation and checks / Current explicit measure and operation pr
- frontend/package.json / devDependencies
- Player QR scanner implementation and entry contract / Shared backend browser-write and QR entry orig
- schema.sql / staff_users
- test_api_answers_scores_not_a_wrong_model_or_saved_subject
- Reviewed examples for later local fine-tuning / Current-context approval and normalization fingerpri
- AppContext.jsx / Settings.jsx
- AdminAssistant.jsx
- 001_initial.sql / game_sessions
- dev.mjs
- demo.js
- assistant.py
- MySQL-compatible schema and current migrations / Memory tombstone revision and staff isolation
- test_assistant_interactions.py
- analytics.py / collect_all()
- AI system rules / Semantic request precedence and eighth score tool policy
- frontend/package.json
- Registration.test.jsx / vitest
- Scanner.jsx / Scanner()
- Dependency-ordered implementation plan / Grounded memory milestone and validation
- Local React and backend setup / Combined launcher starts API waits readiness then Vite
- Technology stack and architecture overview / Grounded memory architecture separate from facts
- context_version() / TrainingStore
- package.json / scripts
- simulated_result() / game.py
- Backend setup and implementation guide / Backend migration003 and private memory endpoints
- 002_player_flow.sql / entry_grants
- Dashboard design contract / Protected Settings with shared chat management state
- scripts / build
- Public Stack Moko Baby introduction and installation guide / Public guide is not internal authority
- Project maintenance instructions / Always read canonical internal docs before project work
- fetch_nlp_datasets.py / main()
- Canonical documentation index and authority
- ai_admin_memory / staff_users
- .prettierrc.json / printWidth
- assistant_query() / within_deadline()
- Pinned backend dependency manifest / Pinned Argon2 and cryptography security dependencies
- React main.jsx module entry and root mount / Stack Moko Baby frontend HTML entry

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 76 edges
2. `normalize()` - 48 edges
3. `Assistant` - 48 edges
4. `Stack Intelligence administrator analytics` - 43 edges
5. `execute()` - 42 edges
6. `Context` - 39 edges
7. `useApp()` - 36 edges
8. `one()` - 33 edges
9. `Reviewed examples for later local fine-tuning` - 32 edges
10. `Current QR player flow and administrator access` - 32 edges

## Surprising Connections (you probably didn't know these)
- `Backend migration003 and private memory endpoints` --references--> `Stack Intelligence administrator analytics`  [EXTRACTED]
  backend/README.md → docs/admin-assistant.md
- `Frontend private-memory controls and refresh` --references--> `Stack Intelligence administrator analytics`  [EXTRACTED]
  frontend/README.md → docs/admin-assistant.md
- `Public guide is not internal authority` --references--> `Canonical documentation index and authority`  [EXTRACTED]
  README.md → docs/README.md
- `main()` --uses--> `Settings`  [INFERRED]
  scripts/export-registration-qr.py → backend/app/config.py
- `main()` --calls--> `one()`  [EXTRACTED]
  scripts/export-registration-qr.py → backend/app/database.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Complete bounded composition preserves mixed subjects and privacy guardrails** — docs_assistant_behavioral_expansion_structural_composed_greeting_failure_and_narrow_spelling_fix, docs_assistant_behavioral_expansion_bounded_full_utterance_social_composition_grammar, docs_assistant_behavioral_expansion_raw_identifier_checks_and_mixed_request_subject_guards, docs_assistant_behavioral_expansion_context_preserving_social_replies_with_honest_day_parts [EXTRACTED 1.00]
- **Backend and API evidence remains separate from broad release or hardware acceptance** — docs_assistant_behavioral_expansion_actual140_backend_and_disposable_api_checks, docs_assistant_behavioral_expansion_local_ollama_mixed_route_and_token_report_verification, docs_assistant_behavioral_expansion_behavioral_validation_excludes_visual_and_training_acceptance [EXTRACTED 1.00]
- **Measured synthetic corpus uses family splits and bounded runtime retrieval without weight training** — docs_assistant_behavioral_expansion_original_behavioral443_categories_and343100_split, docs_assistant_behavioral_expansion_measured_text_tokens18977_with_explicit_exclusions, docs_assistant_behavioral_expansion_qwen_tokenizer_provenance_and_checksum_report, docs_assistant_behavioral_expansion_family_splits_and_prior_evaluation_exclusion, docs_assistant_behavioral_expansion_behavioral_references_are_not_live_answers_or_whole_prompts, docs_assistant_behavioral_expansion_combined634_corpus_and_approval_context_invalidation [EXTRACTED 1.00]
- **Structural freshness and semantic refresh both require source and privacy checks** — docs_graphify_setup_graph_query_structural_update_and_semantic_refresh, docs_graphify_setup_watcher_and_optional_hooks_are_not_startup_services, docs_graphify_setup_privacy_exclusions_and_limits_of_graph_evidence [EXTRACTED 1.00]
- **Current typed semantics select the correct bounded score tool and evidence basis** — docs_nlp_grounding_research_schema_derived_domain_measure_and_operation_features, docs_nlp_grounding_research_current_explicit_measure_and_operation_precedence, docs_nlp_grounding_research_definitions_aggregates_and_individual_scores_are_distinct, docs_nlp_grounding_research_compatible_deduplicated_lexical_demonstrations, docs_nlp_grounding_research_get_player_scores_bounded_best_result_listing, docs_nlp_grounding_research_score_privacy_snapshot_and_no_ddl_context_extension [EXTRACTED 1.00]
- **Primary research motivates locally constrained serving adaptations rather than model guarantees** — docs_nlp_grounding_research_checklist_capability_testing_research_and_adaptation, docs_nlp_grounding_research_canard_typed_ellipsis_research_and_adaptation, docs_nlp_grounding_research_lex_validated_intent_slot_research_and_local_adaptation, docs_nlp_grounding_research_ollama_structured_output_research_versus_semantic_correctness, docs_nlp_grounding_research_google_rules_ml_infrastructure_evaluation_adaptation [EXTRACTED 1.00]
- **Settings relocation and targeted validation retain explicit acceptance limits** — docs_nlp_grounding_research_authenticated_settings_relocation_and_last_answer_review, docs_nlp_grounding_research_shared_administrator_session_settings_state, docs_nlp_grounding_research_actual184_backend_and_score_semantics_verification, docs_nlp_grounding_research_twelve_local_ollama_probes_and_bounded_inference_conclusions, docs_nlp_grounding_research_frontend27_build_and_headless_brave_verification_limits [EXTRACTED 1.00]
- **Combined launch readiness and process ownership** — docs_local_setup_combined_launcher_starts_api_waits_readiness_then_vite, docs_local_setup_manual_xampp_and_launcher_owned_process_lifecycle, docs_local_setup_optional_api_only_and_frontend_only_npm_startup, docs_local_setup_installed_node_startup_independent_of_codex_versioned_runtime, docs_local_setup_connection_refused_reflects_missing_api_and_readiness_timeout, docs_local_setup_session401_differs_from_connectivity_and_prior200_is_time_specific [EXTRACTED 1.00]
- **Private waiting reason and explicit reservation precede a round** — docs_player_flow_and_access_server_registration_with_unused_entry_grant_and_private_identity, docs_player_flow_and_access_owner_only_persistent_ticket_across_refreshes, docs_player_flow_and_access_private_cabinetstate_and_queuestate_waiting_reasons, docs_player_flow_and_access_explicit_operator_call_followed_by_physical_button_start, docs_player_flow_and_access_ready_freshness_admission_and_active_round_queue_guards [EXTRACTED 1.00]
- **Explicit simulator controls preserve source and recovery boundaries** — docs_player_flow_and_access_explicit_queue_page_simulator_action_sequence, docs_player_flow_and_access_release_test_ticket_affects_simulator_reservations_only, docs_player_flow_and_access_simulator_evidence_replay_and_separate_device_leaderboard_cohort, docs_player_flow_and_access_durable_win_loss_alerts_with_focus_refresh_polling [EXTRACTED 1.00]
- **Origin compatibility retains scheme port Host and CSRF boundaries** — docs_qr_scanner_shared_backend_browser_write_and_qr_entry_origin_policy, docs_qr_scanner_loopback_aliases_retain_matching_scheme_and_port, docs_qr_scanner_configured_public_additional_request_host_and_development_origins, docs_qr_scanner_vite_preserves_public_host_without_rewriting_browser_origin, docs_qr_scanner_restart_both_servers_and_defer_request_origin_verification [EXTRACTED 1.00]
- **Local normalization and shared origin policy preserve token validation** — docs_qr_scanner_canonical_local_entry_url_normalization_across_encoded_hosts, docs_qr_scanner_backend_normalized_origin_registered_token_and_enabled_validation, docs_qr_scanner_qrcontent_and_camera_or_upload_method_request_contract, docs_qr_scanner_shared_backend_browser_write_and_qr_entry_origin_policy [EXTRACTED 1.00]

## Communities (58 total, 18 thin omitted)

### Community 0 - "create_app() / execute()"
Cohesion: 0.12
Nodes (48): execute(), one(), create_app(), active(), admin_session(), admissions(), assistant_forget_memory(), assistant_memory() (+40 more)

### Community 1 - "icons.jsx / Registration.jsx"
Cohesion: 0.09
Nodes (37): ArrowRight, CheckCircle2, CircuitBoard, Cpu, Eye, EyeOff, glyphs, HardDrive (+29 more)

### Community 2 - "Overview.jsx / Card()"
Cohesion: 0.21
Nodes (24): ActivityChart(), axis, ChartTip(), LevelChart(), OutcomesChart(), ScoreChart(), CalendarDays, Clock3 (+16 more)

### Community 3 - "Assistant / Question"
Cohesion: 0.13
Nodes (21): Assistant, Question, test_new_social_turns_work_with_ollama_disabled_and_preserve_context(), scenario(), test_specific_reported_greeting_through_the_service_without_ollama(), scenario(), test_answer_enqueues_only_metadata_without_waiting_for_audit(), scenario() (+13 more)

### Community 5 - "ui.jsx / useApp()"
Cohesion: 0.20
Nodes (20): AdminOnly(), App(), PlayerOnly(), Check, QrCode, RegistrationQR(), Shell(), tabs (+12 more)

### Community 6 - "setup_local.py / database.py"
Cohesion: 0.14
Nodes (6): Settings, make_engine(), migrate(), seed(), environment(), main()

### Community 7 - "normalize() / test_assistant.py"
Cohesion: 0.11
Nodes (35): automatic_scope(), compose(), Context, Intent, normalize(), resolve_routing(), RoutingPlan, empty_summary() (+27 more)

### Community 8 - "Current QR player flow and administrator access / Functional specification baseline"
Cohesion: 0.17
Nodes (17): Authenticated synthetic-tested device integration boundary, Completed-round-only source-matched player leaderboard, Current QR player flow and administrator access, Durable win loss alerts with focus-refresh polling, Explicit Queue-page simulator action sequence, Owner-only persistent ticket across refreshes, Preserved Sourcio-derived player styling and font symbols, Private cabinetState and queueState waiting reasons (+9 more)

### Community 9 - "api() / AdminAssistant()"
Cohesion: 0.19
Nodes (19): AssistantTrainingReview(), choose(), exportApproved(), load(), remove(), review(), save(), freshTarget() (+11 more)

### Community 10 - "Leaderboard.jsx / Queue.jsx"
Cohesion: 0.17
Nodes (31): ArrowLeft, ArrowUpRight, ChevronDown, ChevronLeft, ChevronRight, Download, Info, Medal (+23 more)

### Community 11 - "assistant.py / test_assistant_memory.py"
Cohesion: 0.13
Nodes (6): MemoryStore, SavedMemory, routing(), test_explaining_privacy_does_not_allow_identity_retrieval(), test_forget_has_csrf_and_prevents_old_inflight_memory_from_returning(), test_memory_schema_has_no_place_for_raw_text_or_invented_metrics()

### Community 12 - "main.py / security.py"
Cohesion: 0.10
Nodes (15): Admissions, boundaries(), Entry, Heartbeat, Login, Placement, Reason, Registration (+7 more)

### Community 13 - "test_player_flow.py / test_assistant_scope.py"
Cohesion: 0.23
Nodes (13): test_absent_device_results_are_not_inferred_from_registrations(), test_all_sources_are_separate_and_players_are_deduplicated(), entry_payload(), join(), post(), test_access_control_csrf_and_privacy(), test_device_result_replay_and_cohort_separation(), test_fifo_concurrency_idempotency_and_results() (+5 more)

### Community 14 - "test_assistant_training.py"
Cohesion: 0.07
Nodes (29): corpus_digest(), interpretation_choices(), retrieve(), seed_examples(), _seed_examples(), signature(), compatible(), Proposal (+21 more)

### Community 17 - "frontend/package.json / devDependencies"
Cohesion: 0.17
Nodes (11): devDependencies, jsdom@31.0.1, prettier@3.10.1, @testing-library/jest-dom@7.0.1, vite@8.3.8, @vitejs/plugin-react@6.3.0, jsdom, prettier (+3 more)

### Community 18 - "Player QR scanner implementation and entry contract / Shared backend browser-write and QR entry orig"
Cohesion: 0.18
Nodes (13): Backend normalized origin registered token and enabled validation, Canonical local entry URL normalization across encoded hosts, Configured public additional request-host and development origins, Current-event registration PNG export excluded from project graph, Existing html5-qrcode2.3.8 scanner APIs, Existing scanner suite descriptions and correction verification limits, Local camera and image scanning with explicit permission, Loopback aliases retain matching scheme and port (+5 more)

### Community 19 - "schema.sql / staff_users"
Cohesion: 0.25
Nodes (18): ai_admin_memory, ai_requests, ai_training_examples, audit_logs, auth_sessions, device_commands, device_events, events (+10 more)

### Community 22 - "AppContext.jsx / Settings.jsx"
Cohesion: 0.27
Nodes (7): Settings(), AppContext, EMPTY, assistantStatus, Context, useAssistant(), react

### Community 23 - "AdminAssistant.jsx"
Cohesion: 0.19
Nodes (8): AdminAssistant(), send(), submit(), answerLabels, Evidence(), suggestions, mocks, openChat()

### Community 24 - "001_initial.sql / game_sessions"
Cohesion: 0.28
Nodes (16): ai_requests, audit_logs, auth_sessions, device_commands, device_events, events, game_sessions, machines (+8 more)

### Community 25 - "dev.mjs"
Cohesion: 0.06
Nodes (21): errors, @axe-core/playwright@4.14.0, @playwright/test@1.65.1, directory, errors, height, results, routes (+13 more)

### Community 26 - "demo.js"
Cohesion: 0.25
Nodes (9): activity, EVENT, initialQueue, levelStatistics(), names, players, rankPlayers(), rounds (+1 more)

### Community 27 - "assistant.py"
Cohesion: 0.15
Nodes (17): inspect(), basic_response(), compose_all(), endpoint(), intent_payload(), knowledge_response(), MemoryPreferences, model_json() (+9 more)

### Community 31 - "test_assistant_interactions.py"
Cohesion: 0.13
Nodes (18): conversational_reply(), composed_social(), parse(), greeting_answer(), interaction_rows(), interaction_social(), interaction_text(), interaction_words() (+10 more)

### Community 32 - "analytics.py / collect_all()"
Cohesion: 0.29
Nodes (8): clean(), collect(), collect_all(), _collect_snapshot(), _operations(), select(), stamp(), analytics()

### Community 35 - "frontend/package.json"
Cohesion: 0.10
Nodes (27): dependencies, @fontsource-variable/inter@5.3.0, @fortawesome/fontawesome-free@7.3.1, html5-qrcode@2.3.8, qrcode.react@4.2.0, @radix-ui/react-dialog@1.3.1, @radix-ui/react-dropdown-menu@2.2.1, @radix-ui/react-tooltip@1.4.1 (+19 more)

### Community 36 - "Registration.test.jsx / vitest"
Cohesion: 0.16
Nodes (9): @testing-library/react@16.3.3, @testing-library/user-event@14.6.10, vitest@5.1.0, setup(), state, mocks, @testing-library/react, @testing-library/user-event (+1 more)

### Community 37 - "Scanner.jsx / Scanner()"
Cohesion: 0.32
Nodes (9): value(), loadScannerApi(), release(), Scanner(), detected(), startCamera(), stopCamera(), upload() (+1 more)

### Community 39 - "Dependency-ordered implementation plan / Grounded memory milestone and validation"
Cohesion: 0.13
Nodes (4): Dependency-ordered implementation plan, Open hardware rules TLS provider and retention decisions, Primary-source research evidence, Source-backed decisions and open gates

### Community 40 - "Local React and backend setup / Combined launcher starts API waits readiness then Vite"
Cohesion: 0.23
Nodes (8): Combined launcher starts API waits readiness then Vite, Direct backend .venv uvicorn startup without activation, Documented user-installed Node24 npm11 and Python3.13 versions, Installed Node startup independent of Codex versioned runtime, Local React and backend setup, npm ci and Python virtual environment dependency reinstall, Optional API-only and frontend-only npm startup, Restart terminal application after user PATH setup

### Community 42 - "context_version() / TrainingStore"
Cohesion: 0.33
Nodes (4): canonical(), context_version(), TrainingStore, all_rows()

### Community 43 - "package.json / scripts"
Cohesion: 0.18
Nodes (10): engines, node, name, private, scripts, dev, dev:backend, dev:frontend (+2 more)

### Community 44 - "simulated_result() / game.py"
Cohesion: 0.40
Nodes (6): canonical(), replay(), simulated_result(), seed_scores(), test_shared_scoring_vectors(), test_timeout_and_tamper_rejection()

### Community 46 - "002_player_flow.sql / entry_grants"
Cohesion: 0.32
Nodes (4): entry_grants, login_attempts, player_notifications, qr_links

### Community 49 - "Dashboard design contract / Protected Settings with shared chat management state"
Cohesion: 0.15
Nodes (5): Dashboard design contract, Functional specification baseline, Pending physical hardware performance and recovery acceptance, Proposed classic-v1 game rules, Scoped metric denominators and local-day bounds

### Community 50 - "scripts / build"
Cohesion: 0.25
Nodes (8): scripts, build, dev, dev:frontend, format, preview, test, test:browser

### Community 53 - "Project maintenance instructions / Always read canonical internal docs before project work"
Cohesion: 0.29
Nodes (3): Existing html5-qrcode scanner API requirement, Frontend implementation conventions, Project maintenance instructions

### Community 57 - "Canonical documentation index and authority"
Cohesion: 0.15
Nodes (8): Canonical documentation index and authority, Access flow contrast mobile and verification refinement passes, Documented current Edge accessibility unit and production checks, Historical eight-page sample review evidence, QR access and theme five-pass refinement log, Admin neutral-theme and current-access research update, Dashboard and registration design research, Primary dashboard form and custom framework research

### Community 62 - ".prettierrc.json / printWidth"
Cohesion: 0.40
Nodes (4): printWidth, semi, singleQuote, trailingComma

### Community 64 - "Pinned backend dependency manifest / Pinned Argon2 and cryptography security dependencies"
Cohesion: 0.67
Nodes (3): Pinned Argon2 and cryptography security dependencies, Pinned backend dependency manifest, Pinned FastAPI SQLAlchemy PyMySQL Uvicorn runtime

## Knowledge Gaps
- **90 isolated node(s):** `request_receipts`, `login_attempts`, `request_receipts`, `semi`, `singleQuote` (+85 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 323 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Assistant` connect `Assistant / Question` to `create_app() / execute()`, `assistant.py / test_assistant_memory.py`, `assistant.py`, `test_assistant_training.py`?**
  _High betweenness centrality (0.003) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `create_app()` (e.g. with `Question` and `Proposal`) actually correct?**
  _`create_app()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `request_receipts`, `login_attempts`, `request_receipts` to the rest of the system?**
  _90 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `create_app() / execute()` be split into smaller, more focused modules?**
  _Cohesion score 0.1187980433263452 - nodes in this community are weakly interconnected._
- **Why does `Reviewed examples for later local fine-tuning` connect `Reviewed examples for later local fine-tuning / Current-context approval and normalization fingerpri` to `NLP request grounding research implementation and checks / Current explicit measure and operation pr`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `Assistant` (e.g. with `MemoryStore` and `Proposal`) actually correct?**
  _`Assistant` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Should `icons.jsx / Registration.jsx` be split into smaller, more focused modules?**
  _Cohesion score 0.08780487804878048 - nodes in this community are weakly interconnected._