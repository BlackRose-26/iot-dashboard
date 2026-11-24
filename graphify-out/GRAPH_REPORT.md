# Graph Report - iot-dashboard  (2026-11-24)

## Corpus Check
- 238 files · ~158,071 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 23 file(s) not represented in the graph (top: .css 8, (none) 7, .cmd 4)

## Summary
- 2096 nodes · 6257 edges · 106 communities (88 shown, 18 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 269 edges (avg confidence: 0.88)
- Token cost: 307,490 input · 0 output

## Graph Freshness
- Built from commit: `8a609e1a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_device_recovery.py
- evaluate_holdout.py
- evaluation_review.py
- test_assistant_language.py
- create_app
- Dashboard UI Primitives
- Project Rules and Index
- MemoryStore
- Admin Assistant Frontend
- Assistant Question Pipeline
- recovery_emulator.py
- one
- test_assistant_continuation.py
- analytics.py
- assistant.py
- Conservative review hold
- useApp
- test_quality_audit.py
- Stack Moko Baby — MySQL data model
- npm run online:firmware launcher
- Dashboard visual contract with Tailwind integration
- Question Review Pages
- Card
- QR Player Flow Docs
- Frontend Dependencies
- os
- review-pages.mjs
- Assistant Training Datasets Doc
- experiment_history.py
- test_assistant.py
- Cross-system quality audit (19 Nov 2026)
- Render Blueprint
- Verified remaining work
- security.py
- normalize
- device_emulator.py
- execute
- Offline Classifier Experiment
- Candidate MySQL Schema
- test_player_flow.py
- Device Command Tests
- measure_admission.py
- Architecture and Graphify Docs
- analytics.py
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
- .load
- setup_local.py
- build_language_lexicon.py
- Analytics-v1 runtime and development AI system rules
- test_live_updates.py
- Frontend Package Scripts
- collections
- Online Tunnel Launcher
- main.py
- api
- Firmware Transport Job
- dev.mjs
- fastapi
- NLP admission repair — 24 November 2026
- Player Flow Migration
- Step 8: constrained AI analytics
- stack_moko_baby connected firmware (protocol v2)
- Boot registration (POST /api/device/boot)
- Wokwi Wiring Diagram
- httpx
- test_db_backup.py
- run.py
- Assistant Memory Migrations
- Read-only command polling (GET /api/device/commands)
- Firmware Game Engine
- Prettier Config
- test_nlp_lab.py
- Cloudflare Quick Tunnel
- Backend Dependency Pins
- Persist-before-ACK reservation receipt
- Game and Firmware Steps
- Frontend HTML Entry
- prepare-online-firmware.py
- Repository Scaffold Step
- Self-test stages (panel chain, orientation, button, strip, audio)
- Physical cabinet bring-up over a phone hotspot
- summarize_offline_lab.py
- text
- configure-firmware.py
- assistant_learning.py
- AGENTS graphify usage rules
- SparseModel
- FakeSocket

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 117 edges
2. `normalize()` - 100 edges
3. `execute()` - 90 edges
4. `one()` - 82 edges
5. `Context` - 72 edges
6. `Assistant` - 67 edges
7. `now()` - 61 edges
8. `useApp()` - 53 edges
9. `api()` - 51 edges
10. `Project documentation index (canonical internal guide)` - 48 edges

## Surprising Connections (you probably didn't know these)
- `Changes` --references--> `project_words()`  [INFERRED]
  docs/nlp-topic-repair.md → backend/app/assistant_language.py
- `Changes` --references--> `asks_live_state()`  [INFERRED]
  docs/nlp-topic-repair.md → backend/app/assistant.py
- `Changes` --references--> `composed_social()`  [INFERRED]
  docs/nlp-topic-repair.md → backend/app/assistant_interactions.py
- `Changes` --references--> `constraints()`  [INFERRED]
  docs/nlp-topic-repair.md → backend/app/assistant_semantics.py
- `Changes` --references--> `explanation_declined()`  [INFERRED]
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

## Communities (106 total, 18 thin omitted)

### Community 0 - "test_device_recovery.py"
Cohesion: 0.25
Nodes (25): emulator_setup(), fence(), fence_receipt(), resolution(), setup(), start_event(), test_a_new_boot_invalidates_an_old_fence_and_changed_storage_blocks_never_started(), test_boot_lineage_retries_retirement_and_legacy_bypass() (+17 more)

### Community 1 - "evaluate_holdout.py"
Cohesion: 0.08
Nodes (39): check(), evaluate(), ObservedAssistant, score(), build_rows(), canonical(), evaluator_fingerprint(), feature_key() (+31 more)

### Community 2 - "evaluation_review.py"
Cohesion: 0.20
Nodes (8): Annotation, CaseReview, packet(), proposed(), read_reviews(), save_review(), evaluation_decision(), evaluation_questions()

### Community 3 - "test_assistant_language.py"
Cohesion: 0.11
Nodes (23): asks_live_state(), composed_social(), routing_input(), compatible(), constraints(), explanation_declined(), refers_to_previous(), reviewed_explanation() (+15 more)

### Community 4 - "create_app"
Cohesion: 0.09
Nodes (32): create_app(), admin_session(), analytics(), assistant_forget_memory(), assistant_memory(), assistant_prepare(), assistant_query(), within_deadline() (+24 more)

### Community 5 - "Dashboard UI Primitives"
Cohesion: 0.08
Nodes (62): ArrowLeft, ArrowRight, ArrowUpRight, CalendarDays, Check, CheckCircle2, ChevronDown, ChevronLeft (+54 more)

### Community 6 - "Project Rules and Index"
Cohesion: 0.07
Nodes (38): AGENTS.md project instructions, Confirmed stack: React/JSX, Vite, Tailwind, FastAPI, XAMPP MariaDB 10.11.16, Free PC + XAMPP + HTTPS tunnel hosting decision, Frontend conventions (Tailwind v4 tw: prefix, Font Awesome webfonts, Open Sans Variable), html5-qrcode scanner rule, Matrix v1 device decision (16 columns, 15 levels, 1 point per level), Phone hotspot physical cabinet network decision, NLP lab offline requirements (+30 more)

### Community 8 - "Admin Assistant Frontend"
Cohesion: 0.08
Nodes (29): AdminAssistant(), send(), submit(), answerLabels, Evidence(), suggestions, mocks, openChat() (+21 more)

### Community 9 - "Assistant Question Pipeline"
Cohesion: 0.10
Nodes (31): Assistant, Context, Intent, Question, SavedMemory, run(), test_api_answers_scores_not_a_wrong_model_or_saved_subject(), test_new_social_turns_work_with_ollama_disabled_and_preserve_context() (+23 more)

### Community 11 - "one"
Cohesion: 0.19
Nodes (22): one(), acknowledge(), hold_for_review(), current_boot(), journal(), quarantine(), recovery_view(), register_boot() (+14 more)

### Community 12 - "test_assistant_continuation.py"
Cohesion: 0.31
Nodes (5): continuation(), test_edit_preserves_every_unmentioned_field(), test_new_subject_or_unresolved_content_does_not_reuse_previous_tools(), test_real_query_carries_metric_and_clarifies_missing_subject(), test_underdefined_or_incompatible_edits_clarify()

### Community 13 - "analytics.py"
Cohesion: 0.23
Nodes (7): clean(), _collect_snapshot(), select(), stamp(), active_rules(), cabinet_state(), health_data()

### Community 14 - "assistant.py"
Cohesion: 0.07
Nodes (35): automatic_scope(), basic_response(), contextual_follow_up(), conversational_reply(), parse(), greeting_answer(), interaction_rows(), interaction_social() (+27 more)

### Community 15 - "Conservative review hold"
Cohesion: 0.29
Nodes (6): Flag round for review (admin review endpoint), Machine page command diagnostics, Operator recovery workflow (stop, release, void, recover result), Scan-register-assign-play-result flow, First real round and resilience gates, Accessibility and full event rehearsal

### Community 16 - "useApp"
Cohesion: 0.19
Nodes (19): AdminOnly(), App(), PlayerOnly(), X, Shell(), tabs, IconButton(), Logo() (+11 more)

### Community 17 - "test_quality_audit.py"
Cohesion: 0.14
Nodes (8): replace(), test_ai_machine_readiness_agrees_with_dashboard_when_cabinet_is_unavailable(), test_chunked_body_limit_cannot_be_bypassed_without_content_length(), test_fresh_disabled_simulator_cannot_accept_a_new_assignment(), test_malformed_login_text_or_unknown_fields_fail_without_server_errors(), test_readiness_requires_applied_migrations_and_schema(), test_terminal_duration_cannot_extend_beyond_the_ending_placement(), test_unknown_subject_cannot_be_replaced_with_event_data()

### Community 18 - "Stack Moko Baby — MySQL data model"
Cohesion: 0.09
Nodes (9): Student identity raw questions and private values excluded from model context, Commands, Database backups and restore, Keys and privacy, Verification record (24 November 2026), What runs automatically, Where and how backups are stored, Local React and backend setup (+1 more)

### Community 19 - "npm run online:firmware launcher"
Cohesion: 0.25
Nodes (9): start-online-preview.ps1 manual tunnel preview, ESP32 core 4.0.0 TLS watchdog reboot, ESP32 core 2.0.17 compatibility build, Merged Wokwi firmware image, npm run online:firmware launcher, Wokwi public IoT gateway connection blocker, npm run device:flash re-upload, flash-device.py NVS-guarded flasher (+1 more)

### Community 20 - "Dashboard visual contract with Tailwind integration"
Cohesion: 0.11
Nodes (15): Dashboard visual contract with Tailwind integration, Step 6: reference-matched web views, React.js and Tailwind UI conventions, Selector-controlled dark variant (html[data-admin-theme='dark']), Tailwind 4.3.5 Vite plugin build and layer cascade (tw prefix, no Preflight), Semantic color tokens via @theme inline (ink, muted, note, surface, canvas, line, danger), Access flow contrast mobile and verification refinement passes, Documented current Edge accessibility unit and production checks (+7 more)

### Community 21 - "Question Review Pages"
Cohesion: 0.14
Nodes (18): freshTarget(), kinds, topics, actions, Correction(), changeTopic(), subtypesFor(), decisions (+10 more)

### Community 22 - "Card"
Cohesion: 0.13
Nodes (34): ActivityChart(), axis, ChartTip(), LevelChart(), OutcomesChart(), ScoreChart(), ChevronRight, Clock3 (+26 more)

### Community 23 - "QR Player Flow Docs"
Cohesion: 0.15
Nodes (17): Authenticated synthetic-tested device integration boundary, Completed-round-only source-matched player leaderboard, Current QR player flow and administrator access, Durable win loss alerts with focus-refresh polling, Explicit Queue-page simulator action sequence, Owner-only persistent ticket across refreshes, Preserved Sourcio-derived player styling and font symbols, Private cabinetState and queueState waiting reasons (+9 more)

### Community 24 - "Frontend Dependencies"
Cohesion: 0.09
Nodes (27): dependencies, @fontsource-variable/open-sans@5.3.0, @fortawesome/fontawesome-free@7.3.1, html5-qrcode@2.3.8, qr-scanner@1.4.2, qrcode.react@4.2.0, @radix-ui/react-dialog@1.3.1, @radix-ui/react-dropdown-menu@2.2.1 (+19 more)

### Community 25 - "os"
Cohesion: 0.21
Nodes (19): api_running(), app_login(), backup_dir(), backup_key(), client_args(), client_env(), env_values(), latest() (+11 more)

### Community 26 - "review-pages.mjs"
Cohesion: 0.12
Nodes (10): directory, errors, height, results, routes, width, child, python (+2 more)

### Community 27 - "Assistant Training Datasets Doc"
Cohesion: 0.07
Nodes (26): Optimistic revision current public context confirmation and409staleapproval, 1000recordsperowner25perpage bounded parameterized statement-deadline queries, Future evaluation UI confirm correct reject versioneddecisions navigation progressfilters, Predictions hidden during pre-evaluation label review, Future evaluation UI question proposedlabel typedprior expectedstate explanations notes, Post-consumption corrections preserve originalresult new annotationversion, No player identities private chats or credentials in future review UI, Planned21November dedicated admin evaluationcase review page not implemented (+18 more)

### Community 28 - "experiment_history.py"
Cohesion: 0.16
Nodes (9): run(), DenseModel, fit_temperature(), loss(), Heads, policy(), scaled(), evaluate_model() (+1 more)

### Community 29 - "test_assistant.py"
Cohesion: 0.10
Nodes (33): compose(), endpoint(), normalize(), test_choices_only_name_topics_that_the_question_mentions(), test_contextual_follow_up_needs_previous_context_and_no_new_subject(), test_every_topic_choice_routes_to_read_only_analytics_without_the_model(), test_everyday_wording_is_no_longer_unknown(), test_possible_names_stay_unknown() (+25 more)

### Community 30 - "Cross-system quality audit (19 Nov 2026)"
Cohesion: 0.11
Nodes (14): Step 7: durable live updates, Step 9: event readiness and release rehearsal, Deterministic semantic fast path (bypasses Ollama inference gate), Player QR scanner, Cross-system quality audit (19 Nov 2026), 23 confirmed defects fixed (CSRF, origin, identity switching, QR, readiness, NLP scope), Audit coverage ledger, CSRF and configured-origin trust hardening (+6 more)

### Community 31 - "Render Blueprint"
Cohesion: 0.08
Nodes (24): mountPath, name, sizeGB, fromService, generateValue, key, sync, value (+16 more)

### Community 32 - "Verified remaining work"
Cohesion: 0.06
Nodes (31): Applied typed-memory and reviewed-example migrations, Matrix rules and active free same-origin HTTPS backend, Stack Moko Baby backend, Private player journey, live channels and phone HTTPS, Device command delivery and review holds, Boot-bound device recovery, ESP32, Wokwi and online operation, Firmware files and wiring (+23 more)

### Community 33 - "security.py"
Cohesion: 0.14
Nodes (7): RequestSizeLimit, bounded_receive(), csrf_for(), encrypt_identity(), identity_lookup(), verify_csrf(), receive()

### Community 34 - "normalize"
Cohesion: 0.09
Nodes (21): lexical_resource(), requested_metrics(), resolve_routing(), RoutingPlan, resolve_subject(), test_lexicon_v2_keeps_everyday_words_and_still_excludes_names(), test_definition_and_ellipsis_are_distinct_from_a_new_data_subject(), test_directional_changes_select_the_requested_operation() (+13 more)

### Community 36 - "execute"
Cohesion: 0.22
Nodes (31): execute(), record_change(), active(), admissions(), audit(), call_next(), cancel(), device_start() (+23 more)

### Community 37 - "Offline Classifier Experiment"
Cohesion: 0.03
Nodes (68): Stack Moko Baby step-by-step build plan, Current device/hosting milestone: Wokwi, Matrix v1 and free HTTPS tunnel (22 Nov 2026), Matrix v1 game (16 columns, 15 levels, max 15 points), Admin question review (/admin/question-review, migration 006), Candidate evaluation collection v2 (325 AI-authored questions), Holdout v2 AI-reviewed first use: 130/325, Declared language/semantic families per intent, 40of120supported blocked upstream;84of130admitted31unknown14scope1measurement (+60 more)

### Community 38 - "Candidate MySQL Schema"
Cohesion: 0.25
Nodes (18): ai_admin_memory, ai_requests, ai_training_examples, audit_logs, auth_sessions, device_commands, device_events, events (+10 more)

### Community 39 - "test_player_flow.py"
Cohesion: 0.18
Nodes (21): test_absent_device_results_are_not_inferred_from_registrations(), test_all_sources_are_separate_and_players_are_deduplicated(), accept_command(), entry_payload(), join(), post(), test_access_control_csrf_and_privacy(), test_device_result_replay_and_cohort_separation() (+13 more)

### Community 40 - "Device Command Tests"
Cohesion: 0.24
Nodes (13): command_row(), reserve(), test_emulator_refuses_corrupt_journal_before_contacting_device(), test_expired_unknown_start_never_becomes_an_automatic_no_show(), test_invalid_or_stale_receipts_cannot_change_the_command(), test_other_machine_commands_and_maintenance_cannot_be_bypassed(), test_polling_is_authorized_repeatable_and_contains_no_player_identity(), test_receipt_survives_application_recreation_and_emulator_lost_ack() (+5 more)

### Community 41 - "measure_admission.py"
Cohesion: 0.33
Nodes (5): inspect(), model_json(), ScopePlan, main(), stage()

### Community 42 - "Architecture and Graphify Docs"
Cohesion: 0.10
Nodes (9): Local Graphify setup and freshness guide, Stack Moko Baby technology and ownership architecture, Authenticated revision-only invalidation and coherent REST snapshots, Tailwind 4.3.5 semantic utilities Open Sans and Font Awesome webfonts, Bundled public lexicon then projection topical scope and intent routing, Active free PC HTTPS origin with private local database and Ollama, Matrix ownership, active free HTTPS and inactive Render topology, Quality hardening and local recovery/load/restore evidence (+1 more)

### Community 43 - "analytics.py"
Cohesion: 0.19
Nodes (12): collect(), collect_all(), _operations(), compose_all(), simulated_result(), test_player_score_sql_is_paginated_and_keeps_source_evidence(), activate(), test_matrix_assignment_completion_analytics_and_private_leaderboard() (+4 more)

### Community 45 - "Vite and Tailwind Build"
Cohesion: 0.09
Nodes (18): devDependencies, jsdom@31.0.1, prettier@3.10.1, tailwindcss@4.3.5, @tailwindcss/vite@4.3.5, @testing-library/jest-dom@7.0.1, @testing-library/react@16.3.3, @testing-library/user-event@14.6.10 (+10 more)

### Community 46 - "Initial Database Migration"
Cohesion: 0.28
Nodes (16): ai_requests, audit_logs, auth_sessions, device_commands, device_events, events, game_sessions, machines (+8 more)

### Community 47 - "Queue.jsx"
Cohesion: 0.19
Nodes (24): actions, DeviceRecovery(), Pause, Play, QrCode, UserRoundX, UsersRound, Matrix() (+16 more)

### Community 48 - "Functional Spec and Matrix Rules"
Cohesion: 0.09
Nodes (8): Classic v1 ruleset (preserved), Matrix v1 ruleset, 006_matrix_rules.sql migration, Selected Matrix v1 supersedes Classic-only proposals, Stack Moko Baby — functional specification, Pending physical, identity and network release decisions, Durable browser updates, Migration 006 Matrix rules and authenticated command ordering

### Community 49 - "Playwright Browser Tests"
Cohesion: 0.10
Nodes (7): errors, iterator, lines, @axe-core/playwright@4.14.0, @playwright/test@1.65.1, @axe-core/playwright, @playwright/test

### Community 50 - "QR Scanner Components"
Cohesion: 0.28
Nodes (9): Entry(), loadScannerApi(), release(), Scanner(), detected(), startCamera(), stopCamera(), upload() (+1 more)

### Community 51 - "Root Package Scripts"
Cohesion: 0.11
Nodes (18): engines, node, name, private, scripts, db:backup, db:verify, dev (+10 more)

### Community 52 - "json"
Cohesion: 0.22
Nodes (4): main(), plot(), main(), measured()

### Community 53 - "assistant_training.py"
Cohesion: 0.07
Nodes (27): interpretation_choices(), _seed_examples(), canonical(), context_version(), Proposal, Review, TrainingInput, TrainingStore (+19 more)

### Community 55 - ".load"
Cohesion: 0.43
Nodes (4): cloud_env(), test_cloud_origin_and_private_database_without_xampp_paths(), test_production_rejects_insecure_cookies(), test_production_rejects_insecure_or_non_origin_public_urls()

### Community 56 - "setup_local.py"
Cohesion: 0.15
Nodes (15): Settings, make_engine(), main(), start_api(), percentile(), serve(), test_database(), executable() (+7 more)

### Community 57 - "build_language_lexicon.py"
Cohesion: 0.13
Nodes (6): build(), build_v2(), digest(), Links, wordnet_rows(), main()

### Community 58 - "Analytics-v1 runtime and development AI system rules"
Cohesion: 0.08
Nodes (21): Stack Intelligence local administrator analytics guide, Explicit owner-reviewed current-version routing examples, Dashboard Settings houses model memory and training controls, Analytics-v1 runtime and development AI system rules, Explicit current measures override history and contradictory model labels, Matrix-aware analytics and cloud AI disabled, Eight bounded allowlisted read-only analytics operations, System grounded learning retrieval and development corpora (+13 more)

### Community 59 - "test_live_updates.py"
Cohesion: 0.10
Nodes (16): all_rows(), LiveHub, find_players(), health(), revision(), test_global_revisions_and_idempotent_operations(), test_live_rejects_missing_or_foreign_origin(), test_live_requires_the_right_authenticated_role() (+8 more)

### Community 60 - "Frontend Package Scripts"
Cohesion: 0.12
Nodes (16): scripts, build, db:backup, db:verify, dev, dev:frontend, device:flash, device:selftest (+8 more)

### Community 61 - "collections"
Cohesion: 0.29
Nodes (3): build(), wording(), measure()

### Community 62 - "Online Tunnel Launcher"
Cohesion: 0.22
Nodes (12): backend, backupMinutes, backupNow(), children, completed(), main(), occupied(), python (+4 more)

### Community 63 - "main.py"
Cohesion: 0.10
Nodes (19): poll_commands(), requires_review(), APIInput, BootRegistration, JournalEvent, Placement, RecoveryReason, RecoveryResolution (+11 more)

### Community 64 - "api"
Cohesion: 0.12
Nodes (24): AssistantTrainingReview(), choose(), exportApproved(), load(), remove(), review(), save(), submit() (+16 more)

### Community 65 - "Firmware Transport Job"
Cohesion: 0.20
Nodes (7): RequestJob, body, boot, kind, path, response, status

### Community 66 - "dev.mjs"
Cohesion: 0.21
Nodes (10): backend, backendOnly, frontend, health(), main(), owned, portInUse(), root (+2 more)

### Community 67 - "fastapi"
Cohesion: 0.27
Nodes (3): mount_frontend(), test_missing_production_build_fails_at_startup(), test_production_spa_preserves_api_and_private_file_boundaries()

### Community 68 - "NLP admission repair — 24 November 2026"
Cohesion: 0.14
Nodes (12): Consumed 325-case replay (regression only), Human-confirmed v2 replay (regression only), Measured results (development data only), NLP admission repair — 24 November 2026, Problem, Still open, Verification, Measured results (+4 more)

### Community 69 - "Player Flow Migration"
Cohesion: 0.18
Nodes (8): entry_grants, login_attempts, player_notifications, qr_links, device_boots, device_journal_events, device_recovery_conflicts, player_reentry_tokens

### Community 70 - "Step 8: constrained AI analytics"
Cohesion: 0.22
Nodes (8): Private per-admin typed memory (migration 003, ai_admin_memory), Reviewed AI training examples (migration 004, ai_training_examples), Stack Intelligence bottom chat (admin shell), Step 0: resolve physical and operational constraints, Step 3: database, identity and staff authentication, Step 4: queue and transactional session assignment, Step 8: constrained AI analytics, Step status and remaining gates table (steps 0-9)

### Community 71 - "stack_moko_baby connected firmware (protocol v2)"
Cohesion: 0.25
Nodes (7): Device journal events (POST /api/device/journal), Journal phases (reserved, started, terminal, fenced_unstarted, fenced_interrupted), Conflict quarantine, stack_moko_baby connected firmware (protocol v2), ESP32 cabinet wiring (GPIO18 matrix, GPIO27 button, GPIO25 strip, GPIO17 DFPlayer), Public Wokwi source bundle (package-wokwi.py), Verified root certificate preparation

### Community 73 - "Boot registration (POST /api/device/boot)"
Cohesion: 0.33
Nodes (7): Boot registration (POST /api/device/boot), ESP-IDF esp_timer restarts after deep sleep, 005_device_recovery.sql migration, Storage lineage (storageId epoch), Enrollment bootstrap (GET /api/device/enrollment), Connection gates (Wi-Fi, time, registration, heartbeat, ready), Hotspot preparation (2.4 GHz, ASCII name, WPA2)

### Community 74 - "Wokwi Wiring Diagram"
Cohesion: 0.29
Nodes (6): author, connections, dependencies, editor, parts, version

### Community 75 - "httpx"
Cohesion: 0.43
Nodes (3): main(), fetch(), main()

### Community 76 - "test_db_backup.py"
Cohesion: 0.15
Nodes (4): scratch(), flash_helpers(), main(), send()

### Community 77 - "run.py"
Cohesion: 0.25
Nodes (16): manifest(), prepare(), sha(), code_hashes(), finish_model(), freeze(), load(), main() (+8 more)

### Community 78 - "Assistant Memory Migrations"
Cohesion: 0.29
Nodes (3): ai_admin_memory, ai_training_examples, evaluation_case_reviews

### Community 79 - "Read-only command polling (GET /api/device/commands)"
Cohesion: 0.33
Nodes (5): Read-only command polling (GET /api/device/commands), X-Device-Token cabinet authentication, RFC 9110 safe and idempotent methods, ESP-IDF NVS flash commit semantics, Boot-targeted fence command

### Community 80 - "Firmware Game Engine"
Cohesion: 0.47
Nodes (3): press(), timeout(), x()

### Community 81 - "Prettier Config"
Cohesion: 0.40
Nodes (4): printWidth, semi, singleQuote, trailingComma

### Community 82 - "test_nlp_lab.py"
Cohesion: 0.12
Nodes (18): balanced_cases(), partitions(), find(), union(), prepare(), sources(), frame(), Frame (+10 more)

### Community 83 - "Cloudflare Quick Tunnel"
Cohesion: 0.33
Nodes (6): Prepare and run locally, Wokwi connection choices, install-cloudflared.py verified installer, Cloudflare Quick Tunnel, Phone hotspot to ESP32 to HTTPS tunnel topology, Phone/network deployment

### Community 84 - "Backend Dependency Pins"
Cohesion: 0.67
Nodes (3): Pinned Argon2 and cryptography security dependencies, Pinned backend dependency manifest, Pinned FastAPI SQLAlchemy PyMySQL Uvicorn runtime

### Community 85 - "Persist-before-ACK reservation receipt"
Cohesion: 0.40
Nodes (4): device_emulator.py file-journal emulator, MariaDB FOR UPDATE row locks, Receipt-required session start, recovery_emulator.py protocol-v2 emulator

### Community 89 - "prepare-online-firmware.py"
Cohesion: 0.18
Nodes (8): arduino_cli(), check_layout(), detect_port(), main(), partitions(), main(), merge_firmware(), trust_bundle()

### Community 96 - "Self-test stages (panel chain, orientation, button, strip, audio)"
Cohesion: 0.50
Nodes (4): DFPlayer audio cues, npm run device:selftest wiring self-test, pixel() matrix mapping, Self-test stages (panel chain, orientation, button, strip, audio)

### Community 98 - "Physical cabinet bring-up over a phone hotspot"
Cohesion: 0.29
Nodes (7): 1. Prepare the hotspot phone, 2. Wiring self-test (do this as soon as the wiring is finished), 3. Flash the game firmware for the hotspot, 4. Connection gates (watch the serial monitor and the Machines page), 5. First real round, Physical cabinet bring-up over a phone hotspot, Tools added for the physical board

### Community 99 - "summarize_offline_lab.py"
Cohesion: 0.39
Nodes (4): publish(), metrics(), primary(), publish()

### Community 100 - "text"
Cohesion: 0.25
Nodes (9): question_only(), QuestionOnly, training_variants(), text(), test_augmentation_cannot_ingest_calibration_comparison_or_blocked_rows(), test_existing_contextual_examples_are_never_relabelled_or_given_wrong_subject(), test_history_variants_keep_original_question_target_and_family(), test_question_only_features_do_not_change_with_any_validated_prior_subject() (+1 more)

### Community 101 - "configure-firmware.py"
Cohesion: 0.16
Nodes (5): canonical_origin(), main(), private_lan(), wifi_problem(), main()

### Community 102 - "assistant_learning.py"
Cohesion: 0.14
Nodes (17): constrained_route(), intent_payload(), corpus_digest(), retrieve(), seed_examples(), semantic_features(), signature(), evaluate() (+9 more)

### Community 103 - "AGENTS graphify usage rules"
Cohesion: 0.40
Nodes (4): .claude/CLAUDE.md graphify skill pointer, graphify skill (/graphify trigger), CLAUDE.md graphify rules, scripts/graphify.cmd local CLI wrapper (.tools/graphify-py313)

## Knowledge Gaps
- **331 isolated node(s):** `errors`, `ticketLabels`, `mocks`, `TOKEN`, `mocks` (+326 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 678 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Assistant` connect `Assistant Question Pipeline` to `analytics.py`, `analytics.py`, `assistant.py`, `MemoryStore`?**
  _High betweenness centrality (0.003) - this node is a cross-community bridge._
- **What connects `errors`, `ticketLabels`, `mocks` to the rest of the system?**
  _331 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `evaluate_holdout.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08382936507936507 - nodes in this community are weakly interconnected._
- **Why does `create_app()` connect `create_app` to `security.py`, `evaluation_review.py`, `fastapi`, `execute`, `Assistant Question Pipeline`, `analytics.py`, `one`, `analytics.py`, `assistant.py`, `assistant_training.py`, `.load`, `setup_local.py`, `test_live_updates.py`, `main.py`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **Should `test_assistant_language.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10510510510510511 - nodes in this community are weakly interconnected._
- **Why does `Measured NLP routing history with superseding independent quality limits` connect `Analytics-v1 runtime and development AI system rules` to `Offline Classifier Experiment`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **Should `create_app` be split into smaller, more focused modules?**
  _Cohesion score 0.08558558558558559 - nodes in this community are weakly interconnected._