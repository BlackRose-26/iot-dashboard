# Graph Report - iot-dashboard  (2026-11-24)

## Corpus Check
- 240 files · ~160,705 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 23 file(s) not represented in the graph (top: .css 8, (none) 7, .cmd 4)

## Summary
- 2122 nodes · 6363 edges · 91 communities (75 shown, 16 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 269 edges (avg confidence: 0.88)
- Token cost: 307,490 input · 0 output

## Graph Freshness
- Built from commit: `b84cb07b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Project documentation index (canonical internal guide)
- evaluate_holdout.py
- AppContext.jsx
- test_assistant_language.py
- create_app
- Dashboard UI Primitives
- Project Rules and Index
- test_assistant_memory.py
- Admin Assistant Frontend
- Assistant Question Pipeline
- set-device-url.py
- main.py
- within_deadline
- analytics.py
- assistant.py
- useApp
- backups.md
- stack_moko_baby connected firmware (protocol v2)
- Dashboard visual contract with Tailwind integration
- Question Review Pages
- Card
- QR Player Flow Docs
- Frontend Dependencies
- os
- review-pages.mjs
- Assistant Training Datasets Doc
- experiment_history.py
- normalize
- Cross-system quality audit (19 Nov 2026)
- Render Blueprint
- Verified remaining work
- request_limits.py
- test_assistant_admission_v2.py
- Offline Classifier Experiment
- Candidate MySQL Schema
- test_player_flow.py
- Device Command Tests
- measure_admission.py
- Architecture and Graphify Docs
- test_assistant_generalization.py
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
- argparse
- Online Tunnel Launcher
- test_device_recovery.py
- api
- Firmware Transport Job
- dev.mjs
- NLP admission repair — 24 November 2026
- Player Flow Migration
- Step 8: constrained AI analytics
- Boot registration (POST /api/device/boot)
- Wokwi Wiring Diagram
- test_db_backup.py
- run.py
- Assistant Memory Migrations
- Firmware Game Engine
- Prettier Config
- test_nlp_lab.py
- Backend Dependency Pins
- Game and Firmware Steps
- Frontend HTML Entry
- prepare-online-firmware.py
- Repository Scaffold Step
- text
- configure-firmware.py
- assistant_learning.py
- FakeSocket

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 125 edges
2. `normalize()` - 100 edges
3. `execute()` - 93 edges
4. `one()` - 85 edges
5. `Context` - 72 edges
6. `Assistant` - 67 edges
7. `now()` - 63 edges
8. `useApp()` - 56 edges
9. `api()` - 56 edges
10. `Project documentation index (canonical internal guide)` - 48 edges

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

## Communities (91 total, 16 thin omitted)

### Community 0 - "Project documentation index (canonical internal guide)"
Cohesion: 0.09
Nodes (28): Free PC + XAMPP + HTTPS tunnel hosting decision, Phone hotspot physical cabinet network decision, Stack Intelligence local administrator analytics guide, Explicit owner-reviewed current-version routing examples, Dashboard Settings houses model memory and training controls, Dashboard visual contract with Tailwind integration, Stack Moko Baby step-by-step build plan, Current device/hosting milestone: Wokwi, Matrix v1 and free HTTPS tunnel (22 Nov 2026) (+20 more)

### Community 1 - "evaluate_holdout.py"
Cohesion: 0.08
Nodes (41): check(), evaluate(), ObservedAssistant, score(), build_rows(), canonical(), evaluator_fingerprint(), feature_key() (+33 more)

### Community 2 - "AppContext.jsx"
Cohesion: 0.31
Nodes (6): AppContext, EMPTY, CLASSIC_GAME, useLiveUpdates(), connect(), retry()

### Community 3 - "test_assistant_language.py"
Cohesion: 0.16
Nodes (16): asks_live_state(), routing_input(), compatible(), constraints(), explanation_declined(), refers_to_previous(), resolve_subject(), reviewed_explanation() (+8 more)

### Community 4 - "create_app"
Cohesion: 0.09
Nodes (79): execute(), one(), poll_commands(), requires_review(), active_rules(), stored_rules(), create_app(), active() (+71 more)

### Community 5 - "Dashboard UI Primitives"
Cohesion: 0.09
Nodes (40): ArrowUpRight, CheckCircle2, CircuitBoard, Cpu, Eye, EyeOff, glyphs, HardDrive (+32 more)

### Community 6 - "Project Rules and Index"
Cohesion: 0.07
Nodes (30): .claude/CLAUDE.md graphify skill pointer, graphify skill (/graphify trigger), AGENTS.md project instructions, Confirmed stack: React/JSX, Vite, Tailwind, FastAPI, XAMPP MariaDB 10.11.16, Frontend conventions (Tailwind v4 tw: prefix, Font Awesome webfonts, Open Sans Variable), html5-qrcode scanner rule, Matrix v1 device decision (16 columns, 15 levels, 1 point per level), NLP lab offline requirements (+22 more)

### Community 7 - "test_assistant_memory.py"
Cohesion: 0.15
Nodes (7): MemoryStore, SavedMemory, routing(), test_explaining_privacy_does_not_allow_identity_retrieval(), test_forget_has_csrf_and_prevents_old_inflight_memory_from_returning(), test_memory_schema_has_no_place_for_raw_text_or_invented_metrics(), test_preferences_are_private_and_memory_can_be_disabled()

### Community 8 - "Admin Assistant Frontend"
Cohesion: 0.08
Nodes (26): AdminAssistant(), send(), submit(), answerLabels, Evidence(), suggestions, mocks, openChat() (+18 more)

### Community 9 - "Assistant Question Pipeline"
Cohesion: 0.12
Nodes (25): Assistant, Question, run(), test_new_social_turns_work_with_ollama_disabled_and_preserve_context(), scenario(), test_specific_reported_greeting_through_the_service_without_ollama(), scenario(), test_explicit_request_bypasses_a_busy_inference_gate() (+17 more)

### Community 10 - "set-device-url.py"
Cohesion: 0.48
Nodes (3): flash_helpers(), main(), send()

### Community 11 - "main.py"
Cohesion: 0.13
Nodes (20): acknowledge(), CommandAcknowledgement, hold_for_review(), current_boot(), journal(), quarantine(), recovery_view(), register_boot() (+12 more)

### Community 12 - "within_deadline"
Cohesion: 0.50
Nodes (3): assistant_query(), within_deadline(), request()

### Community 13 - "analytics.py"
Cohesion: 0.18
Nodes (11): clean(), collect(), collect_all(), _collect_snapshot(), _operations(), select(), stamp(), cabinet_state() (+3 more)

### Community 14 - "assistant.py"
Cohesion: 0.08
Nodes (36): automatic_scope(), basic_response(), contextual_follow_up(), continuation(), conversational_reply(), endpoint(), composed_social(), parse() (+28 more)

### Community 16 - "useApp"
Cohesion: 0.12
Nodes (29): AdministratorsOnly(), AdminOnly(), App(), PlayerOnly(), Check, Ticket, X, Shell() (+21 more)

### Community 18 - "backups.md"
Cohesion: 0.29
Nodes (6): Commands, Database backups and restore, Keys and privacy, Verification record (24 November 2026), What runs automatically, Where and how backups are stored

### Community 19 - "stack_moko_baby connected firmware (protocol v2)"
Cohesion: 0.05
Nodes (39): Flag round for review (admin review endpoint), device_emulator.py file-journal emulator, Machine page command diagnostics, MariaDB FOR UPDATE row locks, Receipt-required session start, ESP-IDF NVS flash commit semantics, Boot-targeted fence command, Device journal events (POST /api/device/journal) (+31 more)

### Community 20 - "Dashboard visual contract with Tailwind integration"
Cohesion: 0.16
Nodes (14): Step 6: reference-matched web views, React.js and Tailwind UI conventions, Selector-controlled dark variant (html[data-admin-theme='dark']), Tailwind 4.3.5 Vite plugin build and layer cascade (tw prefix, no Preflight), Semantic color tokens via @theme inline (ink, muted, note, surface, canvas, line, danger), Access flow contrast mobile and verification refinement passes, Documented current Edge accessibility unit and production checks, Historical eight-page sample review evidence (+6 more)

### Community 21 - "Question Review Pages"
Cohesion: 0.14
Nodes (18): freshTarget(), kinds, topics, actions, Correction(), changeTopic(), subtypesFor(), decisions (+10 more)

### Community 22 - "Card"
Cohesion: 0.10
Nodes (45): ActivityChart(), axis, ChartTip(), LevelChart(), OutcomesChart(), ScoreChart(), ArrowLeft, ArrowRight (+37 more)

### Community 23 - "QR Player Flow Docs"
Cohesion: 0.15
Nodes (17): Authenticated synthetic-tested device integration boundary, Completed-round-only source-matched player leaderboard, Current QR player flow and administrator access, Durable win loss alerts with focus-refresh polling, Explicit Queue-page simulator action sequence, Owner-only persistent ticket across refreshes, Preserved Sourcio-derived player styling and font symbols, Private cabinetState and queueState waiting reasons (+9 more)

### Community 24 - "Frontend Dependencies"
Cohesion: 0.09
Nodes (27): dependencies, @fontsource-variable/open-sans@5.3.0, @fortawesome/fontawesome-free@7.3.1, html5-qrcode@2.3.8, qr-scanner@1.4.2, qrcode.react@4.2.0, @radix-ui/react-dialog@1.3.1, @radix-ui/react-dropdown-menu@2.2.1 (+19 more)

### Community 25 - "os"
Cohesion: 0.22
Nodes (19): api_running(), app_login(), backup_dir(), backup_key(), client_args(), client_env(), env_values(), latest() (+11 more)

### Community 26 - "review-pages.mjs"
Cohesion: 0.12
Nodes (10): directory, errors, height, results, routes, width, child, python (+2 more)

### Community 27 - "Assistant Training Datasets Doc"
Cohesion: 0.07
Nodes (26): Optimistic revision current public context confirmation and409staleapproval, 1000recordsperowner25perpage bounded parameterized statement-deadline queries, Future evaluation UI confirm correct reject versioneddecisions navigation progressfilters, Predictions hidden during pre-evaluation label review, Future evaluation UI question proposedlabel typedprior expectedstate explanations notes, Post-consumption corrections preserve originalresult new annotationversion, No player identities private chats or credentials in future review UI, Planned21November dedicated admin evaluationcase review page not implemented (+18 more)

### Community 28 - "experiment_history.py"
Cohesion: 0.15
Nodes (3): DenseModel, Heads, SparseModel

### Community 29 - "normalize"
Cohesion: 0.09
Nodes (49): compose(), Context, Intent, normalize(), requested_metrics(), resolve_routing(), RoutingPlan, test_contextual_follow_up_needs_previous_context_and_no_new_subject() (+41 more)

### Community 30 - "Cross-system quality audit (19 Nov 2026)"
Cohesion: 0.08
Nodes (13): Step 7: durable live updates, Step 9: event readiness and release rehearsal, Local React and backend setup, Player QR scanner, Cross-system quality audit (19 Nov 2026), 23 confirmed defects fixed (CSRF, origin, identity switching, QR, readiness, NLP scope), Audit coverage ledger, CSRF and configured-origin trust hardening (+5 more)

### Community 31 - "Render Blueprint"
Cohesion: 0.08
Nodes (24): mountPath, name, sizeGB, fromService, generateValue, key, sync, value (+16 more)

### Community 32 - "Verified remaining work"
Cohesion: 0.05
Nodes (37): Applied typed-memory and reviewed-example migrations, Matrix rules and active free same-origin HTTPS backend, Stack Moko Baby backend, Private player journey, live channels and phone HTTPS, Device command delivery and review holds, Boot-bound device recovery, ESP32, Wokwi and online operation, Firmware files and wiring (+29 more)

### Community 33 - "request_limits.py"
Cohesion: 0.25
Nodes (3): RequestSizeLimit, bounded_receive(), receive()

### Community 34 - "test_assistant_admission_v2.py"
Cohesion: 0.11
Nodes (12): lexical_resource(), topic_choices(), test_choices_only_name_topics_that_the_question_mentions(), test_every_topic_choice_routes_to_read_only_analytics_without_the_model(), test_everyday_wording_is_no_longer_unknown(), test_lexicon_v2_keeps_everyday_words_and_still_excludes_names(), test_possible_names_stay_unknown(), test_unknown_name_gets_one_tap_choices_but_no_answer() (+4 more)

### Community 37 - "Offline Classifier Experiment"
Cohesion: 0.03
Nodes (69): Candidate evaluation collection v2 (325 AI-authored questions), Lexical overlap audit (Jaccard >= .70 and char similarity >= .84), Declared language/semantic families per intent, 40of120supported blocked upstream;84of130admitted31unknown14scope1measurement, 285originaltraining plus792historyvariants1077rows zero new independent questions, Synthetic variants add no missing subtypes language diversity or independent families, Augmentedpolicy answerszero question-onlypolicy answersone of120supported, Collection was empty at history run;later325AI candidates filled independentreviewpending (+61 more)

### Community 38 - "Candidate MySQL Schema"
Cohesion: 0.25
Nodes (18): ai_admin_memory, ai_requests, ai_training_examples, audit_logs, auth_sessions, device_commands, device_events, events (+10 more)

### Community 39 - "test_player_flow.py"
Cohesion: 0.08
Nodes (32): compose_all(), test_absent_device_results_are_not_inferred_from_registrations(), test_all_sources_are_separate_and_players_are_deduplicated(), accept_command(), entry_payload(), join(), post(), test_access_control_csrf_and_privacy() (+24 more)

### Community 40 - "Device Command Tests"
Cohesion: 0.24
Nodes (13): command_row(), reserve(), test_emulator_refuses_corrupt_journal_before_contacting_device(), test_expired_unknown_start_never_becomes_an_automatic_no_show(), test_invalid_or_stale_receipts_cannot_change_the_command(), test_other_machine_commands_and_maintenance_cannot_be_bypassed(), test_polling_is_authorized_repeatable_and_contains_no_player_identity(), test_receipt_survives_application_recreation_and_emulator_lost_ack() (+5 more)

### Community 41 - "measure_admission.py"
Cohesion: 0.13
Nodes (10): inspect(), model_json(), scope_payload(), ScopePlan, main(), stage(), Observer, predict() (+2 more)

### Community 42 - "Architecture and Graphify Docs"
Cohesion: 0.10
Nodes (9): Local Graphify setup and freshness guide, Stack Moko Baby technology and ownership architecture, Authenticated revision-only invalidation and coherent REST snapshots, Tailwind 4.3.5 semantic utilities Open Sans and Font Awesome webfonts, Bundled public lexicon then projection topical scope and intent routing, Active free PC HTTPS origin with private local database and Ollama, Matrix ownership, active free HTTPS and inactive Render topology, Quality hardening and local recovery/load/restore evidence (+1 more)

### Community 43 - "test_assistant_generalization.py"
Cohesion: 0.14
Nodes (15): replay(), rules_hash(), simulated_result(), encrypt_identity(), seed(), seed_scores(), test_api_answers_scores_not_a_wrong_model_or_saved_subject(), test_player_score_sql_is_paginated_and_keeps_source_evidence() (+7 more)

### Community 45 - "Vite and Tailwind Build"
Cohesion: 0.09
Nodes (18): devDependencies, jsdom@31.0.1, prettier@3.10.1, tailwindcss@4.3.5, @tailwindcss/vite@4.3.5, @testing-library/jest-dom@7.0.1, @testing-library/react@16.3.3, @testing-library/user-event@14.6.10 (+10 more)

### Community 46 - "Initial Database Migration"
Cohesion: 0.28
Nodes (16): ai_requests, audit_logs, auth_sessions, device_commands, device_events, events, game_sessions, machines (+8 more)

### Community 47 - "Queue.jsx"
Cohesion: 0.21
Nodes (26): actions, DeviceRecovery(), Pause, Play, QrCode, UserRoundX, UsersRound, Matrix() (+18 more)

### Community 48 - "Functional Spec and Matrix Rules"
Cohesion: 0.09
Nodes (8): Classic v1 ruleset (preserved), Matrix v1 ruleset, 006_matrix_rules.sql migration, Selected Matrix v1 supersedes Classic-only proposals, Stack Moko Baby — functional specification, Pending physical, identity and network release decisions, Durable browser updates, Migration 006 Matrix rules and authenticated command ordering

### Community 49 - "Playwright Browser Tests"
Cohesion: 0.10
Nodes (7): errors, iterator, lines, @axe-core/playwright@4.14.0, @playwright/test@1.65.1, @axe-core/playwright, @playwright/test

### Community 50 - "QR Scanner Components"
Cohesion: 0.32
Nodes (8): loadScannerApi(), release(), Scanner(), detected(), startCamera(), stopCamera(), upload(), registrationQrContent()

### Community 51 - "Root Package Scripts"
Cohesion: 0.11
Nodes (18): engines, node, name, private, scripts, db:backup, db:verify, dev (+10 more)

### Community 52 - "json"
Cohesion: 0.11
Nodes (11): fetch(), main(), main(), plot(), main(), measured(), publish(), metrics() (+3 more)

### Community 53 - "assistant_training.py"
Cohesion: 0.07
Nodes (26): interpretation_choices(), _seed_examples(), canonical(), context_version(), Proposal, Review, TrainingInput, TrainingStore (+18 more)

### Community 55 - ".load"
Cohesion: 0.47
Nodes (5): Settings, cloud_env(), test_cloud_origin_and_private_database_without_xampp_paths(), test_production_rejects_insecure_cookies(), test_production_rejects_insecure_or_non_origin_public_urls()

### Community 56 - "setup_local.py"
Cohesion: 0.13
Nodes (14): replace(), make_engine(), main(), start_api(), percentile(), serve(), test_database(), executable() (+6 more)

### Community 57 - "build_language_lexicon.py"
Cohesion: 0.15
Nodes (6): build(), build_v2(), digest(), Links, word_form(), wordnet_rows()

### Community 58 - "Analytics-v1 runtime and development AI system rules"
Cohesion: 0.14
Nodes (6): Analytics-v1 runtime and development AI system rules, Explicit current measures override history and contradictory model labels, Matrix-aware analytics and cloud AI disabled, Student identity raw questions and private values excluded from model context, Eight bounded allowlisted read-only analytics operations, Stack Moko Baby — MySQL data model

### Community 59 - "test_live_updates.py"
Cohesion: 0.07
Nodes (21): all_rows(), Annotation, CaseReview, packet(), proposed(), read_reviews(), save_review(), LiveHub (+13 more)

### Community 60 - "Frontend Package Scripts"
Cohesion: 0.12
Nodes (16): scripts, build, db:backup, db:verify, dev, dev:frontend, device:flash, device:selftest (+8 more)

### Community 61 - "argparse"
Cohesion: 0.15
Nodes (7): build(), wording(), measure(), main(), main(), private_lan(), wifi_problem()

### Community 62 - "Online Tunnel Launcher"
Cohesion: 0.22
Nodes (12): backend, backupMinutes, backupNow(), children, completed(), main(), occupied(), python (+4 more)

### Community 63 - "test_device_recovery.py"
Cohesion: 0.07
Nodes (42): APIInput, BootRegistration, JournalEvent, Placement, RecoveryReason, RecoveryResolution, Result, Admissions (+34 more)

### Community 64 - "api"
Cohesion: 0.13
Nodes (28): AssistantTrainingReview(), choose(), exportApproved(), load(), remove(), review(), save(), submit() (+20 more)

### Community 65 - "Firmware Transport Job"
Cohesion: 0.20
Nodes (7): RequestJob, body, boot, kind, path, response, status

### Community 66 - "dev.mjs"
Cohesion: 0.21
Nodes (10): backend, backendOnly, frontend, health(), main(), owned, portInUse(), root (+2 more)

### Community 68 - "NLP admission repair — 24 November 2026"
Cohesion: 0.14
Nodes (12): Consumed 325-case replay (regression only), Human-confirmed v2 replay (regression only), Measured results (development data only), NLP admission repair — 24 November 2026, Problem, Still open, Verification, Measured results (+4 more)

### Community 69 - "Player Flow Migration"
Cohesion: 0.18
Nodes (8): entry_grants, login_attempts, player_notifications, qr_links, device_boots, device_journal_events, device_recovery_conflicts, player_reentry_tokens

### Community 70 - "Step 8: constrained AI analytics"
Cohesion: 0.22
Nodes (8): Private per-admin typed memory (migration 003, ai_admin_memory), Reviewed AI training examples (migration 004, ai_training_examples), Stack Intelligence bottom chat (admin shell), Step 0: resolve physical and operational constraints, Step 3: database, identity and staff authentication, Step 4: queue and transactional session assignment, Step 8: constrained AI analytics, Step status and remaining gates table (steps 0-9)

### Community 73 - "Boot registration (POST /api/device/boot)"
Cohesion: 0.22
Nodes (10): Read-only command polling (GET /api/device/commands), X-Device-Token cabinet authentication, RFC 9110 safe and idempotent methods, Boot registration (POST /api/device/boot), ESP-IDF esp_timer restarts after deep sleep, 005_device_recovery.sql migration, Storage lineage (storageId epoch), Enrollment bootstrap (GET /api/device/enrollment) (+2 more)

### Community 74 - "Wokwi Wiring Diagram"
Cohesion: 0.29
Nodes (6): author, connections, dependencies, editor, parts, version

### Community 77 - "run.py"
Cohesion: 0.19
Nodes (24): manifest(), prepare(), run(), sha(), text(), fit_temperature(), loss(), policy() (+16 more)

### Community 78 - "Assistant Memory Migrations"
Cohesion: 0.29
Nodes (3): ai_admin_memory, ai_training_examples, evaluation_case_reviews

### Community 80 - "Firmware Game Engine"
Cohesion: 0.47
Nodes (3): press(), timeout(), x()

### Community 81 - "Prettier Config"
Cohesion: 0.40
Nodes (4): printWidth, semi, singleQuote, trailingComma

### Community 82 - "test_nlp_lab.py"
Cohesion: 0.14
Nodes (18): balanced_cases(), partitions(), find(), union(), prepare(), sources(), frame(), Frame (+10 more)

### Community 84 - "Backend Dependency Pins"
Cohesion: 0.67
Nodes (3): Pinned Argon2 and cryptography security dependencies, Pinned backend dependency manifest, Pinned FastAPI SQLAlchemy PyMySQL Uvicorn runtime

### Community 89 - "prepare-online-firmware.py"
Cohesion: 0.17
Nodes (8): arduino_cli(), check_layout(), detect_port(), main(), partitions(), main(), merge_firmware(), trust_bundle()

### Community 100 - "text"
Cohesion: 0.14
Nodes (11): mount_frontend(), question_only(), QuestionOnly, training_variants(), test_augmentation_cannot_ingest_calibration_comparison_or_blocked_rows(), test_existing_contextual_examples_are_never_relabelled_or_given_wrong_subject(), test_history_variants_keep_original_question_target_and_family(), test_question_only_features_do_not_change_with_any_validated_prior_subject() (+3 more)

### Community 102 - "assistant_learning.py"
Cohesion: 0.14
Nodes (17): constrained_route(), intent_payload(), corpus_digest(), retrieve(), seed_examples(), semantic_features(), signature(), evaluate() (+9 more)

## Knowledge Gaps
- **331 isolated node(s):** `errors`, `answerLabels`, `suggestions`, `actions`, `mocks` (+326 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 680 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Assistant` connect `Assistant Question Pipeline` to `create_app`, `analytics.py`, `assistant.py`, `test_assistant_memory.py`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **What connects `errors`, `answerLabels`, `suggestions` to the rest of the system?**
  _331 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Project documentation index (canonical internal guide)` be split into smaller, more focused modules?**
  _Cohesion score 0.09411764705882353 - nodes in this community are weakly interconnected._
- **Why does `System grounded learning retrieval and development corpora` connect `Behavioral Expansion Corpus` to `Assistant Training Datasets Doc`, `Offline Classifier Experiment`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **Should `evaluate_holdout.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0798611111111111 - nodes in this community are weakly interconnected._
- **Why does `create_app()` connect `create_app` to `text`, `Assistant Question Pipeline`, `main.py`, `test_assistant_generalization.py`, `analytics.py`, `assistant.py`, `within_deadline`, `assistant_training.py`, `.load`, `setup_local.py`, `test_live_updates.py`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **Should `create_app` be split into smaller, more focused modules?**
  _Cohesion score 0.08627450980392157 - nodes in this community are weakly interconnected._