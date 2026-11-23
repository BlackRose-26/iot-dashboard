# Graph Report - iot-dashboard  (2026-11-23)

## Corpus Check
- 221 files · ~145,382 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 22 file(s) not represented in the graph (top: .css 8, (none) 6, .cmd 4)

## Summary
- 1949 nodes · 5833 edges · 93 communities (75 shown, 18 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 269 edges (avg confidence: 0.88)
- Token cost: 307,490 input · 0 output

## Graph Freshness
- Built from commit: `b049034b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_device_recovery.py
- evaluate_holdout.py
- Assistant Training and Learning
- normalize
- FastAPI App and Locking
- Dashboard UI Primitives
- Project Rules and Index
- test_assistant_memory.py
- Admin Assistant Frontend
- Assistant Question Pipeline
- Device Protocol Models
- check_quality.py
- build_language_lexicon.py
- NLP lab offline requirements
- assistant.py
- Conservative review hold
- useApp
- test_assistant_public_language.py
- Backend and Online Operation Docs
- npm run online:firmware launcher
- Dashboard visual contract with Tailwind integration
- Question Review Pages
- Card
- QR Player Flow Docs
- Frontend Dependencies
- argparse
- Node Dev and Device Launchers
- Assistant Training Datasets Doc
- History Experiment Models
- NLP Lab Data and Tests
- Cross-system quality audit (19 Nov 2026)
- Render Blueprint
- fetch_nlp_datasets.py
- Player Registration and Ticket
- Context
- holdout_audit.py
- within_deadline
- Offline Classifier Experiment
- Candidate MySQL Schema
- test_api_answers_scores_not_a_wrong_model_or_saved_subject
- Device Command Tests
- Analytics-v1 runtime and development AI system rules
- Architecture and Graphify Docs
- test_assistant_generalization.py
- NLP Grounding Research
- Vite and Tailwind Build
- Initial Database Migration
- Functional Spec and Matrix Rules
- Playwright Browser Tests
- QR Scanner Components
- Root Package Scripts
- json
- History Experiment Tests
- Behavioral Expansion Corpus
- test_quality_audit.py
- Live Update Hub
- Assistant Follow-up Continuation
- Frontend Package Scripts
- Stack Moko Baby step-by-step build plan
- Online Tunnel Launcher
- context_version
- Demo Data Summaries
- Firmware Transport Job
- evaluation_review.py
- Production Frontend Serving
- Player Flow Migration
- Step 8: constrained AI analytics
- stack_moko_baby connected firmware (protocol v2)
- Physical Cabinet Bring-up
- Boot registration (POST /api/device/boot)
- Wokwi Wiring Diagram
- Frontend Quality Checks
- Frontend Test Setup
- Assistant Memory Migrations
- Read-only command polling (GET /api/device/commands)
- Firmware Game Engine
- Prettier Config
- Live Socket Test Fake
- Cloudflare Quick Tunnel
- Backend Dependency Pins
- Persist-before-ACK reservation receipt
- Game and Firmware Steps
- Frontend HTML Entry
- Repository Scaffold Step
- Self-test stages (panel chain, orientation, button, strip, audio)

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 126 edges
2. `execute()` - 88 edges
3. `normalize()` - 86 edges
4. `one()` - 80 edges
5. `Context` - 70 edges
6. `Assistant` - 67 edges
7. `now()` - 59 edges
8. `useApp()` - 47 edges
9. `Project documentation index (canonical internal guide)` - 46 edges
10. `Question` - 42 edges

## Surprising Connections (you probably didn't know these)
- `main()` --uses--> `Settings`  [INFERRED]
  scripts/export-registration-qr.py → backend/app/config.py
- `audit()` --uses--> `Context`  [INFERRED]
  docs/nlp-evaluation/audit_lab_context.py → backend/app/assistant.py
- `publish()` --calls--> `manifest()`  [INFERRED]
  docs/nlp-evaluation/summarize_history_lab.py → backend/experiment_history.py
- `Confirmed stack: React/JSX, Vite, Tailwind, FastAPI, XAMPP MariaDB 10.11.16` --conceptually_related_to--> `User-confirmed project decisions`  [INFERRED]
  AGENTS.md → docs/README.md
- `scikit-learn 1.9.1` --conceptually_related_to--> `Offline classifier comparison (SetFit, TF-IDF, multilingual E5)`  [INFERRED]
  backend/nlp_lab/requirements.txt → docs/README.md

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

## Communities (93 total, 18 thin omitted)

### Community 0 - "test_device_recovery.py"
Cohesion: 0.16
Nodes (29): RecoveryEmulator, emulator_setup(), fence(), fence_receipt(), resolution(), setup(), start_event(), test_a_new_boot_invalidates_an_old_fence_and_changed_storage_blocks_never_started() (+21 more)

### Community 1 - "evaluate_holdout.py"
Cohesion: 0.12
Nodes (29): lexical_resource(), corpus_digest(), check(), evaluate(), ObservedAssistant, score(), build_rows(), evaluator_fingerprint() (+21 more)

### Community 2 - "Assistant Training and Learning"
Cohesion: 0.08
Nodes (29): interpretation_choices(), retrieve(), seed_examples(), _seed_examples(), semantic_features(), signature(), Proposal, Review (+21 more)

### Community 3 - "normalize"
Cohesion: 0.10
Nodes (29): constrained_route(), intent_payload(), requested_metrics(), resolve_routing(), routing_input(), RoutingPlan, compatible(), constraints() (+21 more)

### Community 4 - "FastAPI App and Locking"
Cohesion: 0.09
Nodes (78): all_rows(), execute(), one(), acknowledge(), hold_for_review(), poll_commands(), requires_review(), current_boot() (+70 more)

### Community 5 - "Dashboard UI Primitives"
Cohesion: 0.07
Nodes (57): ActivityChart(), axis, ChartTip(), LevelChart(), ArrowLeft, CalendarDays, Check, CheckCircle2 (+49 more)

### Community 6 - "Project Rules and Index"
Cohesion: 0.07
Nodes (33): .claude/CLAUDE.md graphify skill pointer, graphify skill (/graphify trigger), AGENTS.md project instructions, Confirmed stack: React/JSX, Vite, Tailwind, FastAPI, XAMPP MariaDB 10.11.16, Free PC + XAMPP + HTTPS tunnel hosting decision, Frontend conventions (Tailwind v4 tw: prefix, Font Awesome webfonts, Open Sans Variable), html5-qrcode scanner rule, Matrix v1 device decision (16 columns, 15 levels, 1 point per level) (+25 more)

### Community 7 - "test_assistant_memory.py"
Cohesion: 0.11
Nodes (11): MemoryStore, MemoryPreferences, SavedMemory, ScopePlan, routing(), test_explaining_privacy_does_not_allow_identity_retrieval(), test_explicit_system_subject_beats_an_older_conversation(), test_forget_has_csrf_and_prevents_old_inflight_memory_from_returning() (+3 more)

### Community 8 - "Admin Assistant Frontend"
Cohesion: 0.06
Nodes (51): AdminAssistant(), send(), submit(), answerLabels, Evidence(), suggestions, mocks, openChat() (+43 more)

### Community 9 - "Assistant Question Pipeline"
Cohesion: 0.11
Nodes (27): Assistant, Question, run(), evaluate(), intent_label(), test_new_social_turns_work_with_ollama_disabled_and_preserve_context(), scenario(), test_specific_reported_greeting_through_the_service_without_ollama() (+19 more)

### Community 10 - "Device Protocol Models"
Cohesion: 0.07
Nodes (24): APIInput, BootRegistration, JournalEvent, Placement, RecoveryReason, RecoveryResolution, Result, Admissions (+16 more)

### Community 11 - "check_quality.py"
Cohesion: 0.10
Nodes (22): Settings, make_engine(), main(), start_api(), percentile(), serve(), test_database(), executable() (+14 more)

### Community 12 - "build_language_lexicon.py"
Cohesion: 0.19
Nodes (4): build(), digest(), Links, word_form()

### Community 13 - "NLP lab offline requirements"
Cohesion: 0.28
Nodes (9): NLP lab offline requirements, datasets 3.6.0, scikit-learn 1.9.1, sentence-transformers 3.4.1, setfit 1.1.3, torch 2.9.1 (CPU), transformers 4.57.6, Follow-on history ablation (792 training-only variants) (+1 more)

### Community 14 - "assistant.py"
Cohesion: 0.09
Nodes (30): inspect(), basic_response(), conversational_reply(), endpoint(), composed_social(), parse(), greeting_answer(), interaction_rows() (+22 more)

### Community 15 - "Conservative review hold"
Cohesion: 0.29
Nodes (6): Flag round for review (admin review endpoint), Machine page command diagnostics, Operator recovery workflow (stop, release, void, recover result), Scan-register-assign-play-result flow, First real round and resilience gates, Accessibility and full event rehearsal

### Community 16 - "useApp"
Cohesion: 0.26
Nodes (14): AdminOnly(), App(), PlayerOnly(), X, Shell(), tabs, IconButton(), Logo() (+6 more)

### Community 17 - "test_assistant_public_language.py"
Cohesion: 0.25
Nodes (3): test_development_wording_preserves_public_content_or_rejects_locally(), test_polysemous_word_does_not_silently_change_a_measure(), test_scope_rejection_stops_before_router_and_analytics()

### Community 18 - "Backend and Online Operation Docs"
Cohesion: 0.06
Nodes (31): Applied typed-memory and reviewed-example migrations, Matrix rules and active free same-origin HTTPS backend, Stack Moko Baby backend, Private player journey, live channels and phone HTTPS, Device command delivery and review holds, Boot-bound device recovery, ESP32, Wokwi and online operation, Firmware files and wiring (+23 more)

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
Cohesion: 0.20
Nodes (27): OutcomesChart(), ScoreChart(), actions, DeviceRecovery(), Download, Pause, Play, UsersRound (+19 more)

### Community 23 - "QR Player Flow Docs"
Cohesion: 0.15
Nodes (17): Authenticated synthetic-tested device integration boundary, Completed-round-only source-matched player leaderboard, Current QR player flow and administrator access, Durable win loss alerts with focus-refresh polling, Explicit Queue-page simulator action sequence, Owner-only persistent ticket across refreshes, Preserved Sourcio-derived player styling and font symbols, Private cabinetState and queueState waiting reasons (+9 more)

### Community 24 - "Frontend Dependencies"
Cohesion: 0.09
Nodes (28): dependencies, @fontsource-variable/open-sans@5.3.0, @fortawesome/fontawesome-free@7.3.1, html5-qrcode@2.3.8, qr-scanner@1.4.2, qrcode.react@4.2.0, @radix-ui/react-dialog@1.3.1, @radix-ui/react-dropdown-menu@2.2.1 (+20 more)

### Community 25 - "argparse"
Cohesion: 0.09
Nodes (13): canonical_origin(), main(), main(), private_lan(), wifi_problem(), main(), arduino_cli(), check_layout() (+5 more)

### Community 26 - "Node Dev and Device Launchers"
Cohesion: 0.09
Nodes (19): directory, errors, height, results, routes, width, backend, backendOnly (+11 more)

### Community 27 - "Assistant Training Datasets Doc"
Cohesion: 0.07
Nodes (26): Optimistic revision current public context confirmation and409staleapproval, 1000recordsperowner25perpage bounded parameterized statement-deadline queries, Future evaluation UI confirm correct reject versioneddecisions navigation progressfilters, Predictions hidden during pre-evaluation label review, Future evaluation UI question proposedlabel typedprior expectedstate explanations notes, Post-consumption corrections preserve originalresult new annotationversion, No player identities private chats or credentials in future review UI, Planned21November dedicated admin evaluationcase review page not implemented (+18 more)

### Community 28 - "History Experiment Models"
Cohesion: 0.10
Nodes (28): manifest(), prepare(), run(), predict(), sha(), text(), DenseModel, fit_temperature() (+20 more)

### Community 29 - "NLP Lab Data and Tests"
Cohesion: 0.11
Nodes (16): Observer, balanced_cases(), partitions(), find(), union(), Frame, collection(), validate() (+8 more)

### Community 30 - "Cross-system quality audit (19 Nov 2026)"
Cohesion: 0.08
Nodes (15): Step 7: durable live updates, Step 9: event readiness and release rehearsal, Local React and backend setup, Deterministic semantic fast path (bypasses Ollama inference gate), Player QR scanner, Cross-system quality audit (19 Nov 2026), 23 confirmed defects fixed (CSRF, origin, identity switching, QR, readiness, NLP scope), Audit coverage ledger (+7 more)

### Community 31 - "Render Blueprint"
Cohesion: 0.08
Nodes (24): mountPath, name, sizeGB, fromService, generateValue, key, sync, value (+16 more)

### Community 33 - "Player Registration and Ticket"
Cohesion: 0.19
Nodes (21): ArrowRight, ArrowUpRight, ChevronLeft, Eye, EyeOff, Hash, Medal, ShieldCheck (+13 more)

### Community 34 - "Context"
Cohesion: 0.11
Nodes (33): automatic_scope(), compose(), Context, Intent, normalize(), frame(), test_real_query_carries_metric_and_clarifies_missing_subject(), empty_summary() (+25 more)

### Community 35 - "holdout_audit.py"
Cohesion: 0.22
Nodes (10): reference_questions(), audit(), build(), followup(), main(), references(), test_candidate_internal_duplicates_are_flagged_without_predictions(), test_followup_annotation_keeps_subject_and_validates_changed_filters() (+2 more)

### Community 36 - "within_deadline"
Cohesion: 0.50
Nodes (3): assistant_query(), within_deadline(), request()

### Community 37 - "Offline Classifier Experiment"
Cohesion: 0.06
Nodes (38): 40of120supported blocked upstream;84of130admitted31unknown14scope1measurement, 285originaltraining plus792historyvariants1077rows zero new independent questions, Synthetic variants add no missing subtypes language diversity or independent families, Augmentedpolicy answerszero question-onlypolicy answersone of120supported, Collection was empty at history run;later325AI candidates filled independentreviewpending, Frozen multilingual E5 hierarchical heads history and question-only ablations, Retained protocol variants heads predictions and14offlinechecks, AugmentedE5 ordinary61of130 stress47of120 vsoriginal63and14 (+30 more)

### Community 38 - "Candidate MySQL Schema"
Cohesion: 0.25
Nodes (18): ai_admin_memory, ai_requests, ai_training_examples, audit_logs, auth_sessions, device_commands, device_events, events (+10 more)

### Community 40 - "Device Command Tests"
Cohesion: 0.16
Nodes (15): CommandAcknowledgement, CommandEmulator, command_row(), reserve(), test_emulator_refuses_corrupt_journal_before_contacting_device(), test_expired_unknown_start_never_becomes_an_automatic_no_show(), test_invalid_or_stale_receipts_cannot_change_the_command(), test_other_machine_commands_and_maintenance_cannot_be_bypassed() (+7 more)

### Community 41 - "Analytics-v1 runtime and development AI system rules"
Cohesion: 0.07
Nodes (24): Stack Intelligence local administrator analytics guide, Explicit owner-reviewed current-version routing examples, Dashboard Settings houses model memory and training controls, Analytics-v1 runtime and development AI system rules, Explicit current measures override history and contradictory model labels, Matrix-aware analytics and cloud AI disabled, Student identity raw questions and private values excluded from model context, Eight bounded allowlisted read-only analytics operations (+16 more)

### Community 42 - "Architecture and Graphify Docs"
Cohesion: 0.10
Nodes (9): Local Graphify setup and freshness guide, Stack Moko Baby technology and ownership architecture, Authenticated revision-only invalidation and coherent REST snapshots, Tailwind 4.3.5 semantic utilities Open Sans and Font Awesome webfonts, Bundled public lexicon then projection topical scope and intent routing, Active free PC HTTPS origin with private local database and Ollama, Matrix ownership, active free HTTPS and inactive Render topology, Quality hardening and local recovery/load/restore evidence (+1 more)

### Community 43 - "test_assistant_generalization.py"
Cohesion: 0.11
Nodes (25): clean(), collect(), collect_all(), _collect_snapshot(), _operations(), select(), stamp(), compose_all() (+17 more)

### Community 45 - "Vite and Tailwind Build"
Cohesion: 0.12
Nodes (16): devDependencies, jsdom@31.0.1, prettier@3.10.1, tailwindcss@4.3.5, @tailwindcss/vite@4.3.5, @testing-library/react@16.3.3, @testing-library/user-event@14.6.10, vite@8.3.8 (+8 more)

### Community 46 - "Initial Database Migration"
Cohesion: 0.28
Nodes (16): ai_requests, audit_logs, auth_sessions, device_commands, device_events, events, game_sessions, machines (+8 more)

### Community 48 - "Functional Spec and Matrix Rules"
Cohesion: 0.08
Nodes (9): Classic v1 ruleset (preserved), Matrix v1 ruleset, 006_matrix_rules.sql migration, Selected Matrix v1 supersedes Classic-only proposals, Stack Moko Baby — functional specification, Pending physical, identity and network release decisions, Durable browser updates, Migration 006 Matrix rules and authenticated command ordering (+1 more)

### Community 49 - "Playwright Browser Tests"
Cohesion: 0.14
Nodes (5): errors, @axe-core/playwright@4.14.0, @playwright/test@1.65.1, @axe-core/playwright, @playwright/test

### Community 50 - "QR Scanner Components"
Cohesion: 0.32
Nodes (8): loadScannerApi(), release(), Scanner(), detected(), startCamera(), stopCamera(), upload(), registrationQrContent()

### Community 51 - "Root Package Scripts"
Cohesion: 0.12
Nodes (15): engines, node, name, private, scripts, dev, dev:backend, dev:frontend (+7 more)

### Community 52 - "json"
Cohesion: 0.08
Nodes (16): build(), wording(), measure(), route_label(), canonical(), sources(), test_public_explanations_do_not_enable_assignments_identifiers_or_unknown_subjects(), main() (+8 more)

### Community 53 - "History Experiment Tests"
Cohesion: 0.23
Nodes (9): question_only(), QuestionOnly, training_variants(), prepare(), test_augmentation_cannot_ingest_calibration_comparison_or_blocked_rows(), test_existing_contextual_examples_are_never_relabelled_or_given_wrong_subject(), test_history_variants_keep_original_question_target_and_family(), test_question_only_features_do_not_change_with_any_validated_prior_subject() (+1 more)

### Community 55 - "test_quality_audit.py"
Cohesion: 0.10
Nodes (18): replace(), entry_payload(), join(), test_access_control_csrf_and_privacy(), test_fifo_concurrency_idempotency_and_results(), test_identity_encryption_and_cookie_flags(), test_leaderboard_relocks_on_next_registration(), test_rate_limit_expired_sessions_and_skip_audit() (+10 more)

### Community 56 - "Live Update Hub"
Cohesion: 0.15
Nodes (11): LiveHub, revision(), test_global_revisions_and_idempotent_operations(), test_live_rejects_missing_or_foreign_origin(), test_live_requires_the_right_authenticated_role(), test_logout_revokes_existing_socket_and_commands_are_rejected(), test_outbox_is_atomic_and_recovers_after_dispatcher_restart(), restart() (+3 more)

### Community 58 - "Assistant Follow-up Continuation"
Cohesion: 0.43
Nodes (4): continuation(), test_edit_preserves_every_unmentioned_field(), test_new_subject_or_unresolved_content_does_not_reuse_previous_tools(), test_underdefined_or_incompatible_edits_clarify()

### Community 60 - "Frontend Package Scripts"
Cohesion: 0.15
Nodes (13): scripts, build, dev, dev:frontend, device:flash, device:selftest, format, online (+5 more)

### Community 61 - "Stack Moko Baby step-by-step build plan"
Cohesion: 0.07
Nodes (30): Stack Moko Baby step-by-step build plan, Current device/hosting milestone: Wokwi, Matrix v1 and free HTTPS tunnel (22 Nov 2026), Matrix v1 game (16 columns, 15 levels, max 15 points), Admin question review (/admin/question-review, migration 006), Candidate evaluation collection v2 (325 AI-authored questions), Holdout v2 AI-reviewed first use: 130/325, Declared language/semantic families per intent, 130developer-labelled synthetic developmentcases tenperintent notunseen (+22 more)

### Community 62 - "Online Tunnel Launcher"
Cohesion: 0.23
Nodes (10): backend, children, completed(), main(), occupied(), python, root, start() (+2 more)

### Community 63 - "context_version"
Cohesion: 0.36
Nodes (3): canonical(), context_version(), TrainingStore

### Community 64 - "Demo Data Summaries"
Cohesion: 0.24
Nodes (8): activity, EVENT, initialQueue, levelStatistics(), names, players, rounds, scoreBuckets()

### Community 65 - "Firmware Transport Job"
Cohesion: 0.20
Nodes (7): RequestJob, body, boot, kind, path, response, status

### Community 66 - "evaluation_review.py"
Cohesion: 0.20
Nodes (8): Annotation, CaseReview, packet(), proposed(), read_reviews(), save_review(), evaluation_decision(), evaluation_questions()

### Community 67 - "Production Frontend Serving"
Cohesion: 0.31
Nodes (3): mount_frontend(), test_missing_production_build_fails_at_startup(), test_production_spa_preserves_api_and_private_file_boundaries()

### Community 69 - "Player Flow Migration"
Cohesion: 0.24
Nodes (7): entry_grants, login_attempts, player_notifications, qr_links, device_boots, device_journal_events, device_recovery_conflicts

### Community 70 - "Step 8: constrained AI analytics"
Cohesion: 0.22
Nodes (8): Private per-admin typed memory (migration 003, ai_admin_memory), Reviewed AI training examples (migration 004, ai_training_examples), Stack Intelligence bottom chat (admin shell), Step 0: resolve physical and operational constraints, Step 3: database, identity and staff authentication, Step 4: queue and transactional session assignment, Step 8: constrained AI analytics, Step status and remaining gates table (steps 0-9)

### Community 71 - "stack_moko_baby connected firmware (protocol v2)"
Cohesion: 0.25
Nodes (7): Device journal events (POST /api/device/journal), Journal phases (reserved, started, terminal, fenced_unstarted, fenced_interrupted), Conflict quarantine, stack_moko_baby connected firmware (protocol v2), ESP32 cabinet wiring (GPIO18 matrix, GPIO27 button, GPIO25 strip, GPIO17 DFPlayer), Public Wokwi source bundle (package-wokwi.py), Verified root certificate preparation

### Community 72 - "Physical Cabinet Bring-up"
Cohesion: 0.29
Nodes (7): 1. Prepare the hotspot phone, 2. Wiring self-test (do this as soon as the wiring is finished), 3. Flash the game firmware for the hotspot, 4. Connection gates (watch the serial monitor and the Machines page), 5. First real round, Physical cabinet bring-up over a phone hotspot, Tools added for the physical board

### Community 73 - "Boot registration (POST /api/device/boot)"
Cohesion: 0.33
Nodes (7): Boot registration (POST /api/device/boot), ESP-IDF esp_timer restarts after deep sleep, 005_device_recovery.sql migration, Storage lineage (storageId epoch), Enrollment bootstrap (GET /api/device/enrollment), Connection gates (Wi-Fi, time, registration, heartbeat, ready), Hotspot preparation (2.4 GHz, ASCII name, WPA2)

### Community 74 - "Wokwi Wiring Diagram"
Cohesion: 0.29
Nodes (6): author, connections, dependencies, editor, parts, version

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

### Community 83 - "Cloudflare Quick Tunnel"
Cohesion: 0.33
Nodes (6): Prepare and run locally, Wokwi connection choices, install-cloudflared.py verified installer, Cloudflare Quick Tunnel, Phone hotspot to ESP32 to HTTPS tunnel topology, Phone/network deployment

### Community 84 - "Backend Dependency Pins"
Cohesion: 0.67
Nodes (3): Pinned Argon2 and cryptography security dependencies, Pinned backend dependency manifest, Pinned FastAPI SQLAlchemy PyMySQL Uvicorn runtime

### Community 85 - "Persist-before-ACK reservation receipt"
Cohesion: 0.40
Nodes (4): device_emulator.py file-journal emulator, MariaDB FOR UPDATE row locks, Receipt-required session start, recovery_emulator.py protocol-v2 emulator

### Community 96 - "Self-test stages (panel chain, orientation, button, strip, audio)"
Cohesion: 0.50
Nodes (4): DFPlayer audio cues, npm run device:selftest wiring self-test, pixel() matrix mapping, Self-test stages (panel chain, orientation, button, strip, audio)

## Knowledge Gaps
- **302 isolated node(s):** `tabs`, `Firmware files and wiring`, `Journal and operational limits`, `Keeping XAMPP and local Ollama online`, `Rules and historical results` (+297 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 622 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Cross-system quality audit (19 Nov 2026)` connect `Cross-system quality audit (19 Nov 2026)` to `Backend and Online Operation Docs`, `check_quality.py`?**
  _High betweenness centrality (0.005) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `create_app()` (e.g. with `Question` and `Proposal`) actually correct?**
  _`create_app()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tabs`, `Firmware files and wiring`, `Journal and operational limits` to the rest of the system?**
  _302 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `evaluate_holdout.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11933395004625347 - nodes in this community are weakly interconnected._
- **Why does `create_app()` connect `FastAPI App and Locking` to `Assistant Training and Learning`, `evaluation_review.py`, `within_deadline`, `Production Frontend Serving`, `Device Command Tests`, `Assistant Question Pipeline`, `Device Protocol Models`, `test_assistant_generalization.py`, `check_quality.py`, `assistant.py`, `Live Update Hub`, `context_version`?**
  _High betweenness centrality (0.003) - this node is a cross-community bridge._
- **Should `Assistant Training and Learning` be split into smaller, more focused modules?**
  _Cohesion score 0.07539450613676213 - nodes in this community are weakly interconnected._
- **Why does `System grounded learning retrieval and development corpora` connect `Analytics-v1 runtime and development AI system rules` to `Assistant Training Datasets Doc`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._