# Graph Report - iot-dashboard  (2026-11-24)

## Corpus Check
- 250 files · ~170,925 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 24 file(s) not represented in the graph (top: .css 9, (none) 7, .cmd 4)

## Summary
- 2211 nodes · 6649 edges · 104 communities (87 shown, 17 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 286 edges (avg confidence: 0.88)
- Token cost: 307,490 input · 0 output

## Graph Freshness
- Built from commit: `83de8f5f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Project documentation index (canonical internal guide)
- evaluate_holdout.py
- useLiveUpdates
- assistant.py
- create_app
- Dashboard UI Primitives
- Project Rules and Index
- evaluation_review.py
- Admin Assistant Frontend
- Assistant Question Pipeline
- Verified remaining work
- normalize
- test_device_recovery.py
- check_quality.py
- assistant.py
- run.py
- useApp
- rehearse_event.py
- execute
- stack_moko_baby connected firmware (protocol v2)
- Dashboard visual contract with Tailwind integration
- Question Review Pages
- Analytics.jsx
- QR Player Flow Docs
- Frontend Dependencies
- event-check.py
- review-pages.mjs
- Assistant Training Datasets Doc
- models.py
- test_assistant_admission_v2.py
- one
- Render Blueprint
- ESP32, Wokwi and online operation
- Settings
- database.py
- Database backups and restore
- Analytics-v1 runtime and development AI system rules
- Offline Classifier Experiment
- Candidate MySQL Schema
- test_player_flow.py
- Device Command Tests
- asyncio
- Architecture and Graphify Docs
- pytest
- NLP Grounding Research
- Vite and Tailwind Build
- Initial Database Migration
- Queue.jsx
- Functional Spec and Matrix Rules
- Playwright Browser Tests
- QR Scanner Components
- Root Package Scripts
- json
- assistant_training.py
- Behavioral Expansion Corpus
- os
- db-backup.py
- test_identity_retention.py
- Stack Moko Baby — MySQL data model
- LiveHub
- Frontend Package Scripts
- build_language_lexicon.py
- Online Tunnel Launcher
- main.py
- api
- Firmware Transport Job
- dev.mjs
- test_assistant_training.py
- NLP admission repair — 24 November 2026
- Player Flow Migration
- Step 8: constrained AI analytics
- fastapi
- analytics.py
- Boot registration (POST /api/device/boot)
- Wokwi Wiring Diagram
- context_version
- test_db_backup.py
- summarize_offline_lab.py
- event_lock
- uuid
- Firmware Game Engine
- Prettier Config
- test_nlp_lab.py
- security.py
- Backend Dependency Pins
- NLP lab offline requirements
- Game and Firmware Steps
- Frontend HTML Entry
- subprocess
- Repository Scaffold Step
- entry
- cabinet_state
- test-setup.js
- text
- SparseModel
- test_assistant_memory.py
- FakeSocket

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 131 edges
2. `normalize()` - 100 edges
3. `execute()` - 95 edges
4. `one()` - 89 edges
5. `Context` - 72 edges
6. `Assistant` - 71 edges
7. `now()` - 69 edges
8. `api()` - 60 edges
9. `useApp()` - 56 edges
10. `Project documentation index (canonical internal guide)` - 49 edges

## Surprising Connections (you probably didn't know these)
- `Changes` --references--> `topic_choices()`  [INFERRED]
  docs/nlp-admission-repair.md → backend/app/assistant_learning.py
- `Changes` --references--> `composed_social()`  [INFERRED]
  docs/nlp-topic-repair.md → backend/app/assistant_interactions.py
- `Changes` --references--> `project_words()`  [INFERRED]
  docs/nlp-topic-repair.md → backend/app/assistant_language.py
- `Changes` --references--> `contextual_follow_up()`  [INFERRED]
  docs/nlp-admission-repair.md → backend/app/assistant.py
- `Changes` --references--> `project_words()`  [INFERRED]
  docs/nlp-admission-repair.md → backend/app/assistant_language.py

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

## Communities (104 total, 17 thin omitted)

### Community 0 - "Project documentation index (canonical internal guide)"
Cohesion: 0.04
Nodes (56): Stack Intelligence local administrator analytics guide, Explicit owner-reviewed current-version routing examples, Dashboard Settings houses model memory and training controls, System grounded learning retrieval and development corpora, Stack Moko Baby step-by-step build plan, Current device/hosting milestone: Wokwi, Matrix v1 and free HTTPS tunnel (22 Nov 2026), Matrix v1 game (16 columns, 15 levels, max 15 points), Admin question review (/admin/question-review, migration 006) (+48 more)

### Community 1 - "evaluate_holdout.py"
Cohesion: 0.06
Nodes (46): check(), evaluate(), ObservedAssistant, score(), build_rows(), canonical(), evaluator_fingerprint(), feature_key() (+38 more)

### Community 2 - "useLiveUpdates"
Cohesion: 0.70
Nodes (3): useLiveUpdates(), connect(), retry()

### Community 3 - "assistant.py"
Cohesion: 0.10
Nodes (26): asks_live_state(), automatic_scope(), MemoryPreferences, requested_metrics(), resolve_routing(), routing_input(), compatible(), constraints() (+18 more)

### Community 4 - "create_app"
Cohesion: 0.09
Nodes (42): read_reviews(), create_app(), add_operator(), admin_session(), admissions(), analytics(), assistant_forget_memory(), assistant_memory() (+34 more)

### Community 5 - "Dashboard UI Primitives"
Cohesion: 0.07
Nodes (72): ArrowLeft, ArrowRight, ArrowUpRight, CalendarDays, CheckCircle2, ChevronDown, ChevronLeft, ChevronRight (+64 more)

### Community 6 - "Project Rules and Index"
Cohesion: 0.07
Nodes (28): .claude/CLAUDE.md graphify skill pointer, graphify skill (/graphify trigger), AGENTS.md project instructions, Confirmed stack: React/JSX, Vite, Tailwind, FastAPI, XAMPP MariaDB 10.11.16, Free PC + XAMPP + HTTPS tunnel hosting decision, Frontend conventions (Tailwind v4 tw: prefix, Font Awesome webfonts, Open Sans Variable), html5-qrcode scanner rule, Matrix v1 device decision (16 columns, 15 levels, 1 point per level) (+20 more)

### Community 7 - "evaluation_review.py"
Cohesion: 0.18
Nodes (5): Annotation, CaseReview, proposed(), save_review(), evaluation_decision()

### Community 8 - "Admin Assistant Frontend"
Cohesion: 0.09
Nodes (23): AdminAssistant(), send(), submit(), answerLabels, Evidence(), suggestions, mocks, openChat() (+15 more)

### Community 9 - "Assistant Question Pipeline"
Cohesion: 0.11
Nodes (26): Assistant, Question, run(), test_new_social_turns_work_with_ollama_disabled_and_preserve_context(), scenario(), test_specific_reported_greeting_through_the_service_without_ollama(), scenario(), test_explicit_request_bypasses_a_busy_inference_gate() (+18 more)

### Community 10 - "Verified remaining work"
Cohesion: 0.05
Nodes (43): Applied typed-memory and reviewed-example migrations, Stack Moko Baby backend, Private player journey, live channels and phone HTTPS, Device command delivery and review holds, Boot-bound device recovery, Local Ollama retained via PC tunnel, Render option, 1. Prepare the hotspot phone (+35 more)

### Community 11 - "normalize"
Cohesion: 0.08
Nodes (43): compose(), Context, Intent, interpretation_choices(), normalize(), RoutingPlan, frame(), test_real_query_carries_metric_and_clarifies_missing_subject() (+35 more)

### Community 12 - "test_device_recovery.py"
Cohesion: 0.25
Nodes (25): emulator_setup(), fence(), fence_receipt(), resolution(), setup(), start_event(), test_a_new_boot_invalidates_an_old_fence_and_changed_storage_blocks_never_started(), test_boot_lineage_retries_retirement_and_legacy_bypass() (+17 more)

### Community 13 - "check_quality.py"
Cohesion: 0.13
Nodes (12): replace(), bounded_receive(), main(), receive(), start_api(), percentile(), serve(), test_database() (+4 more)

### Community 14 - "assistant.py"
Cohesion: 0.07
Nodes (36): basic_response(), contextual_follow_up(), continuation(), conversational_reply(), endpoint(), composed_social(), parse(), greeting_answer() (+28 more)

### Community 15 - "run.py"
Cohesion: 0.29
Nodes (14): manifest(), prepare(), sha(), code_hashes(), freeze(), load(), main(), protected() (+6 more)

### Community 16 - "useApp"
Cohesion: 0.15
Nodes (29): AdministratorsOnly(), AdminOnly(), App(), PlayerOnly(), Check, Shell(), tabs, IconButton() (+21 more)

### Community 17 - "rehearse_event.py"
Cohesion: 0.23
Nodes (7): main(), operator(), percentile(), phone(), Recorder, start_tunnel(), wait_ready()

### Community 18 - "execute"
Cohesion: 0.18
Nodes (21): execute(), acknowledge(), CommandAcknowledgement, hold_for_review(), current_boot(), journal(), quarantine(), recovery_view() (+13 more)

### Community 19 - "stack_moko_baby connected firmware (protocol v2)"
Cohesion: 0.08
Nodes (24): Device journal events (POST /api/device/journal), Journal phases (reserved, started, terminal, fenced_unstarted, fenced_interrupted), Conflict quarantine, stack_moko_baby connected firmware (protocol v2), DFPlayer audio cues, Firmware NVS journal snapshot and delivery high-water mark, Scan-register-assign-play-result flow, start-online-preview.ps1 manual tunnel preview (+16 more)

### Community 20 - "Dashboard visual contract with Tailwind integration"
Cohesion: 0.11
Nodes (15): Dashboard visual contract with Tailwind integration, Step 6: reference-matched web views, React.js and Tailwind UI conventions, Selector-controlled dark variant (html[data-admin-theme='dark']), Tailwind 4.3.5 Vite plugin build and layer cascade (tw prefix, no Preflight), Semantic color tokens via @theme inline (ink, muted, note, surface, canvas, line, danger), Access flow contrast mobile and verification refinement passes, Documented current Edge accessibility unit and production checks (+7 more)

### Community 21 - "Question Review Pages"
Cohesion: 0.14
Nodes (18): freshTarget(), kinds, topics, actions, Correction(), changeTopic(), subtypesFor(), decisions (+10 more)

### Community 22 - "Analytics.jsx"
Cohesion: 0.16
Nodes (21): ActivityChart(), axis, ChartTip(), LevelChart(), OutcomesChart(), ScoreChart(), Clock3, Target (+13 more)

### Community 23 - "QR Player Flow Docs"
Cohesion: 0.11
Nodes (18): Authenticated synthetic-tested device integration boundary, Completed-round-only source-matched player leaderboard, Current QR player flow and administrator access, Durable win loss alerts with focus-refresh polling, Explicit Queue-page simulator action sequence, Owner-only persistent ticket across refreshes, Preserved Sourcio-derived player styling and font symbols, Private cabinetState and queueState waiting reasons (+10 more)

### Community 24 - "Frontend Dependencies"
Cohesion: 0.09
Nodes (27): dependencies, @fontsource-variable/open-sans@5.3.0, @fortawesome/fontawesome-free@7.3.1, html5-qrcode@2.3.8, qr-scanner@1.4.2, qrcode.react@4.2.0, @radix-ui/react-dialog@1.3.1, @radix-ui/react-dropdown-menu@2.2.1 (+19 more)

### Community 25 - "event-check.py"
Cohesion: 0.40
Nodes (8): checks(), fix_power(), main(), on_charger(), pending_restart(), port_open(), power_value(), run()

### Community 26 - "review-pages.mjs"
Cohesion: 0.25
Nodes (6): directory, errors, height, results, routes, width

### Community 27 - "Assistant Training Datasets Doc"
Cohesion: 0.07
Nodes (26): Optimistic revision current public context confirmation and409staleapproval, 1000recordsperowner25perpage bounded parameterized statement-deadline queries, Future evaluation UI confirm correct reject versioneddecisions navigation progressfilters, Predictions hidden during pre-evaluation label review, Future evaluation UI question proposedlabel typedprior expectedstate explanations notes, Post-consumption corrections preserve originalresult new annotationversion, No player identities private chats or credentials in future review UI, Planned21November dedicated admin evaluationcase review page not implemented (+18 more)

### Community 28 - "models.py"
Cohesion: 0.16
Nodes (11): run(), DenseModel, fit_temperature(), loss(), Heads, policy(), scaled(), evaluate_model() (+3 more)

### Community 29 - "test_assistant_admission_v2.py"
Cohesion: 0.10
Nodes (14): lexical_resource(), topic_choices(), test_choices_only_name_topics_that_the_question_mentions(), test_contextual_follow_up_needs_previous_context_and_no_new_subject(), test_every_topic_choice_routes_to_read_only_analytics_without_the_model(), test_everyday_wording_is_no_longer_unknown(), test_lexicon_v2_keeps_everyday_words_and_still_excludes_names(), test_possible_names_stay_unknown() (+6 more)

### Community 30 - "one"
Cohesion: 0.17
Nodes (27): all_rows(), one(), poll_commands(), requires_review(), active_rules(), stored_rules(), active(), call_next() (+19 more)

### Community 31 - "Render Blueprint"
Cohesion: 0.08
Nodes (24): mountPath, name, sizeGB, fromService, generateValue, key, sync, value (+16 more)

### Community 32 - "ESP32, Wokwi and online operation"
Cohesion: 0.14
Nodes (14): Matrix rules and active free same-origin HTTPS backend, ESP32, Wokwi and online operation, Firmware files and wiring, Journal and operational limits, Keeping XAMPP and local Ollama online, Prepare and run locally, Rules and historical results, Verification record — 22 November 2026 (+6 more)

### Community 33 - "Settings"
Cohesion: 0.29
Nodes (6): Settings, cloud_env(), test_cloud_origin_and_private_database_without_xampp_paths(), test_production_rejects_insecure_cookies(), test_production_rejects_insecure_or_non_origin_public_urls(), main()

### Community 34 - "database.py"
Cohesion: 0.11
Nodes (7): test_review_round_trip_access_and_versioning(), environment(), test_ai_machine_readiness_agrees_with_dashboard_when_cabinet_is_unavailable(), test_chunked_body_limit_cannot_be_bypassed_without_content_length(), test_malformed_login_text_or_unknown_fields_fail_without_server_errors(), test_readiness_requires_applied_migrations_and_schema(), test_unknown_subject_cannot_be_replaced_with_event_data()

### Community 35 - "Database backups and restore"
Cohesion: 0.25
Nodes (7): Commands, Database backups and restore, Deleting student IDs after the event, Keys and privacy, Verification record (24 November 2026), What runs automatically, Where and how backups are stored

### Community 36 - "Analytics-v1 runtime and development AI system rules"
Cohesion: 0.13
Nodes (6): Analytics-v1 runtime and development AI system rules, Explicit current measures override history and contradictory model labels, Matrix-aware analytics and cloud AI disabled, Student identity raw questions and private values excluded from model context, Eight bounded allowlisted read-only analytics operations, Stack Moko Baby — MySQL data model

### Community 37 - "Offline Classifier Experiment"
Cohesion: 0.06
Nodes (38): 40of120supported blocked upstream;84of130admitted31unknown14scope1measurement, 285originaltraining plus792historyvariants1077rows zero new independent questions, Synthetic variants add no missing subtypes language diversity or independent families, Augmentedpolicy answerszero question-onlypolicy answersone of120supported, Collection was empty at history run;later325AI candidates filled independentreviewpending, Frozen multilingual E5 hierarchical heads history and question-only ablations, Retained protocol variants heads predictions and14offlinechecks, AugmentedE5 ordinary61of130 stress47of120 vsoriginal63and14 (+30 more)

### Community 38 - "Candidate MySQL Schema"
Cohesion: 0.25
Nodes (18): ai_admin_memory, ai_requests, ai_training_examples, audit_logs, auth_sessions, device_commands, device_events, events (+10 more)

### Community 39 - "test_player_flow.py"
Cohesion: 0.11
Nodes (32): compose_all(), test_absent_device_results_are_not_inferred_from_registrations(), test_all_sources_are_separate_and_players_are_deduplicated(), revision(), test_global_revisions_and_idempotent_operations(), test_live_rejects_missing_or_foreign_origin(), test_live_requires_the_right_authenticated_role(), test_logout_revokes_existing_socket_and_commands_are_rejected() (+24 more)

### Community 40 - "Device Command Tests"
Cohesion: 0.26
Nodes (13): command_row(), reserve(), test_emulator_refuses_corrupt_journal_before_contacting_device(), test_expired_unknown_start_never_becomes_an_automatic_no_show(), test_invalid_or_stale_receipts_cannot_change_the_command(), test_other_machine_commands_and_maintenance_cannot_be_bypassed(), test_polling_is_authorized_repeatable_and_contains_no_player_identity(), test_receipt_survives_application_recreation_and_emulator_lost_ack() (+5 more)

### Community 41 - "asyncio"
Cohesion: 0.15
Nodes (9): inspect(), model_json(), scope_payload(), ScopePlan, main(), stage(), Observer, predict() (+1 more)

### Community 42 - "Architecture and Graphify Docs"
Cohesion: 0.09
Nodes (14): Address and availability, Daily startup, Free online operation with XAMPP, Verification and remaining checks, Wokwi firmware, Local Graphify setup and freshness guide, Stack Moko Baby technology and ownership architecture, Authenticated revision-only invalidation and coherent REST snapshots (+6 more)

### Community 43 - "pytest"
Cohesion: 0.18
Nodes (12): replay(), simulated_result(), seed_scores(), test_api_answers_scores_not_a_wrong_model_or_saved_subject(), test_player_score_sql_is_paginated_and_keeps_source_evidence(), activate(), test_matrix_assignment_completion_analytics_and_private_leaderboard(), test_matrix_win_timeout_and_invalid_trace() (+4 more)

### Community 45 - "Vite and Tailwind Build"
Cohesion: 0.12
Nodes (16): devDependencies, jsdom@31.0.1, prettier@3.10.1, tailwindcss@4.3.5, @tailwindcss/vite@4.3.5, @testing-library/react@16.3.3, @testing-library/user-event@14.6.10, vite@8.3.8 (+8 more)

### Community 46 - "Initial Database Migration"
Cohesion: 0.28
Nodes (16): ai_requests, audit_logs, auth_sessions, device_commands, device_events, events, game_sessions, machines (+8 more)

### Community 47 - "Queue.jsx"
Cohesion: 0.19
Nodes (25): actions, DeviceRecovery(), Pause, Play, QrCode, UserRoundX, UsersRound, Matrix() (+17 more)

### Community 48 - "Functional Spec and Matrix Rules"
Cohesion: 0.12
Nodes (7): Classic v1 ruleset (preserved), Matrix v1 ruleset, 006_matrix_rules.sql migration, Selected Matrix v1 supersedes Classic-only proposals, Stack Moko Baby — functional specification, Pending physical, identity and network release decisions, Migration 006 Matrix rules and authenticated command ordering

### Community 49 - "Playwright Browser Tests"
Cohesion: 0.10
Nodes (7): errors, iterator, lines, @axe-core/playwright@4.14.0, @playwright/test@1.65.1, @axe-core/playwright, @playwright/test

### Community 50 - "QR Scanner Components"
Cohesion: 0.17
Nodes (14): cabinetLabels, LobbyStatus(), PlayerAssistant(), mocks, Entry(), loadScannerApi(), release(), Scanner() (+6 more)

### Community 51 - "Root Package Scripts"
Cohesion: 0.10
Nodes (20): engines, node, name, private, scripts, db:backup, db:purge-ids, db:verify (+12 more)

### Community 52 - "json"
Cohesion: 0.18
Nodes (4): main(), plot(), main(), measured()

### Community 53 - "assistant_training.py"
Cohesion: 0.08
Nodes (32): constrained_route(), intent_payload(), corpus_digest(), retrieve(), seed_examples(), _seed_examples(), semantic_features(), signature() (+24 more)

### Community 55 - "os"
Cohesion: 0.22
Nodes (7): make_engine(), executable(), main(), migrate(), seed(), main(), main()

### Community 56 - "db-backup.py"
Cohesion: 0.22
Nodes (19): api_running(), app_login(), backup_dir(), backup_key(), client_args(), client_env(), env_values(), latest() (+11 more)

### Community 57 - "test_identity_retention.py"
Cohesion: 0.30
Nodes (7): purge(), summary(), load_script(), test_dry_run_is_the_default(), test_older_backup_selection_only_picks_earlier_backups(), test_purge_removes_only_due_ids_then_all_keeping_players_and_tickets(), test_purge_with_nothing_due_changes_nothing()

### Community 58 - "Stack Moko Baby — MySQL data model"
Cohesion: 0.11
Nodes (3): Durable browser updates, Local React and backend setup, React JavaScript frontend with Tailwind conventions

### Community 59 - "LiveHub"
Cohesion: 0.27
Nodes (4): LiveHub, restart(), test_slow_clients_coalesce_and_connection_caps_are_bounded(), check()

### Community 60 - "Frontend Package Scripts"
Cohesion: 0.12
Nodes (16): scripts, build, db:backup, db:verify, dev, dev:frontend, device:flash, device:selftest (+8 more)

### Community 61 - "build_language_lexicon.py"
Cohesion: 0.09
Nodes (18): answer(), classify(), is_tagalog(), line_sentence(), minutes(), normalize(), stage(), build() (+10 more)

### Community 62 - "Online Tunnel Launcher"
Cohesion: 0.21
Nodes (15): backend, backupMinutes, backupNow(), children, completed(), ensureMysql(), main(), mysqld (+7 more)

### Community 63 - "main.py"
Cohesion: 0.09
Nodes (21): APIInput, BootRegistration, JournalEvent, Placement, RecoveryReason, RecoveryResolution, Result, Admissions (+13 more)

### Community 64 - "api"
Cohesion: 0.12
Nodes (27): AssistantTrainingReview(), choose(), exportApproved(), load(), remove(), review(), save(), submit() (+19 more)

### Community 65 - "Firmware Transport Job"
Cohesion: 0.20
Nodes (7): RequestJob, body, boot, kind, path, response, status

### Community 66 - "dev.mjs"
Cohesion: 0.12
Nodes (14): backend, backendOnly, frontend, health(), main(), owned, portInUse(), root (+6 more)

### Community 67 - "test_assistant_training.py"
Cohesion: 0.16
Nodes (13): test_ambiguous_query_does_not_query_live_data_until_choice(), ready(), test_exact_correction_routes_without_model_but_reads_fresh_data(), test_learning_is_owner_scoped_approved_current_and_disableable(), approve(), candidate(), test_duplicate_does_not_overwrite_reviewed_label_and_context_change_needs_review(), test_labels_and_context_are_strict() (+5 more)

### Community 68 - "NLP admission repair — 24 November 2026"
Cohesion: 0.29
Nodes (7): Consumed 325-case replay (regression only), Human-confirmed v2 replay (regression only), Measured results (development data only), NLP admission repair — 24 November 2026, Problem, Still open, Verification

### Community 69 - "Player Flow Migration"
Cohesion: 0.12
Nodes (11): entry_grants, login_attempts, player_notifications, qr_links, ai_admin_memory, ai_training_examples, device_boots, device_journal_events (+3 more)

### Community 70 - "Step 8: constrained AI analytics"
Cohesion: 0.22
Nodes (8): Private per-admin typed memory (migration 003, ai_admin_memory), Reviewed AI training examples (migration 004, ai_training_examples), Stack Intelligence bottom chat (admin shell), Step 0: resolve physical and operational constraints, Step 3: database, identity and staff authentication, Step 4: queue and transactional session assignment, Step 8: constrained AI analytics, Step status and remaining gates table (steps 0-9)

### Community 71 - "fastapi"
Cohesion: 0.17
Nodes (4): RequestSizeLimit, mount_frontend(), test_missing_production_build_fails_at_startup(), test_production_spa_preserves_api_and_private_file_boundaries()

### Community 72 - "analytics.py"
Cohesion: 0.27
Nodes (8): clean(), collect(), collect_all(), _collect_snapshot(), _operations(), select(), stamp(), test_fresh_disabled_simulator_cannot_accept_a_new_assignment()

### Community 73 - "Boot registration (POST /api/device/boot)"
Cohesion: 0.10
Nodes (19): Flag round for review (admin review endpoint), Read-only command polling (GET /api/device/commands), device_emulator.py file-journal emulator, X-Device-Token cabinet authentication, Machine page command diagnostics, MariaDB FOR UPDATE row locks, Receipt-required session start, RFC 9110 safe and idempotent methods (+11 more)

### Community 74 - "Wokwi Wiring Diagram"
Cohesion: 0.29
Nodes (6): author, connections, dependencies, editor, parts, version

### Community 75 - "context_version"
Cohesion: 0.36
Nodes (3): canonical(), context_version(), TrainingStore

### Community 77 - "summarize_offline_lab.py"
Cohesion: 0.39
Nodes (4): publish(), metrics(), primary(), publish()

### Community 78 - "event_lock"
Cohesion: 0.38
Nodes (10): require_boot(), device(), device_ack(), device_boot(), device_journal(), device_result(), device_start(), enrollment() (+2 more)

### Community 79 - "uuid"
Cohesion: 0.36
Nodes (5): add_operator(), recovery(), sign_in(), test_admin_manages_operator_accounts_with_audit(), test_operator_runs_the_line_but_cannot_change_scores_accounts_or_training()

### Community 80 - "Firmware Game Engine"
Cohesion: 0.47
Nodes (3): press(), timeout(), x()

### Community 81 - "Prettier Config"
Cohesion: 0.40
Nodes (4): printWidth, semi, singleQuote, trailingComma

### Community 82 - "test_nlp_lab.py"
Cohesion: 0.13
Nodes (14): balanced_cases(), partitions(), find(), union(), Frame, collection(), test_balanced_development_counts_are_not_independent_holdout_claims(), test_data_sources_never_include_holdout_private_exports_or_existing_test_rows() (+6 more)

### Community 83 - "security.py"
Cohesion: 0.31
Nodes (5): register(), csrf_for(), encrypt_identity(), identity_lookup(), verify_csrf()

### Community 84 - "Backend Dependency Pins"
Cohesion: 0.67
Nodes (3): Pinned Argon2 and cryptography security dependencies, Pinned backend dependency manifest, Pinned FastAPI SQLAlchemy PyMySQL Uvicorn runtime

### Community 85 - "NLP lab offline requirements"
Cohesion: 0.28
Nodes (9): NLP lab offline requirements, datasets 3.6.0, scikit-learn 1.9.1, sentence-transformers 3.4.1, setfit 1.1.3, torch 2.9.1 (CPU), transformers 4.57.6, Follow-on history ablation (792 training-only variants) (+1 more)

### Community 89 - "subprocess"
Cohesion: 0.16
Nodes (8): arduino_cli(), check_layout(), detect_port(), main(), partitions(), main(), merge_firmware(), trust_bundle()

### Community 96 - "entry"
Cohesion: 0.29
Nodes (5): boundaries(), entry(), canonical_origin(), origin_allowed(), set_cookie()

### Community 100 - "text"
Cohesion: 0.25
Nodes (9): question_only(), QuestionOnly, training_variants(), text(), test_augmentation_cannot_ingest_calibration_comparison_or_blocked_rows(), test_existing_contextual_examples_are_never_relabelled_or_given_wrong_subject(), test_history_variants_keep_original_question_target_and_family(), test_question_only_features_do_not_change_with_any_validated_prior_subject() (+1 more)

### Community 103 - "test_assistant_memory.py"
Cohesion: 0.15
Nodes (7): MemoryStore, SavedMemory, routing(), test_explaining_privacy_does_not_allow_identity_retrieval(), test_forget_has_csrf_and_prevents_old_inflight_memory_from_returning(), test_memory_schema_has_no_place_for_raw_text_or_invented_metrics(), test_preferences_are_private_and_memory_can_be_disabled()

## Knowledge Gaps
- **343 isolated node(s):** `errors`, `cabinetLabels`, `mocks`, `assistantSuggestions`, `titles` (+338 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 708 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Verified remaining work` connect `Verified remaining work` to `Project documentation index (canonical internal guide)`, `ESP32, Wokwi and online operation`, `Database backups and restore`, `Offline Classifier Experiment`, `stack_moko_baby connected firmware (protocol v2)`?**
  _High betweenness centrality (0.005) - this node is a cross-community bridge._
- **What connects `errors`, `cabinetLabels`, `mocks` to the rest of the system?**
  _343 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Project documentation index (canonical internal guide)` be split into smaller, more focused modules?**
  _Cohesion score 0.04115784712799638 - nodes in this community are weakly interconnected._
- **Why does `create_app()` connect `create_app` to `entry`, `Settings`, `cabinet_state`, `evaluation_review.py`, `analytics.py`, `Assistant Question Pipeline`, `fastapi`, `context_version`, `pytest`, `assistant.py`, `event_lock`, `execute`, `security.py`, `os`, `LiveHub`, `build_language_lexicon.py`, `one`?**
  _High betweenness centrality (0.004) - this node is a cross-community bridge._
- **Should `evaluate_holdout.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06080246913580247 - nodes in this community are weakly interconnected._
- **Why does `Stack Moko Baby — MySQL data model` connect `Analytics-v1 runtime and development AI system rules` to `ESP32, Wokwi and online operation`, `Verified remaining work`, `NLP Grounding Research`, `Functional Spec and Matrix Rules`, `QR Player Flow Docs`, `Stack Moko Baby — MySQL data model`, `Assistant Training Datasets Doc`?**
  _High betweenness centrality (0.003) - this node is a cross-community bridge._
- **Should `assistant.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10220673635307782 - nodes in this community are weakly interconnected._