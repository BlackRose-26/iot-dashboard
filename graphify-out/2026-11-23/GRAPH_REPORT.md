# Graph Report - iot-dashboard  (2026-11-23)

## Corpus Check
- 136 files · ~144,076 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1950 nodes · 5272 edges · 96 communities (78 shown, 18 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 276 edges (avg confidence: 0.88)
- Token cost: 307,490 input · 0 output

## Community Hubs (Navigation)
- Device Recovery and Audit Tests
- NLP Holdout Evaluation Scripts
- Assistant Training and Learning
- Assistant Routing Core
- FastAPI App and Locking
- Dashboard UI Primitives
- Project Rules and Index
- Assistant Context and Memory
- Admin Assistant Frontend
- Assistant Question Pipeline
- Device Protocol Models
- Quality and Browser Runners
- Player Flow and Live Tests
- Assistant Semantic Constraints
- Language Lexicon and Interactions
- Device Commands and Recovery Docs
- Frontend App Shell
- NLP Dataset Builders
- Backend and Online Operation Docs
- Firmware and Free Tunnel
- Build Plan and Tailwind
- Question Review Pages
- Analytics and Machine Pages
- QR Player Flow Docs
- Frontend Dependencies
- Firmware Prep and Flashing
- Node Dev and Device Launchers
- Assistant Training Datasets Doc
- History Experiment Models
- NLP Lab Data and Tests
- Schema, Live Updates, Setup Docs
- Render Blueprint
- NLP Lab Runner
- Player Registration and Ticket
- Queue and Sessions Pages
- Public Language Resources
- Security and Command Emulator
- Offline Classifier Experiment
- Candidate MySQL Schema
- Device Recovery Service
- Device Command Tests
- Stack Intelligence Docs
- Architecture and Graphify Docs
- History Ablation Findings
- NLP Grounding Research
- Vite and Tailwind Build
- Initial Database Migration
- Game Rules and Hashing
- Functional Spec and Matrix Rules
- Playwright Browser Tests
- QR Scanner Components
- Root Package Scripts
- Routing Evaluation Harness
- History Experiment Tests
- Behavioral Expansion Corpus
- Settings and Render Config
- Live Update Hub
- AI System Rules
- Assistant Follow-up Continuation
- Lab Summary Utilities
- Frontend Package Scripts
- Offline Lab Results
- Online Tunnel Launcher
- Quality Audit Findings
- Demo Data Summaries
- Firmware Transport Job
- Evaluation Review Storage
- Production Frontend Serving
- Assistant Memory Store
- Player Flow Migration
- NLP Label Guide
- Device Recovery Migration
- Physical Cabinet Bring-up
- NLP Evaluation Overview
- Wokwi Wiring Diagram
- Frontend Quality Checks
- Frontend Test Setup
- Request Size Limits
- Assistant Memory Migrations
- UI Iteration Log
- Firmware Game Engine
- Prettier Config
- Live Socket Test Fake
- Evaluation Review Migration
- Backend Dependency Pins
- Research and Decisions
- Game and Firmware Steps
- Frontend HTML Entry
- Repository Scaffold Step

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 110 edges
2. `normalize()` - 85 edges
3. `Context` - 70 edges
4. `Assistant` - 66 edges
5. `useApp()` - 47 edges
6. `Question` - 42 edges
7. `RoutingPlan` - 39 edges
8. `Card()` - 36 edges
9. `Reviewed routing examples privacy workflow and planned evaluation review page` - 31 edges
10. `simulated_result()` - 31 edges

## Surprising Connections (you probably didn't know these)
- `audit()` --uses--> `Context`  [INFERRED]
  docs/nlp-evaluation/audit_lab_context.py → backend/app/assistant.py
- `audit()` --uses--> `DenseModel`  [INFERRED]
  docs/nlp-evaluation/audit_lab_context.py → backend/nlp_lab/models.py
- `publish()` --calls--> `manifest()`  [INFERRED]
  docs/nlp-evaluation/summarize_history_lab.py → backend/experiment_history.py
- `Confirmed stack: React/JSX, Vite, Tailwind, FastAPI, XAMPP MariaDB 10.11.16` --conceptually_related_to--> `User-confirmed project decisions`  [INFERRED]
  AGENTS.md → docs/README.md
- `Technology stack table` --conceptually_related_to--> `User-confirmed project decisions`  [INFERRED]
  README.md → docs/README.md

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
- **Free HTTPS tunnel and phone-hotspot device operation path** — agents_free_hosting_decision, readme_online_firmware_launcher, agents_phone_hotspot_network_decision, readme_online_device, docs_readme_physical_cabinet_preparation [INFERRED 0.85]
- **Stack Intelligence NLP evaluation and offline experimentation** — agents_evaluation_holdout_rule, readme_nlp_holdout_results, docs_readme_offline_classifier_comparison, docs_readme_history_ablation, backend_nlp_lab_requirements_setfit [INFERRED 0.85]
- **Matrix v1 ESP32 firmware dependencies** — agents_matrix_v1_device_decision, firmware_stack_moko_baby_libraries_adafruit_neopixel, firmware_stack_moko_baby_libraries_arduinojson [INFERRED 0.75]
- **Boot-bound protocol v2 recovery flow** — docs_device_recovery_boot_registration, docs_device_recovery_journal_endpoint, docs_device_recovery_fence_command, docs_device_recovery_persistent_stop_tombstone, docs_device_recovery_operator_resolution, docs_esp32_online_nvs_journal [EXTRACTED 1.00]
- **Free tunnel online firmware pipeline** — docs_free_online_online_firmware_command, docs_free_online_quick_tunnel, docs_free_online_certificate_preparation, docs_free_online_merged_image, docs_hardware_bringup_online_device, docs_hardware_bringup_flash_device_script [INFERRED 0.85]
- **NVS journal preservation safeguards** — docs_hardware_bringup_flash_device_script, docs_free_online_merged_image, docs_esp32_online_nvs_journal, docs_device_recovery_storage_lineage [INFERRED 0.85]
- **NLP evaluation freeze/consume/regression discipline** — docs_nlp_evaluation_holdout_v1_frozen_protocol, docs_nlp_evaluation_holdout_v1_consumption_ledger, backend_replay_consumed_holdout, docs_nlp_evaluation_candidate_v2_preparation_review_protocol, docs_nlp_routing_repair_v11_regression [INFERRED 0.85]
- **V11 assistant language pipeline stages** — docs_nlp_routing_repair_privacy_before_projection, docs_nlp_routing_repair_public_lexical_projection, docs_nlp_routing_repair_deterministic_fast_path, docs_nlp_routing_repair_topical_scope_decision [EXTRACTED 1.00]
- **Tailwind styling foundation** — docs_tailwind_ui_build_cascade, docs_tailwind_ui_semantic_tokens, docs_tailwind_ui_admin_dark_variant, frontend_src_styles_tailwind, frontend_src_components_ui [EXTRACTED 1.00]

## Communities (96 total, 18 thin omitted)

### Community 0 - "Device Recovery and Audit Tests"
Cohesion: 0.06
Nodes (48): clean(), collect(), collect_all(), _collect_snapshot(), _operations(), select(), stamp(), simulated_result() (+40 more)

### Community 1 - "NLP Holdout Evaluation Scripts"
Cohesion: 0.08
Nodes (45): check(), evaluate(), ObservedAssistant, score(), build_rows(), canonical(), evaluator_fingerprint(), feature_key() (+37 more)

### Community 2 - "Assistant Training and Learning"
Cohesion: 0.07
Nodes (33): corpus_digest(), interpretation_choices(), retrieve(), seed_examples(), _seed_examples(), semantic_features(), signature(), canonical() (+25 more)

### Community 3 - "Assistant Routing Core"
Cohesion: 0.09
Nodes (43): compose(), endpoint(), Intent, normalize(), resolve_routing(), RoutingPlan, empty_summary(), fixture_data() (+35 more)

### Community 4 - "FastAPI App and Locking"
Cohesion: 0.09
Nodes (50): poll_commands(), require_boot(), create_app(), admin_session(), admissions(), analytics(), assistant_forget_memory(), assistant_memory() (+42 more)

### Community 5 - "Dashboard UI Primitives"
Cohesion: 0.06
Nodes (46): axis, ArrowLeft, ArrowRight, Check, CheckCircle2, ChevronDown, CircuitBoard, Clock3 (+38 more)

### Community 6 - "Project Rules and Index"
Cohesion: 0.06
Nodes (42): .claude/CLAUDE.md graphify skill pointer, graphify skill (/graphify trigger), AGENTS.md project instructions, Confirmed stack: React/JSX, Vite, Tailwind, FastAPI, XAMPP MariaDB 10.11.16, Free PC + XAMPP + HTTPS tunnel hosting decision, Frontend conventions (Tailwind v4 tw: prefix, Font Awesome webfonts, Open Sans Variable), html5-qrcode scanner rule, Matrix v1 device decision (16 columns, 15 levels, 1 point per level) (+34 more)

### Community 7 - "Assistant Context and Memory"
Cohesion: 0.07
Nodes (26): automatic_scope(), basic_response(), compose_all(), Context, conversational_reply(), knowledge_response(), MemoryPreferences, preference_reply() (+18 more)

### Community 8 - "Admin Assistant Frontend"
Cohesion: 0.09
Nodes (26): AdminAssistant(), send(), submit(), answerLabels, Evidence(), suggestions, mocks, openChat() (+18 more)

### Community 9 - "Assistant Question Pipeline"
Cohesion: 0.10
Nodes (26): Assistant, inspect(), Question, run(), test_new_social_turns_work_with_ollama_disabled_and_preserve_context(), scenario(), test_specific_reported_greeting_through_the_service_without_ollama(), scenario() (+18 more)

### Community 10 - "Device Protocol Models"
Cohesion: 0.10
Nodes (16): APIInput, BootRegistration, JournalEvent, Placement, RecoveryReason, RecoveryResolution, Result, Admissions (+8 more)

### Community 11 - "Quality and Browser Runners"
Cohesion: 0.12
Nodes (14): replace(), make_engine(), main(), start_api(), percentile(), test_database(), executable(), main() (+6 more)

### Community 12 - "Player Flow and Live Tests"
Cohesion: 0.14
Nodes (26): all_rows(), execute(), one(), record_change(), now(), revision(), test_global_revisions_and_idempotent_operations(), test_live_rejects_missing_or_foreign_origin() (+18 more)

### Community 13 - "Assistant Semantic Constraints"
Cohesion: 0.11
Nodes (19): constrained_route(), intent_payload(), requested_metrics(), routing_input(), compatible(), constraints(), outside_event(), refers_to_previous() (+11 more)

### Community 14 - "Language Lexicon and Interactions"
Cohesion: 0.08
Nodes (18): composed_social(), parse(), greeting_answer(), interaction_rows(), interaction_social(), interaction_text(), interaction_words(), social_phrases() (+10 more)

### Community 15 - "Device Commands and Recovery Docs"
Cohesion: 0.07
Nodes (30): Device command delivery and review holds, Flag round for review (admin review endpoint), Read-only command polling (GET /api/device/commands), device_emulator.py file-journal emulator, X-Device-Token cabinet authentication, Machine page command diagnostics, MariaDB FOR UPDATE row locks, Receipt-required session start (+22 more)

### Community 16 - "Frontend App Shell"
Cohesion: 0.14
Nodes (23): AdminOnly(), App(), PlayerOnly(), Shell(), tabs, IconButton(), Logo(), UpdateStatus() (+15 more)

### Community 17 - "NLP Dataset Builders"
Cohesion: 0.12
Nodes (8): measure(), fetch(), main(), main(), plot(), main(), measured(), main()

### Community 18 - "Backend and Online Operation Docs"
Cohesion: 0.09
Nodes (21): Applied typed-memory and reviewed-example migrations, Matrix rules and active free same-origin HTTPS backend, Stack Moko Baby backend, Private player journey, live channels and phone HTTPS, ESP32, Wokwi and online operation, Firmware files and wiring, Journal and operational limits, Keeping XAMPP and local Ollama online (+13 more)

### Community 19 - "Firmware and Free Tunnel"
Cohesion: 0.07
Nodes (27): ESP-IDF NVS flash commit semantics, Device journal events (POST /api/device/journal), Journal phases (reserved, started, terminal, fenced_unstarted, fenced_interrupted), Conflict quarantine, stack_moko_baby connected firmware (protocol v2), DFPlayer audio cues, Firmware NVS journal snapshot and delivery high-water mark, Prepare and run locally (+19 more)

### Community 20 - "Build Plan and Tailwind"
Cohesion: 0.08
Nodes (27): Stack Moko Baby step-by-step build plan, Private per-admin typed memory (migration 003, ai_admin_memory), Current device/hosting milestone: Wokwi, Matrix v1 and free HTTPS tunnel (22 Nov 2026), Matrix v1 game (16 columns, 15 levels, max 15 points), Admin question review (/admin/question-review, migration 006), Reviewed AI training examples (migration 004, ai_training_examples), Stack Intelligence bottom chat (admin shell), Step 0: resolve physical and operational constraints (+19 more)

### Community 21 - "Question Review Pages"
Cohesion: 0.11
Nodes (23): AssistantTrainingReview(), choose(), load(), remove(), review(), save(), freshTarget(), kinds (+15 more)

### Community 22 - "Analytics and Machine Pages"
Cohesion: 0.17
Nodes (23): ActivityChart(), ChartTip(), LevelChart(), OutcomesChart(), ScoreChart(), actions, DeviceRecovery(), CalendarDays (+15 more)

### Community 23 - "QR Player Flow Docs"
Cohesion: 0.11
Nodes (18): Authenticated synthetic-tested device integration boundary, Completed-round-only source-matched player leaderboard, Current QR player flow and administrator access, Durable win loss alerts with focus-refresh polling, Explicit Queue-page simulator action sequence, Owner-only persistent ticket across refreshes, Preserved Sourcio-derived player styling and font symbols, Private cabinetState and queueState waiting reasons (+10 more)

### Community 24 - "Frontend Dependencies"
Cohesion: 0.09
Nodes (28): dependencies, @fontsource-variable/open-sans@5.3.0, @fortawesome/fontawesome-free@7.3.1, html5-qrcode@2.3.8, qr-scanner@1.4.2, qrcode.react@4.2.0, @radix-ui/react-dialog@1.3.1, @radix-ui/react-dropdown-menu@2.2.1 (+20 more)

### Community 25 - "Firmware Prep and Flashing"
Cohesion: 0.13
Nodes (10): main(), private_lan(), wifi_problem(), arduino_cli(), check_layout(), detect_port(), main(), partitions() (+2 more)

### Community 26 - "Node Dev and Device Launchers"
Cohesion: 0.09
Nodes (19): directory, errors, height, results, routes, width, backend, backendOnly (+11 more)

### Community 27 - "Assistant Training Datasets Doc"
Cohesion: 0.07
Nodes (26): Optimistic revision current public context confirmation and409staleapproval, 1000recordsperowner25perpage bounded parameterized statement-deadline queries, Future evaluation UI confirm correct reject versioneddecisions navigation progressfilters, Predictions hidden during pre-evaluation label review, Future evaluation UI question proposedlabel typedprior expectedstate explanations notes, Post-consumption corrections preserve originalresult new annotationversion, No player identities private chats or credentials in future review UI, Planned21November dedicated admin evaluationcase review page not implemented (+18 more)

### Community 28 - "History Experiment Models"
Cohesion: 0.16
Nodes (9): run(), DenseModel, fit_temperature(), loss(), Heads, policy(), scaled(), evaluate_model() (+1 more)

### Community 29 - "NLP Lab Data and Tests"
Cohesion: 0.14
Nodes (18): balanced_cases(), partitions(), find(), union(), prepare(), sources(), frame(), Frame (+10 more)

### Community 30 - "Schema, Live Updates, Setup Docs"
Cohesion: 0.09
Nodes (4): Durable browser updates, Local React and backend setup, Stack Moko Baby — MySQL data model, React JavaScript frontend with Tailwind conventions

### Community 31 - "Render Blueprint"
Cohesion: 0.08
Nodes (24): mountPath, name, sizeGB, fromService, generateValue, key, sync, value (+16 more)

### Community 32 - "NLP Lab Runner"
Cohesion: 0.21
Nodes (17): manifest(), prepare(), sha(), SparseModel, code_hashes(), finish_model(), freeze(), load() (+9 more)

### Community 33 - "Player Registration and Ticket"
Cohesion: 0.25
Nodes (18): ArrowUpRight, Trophy, Badge(), EmptyState(), InfoNote(), StepLabel(), rankPlayers(), validateRegistration() (+10 more)

### Community 34 - "Queue and Sessions Pages"
Cohesion: 0.17
Nodes (19): ChevronLeft, ChevronRight, Download, History, Pause, Play, Timer, UserRoundX (+11 more)

### Community 35 - "Public Language Resources"
Cohesion: 0.10
Nodes (8): lexical_resource(), tagalog_language_words(), test_development_wording_preserves_public_content_or_rejects_locally(), test_polysemous_word_does_not_silently_change_a_measure(), test_public_dictionary_is_word_only_filtered_and_content_addressed(), test_scope_rejection_stops_before_router_and_analytics(), Public language projection (contractions, reviewed synonyms, bounded inflections), V11 public linguistic resource (WordNet + Kaikki Tagalog, 158,705 forms)

### Community 36 - "Security and Command Emulator"
Cohesion: 0.13
Nodes (8): CommandAcknowledgement, csrf_for(), digest(), encrypt_identity(), identity_lookup(), verify_csrf(), CommandEmulator, main()

### Community 37 - "Offline Classifier Experiment"
Cohesion: 0.10
Nodes (21): Baseline merges refusal and clarification unlike guarded learned argmax, Scikit learn disjoint calibration and probability reliability, TFIDF E5 SetFit hierarchical heads and no-data Ollama baseline, Schema Guided Dialogue explicit state annotation motivation, Multilingual E5 query prefix and language limitations, 325AI-authored candidate questions proposedlabels automated overlap checks independentreviewpending, Independent final labels overlap audit frozen predictor decoder scorer beforefirstuse, Family grouped295train98cal101comparison hashes protect original inputs (+13 more)

### Community 38 - "Candidate MySQL Schema"
Cohesion: 0.25
Nodes (18): ai_admin_memory, ai_requests, ai_training_examples, audit_logs, auth_sessions, device_commands, device_events, events (+10 more)

### Community 39 - "Device Recovery Service"
Cohesion: 0.27
Nodes (14): acknowledge(), hold_for_review(), current_boot(), journal(), quarantine(), recovery_view(), register_boot(), request_fence() (+6 more)

### Community 40 - "Device Command Tests"
Cohesion: 0.24
Nodes (13): command_row(), reserve(), test_emulator_refuses_corrupt_journal_before_contacting_device(), test_expired_unknown_start_never_becomes_an_automatic_no_show(), test_invalid_or_stale_receipts_cannot_change_the_command(), test_other_machine_commands_and_maintenance_cannot_be_bypassed(), test_polling_is_authorized_repeatable_and_contains_no_player_identity(), test_receipt_survives_application_recreation_and_emulator_lost_ack() (+5 more)

### Community 41 - "Stack Intelligence Docs"
Cohesion: 0.11
Nodes (5): Stack Intelligence local administrator analytics guide, Explicit owner-reviewed current-version routing examples, Dashboard Settings houses model memory and training controls, System grounded learning retrieval and development corpora, Dashboard visual contract with Tailwind integration

### Community 42 - "Architecture and Graphify Docs"
Cohesion: 0.12
Nodes (9): Local Graphify setup and freshness guide, Stack Moko Baby technology and ownership architecture, Authenticated revision-only invalidation and coherent REST snapshots, Tailwind 4.3.5 semantic utilities Open Sans and Font Awesome webfonts, Bundled public lexicon then projection topical scope and intent routing, Active free PC HTTPS origin with private local database and Ollama, Matrix ownership, active free HTTPS and inactive Render topology, Quality hardening and local recovery/load/restore evidence (+1 more)

### Community 43 - "History Ablation Findings"
Cohesion: 0.12
Nodes (17): 40of120supported blocked upstream;84of130admitted31unknown14scope1measurement, 285originaltraining plus792historyvariants1077rows zero new independent questions, Synthetic variants add no missing subtypes language diversity or independent families, Augmentedpolicy answerszero question-onlypolicy answersone of120supported, Collection was empty at history run;later325AI candidates filled independentreviewpending, Frozen multilingual E5 hierarchical heads history and question-only ablations, Retained protocol variants heads predictions and14offlinechecks, AugmentedE5 ordinary61of130 stress47of120 vsoriginal63and14 (+9 more)

### Community 45 - "Vite and Tailwind Build"
Cohesion: 0.12
Nodes (16): devDependencies, jsdom@31.0.1, prettier@3.10.1, tailwindcss@4.3.5, @tailwindcss/vite@4.3.5, @testing-library/react@16.3.3, @testing-library/user-event@14.6.10, vite@8.3.8 (+8 more)

### Community 46 - "Initial Database Migration"
Cohesion: 0.28
Nodes (16): ai_requests, audit_logs, auth_sessions, device_commands, device_events, events, game_sessions, machines (+8 more)

### Community 47 - "Game Rules and Hashing"
Cohesion: 0.25
Nodes (15): requires_review(), active_rules(), rules_hash(), stored_rules(), active(), boundaries(), call_next(), context() (+7 more)

### Community 48 - "Functional Spec and Matrix Rules"
Cohesion: 0.12
Nodes (7): Classic v1 ruleset (preserved), Matrix v1 ruleset, 006_matrix_rules.sql migration, Selected Matrix v1 supersedes Classic-only proposals, Stack Moko Baby — functional specification, Pending physical, identity and network release decisions, Migration 006 Matrix rules and authenticated command ordering

### Community 49 - "Playwright Browser Tests"
Cohesion: 0.14
Nodes (5): errors, @axe-core/playwright@4.14.0, @playwright/test@1.65.1, @axe-core/playwright, @playwright/test

### Community 50 - "QR Scanner Components"
Cohesion: 0.26
Nodes (10): Entry(), ScanGate(), loadScannerApi(), release(), Scanner(), detected(), startCamera(), stopCamera() (+2 more)

### Community 51 - "Root Package Scripts"
Cohesion: 0.12
Nodes (15): engines, node, name, private, scripts, dev, dev:backend, dev:frontend (+7 more)

### Community 52 - "Routing Evaluation Harness"
Cohesion: 0.20
Nodes (7): model_json(), evaluate(), intent_label(), route_label(), Observer, predict(), test_offline_ollama_adapter_can_route_explicit_question_without_model_or_database()

### Community 53 - "History Experiment Tests"
Cohesion: 0.25
Nodes (9): question_only(), QuestionOnly, training_variants(), text(), test_augmentation_cannot_ingest_calibration_comparison_or_blocked_rows(), test_existing_contextual_examples_are_never_relabelled_or_given_wrong_subject(), test_history_variants_keep_original_question_target_and_family(), test_question_only_features_do_not_change_with_any_validated_prior_subject() (+1 more)

### Community 55 - "Settings and Render Config"
Cohesion: 0.27
Nodes (7): Settings, serve(), cloud_env(), test_cloud_origin_and_private_database_without_xampp_paths(), test_production_rejects_insecure_cookies(), test_production_rejects_insecure_or_non_origin_public_urls(), main()

### Community 56 - "Live Update Hub"
Cohesion: 0.24
Nodes (4): LiveHub, restart(), test_slow_clients_coalesce_and_connection_caps_are_bounded(), check()

### Community 57 - "AI System Rules"
Cohesion: 0.19
Nodes (5): Analytics-v1 runtime and development AI system rules, Explicit current measures override history and contradictory model labels, Matrix-aware analytics and cloud AI disabled, Student identity raw questions and private values excluded from model context, Eight bounded allowlisted read-only analytics operations

### Community 58 - "Assistant Follow-up Continuation"
Cohesion: 0.24
Nodes (6): continuation(), linguistic_text(), test_edit_preserves_every_unmentioned_field(), test_new_subject_or_unresolved_content_does_not_reuse_previous_tools(), test_real_query_carries_metric_and_clarifies_missing_subject(), test_underdefined_or_incompatible_edits_clarify()

### Community 59 - "Lab Summary Utilities"
Cohesion: 0.26
Nodes (4): publish(), metrics(), primary(), publish()

### Community 60 - "Frontend Package Scripts"
Cohesion: 0.15
Nodes (13): scripts, build, dev, dev:frontend, device:flash, device:selftest, format, online (+5 more)

### Community 61 - "Offline Lab Results"
Cohesion: 0.17
Nodes (12): 130developer-labelled synthetic developmentcases tenperintent notunseen, Run-time325blanks nowfilledAI candidates reviewpending no new accuracy, Reused120paired misleadinghistory diagnostic notadditionalunseencases, Primary Ollama63 TFIDF47 normalized48 E563 SetFit61of130, 515source315social8definitions;494usable154groups29598and101split, Retained protocol sourcehashes casepredictions plots and commands, Baseline merges refusalclarification unlike learnedguardedargmax pipelinecomparison, Coverage Ollama74 TFIDF0 E58 SetFit29of120supported differentpolicies (+4 more)

### Community 62 - "Online Tunnel Launcher"
Cohesion: 0.23
Nodes (10): backend, children, completed(), main(), occupied(), python, root, start() (+2 more)

### Community 63 - "Quality Audit Findings"
Cohesion: 0.18
Nodes (11): Step 7: durable live updates, Step 9: event readiness and release rehearsal, Cross-system quality audit (19 Nov 2026), 23 confirmed defects fixed (CSRF, origin, identity switching, QR, readiness, NLP scope), Audit coverage ledger, CSRF and configured-origin trust hardening, Loopback load (50 browsers) and actual API kill/restart, Outstanding feature/release boundaries (+3 more)

### Community 64 - "Demo Data Summaries"
Cohesion: 0.24
Nodes (9): activity, EVENT, initialQueue, levelStatistics(), names, players, rounds, scoreBuckets() (+1 more)

### Community 65 - "Firmware Transport Job"
Cohesion: 0.20
Nodes (7): RequestJob, body, boot, kind, path, response, status

### Community 66 - "Evaluation Review Storage"
Cohesion: 0.36
Nodes (6): Annotation, CaseReview, packet(), proposed(), read_reviews(), save_review()

### Community 67 - "Production Frontend Serving"
Cohesion: 0.31
Nodes (3): mount_frontend(), test_missing_production_build_fails_at_startup(), test_production_spa_preserves_api_and_private_file_boundaries()

### Community 69 - "Player Flow Migration"
Cohesion: 0.32
Nodes (4): entry_grants, login_attempts, player_notifications, qr_links

### Community 70 - "NLP Label Guide"
Cohesion: 0.25
Nodes (8): Current publicquestion and validated priorstate requestedmeaning not SQL, 325AI candidatequestions25perintent overlapchecked independentreviewpending, Typed mode domain operation dialogueact boundedfilters noidentities rawhistory SQL, No finaltest unseen claim until reviewedlabels overlaps predictor decoder scorer frozen, Secondreviewer languagefamily privacy topic-change and followup codebook, Stack Intelligence label guide and independent review requirements, Thirteen legacy intents and required knowledge social definition subtypes, Source315social8definitions absentnegative rare subtypes and contextualshortcut

### Community 71 - "Device Recovery Migration"
Cohesion: 0.48
Nodes (3): device_boots, device_journal_events, device_recovery_conflicts

### Community 72 - "Physical Cabinet Bring-up"
Cohesion: 0.29
Nodes (7): 1. Prepare the hotspot phone, 2. Wiring self-test (do this as soon as the wiring is finished), 3. Flash the game firmware for the hotspot, 4. Connection gates (watch the serial monitor and the Machines page), 5. First real round, Physical cabinet bring-up over a phone hotspot, Tools added for the physical board

### Community 73 - "NLP Evaluation Overview"
Cohesion: 0.29
Nodes (7): Historical42synthetic contrasts schema kind constraints and filtered retrieval, 325AI candidate collection now filled independentreview and finalevaluationpending, Measured NLP routing history with superseding independent quality limits, Ollama structured outputs leakage guidance and dataset separation, Historical323backend44localmodel checks, Historical21case and24case development results not generalaccuracy, Small synthetic measurements and volume do not establish unseen improvement

### Community 74 - "Wokwi Wiring Diagram"
Cohesion: 0.29
Nodes (6): author, connections, dependencies, editor, parts, version

### Community 77 - "Request Size Limits"
Cohesion: 0.40
Nodes (3): RequestSizeLimit, bounded_receive(), receive()

### Community 79 - "UI Iteration Log"
Cohesion: 0.50
Nodes (4): Access flow contrast mobile and verification refinement passes, Documented current Edge accessibility unit and production checks, Historical eight-page sample review evidence, QR access and theme five-pass refinement log

### Community 80 - "Firmware Game Engine"
Cohesion: 0.60
Nodes (3): press(), timeout(), x()

### Community 81 - "Prettier Config"
Cohesion: 0.40
Nodes (4): printWidth, semi, singleQuote, trailingComma

### Community 84 - "Backend Dependency Pins"
Cohesion: 0.67
Nodes (3): Pinned Argon2 and cryptography security dependencies, Pinned backend dependency manifest, Pinned FastAPI SQLAlchemy PyMySQL Uvicorn runtime

### Community 85 - "Research and Decisions"
Cohesion: 0.67
Nodes (3): Open hardware rules TLS provider and retention decisions, Primary-source research evidence, Source-backed decisions and open gates

## Knowledge Gaps
- **302 isolated node(s):** `mocks`, `mocks`, `state`, `Context`, `1. Prepare the hotspot phone` (+297 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 641 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Assistant` connect `Assistant Question Pipeline` to `Assistant Training and Learning`, `Assistant Context and Memory`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `create_app()` (e.g. with `Question` and `Proposal`) actually correct?**
  _`create_app()` has 12 INFERRED edges - model-reasoned connections that need verification._
- **What connects `mocks`, `mocks`, `state` to the rest of the system?**
  _302 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Device Recovery and Audit Tests` be split into smaller, more focused modules?**
  _Cohesion score 0.06255012028869286 - nodes in this community are weakly interconnected._
- **Why does `Stack Intelligence local administrator analytics guide` connect `Stack Intelligence Docs` to `NLP Evaluation Overview`, `Assistant Training Datasets Doc`, `NLP Grounding Research`, `Behavioral Expansion Corpus`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Assistant` (e.g. with `Proposal` and `TrainingInput`) actually correct?**
  _`Assistant` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `NLP Holdout Evaluation Scripts` be split into smaller, more focused modules?**
  _Cohesion score 0.07550482879719052 - nodes in this community are weakly interconnected._