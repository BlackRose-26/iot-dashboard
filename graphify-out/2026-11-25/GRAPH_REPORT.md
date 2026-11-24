# Graph Report - iot-dashboard  (2026-11-25)

## Corpus Check
- 275 files · ~190,508 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 23 file(s) not represented in the graph (top: (none) 7, .css 7, .cmd 4)

## Summary
- 2403 nodes · 7124 edges · 115 communities (97 shown, 18 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 291 edges (avg confidence: 0.88)
- Token cost: 307,490 input · 0 output

## Graph Freshness
- Built from commit: `a35f5f69`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- GameScreen.jsx
- evaluate_holdout.py
- 23 confirmed defects fixed (CSRF, origin, identity switching, QR, readiness, NLP scope)
- assistant.py
- create_app
- Dashboard UI Primitives
- Project Rules and Index
- api
- test_assistant_admission_v2.py
- Assistant Question Pipeline
- Project documentation index (canonical internal guide)
- normalize
- test_device_recovery.py
- run.py
- build_language_lexicon.py
- siteStyles.js
- useApp
- rehearse_event.py
- execute
- npm run online:firmware launcher
- Dashboard and registration design research
- Question Review Pages
- Analytics.jsx
- QR Player Flow Docs
- Frontend Dependencies
- pytest
- The web game screen (default game display)
- Assistant Training Datasets Doc
- experiment_history.py
- Settings
- argparse
- Render Blueprint
- Cloudflare Quick Tunnel
- stack_moko_baby connected firmware (protocol v2)
- uuid
- NLP admission repair — 24 November 2026
- Analytics-v1 runtime and development AI system rules
- Offline Classifier Experiment
- Candidate MySQL Schema
- test_player_flow.py
- Device Command Tests
- Conservative review hold
- Architecture and Graphify Docs
- Durable browser updates
- NLP Grounding Research
- Vite and Tailwind Build
- Initial Database Migration
- Queue.jsx
- Functional Spec and Matrix Rules
- Playwright Browser Tests
- Scanner.jsx
- Root Package Scripts
- numpy
- assistant_training.py
- Behavioral Expansion Corpus
- check_quality.py
- db-backup.py
- flows.spec.js
- Stack Moko Baby backend
- LiveHub
- Frontend Package Scripts
- answer
- Online Tunnel Launcher
- main.py
- api
- Firmware Transport Job
- dev.mjs
- Physical cabinet bring-up over a phone hotspot
- check_quality.py
- Player Flow Migration
- Step 8: constrained AI analytics
- fastapi
- quality-checks.mjs
- Boot registration (POST /api/device/boot)
- Wokwi Wiring Diagram
- assistant.py
- test_db_backup.py
- configure-firmware.py
- Read-only command polling (GET /api/device/commands)
- analytics.py
- Firmware Game Engine
- Prettier Config
- test_nlp_lab.py
- AppContext.jsx
- Backend Dependency Pins
- re
- Game and Firmware Steps
- Frontend HTML Entry
- event_lock
- Repository Scaffold Step
- active_rules
- RecoveryEmulator
- test-setup.js
- text
- Public language projection (contractions, reviewed synonyms, bounded inflections)
- Persist-before-ACK reservation receipt
- test_identity_retention.py
- FakeSocket
- Self-test stages (panel chain, orientation, button, strip, audio)
- security.py
- test_assistant_continuation.py
- subprocess
- device_emulator.py
- NLP lab offline requirements
- Database backups and restore
- Stack Moko Baby — firmware
- Wrong-topic answers and generic replies — 24 November 2026

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 134 edges
2. `normalize()` - 100 edges
3. `execute()` - 98 edges
4. `one()` - 93 edges
5. `Context` - 72 edges
6. `Assistant` - 71 edges
7. `now()` - 69 edges
8. `api()` - 66 edges
9. `useApp()` - 61 edges
10. `Card()` - 46 edges

## Surprising Connections (you probably didn't know these)
- `Changes` --references--> `project_words()`  [INFERRED]
  docs/nlp-topic-repair.md → backend/app/assistant_language.py
- `Changes` --references--> `project_words()`  [INFERRED]
  docs/nlp-admission-repair.md → backend/app/assistant_language.py
- `Changes` --references--> `asks_live_state()`  [INFERRED]
  docs/nlp-topic-repair.md → backend/app/assistant.py
- `Changes` --references--> `composed_social()`  [INFERRED]
  docs/nlp-topic-repair.md → backend/app/assistant_interactions.py
- `Changes` --references--> `constraints()`  [INFERRED]
  docs/nlp-topic-repair.md → backend/app/assistant_semantics.py

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
- **Future evaluation review isolates held-out cases and versions decisions without rewriting evidence** — docs_assistant_training_evaluation_review_later, docs_assistant_training_evaluation_actions, docs_assistant_training_evaluation_separation, docs_assistant_training_evaluation_blinding, docs_assistant_training_evaluation_history [EXTRACTED 1.00]
- **History experiment evidence remains consumed regression; latercandidateauthoring doesnotimply revieworaccuracy** — docs_nlp_evaluation_history_lab_20261120_history_report, docs_nlp_evaluation_history_lab_20261120_history_measured, docs_nlp_evaluation_history_lab_20261120_coverage_failure, docs_nlp_evaluation_history_lab_20261120_admission_bottleneck, docs_nlp_evaluation_history_lab_20261120_history_no_promotion, docs_nlp_evaluation_history_lab_20261120_final_pending [EXTRACTED 1.00]
- **Constrained interpretation with fresh server-owned facts** — docs_ai_system_rules_language_policy, docs_ai_system_rules_current_measure, docs_ai_system_rules_typed_memory_policy, docs_ai_system_rules_reviewed_example_policy, docs_ai_system_rules_read_only_tools, docs_ai_system_rules_factual_response_enforcement [EXTRACTED 1.00]
- **Boot-bound protocol v2 recovery flow** — docs_device_recovery_boot_registration, docs_device_recovery_journal_endpoint, docs_device_recovery_fence_command, docs_device_recovery_persistent_stop_tombstone, docs_device_recovery_operator_resolution, docs_esp32_online_nvs_journal [EXTRACTED 1.00]
- **Tailwind styling foundation** — docs_tailwind_ui_build_cascade, docs_tailwind_ui_semantic_tokens, docs_tailwind_ui_admin_dark_variant, frontend_src_styles_tailwind, frontend_src_components_ui [EXTRACTED 1.00]
- **V11 assistant language pipeline stages** — docs_nlp_routing_repair_privacy_before_projection, docs_nlp_routing_repair_public_lexical_projection, docs_nlp_routing_repair_deterministic_fast_path, docs_nlp_routing_repair_topical_scope_decision [EXTRACTED 1.00]
- **Matrix v1 ESP32 firmware dependencies** — agents_matrix_v1_device_decision, firmware_stack_moko_baby_libraries_adafruit_neopixel, firmware_stack_moko_baby_libraries_arduinojson [INFERRED 0.75]
- **Free tunnel online firmware pipeline** — docs_free_online_online_firmware_command, docs_free_online_quick_tunnel, docs_free_online_certificate_preparation, docs_free_online_merged_image, docs_hardware_bringup_online_device, docs_hardware_bringup_flash_device_script [INFERRED 0.85]
- **Stack Intelligence NLP evaluation and offline experimentation** — agents_evaluation_holdout_rule, readme_nlp_holdout_results, docs_readme_offline_classifier_comparison, docs_readme_history_ablation, backend_nlp_lab_requirements_setfit [INFERRED 0.85]
- **NLP evaluation freeze/consume/regression discipline** — docs_nlp_evaluation_holdout_v1_frozen_protocol, docs_nlp_evaluation_holdout_v1_consumption_ledger, backend_replay_consumed_holdout, docs_nlp_evaluation_candidate_v2_preparation_review_protocol, docs_nlp_routing_repair_v11_regression [INFERRED 0.85]
- **NVS journal preservation safeguards** — docs_hardware_bringup_flash_device_script, docs_free_online_merged_image, docs_esp32_online_nvs_journal, docs_device_recovery_storage_lineage [INFERRED 0.85]
- **Free HTTPS tunnel and phone-hotspot device operation path** — agents_free_hosting_decision, readme_online_firmware_launcher, agents_phone_hotspot_network_decision, readme_online_device, docs_readme_physical_cabinet_preparation [INFERRED 0.85]

## Communities (115 total, 18 thin omitted)

### Community 0 - "GameScreen.jsx"
Cohesion: 0.05
Nodes (42): COLORS, Deadline(), drawBoard(), GameScreen(), connectButton(), fullScreen(), Overlay(), readFlag() (+34 more)

### Community 1 - "evaluate_holdout.py"
Cohesion: 0.06
Nodes (56): inspect(), corpus_digest(), model_json(), scope_payload(), ScopePlan, packet(), measure(), check() (+48 more)

### Community 2 - "23 confirmed defects fixed (CSRF, origin, identity switching, QR, readiness, NLP scope)"
Cohesion: 0.50
Nodes (4): 23 confirmed defects fixed (CSRF, origin, identity switching, QR, readiness, NLP scope), CSRF and configured-origin trust hardening, QR image API fallback (html5-qrcode failure reproduced), Schema/migration/configuration readiness check

### Community 3 - "assistant.py"
Cohesion: 0.09
Nodes (28): asks_live_state(), constrained_route(), intent_payload(), composed_social(), parse(), linguistic_text(), routing_input(), compatible() (+20 more)

### Community 4 - "create_app"
Cohesion: 0.08
Nodes (51): all_rows(), read_reviews(), save_review(), create_app(), add_operator(), admin_session(), admissions(), analytics() (+43 more)

### Community 5 - "Dashboard UI Primitives"
Cohesion: 0.09
Nodes (58): ArrowLeft, ArrowRight, ArrowUpRight, CheckCircle2, ChevronDown, ChevronLeft, ChevronRight, CircuitBoard (+50 more)

### Community 6 - "Project Rules and Index"
Cohesion: 0.07
Nodes (28): .claude/CLAUDE.md graphify skill pointer, graphify skill (/graphify trigger), AGENTS.md project instructions, Confirmed stack: React/JSX, Vite, Tailwind, FastAPI, XAMPP MariaDB 10.11.16, Free PC + XAMPP + HTTPS tunnel hosting decision, Frontend conventions (Tailwind v4 tw: prefix, Font Awesome webfonts, Open Sans Variable), html5-qrcode scanner rule, Matrix v1 device decision (16 columns, 15 levels, 1 point per level) (+20 more)

### Community 7 - "api"
Cohesion: 0.13
Nodes (25): AssistantTrainingReview(), choose(), exportApproved(), load(), remove(), review(), save(), submit() (+17 more)

### Community 8 - "test_assistant_admission_v2.py"
Cohesion: 0.09
Nodes (18): contextual_follow_up(), lexical_resource(), topic_choices(), outside_event(), canonical(), context_version(), TrainingStore, test_choices_only_name_topics_that_the_question_mentions() (+10 more)

### Community 9 - "Assistant Question Pipeline"
Cohesion: 0.08
Nodes (32): Assistant, automatic_scope(), basic_response(), knowledge_response(), MemoryPreferences, preference_reply(), Question, run() (+24 more)

### Community 10 - "Project documentation index (canonical internal guide)"
Cohesion: 0.09
Nodes (35): Device command delivery and review holds, Boot-bound device recovery, Stack Moko Baby step-by-step build plan, Current device/hosting milestone: Wokwi, Matrix v1 and free HTTPS tunnel (22 Nov 2026), Matrix v1 game (16 columns, 15 levels, max 15 points), Admin question review (/admin/question-review, migration 006), Step 7: durable live updates, Step 9: event readiness and release rehearsal (+27 more)

### Community 11 - "normalize"
Cohesion: 0.07
Nodes (55): compose(), compose_all(), Context, endpoint(), Intent, normalize(), requested_metrics(), resolve_routing() (+47 more)

### Community 12 - "test_device_recovery.py"
Cohesion: 0.25
Nodes (25): emulator_setup(), fence(), fence_receipt(), resolution(), setup(), start_event(), test_a_new_boot_invalidates_an_old_fence_and_changed_storage_blocks_never_started(), test_boot_lineage_retries_retirement_and_legacy_bypass() (+17 more)

### Community 13 - "run.py"
Cohesion: 0.36
Nodes (11): text(), code_hashes(), evaluate_model(), finish_model(), freeze(), load(), main(), run_baseline() (+3 more)

### Community 14 - "build_language_lexicon.py"
Cohesion: 0.16
Nodes (6): build(), build_v2(), digest(), Links, word_form(), wordnet_rows()

### Community 15 - "siteStyles.js"
Cohesion: 0.08
Nodes (24): band, bandLabel, bandTitle, bandValue, box, boxText, boxTitle, button (+16 more)

### Community 16 - "useApp"
Cohesion: 0.16
Nodes (23): AdministratorsOnly(), AdminOnly(), App(), PlayerOnly(), Check, Menu, QrCode, RegistrationQR() (+15 more)

### Community 17 - "rehearse_event.py"
Cohesion: 0.20
Nodes (8): test_database(), main(), operator(), percentile(), phone(), Recorder, start_tunnel(), wait_ready()

### Community 18 - "execute"
Cohesion: 0.18
Nodes (26): execute(), one(), acknowledge(), hold_for_review(), current_boot(), journal(), quarantine(), recovery_view() (+18 more)

### Community 19 - "npm run online:firmware launcher"
Cohesion: 0.25
Nodes (9): start-online-preview.ps1 manual tunnel preview, ESP32 core 4.0.0 TLS watchdog reboot, ESP32 core 2.0.17 compatibility build, Merged Wokwi firmware image, npm run online:firmware launcher, Wokwi public IoT gateway connection blocker, npm run device:flash re-upload, flash-device.py NVS-guarded flasher (+1 more)

### Community 20 - "Dashboard and registration design research"
Cohesion: 0.15
Nodes (12): Step 6: reference-matched web views, Tailwind 4.3.5 Vite plugin build and layer cascade (tw prefix, no Preflight), Semantic color tokens via @theme inline (ink, muted, note, surface, canvas, line, danger), Access flow contrast mobile and verification refinement passes, Documented current Edge accessibility unit and production checks, Historical eight-page sample review evidence, QR access and theme five-pass refinement log, Dashboard and registration design research (+4 more)

### Community 21 - "Question Review Pages"
Cohesion: 0.14
Nodes (18): freshTarget(), kinds, topics, actions, Correction(), changeTopic(), subtypesFor(), decisions (+10 more)

### Community 22 - "Analytics.jsx"
Cohesion: 0.13
Nodes (25): ActivityChart(), axis, ChartTip(), LevelChart(), OutcomesChart(), ScoreChart(), CalendarDays, Clock3 (+17 more)

### Community 23 - "QR Player Flow Docs"
Cohesion: 0.15
Nodes (17): Authenticated synthetic-tested device integration boundary, Completed-round-only source-matched player leaderboard, Current QR player flow and administrator access, Durable win loss alerts with focus-refresh polling, Explicit Queue-page simulator action sequence, Owner-only persistent ticket across refreshes, Preserved Sourcio-derived player styling and font symbols, Private cabinetState and queueState waiting reasons (+9 more)

### Community 24 - "Frontend Dependencies"
Cohesion: 0.09
Nodes (27): dependencies, @fontsource-variable/open-sans@5.3.0, @fortawesome/fontawesome-free@7.3.1, html5-qrcode@2.3.8, qr-scanner@1.4.2, qrcode.react@4.2.0, @radix-ui/react-dialog@1.3.1, @radix-ui/react-dropdown-menu@2.2.1 (+19 more)

### Community 25 - "pytest"
Cohesion: 0.12
Nodes (11): simulated_result(), test_matrix_win_timeout_and_invalid_trace(), test_ai_machine_readiness_agrees_with_dashboard_when_cabinet_is_unavailable(), test_chunked_body_limit_cannot_be_bypassed_without_content_length(), test_fresh_disabled_simulator_cannot_accept_a_new_assignment(), test_malformed_login_text_or_unknown_fields_fail_without_server_errors(), test_readiness_requires_applied_migrations_and_schema(), test_terminal_duration_cannot_extend_beyond_the_ending_placement() (+3 more)

### Community 26 - "The web game screen (default game display)"
Cohesion: 0.20
Nodes (10): Button wiring, Code map, Fallbacks and fixes, How a round works, Roles, Setup, Switching back to the LED cabinet, The web game screen (default game display) (+2 more)

### Community 27 - "Assistant Training Datasets Doc"
Cohesion: 0.07
Nodes (26): Optimistic revision current public context confirmation and409staleapproval, 1000recordsperowner25perpage bounded parameterized statement-deadline queries, Future evaluation UI confirm correct reject versioneddecisions navigation progressfilters, Predictions hidden during pre-evaluation label review, Future evaluation UI question proposedlabel typedprior expectedstate explanations notes, Post-consumption corrections preserve originalresult new annotationversion, No player identities private chats or credentials in future review UI, Planned21November dedicated admin evaluationcase review page not implemented (+18 more)

### Community 28 - "experiment_history.py"
Cohesion: 0.13
Nodes (9): run(), DenseModel, fit_temperature(), loss(), Heads, policy(), scaled(), SparseModel (+1 more)

### Community 29 - "Settings"
Cohesion: 0.27
Nodes (7): Settings, serve(), cloud_env(), test_cloud_origin_and_private_database_without_xampp_paths(), test_production_rejects_insecure_cookies(), test_production_rejects_insecure_or_non_origin_public_urls(), main()

### Community 30 - "argparse"
Cohesion: 0.20
Nodes (10): manifest(), prepare(), sha(), protected(), audit(), open_run(), publish(), metrics() (+2 more)

### Community 31 - "Render Blueprint"
Cohesion: 0.08
Nodes (24): mountPath, name, sizeGB, fromService, generateValue, key, sync, value (+16 more)

### Community 32 - "Cloudflare Quick Tunnel"
Cohesion: 0.33
Nodes (6): Prepare and run locally, Wokwi connection choices, install-cloudflared.py verified installer, Cloudflare Quick Tunnel, Phone hotspot to ESP32 to HTTPS tunnel topology, Phone/network deployment

### Community 33 - "stack_moko_baby connected firmware (protocol v2)"
Cohesion: 0.25
Nodes (7): Device journal events (POST /api/device/journal), Journal phases (reserved, started, terminal, fenced_unstarted, fenced_interrupted), Conflict quarantine, stack_moko_baby connected firmware (protocol v2), ESP32 cabinet wiring (GPIO18 matrix, GPIO27 button, GPIO25 strip, GPIO17 DFPlayer), Public Wokwi source bundle (package-wokwi.py), Verified root certificate preparation

### Community 34 - "uuid"
Cohesion: 0.23
Nodes (12): matrix(), pair(), screen(), test_only_an_administrator_pairs_and_the_old_token_stops_working(), test_screen_plays_a_ranked_round_and_pairing_waits_for_it(), test_switching_back_to_the_led_cabinet_restores_its_configured_token(), uid(), add_operator() (+4 more)

### Community 35 - "NLP admission repair — 24 November 2026"
Cohesion: 0.29
Nodes (7): Consumed 325-case replay (regression only), Human-confirmed v2 replay (regression only), Measured results (development data only), NLP admission repair — 24 November 2026, Problem, Still open, Verification

### Community 36 - "Analytics-v1 runtime and development AI system rules"
Cohesion: 0.07
Nodes (26): Stack Intelligence local administrator analytics guide, Explicit owner-reviewed current-version routing examples, Dashboard Settings houses model memory and training controls, Analytics-v1 runtime and development AI system rules, Explicit current measures override history and contradictory model labels, Matrix-aware analytics and cloud AI disabled, Eight bounded allowlisted read-only analytics operations, System grounded learning retrieval and development corpora (+18 more)

### Community 37 - "Offline Classifier Experiment"
Cohesion: 0.04
Nodes (58): 40of120supported blocked upstream;84of130admitted31unknown14scope1measurement, 285originaltraining plus792historyvariants1077rows zero new independent questions, Synthetic variants add no missing subtypes language diversity or independent families, Augmentedpolicy answerszero question-onlypolicy answersone of120supported, Collection was empty at history run;later325AI candidates filled independentreviewpending, Frozen multilingual E5 hierarchical heads history and question-only ablations, Retained protocol variants heads predictions and14offlinechecks, AugmentedE5 ordinary61of130 stress47of120 vsoriginal63and14 (+50 more)

### Community 38 - "Candidate MySQL Schema"
Cohesion: 0.25
Nodes (18): ai_admin_memory, ai_requests, ai_training_examples, audit_logs, auth_sessions, device_commands, device_events, events (+10 more)

### Community 39 - "test_player_flow.py"
Cohesion: 0.11
Nodes (30): test_absent_device_results_are_not_inferred_from_registrations(), test_all_sources_are_separate_and_players_are_deduplicated(), test_review_round_trip_access_and_versioning(), revision(), test_global_revisions_and_idempotent_operations(), test_live_rejects_missing_or_foreign_origin(), test_live_requires_the_right_authenticated_role(), test_logout_revokes_existing_socket_and_commands_are_rejected() (+22 more)

### Community 40 - "Device Command Tests"
Cohesion: 0.24
Nodes (13): command_row(), reserve(), test_emulator_refuses_corrupt_journal_before_contacting_device(), test_expired_unknown_start_never_becomes_an_automatic_no_show(), test_invalid_or_stale_receipts_cannot_change_the_command(), test_other_machine_commands_and_maintenance_cannot_be_bypassed(), test_polling_is_authorized_repeatable_and_contains_no_player_identity(), test_receipt_survives_application_recreation_and_emulator_lost_ack() (+5 more)

### Community 41 - "Conservative review hold"
Cohesion: 0.29
Nodes (6): Flag round for review (admin review endpoint), Machine page command diagnostics, Operator recovery workflow (stop, release, void, recover result), Scan-register-assign-play-result flow, First real round and resilience gates, Accessibility and full event rehearsal

### Community 42 - "Architecture and Graphify Docs"
Cohesion: 0.10
Nodes (9): Local Graphify setup and freshness guide, Stack Moko Baby technology and ownership architecture, Authenticated revision-only invalidation and coherent REST snapshots, Tailwind 4.3.5 semantic utilities Open Sans and Font Awesome webfonts, Bundled public lexicon then projection topical scope and intent routing, Active free PC HTTPS origin with private local database and Ollama, Matrix ownership, active free HTTPS and inactive Render topology, Quality hardening and local recovery/load/restore evidence (+1 more)

### Community 43 - "Durable browser updates"
Cohesion: 0.12
Nodes (3): Durable browser updates, Player QR scanner, React JavaScript frontend with Tailwind conventions

### Community 45 - "Vite and Tailwind Build"
Cohesion: 0.12
Nodes (17): devDependencies, jsdom@31.0.1, @playwright/test@1.65.1, prettier@3.10.1, tailwindcss@4.3.5, @tailwindcss/vite@4.3.5, @testing-library/react@16.3.3, @testing-library/user-event@14.6.10 (+9 more)

### Community 46 - "Initial Database Migration"
Cohesion: 0.28
Nodes (16): ai_requests, audit_logs, auth_sessions, device_commands, device_events, events, game_sessions, machines (+8 more)

### Community 47 - "Queue.jsx"
Cohesion: 0.15
Nodes (34): actions, DeviceRecovery(), GameScreenPairing(), Info, Pause, Play, Radio, Search (+26 more)

### Community 48 - "Functional Spec and Matrix Rules"
Cohesion: 0.10
Nodes (8): Dashboard visual contract with Tailwind integration, Classic v1 ruleset (preserved), Matrix v1 ruleset, 006_matrix_rules.sql migration, Selected Matrix v1 supersedes Classic-only proposals, Stack Moko Baby — functional specification, Pending physical, identity and network release decisions, Migration 006 Matrix rules and authenticated command ordering

### Community 49 - "Playwright Browser Tests"
Cohesion: 0.10
Nodes (8): sizes, directory, errors, height, results, routes, width, @playwright/test

### Community 50 - "Scanner.jsx"
Cohesion: 0.08
Nodes (40): chatContext(), ChatWidget(), dismissNudge(), openChat(), remember(), seen(), mocks, show() (+32 more)

### Community 51 - "Root Package Scripts"
Cohesion: 0.09
Nodes (21): engines, node, name, private, scripts, db:backup, db:purge-ids, db:verify (+13 more)

### Community 52 - "numpy"
Cohesion: 0.20
Nodes (4): main(), plot(), main(), measured()

### Community 53 - "assistant_training.py"
Cohesion: 0.08
Nodes (28): interpretation_choices(), retrieve(), seed_examples(), _seed_examples(), semantic_features(), signature(), Proposal, Review (+20 more)

### Community 55 - "check_quality.py"
Cohesion: 0.22
Nodes (7): make_engine(), main(), migrate(), seed(), main(), environment(), main()

### Community 56 - "db-backup.py"
Cohesion: 0.22
Nodes (19): api_running(), app_login(), backup_dir(), backup_key(), client_args(), client_env(), env_values(), latest() (+11 more)

### Community 57 - "flows.spec.js"
Cohesion: 0.29
Nodes (3): errors, @axe-core/playwright@4.14.0, @axe-core/playwright

### Community 58 - "Stack Moko Baby backend"
Cohesion: 0.06
Nodes (21): Applied typed-memory and reviewed-example migrations, Matrix rules and active free same-origin HTTPS backend, Stack Moko Baby backend, Private player journey, live channels and phone HTTPS, Student identity raw questions and private values excluded from model context, ESP32, Wokwi and online operation, Firmware files and wiring, Journal and operational limits (+13 more)

### Community 59 - "LiveHub"
Cohesion: 0.25
Nodes (5): LiveHub, test_outbox_is_atomic_and_recovers_after_dispatcher_restart(), restart(), test_slow_clients_coalesce_and_connection_caps_are_bounded(), check()

### Community 60 - "Frontend Package Scripts"
Cohesion: 0.12
Nodes (17): scripts, build, db:backup, db:verify, dev, dev:frontend, device:bridge, device:flash (+9 more)

### Community 61 - "answer"
Cohesion: 0.20
Nodes (13): answer(), classify(), is_tagalog(), line_sentence(), minutes(), stage(), facts(), mine_score() (+5 more)

### Community 62 - "Online Tunnel Launcher"
Cohesion: 0.21
Nodes (15): backend, backupMinutes, backupNow(), children, completed(), ensureMysql(), main(), mysqld (+7 more)

### Community 63 - "main.py"
Cohesion: 0.11
Nodes (20): APIInput, BootRegistration, JournalEvent, Placement, RecoveryReason, RecoveryResolution, Result, Admissions (+12 more)

### Community 64 - "api"
Cohesion: 0.10
Nodes (24): AdminAssistant(), send(), submit(), answerLabels, Evidence(), suggestions, mocks, openChat() (+16 more)

### Community 65 - "Firmware Transport Job"
Cohesion: 0.20
Nodes (7): RequestJob, body, boot, kind, path, response, status

### Community 66 - "dev.mjs"
Cohesion: 0.13
Nodes (14): backend, backendOnly, frontend, health(), main(), owned, portInUse(), root (+6 more)

### Community 67 - "Physical cabinet bring-up over a phone hotspot"
Cohesion: 0.29
Nodes (7): 1. Prepare the hotspot phone, 2. Wiring self-test (do this as soon as the wiring is finished), 3. Flash the game firmware for the hotspot, 4. Connection gates (watch the serial monitor and the Machines page), 5. First real round, Physical cabinet bring-up over a phone hotspot, Tools added for the physical board

### Community 68 - "check_quality.py"
Cohesion: 0.12
Nodes (13): replace(), bounded_receive(), main(), receive(), start_api(), percentile(), fetch(), main() (+5 more)

### Community 69 - "Player Flow Migration"
Cohesion: 0.12
Nodes (11): entry_grants, login_attempts, player_notifications, qr_links, ai_admin_memory, ai_training_examples, device_boots, device_journal_events (+3 more)

### Community 70 - "Step 8: constrained AI analytics"
Cohesion: 0.22
Nodes (8): Private per-admin typed memory (migration 003, ai_admin_memory), Reviewed AI training examples (migration 004, ai_training_examples), Stack Intelligence bottom chat (admin shell), Step 0: resolve physical and operational constraints, Step 3: database, identity and staff authentication, Step 4: queue and transactional session assignment, Step 8: constrained AI analytics, Step status and remaining gates table (steps 0-9)

### Community 71 - "fastapi"
Cohesion: 0.17
Nodes (4): RequestSizeLimit, mount_frontend(), test_missing_production_build_fails_at_startup(), test_production_spa_preserves_api_and_private_file_boundaries()

### Community 73 - "Boot registration (POST /api/device/boot)"
Cohesion: 0.33
Nodes (7): Boot registration (POST /api/device/boot), ESP-IDF esp_timer restarts after deep sleep, 005_device_recovery.sql migration, Storage lineage (storageId epoch), Enrollment bootstrap (GET /api/device/enrollment), Connection gates (Wi-Fi, time, registration, heartbeat, ready), Hotspot preparation (2.4 GHz, ASCII name, WPA2)

### Community 74 - "Wokwi Wiring Diagram"
Cohesion: 0.29
Nodes (6): author, connections, dependencies, editor, parts, version

### Community 75 - "assistant.py"
Cohesion: 0.10
Nodes (9): MemoryStore, SavedMemory, Annotation, CaseReview, proposed(), routing(), test_explaining_privacy_does_not_allow_identity_retrieval(), test_forget_has_csrf_and_prevents_old_inflight_memory_from_returning() (+1 more)

### Community 76 - "test_db_backup.py"
Cohesion: 0.14
Nodes (4): scratch(), backup_module(), main(), older_backups()

### Community 77 - "configure-firmware.py"
Cohesion: 0.22
Nodes (4): canonical_origin(), main(), private_lan(), wifi_problem()

### Community 78 - "Read-only command polling (GET /api/device/commands)"
Cohesion: 0.33
Nodes (5): Read-only command polling (GET /api/device/commands), X-Device-Token cabinet authentication, RFC 9110 safe and idempotent methods, ESP-IDF NVS flash commit semantics, Boot-targeted fence command

### Community 79 - "analytics.py"
Cohesion: 0.16
Nodes (16): clean(), collect(), collect_all(), _collect_snapshot(), _operations(), select(), stamp(), replay() (+8 more)

### Community 80 - "Firmware Game Engine"
Cohesion: 0.47
Nodes (3): press(), timeout(), x()

### Community 81 - "Prettier Config"
Cohesion: 0.40
Nodes (4): printWidth, semi, singleQuote, trailingComma

### Community 82 - "test_nlp_lab.py"
Cohesion: 0.15
Nodes (14): balanced_cases(), partitions(), find(), union(), prepare(), Frame, summarize(), test_balanced_development_counts_are_not_independent_holdout_claims() (+6 more)

### Community 83 - "AppContext.jsx"
Cohesion: 0.20
Nodes (11): Reenter(), mocks, open(), TOKEN, AppContext, EMPTY, newest(), useLiveUpdates() (+3 more)

### Community 84 - "Backend Dependency Pins"
Cohesion: 0.67
Nodes (3): Pinned Argon2 and cryptography security dependencies, Pinned backend dependency manifest, Pinned FastAPI SQLAlchemy PyMySQL Uvicorn runtime

### Community 85 - "re"
Cohesion: 0.12
Nodes (20): conversational_reply(), greeting_answer(), interaction_rows(), interaction_social(), interaction_text(), interaction_words(), social_phrases(), social_spelling() (+12 more)

### Community 89 - "event_lock"
Cohesion: 0.25
Nodes (14): poll_commands(), requires_review(), require_boot(), device(), device_ack(), device_boot(), device_commands(), device_journal() (+6 more)

### Community 96 - "active_rules"
Cohesion: 0.30
Nodes (14): active_rules(), stored_rules(), active(), call_next(), context(), leaderboard(), lobby(), machine() (+6 more)

### Community 100 - "text"
Cohesion: 0.25
Nodes (8): question_only(), QuestionOnly, training_variants(), test_augmentation_cannot_ingest_calibration_comparison_or_blocked_rows(), test_existing_contextual_examples_are_never_relabelled_or_given_wrong_subject(), test_history_variants_keep_original_question_target_and_family(), test_question_only_features_do_not_change_with_any_validated_prior_subject(), training_row()

### Community 102 - "Persist-before-ACK reservation receipt"
Cohesion: 0.40
Nodes (4): device_emulator.py file-journal emulator, MariaDB FOR UPDATE row locks, Receipt-required session start, recovery_emulator.py protocol-v2 emulator

### Community 103 - "test_identity_retention.py"
Cohesion: 0.30
Nodes (7): purge(), summary(), load_script(), test_dry_run_is_the_default(), test_older_backup_selection_only_picks_earlier_backups(), test_purge_removes_only_due_ids_then_all_keeping_players_and_tickets(), test_purge_with_nothing_due_changes_nothing()

### Community 106 - "Self-test stages (panel chain, orientation, button, strip, audio)"
Cohesion: 0.50
Nodes (4): DFPlayer audio cues, npm run device:selftest wiring self-test, pixel() matrix mapping, Self-test stages (panel chain, orientation, button, strip, audio)

### Community 107 - "security.py"
Cohesion: 0.29
Nodes (7): register(), session(), csrf_for(), encrypt_identity(), identity_lookup(), set_cookie(), verify_csrf()

### Community 108 - "test_assistant_continuation.py"
Cohesion: 0.33
Nodes (4): continuation(), test_edit_preserves_every_unmentioned_field(), test_new_subject_or_unresolved_content_does_not_reuse_previous_tools(), test_underdefined_or_incompatible_edits_clarify()

### Community 109 - "subprocess"
Cohesion: 0.12
Nodes (16): checks(), fix_power(), main(), on_charger(), pending_restart(), port_open(), power_value(), run() (+8 more)

### Community 110 - "device_emulator.py"
Cohesion: 0.29
Nodes (3): CommandAcknowledgement, CommandEmulator, main()

### Community 111 - "NLP lab offline requirements"
Cohesion: 0.28
Nodes (9): NLP lab offline requirements, datasets 3.6.0, scikit-learn 1.9.1, sentence-transformers 3.4.1, setfit 1.1.3, torch 2.9.1 (CPU), transformers 4.57.6, Follow-on history ablation (792 training-only variants) (+1 more)

### Community 112 - "Database backups and restore"
Cohesion: 0.29
Nodes (7): Commands, Database backups and restore, Deleting student IDs after the event, Keys and privacy, Verification record (24 November 2026), What runs automatically, Where and how backups are stored

### Community 113 - "Stack Moko Baby — firmware"
Cohesion: 0.33
Nodes (6): Behaviour worth knowing, Building and flashing, Files, Pins, Stack Moko Baby — firmware, Status

### Community 114 - "Wrong-topic answers and generic replies — 24 November 2026"
Cohesion: 0.40
Nodes (5): Measured results, Problem, Still open, Verification, Wrong-topic answers and generic replies — 24 November 2026

## Knowledge Gaps
- **391 isolated node(s):** `Why the web screen is the default (assessment, 25 November)`, `Roles`, `Button wiring`, `Setup`, `How a round works` (+386 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 775 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create_app()` connect `create_app` to `active_rules`, `fastapi`, `test_assistant_admission_v2.py`, `Assistant Question Pipeline`, `security.py`, `analytics.py`, `execute`, `answer`, `re`, `check_quality.py`, `event_lock`, `LiveHub`, `Settings`, `pytest`?**
  _High betweenness centrality (0.003) - this node is a cross-community bridge._
- **What connects `Why the web screen is the default (assessment, 25 November)`, `Roles`, `Button wiring` to the rest of the system?**
  _391 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `GameScreen.jsx` be split into smaller, more focused modules?**
  _Cohesion score 0.05040611562350693 - nodes in this community are weakly interconnected._
- **Why does `Assistant` connect `Assistant Question Pipeline` to `normalize`, `execute`, `assistant.py`, `assistant_training.py`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **Should `evaluate_holdout.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05623762376237624 - nodes in this community are weakly interconnected._
- **Why does `environment()` connect `check_quality.py` to `create_app`, `Settings`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **Should `assistant.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08562367864693446 - nodes in this community are weakly interconnected._