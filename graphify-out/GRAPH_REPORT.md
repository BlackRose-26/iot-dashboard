# Graph Report - iot-dashboard  (2026-11-19)

## Corpus Check
- 121 files · ~86,413 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: .css 7, (none) 3, .cmd 3)

## Summary
- 1236 nodes · 3404 edges · 56 communities (39 shown, 17 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 105 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `33267d70`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- icons.jsx / ui.jsx
- create_app() / execute()
- api() / AdminAssistant.jsx
- Current QR player flow and administrator access / Durable browser updates
- Assistant / Question
- main.py / test_assistant_memory.py
- normalize() / test_assistant.py
- analytics.py
- json / test_assistant_learning.py
- Stack Intelligence learning and clarification / Conversational behavior expansion
- test_device_commands.py / test_live_updates.py
- test_player_flow.py / setup_local.py
- assistant.py / conversational_reply()
- frontend/package.json / dependencies
- test_device_commands.py
- Stack Intelligence administrator analytics / Memory controls and stale-write resistance
- test_assistant_training.py / candidate()
- NLP request grounding research implementation and checks / Current explicit measure and operation pr
- Reviewed examples for later local fine-tuning / Current-context approval and normalization fingerpri
- Player QR scanner implementation and entry contract / Shared backend browser-write and QR entry orig
- schema.sql / staff_users
- Device command delivery and review holds / No force release or automatic no-show resolution
- 001_initial.sql / game_sessions
- MySQL-compatible schema and current migrations / Memory tombstone revision and staff isolation
- review-pages.mjs / @playwright/test
- devDependencies / vite.config.js
- Dependency-ordered implementation plan / Command step4 complete portion and pending resolution
- dev.mjs / main()
- Frontend startup access and design guide / Roadmap paused 19 November
- LiveHub / test_outbox_is_atomic_and_recovers_after_dispatcher_restart()
- AI system rules / Semantic request precedence and eighth score tool policy
- Technology stack and architecture overview / Implemented API route and partial device recovery bound
- Current QR player flow and administrator access
- requested_metrics() / constraints()
- Local React and backend setup / Combined launcher starts API waits readiness then Vite
- Context
- context_version() / TrainingStore
- Backend setup and implementation guide / Backend authenticated live-update integration
- Canonical documentation index and authority
- main.jsx / @radix-ui/react-tooltip
- package.json / scripts
- test_assistant_generalization.py
- 002_player_flow.sql / entry_grants
- routing
- scripts / build
- MemoryStore / test_forget_has_csrf_and_prevents_old_inflight_memory_from_returning()
- origin_allowed() / origins.py
- flows.spec.js / @axe-core/playwright
- ai_admin_memory / staff_users
- QR access and theme five-pass refinement log / Documented current Edge accessibility unit and produc
- .prettierrc.json / printWidth
- Pinned backend dependency manifest / Pinned Argon2 and cryptography security dependencies
- React main.jsx module entry and root mount / Stack Moko Baby frontend HTML entry

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 90 edges
2. `execute()` - 53 edges
3. `one()` - 49 edges
4. `normalize()` - 48 edges
5. `Assistant` - 48 edges
6. `now()` - 44 edges
7. `useApp()` - 43 edges
8. `Context` - 39 edges
9. `Stack Intelligence administrator analytics` - 38 edges
10. `Current QR player flow and administrator access` - 36 edges

## Surprising Connections (you probably didn't know these)
- `Canonical guide and user authority` --references--> `Canonical documentation index and authority`  [EXTRACTED]
  AGENTS.md → docs/README.md
- `Canonical frontend composition` --references--> `Dashboard design contract`  [EXTRACTED]
  AGENTS.md → docs/dashboard-design.md
- `main()` --uses--> `Settings`  [INFERRED]
  scripts/export-registration-qr.py → backend/app/config.py
- `main()` --calls--> `one()`  [EXTRACTED]
  scripts/export-registration-qr.py → backend/app/database.py
- `Frontend startup access and design guide` --references--> `Backend setup and implementation guide`  [EXTRACTED]
  frontend/README.md → backend/README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Complete bounded composition preserves mixed subjects and privacy guardrails** — docs_assistant_behavioral_expansion_structural_composed_greeting_failure_and_narrow_spelling_fix, docs_assistant_behavioral_expansion_bounded_full_utterance_social_composition_grammar, docs_assistant_behavioral_expansion_raw_identifier_checks_and_mixed_request_subject_guards, docs_assistant_behavioral_expansion_context_preserving_social_replies_with_honest_day_parts [EXTRACTED 1.00]
- **Backend and API evidence remains separate from broad release or hardware acceptance** — docs_assistant_behavioral_expansion_actual140_backend_and_disposable_api_checks, docs_assistant_behavioral_expansion_local_ollama_mixed_route_and_token_report_verification, docs_assistant_behavioral_expansion_behavioral_validation_excludes_visual_and_training_acceptance [EXTRACTED 1.00]
- **Measured synthetic corpus uses family splits and bounded runtime retrieval without weight training** — docs_assistant_behavioral_expansion_original_behavioral443_categories_and343100_split, docs_assistant_behavioral_expansion_measured_text_tokens18977_with_explicit_exclusions, docs_assistant_behavioral_expansion_qwen_tokenizer_provenance_and_checksum_report, docs_assistant_behavioral_expansion_family_splits_and_prior_evaluation_exclusion, docs_assistant_behavioral_expansion_behavioral_references_are_not_live_answers_or_whole_prompts, docs_assistant_behavioral_expansion_combined634_corpus_and_approval_context_invalidation [EXTRACTED 1.00]
- **Read-only delivery persist-before-ACK and durable receipts gate a single physical start** — docs_device_command_delivery_atomic_reservation_creation_and_read_only_command_polling, docs_device_command_delivery_persist_before_ack_accepted_reservation_receipt, docs_device_command_delivery_stable_receipt_retries_and_explicit_rejection_codes, docs_device_command_delivery_receipt_required_non_expired_physical_start_and_terminal_replay [EXTRACTED 1.00]
- **Conservative review preserves assignment and evidence until future trusted reconciliation** — docs_device_command_delivery_read_only_expiry_detection_versus_persisted_conservative_hold, docs_device_command_delivery_reason_and_revision_protected_staff_review_is_not_abort, docs_device_command_delivery_no_force_release_or_automatic_no_show_resolution, docs_remaining_work_next_trusted_reconciliation_then_guarded_operator_resolution [EXTRACTED 1.00]
- **Synthetic API and file-journal evidence does not prove process-kill NVS or physical behavior** — docs_device_command_delivery_single_step_emulator_scope_and_ignored_bounded_journal, docs_device_command_delivery_backend213_and_api_emulator_recreation_evidence, docs_device_command_delivery_frontend36_brave_axe_and_xampp_operational_evidence, docs_device_command_delivery_unverified_physical_reconciliation_and_release_gates [EXTRACTED 1.00]
- **Structural freshness and semantic refresh both require source and privacy checks** — docs_graphify_setup_graph_query_structural_update_and_semantic_refresh, docs_graphify_setup_watcher_and_optional_hooks_are_not_startup_services, docs_graphify_setup_privacy_exclusions_and_limits_of_graph_evidence [EXTRACTED 1.00]
- **Authenticated revision-only invalidations preserve role and HTTP control boundaries** — docs_live_updates_separate_staff_and_player_live_channels_with_no_public_stream, docs_live_updates_revision_only_frames_expose_no_entity_or_score_data, docs_live_updates_origin_session_revalidation_and_rejected_socket_commands, docs_live_updates_bounded_socket_capacity_and_incoming_resources [EXTRACTED 1.00]
- **Local software validation remains distinct from process-kill LAN load and cabinet gates** — docs_live_updates_backend197_tests_and_replacement_dispatcher_coverage, docs_live_updates_frontend33_tests_and_production_build_evidence, docs_live_updates_synthetic_brave_live_flow_and_limited_latency_samples, docs_live_updates_open_process_kill_lan_phone_and_hardware_acceptance, docs_live_updates_one_worker_deployment_and_unfinished_device_recovery [EXTRACTED 1.00]
- **Transactional revisions outbox and coherent snapshots tolerate repeated or missed hints** — docs_live_updates_global_event_revisions_atomic_with_state_and_outbox, docs_live_updates_lifespan_dispatcher_batches_committed_rows_and_coalesces, docs_live_updates_publication_is_not_delivery_and_replay_is_harmless, docs_live_updates_coherent_snapshot_revisions_and_stale_read_rejection, docs_live_updates_reconnect_fallback_cadence_and_freshness_ui [EXTRACTED 1.00]
- **Current typed semantics select the correct bounded score tool and evidence basis** — docs_nlp_grounding_research_schema_derived_domain_measure_and_operation_features, docs_nlp_grounding_research_current_explicit_measure_and_operation_precedence, docs_nlp_grounding_research_definitions_aggregates_and_individual_scores_are_distinct, docs_nlp_grounding_research_compatible_deduplicated_lexical_demonstrations, docs_nlp_grounding_research_get_player_scores_bounded_best_result_listing, docs_nlp_grounding_research_score_privacy_snapshot_and_no_ddl_context_extension [EXTRACTED 1.00]
- **Primary research motivates locally constrained serving adaptations rather than model guarantees** — docs_nlp_grounding_research_checklist_capability_testing_research_and_adaptation, docs_nlp_grounding_research_canard_typed_ellipsis_research_and_adaptation, docs_nlp_grounding_research_lex_validated_intent_slot_research_and_local_adaptation, docs_nlp_grounding_research_ollama_structured_output_research_versus_semantic_correctness, docs_nlp_grounding_research_google_rules_ml_infrastructure_evaluation_adaptation [EXTRACTED 1.00]
- **Settings relocation and targeted validation retain explicit acceptance limits** — docs_nlp_grounding_research_authenticated_settings_relocation_and_last_answer_review, docs_nlp_grounding_research_shared_administrator_session_settings_state, docs_nlp_grounding_research_actual184_backend_and_score_semantics_verification, docs_nlp_grounding_research_twelve_local_ollama_probes_and_bounded_inference_conclusions, docs_nlp_grounding_research_frontend27_build_and_headless_brave_verification_limits [EXTRACTED 1.00]
- **Combined launch readiness and process ownership** — docs_local_setup_combined_launcher_starts_api_waits_readiness_then_vite, docs_local_setup_manual_xampp_and_launcher_owned_process_lifecycle, docs_local_setup_optional_api_only_and_frontend_only_npm_startup, docs_local_setup_installed_node_startup_independent_of_codex_versioned_runtime, docs_local_setup_connection_refused_reflects_missing_api_and_readiness_timeout, docs_local_setup_session401_differs_from_connectivity_and_prior200_is_time_specific [EXTRACTED 1.00]
- **Origin compatibility retains scheme port Host and CSRF boundaries** — docs_qr_scanner_shared_backend_browser_write_and_qr_entry_origin_policy, docs_qr_scanner_loopback_aliases_retain_matching_scheme_and_port, docs_qr_scanner_configured_public_additional_request_host_and_development_origins, docs_qr_scanner_vite_preserves_public_host_without_rewriting_browser_origin, docs_qr_scanner_restart_both_servers_and_defer_request_origin_verification [EXTRACTED 1.00]
- **Local normalization and shared origin policy preserve token validation** — docs_qr_scanner_canonical_local_entry_url_normalization_across_encoded_hosts, docs_qr_scanner_backend_normalized_origin_registered_token_and_enabled_validation, docs_qr_scanner_qrcontent_and_camera_or_upload_method_request_contract, docs_qr_scanner_shared_backend_browser_write_and_qr_entry_origin_policy [EXTRACTED 1.00]
- **Explicit pause and separately authorized font update** — agents_explicit_user_pause_overrides_continuation, docs_readme_paused_baseline_and_confirmed_typeface, frontend_readme_font_change_scoped_verification_and_pause [INFERRED 0.95]
- **Shared locally bundled typography and preserved symbol foundation** — agents_shared_open_sans_and_font_awesome_conventions, docs_dashboard_design_confirmed_open_sans_variable_typography, frontend_readme_shared_foundation_radix_and_local_fonts [INFERRED 0.95]

## Communities (56 total, 17 thin omitted)

### Community 0 - "icons.jsx / ui.jsx"
Cohesion: 0.05
Nodes (136): AdminOnly(), App(), PlayerOnly(), ActivityChart(), axis, ChartTip(), LevelChart(), OutcomesChart() (+128 more)

### Community 1 - "create_app() / execute()"
Cohesion: 0.11
Nodes (50): execute(), one(), acknowledge(), hold_for_review(), record_change(), create_app(), active(), admin_session() (+42 more)

### Community 2 - "api() / AdminAssistant.jsx"
Cohesion: 0.05
Nodes (44): AdminAssistant(), send(), submit(), answerLabels, Evidence(), suggestions, mocks, openChat() (+36 more)

### Community 3 - "Current QR player flow and administrator access / Durable browser updates"
Cohesion: 0.10
Nodes (5): Functional specification baseline, Pending physical hardware performance and recovery acceptance, Proposed classic-v1 game rules, Scoped metric denominators and local-day bounds, Durable browser updates

### Community 4 - "Assistant / Question"
Cohesion: 0.13
Nodes (21): Assistant, Question, test_new_social_turns_work_with_ollama_disabled_and_preserve_context(), scenario(), test_specific_reported_greeting_through_the_service_without_ollama(), scenario(), test_answer_enqueues_only_metadata_without_waiting_for_audit(), scenario() (+13 more)

### Community 5 - "main.py / test_assistant_memory.py"
Cohesion: 0.09
Nodes (16): Review, all_rows(), poll_commands(), requires_review(), Admissions, device_commands(), Entry, Heartbeat (+8 more)

### Community 6 - "normalize() / test_assistant.py"
Cohesion: 0.13
Nodes (23): interpretation_choices(), normalize(), RoutingPlan, test_ambiguous_question_gets_exactly_two_safe_scoped_interpretations(), test_clear_questions_do_not_get_two_options(), test_explaining_privacy_does_not_allow_identity_retrieval(), test_explicit_system_subject_beats_an_older_conversation(), test_missing_unrelated_subject_is_not_silently_replaced_with_event_facts() (+15 more)

### Community 7 - "analytics.py"
Cohesion: 0.26
Nodes (8): clean(), collect(), collect_all(), _collect_snapshot(), _operations(), select(), stamp(), analytics()

### Community 8 - "json / test_assistant_learning.py"
Cohesion: 0.13
Nodes (17): interaction_rows(), corpus_digest(), retrieve(), seed_examples(), _seed_examples(), signature(), Proposal, TrainingInput (+9 more)

### Community 10 - "test_device_commands.py / test_live_updates.py"
Cohesion: 0.13
Nodes (25): automatic_scope(), compose_all(), test_absent_device_results_are_not_inferred_from_registrations(), test_all_sources_are_separate_and_players_are_deduplicated(), test_default_scope_and_natural_followups(), revision(), test_global_revisions_and_idempotent_operations(), test_live_rejects_missing_or_foreign_origin() (+17 more)

### Community 11 - "test_player_flow.py / setup_local.py"
Cohesion: 0.08
Nodes (17): Settings, make_engine(), register(), session(), csrf_for(), digest(), encrypt_identity(), identity_lookup() (+9 more)

### Community 12 - "assistant.py / conversational_reply()"
Cohesion: 0.12
Nodes (21): inspect(), basic_response(), conversational_reply(), endpoint(), intent_payload(), composed_social(), parse(), greeting_answer() (+13 more)

### Community 13 - "frontend/package.json / dependencies"
Cohesion: 0.11
Nodes (23): dependencies, @fontsource-variable/open-sans@5.3.0, html5-qrcode@2.3.8, qrcode.react@4.2.0, @radix-ui/react-dialog@1.3.1, @radix-ui/react-dropdown-menu@2.2.1, react@19.3.1, react-dom@19.3.1 (+15 more)

### Community 14 - "test_device_commands.py"
Cohesion: 0.15
Nodes (15): CommandAcknowledgement, CommandEmulator, command_row(), reserve(), test_emulator_refuses_corrupt_journal_before_contacting_device(), test_expired_unknown_start_never_becomes_an_automatic_no_show(), test_invalid_or_stale_receipts_cannot_change_the_command(), test_other_machine_commands_and_maintenance_cannot_be_bypassed() (+7 more)

### Community 16 - "test_assistant_training.py / candidate()"
Cohesion: 0.16
Nodes (12): test_ambiguous_query_does_not_query_live_data_until_choice(), ready(), test_exact_correction_routes_without_model_but_reads_fresh_data(), test_learning_is_owner_scoped_approved_current_and_disableable(), approve(), candidate(), test_duplicate_does_not_overwrite_reviewed_label_and_context_change_needs_review(), test_owner_queue_has_a_bounded_capacity() (+4 more)

### Community 19 - "Player QR scanner implementation and entry contract / Shared backend browser-write and QR entry orig"
Cohesion: 0.18
Nodes (13): Backend normalized origin registered token and enabled validation, Canonical local entry URL normalization across encoded hosts, Configured public additional request-host and development origins, Current-event registration PNG export excluded from project graph, Existing html5-qrcode2.3.8 scanner APIs, Existing scanner suite descriptions and correction verification limits, Local camera and image scanning with explicit permission, Loopback aliases retain matching scheme and port (+5 more)

### Community 20 - "schema.sql / staff_users"
Cohesion: 0.25
Nodes (18): ai_admin_memory, ai_requests, ai_training_examples, audit_logs, auth_sessions, device_commands, device_events, events (+10 more)

### Community 22 - "001_initial.sql / game_sessions"
Cohesion: 0.28
Nodes (16): ai_requests, audit_logs, auth_sessions, device_commands, device_events, events, game_sessions, machines (+8 more)

### Community 24 - "review-pages.mjs / @playwright/test"
Cohesion: 0.14
Nodes (8): @playwright/test@1.65.1, directory, errors, height, results, routes, width, @playwright/test

### Community 25 - "devDependencies / vite.config.js"
Cohesion: 0.13
Nodes (14): devDependencies, jsdom@31.0.1, prettier@3.10.1, @testing-library/jest-dom@7.0.1, @testing-library/react@16.3.3, @testing-library/user-event@14.6.10, vite@8.3.8, @vitejs/plugin-react@6.3.0 (+6 more)

### Community 26 - "Dependency-ordered implementation plan / Command step4 complete portion and pending resolution"
Cohesion: 0.12
Nodes (4): Dependency-ordered implementation plan, Open hardware rules TLS provider and retention decisions, Primary-source research evidence, Source-backed decisions and open gates

### Community 27 - "dev.mjs / main()"
Cohesion: 0.17
Nodes (10): backend, backendOnly, frontend, health(), main(), owned, portInUse(), root (+2 more)

### Community 29 - "LiveHub / test_outbox_is_atomic_and_recovers_after_dispatcher_restart()"
Cohesion: 0.25
Nodes (5): LiveHub, test_outbox_is_atomic_and_recovers_after_dispatcher_restart(), restart(), test_slow_clients_coalesce_and_connection_caps_are_bounded(), check()

### Community 32 - "Current QR player flow and administrator access"
Cohesion: 0.13
Nodes (20): Authenticated synthetic-tested device integration boundary, Completed-round-only source-matched player leaderboard, Current QR player flow and administrator access, Durable win loss alerts with focus-refresh polling, Explicit Queue-page simulator action sequence, Owner-only persistent ticket across refreshes, Preserved Sourcio-derived player styling and font symbols, Private cabinetState and queueState waiting reasons (+12 more)

### Community 33 - "requested_metrics() / constraints()"
Cohesion: 0.24
Nodes (11): requested_metrics(), resolve_routing(), compatible(), constraints(), refers_to_previous(), resolve_subject(), semantic_words(), test_definition_and_ellipsis_are_distinct_from_a_new_data_subject() (+3 more)

### Community 34 - "Local React and backend setup / Combined launcher starts API waits readiness then Vite"
Cohesion: 0.23
Nodes (8): Combined launcher starts API waits readiness then Vite, Direct backend .venv uvicorn startup without activation, Documented user-installed Node24 npm11 and Python3.13 versions, Installed Node startup independent of Codex versioned runtime, Local React and backend setup, npm ci and Python virtual environment dependency reinstall, Optional API-only and frontend-only npm startup, Restart terminal application after user PATH setup

### Community 35 - "Context"
Cohesion: 0.18
Nodes (14): compose(), Context, Intent, SavedMemory, empty_summary(), fixture_data(), test_api_answers_scores_not_a_wrong_model_or_saved_subject(), test_memory_schema_has_no_place_for_raw_text_or_invented_metrics() (+6 more)

### Community 36 - "context_version() / TrainingStore"
Cohesion: 0.36
Nodes (3): canonical(), context_version(), TrainingStore

### Community 38 - "Canonical documentation index and authority"
Cohesion: 0.08
Nodes (3): Dashboard design contract, Canonical documentation index and authority, Public Stack Moko Baby introduction and installation guide

### Community 39 - "main.jsx / @radix-ui/react-tooltip"
Cohesion: 0.18
Nodes (4): @fortawesome/fontawesome-free@7.3.1, @radix-ui/react-tooltip@1.4.1, @fortawesome/fontawesome-free, @radix-ui/react-tooltip

### Community 40 - "package.json / scripts"
Cohesion: 0.18
Nodes (10): engines, node, name, private, scripts, dev, dev:backend, dev:frontend (+2 more)

### Community 41 - "test_assistant_generalization.py"
Cohesion: 0.35
Nodes (7): canonical(), replay(), simulated_result(), seed_scores(), test_player_score_sql_is_paginated_and_keeps_source_evidence(), test_shared_scoring_vectors(), test_timeout_and_tamper_rejection()

### Community 42 - "002_player_flow.sql / entry_grants"
Cohesion: 0.32
Nodes (4): entry_grants, login_attempts, player_notifications, qr_links

### Community 44 - "scripts / build"
Cohesion: 0.25
Nodes (8): scripts, build, dev, dev:frontend, format, preview, test, test:browser

### Community 46 - "origin_allowed() / origins.py"
Cohesion: 0.33
Nodes (4): boundaries(), live_updates(), canonical_origin(), origin_allowed()

### Community 48 - "flows.spec.js / @axe-core/playwright"
Cohesion: 0.29
Nodes (3): errors, @axe-core/playwright@4.14.0, @axe-core/playwright

### Community 51 - "QR access and theme five-pass refinement log / Documented current Edge accessibility unit and produc"
Cohesion: 0.50
Nodes (4): Access flow contrast mobile and verification refinement passes, Documented current Edge accessibility unit and production checks, Historical eight-page sample review evidence, QR access and theme five-pass refinement log

### Community 52 - ".prettierrc.json / printWidth"
Cohesion: 0.40
Nodes (4): printWidth, semi, singleQuote, trailingComma

### Community 54 - "Pinned backend dependency manifest / Pinned Argon2 and cryptography security dependencies"
Cohesion: 0.67
Nodes (3): Pinned Argon2 and cryptography security dependencies, Pinned backend dependency manifest, Pinned FastAPI SQLAlchemy PyMySQL Uvicorn runtime

## Knowledge Gaps
- **89 isolated node(s):** `request_receipts`, `login_attempts`, `request_receipts`, `semi`, `singleQuote` (+84 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 377 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Assistant` connect `Assistant / Question` to `json / test_assistant_learning.py`, `create_app() / execute()`, `assistant.py / conversational_reply()`, `MemoryStore / test_forget_has_csrf_and_prevents_old_inflight_memory_from_returning()`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `create_app()` (e.g. with `Question` and `Proposal`) actually correct?**
  _`create_app()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `request_receipts`, `login_attempts`, `request_receipts` to the rest of the system?**
  _89 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `icons.jsx / ui.jsx` be split into smaller, more focused modules?**
  _Cohesion score 0.050748346675948484 - nodes in this community are weakly interconnected._
- **Why does `conversational_reply()` connect `assistant.py / conversational_reply()` to `Context`, `normalize() / test_assistant.py`?**
  _High betweenness centrality (0.000) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `Assistant` (e.g. with `MemoryStore` and `Proposal`) actually correct?**
  _`Assistant` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Should `create_app() / execute()` be split into smaller, more focused modules?**
  _Cohesion score 0.10734463276836158 - nodes in this community are weakly interconnected._