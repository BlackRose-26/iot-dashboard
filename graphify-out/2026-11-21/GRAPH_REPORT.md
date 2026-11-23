# Graph Report - iot-dashboard  (2026-11-21)

## Corpus Check
- 189 files · ~131,427 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 16 file(s) not represented in the graph (top: .css 8, .cmd 4, (none) 3)

## Summary
- 1729 nodes · 5279 edges · 75 communities (62 shown, 13 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 225 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e0ce1918`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- api() / AppContext.jsx
- run.py / experiment_history.py
- json
- Candidate evaluation preparation, review and first-use chronology / Initial five-candidate local mea
- icons.jsx / Registration.jsx
- assistant.py / re
- assistant.py
- create_app() / subject()
- V11 language coverage and topical scope repair / Analytics-v1 runtime and development AI system rule
- Assistant / Question
- test_device_recovery.py / RecoveryEmulator
- main.py / recovery_emulator.py
- check_quality.py / main()
- Boot-bound device recovery
- test_assistant_training.py / test_assistant_learning.py
- Context / test_assistant.py
- test_api_keeps_real_summary_and_design_explanations_despite_wrong_model
- test_player_flow.py / post()
- test_nlp_lab.py / data.py
- useApp
- evaluate_holdout.py / replay_consumed_holdout.py
- frontend/package.json / dependencies
- one() / device_recovery.py
- Cross-system quality audit
- Reviewed routing examples privacy workflow and planned evaluation review page / Implemented administ
- holdout_audit.py / prepare_candidate_holdout.py
- Stack Moko Baby canonical internal documentation index / Local Graphify setup and freshness guide
- History shortcut offline representation and training experiment / Verified remaining software releas
- Queue.jsx / Machines.jsx
- Confirmed React.js Tailwind UI integration and conventions / Dashboard visual contract with Tailwind
- Card() / Analytics.jsx
- assistant_training.py / evaluate_routing.py
- Overview.jsx / Leaderboard.jsx
- Current QR player flow and administrator access / Explicit Queue-page simulator action sequence
- Stack Moko Baby step-by-step implementation and acceptance gates / Source-backed decisions and open 
- test_assistant_generalization.py / security.py
- request_limits.py
- execute() / database.py
- schema.sql / staff_users
- QuestionReview.jsx / QuestionReview()
- NLP request grounding research implementation and checks / Current explicit measure and operation pr
- devDependencies / vite.config.js
- 001_initial.sql / game_sessions
- @playwright/test / flows.spec.js
- analytics.py / uuid
- test_quality_audit.py / test_ai_machine_readiness_agrees_with_dashboard_when_cabinet_is_unavailable(
- evaluation_review.py / live.py
- test_device_commands.py / reserve()
- Conversational behavior expansion / Bounded full-utterance social composition grammar
- dev.mjs / main()
- now() / all_rows()
- LiveHub / check()
- test_history_experiment.py / training_variants()
- device_boots / 002_player_flow.sql
- build_language_lexicon.py / build()
- package.json / scripts
- Context
- staff_users / evaluation_case_reviews
- register() / verify_csrf()
- scripts / build
- review-pages.mjs / ref_node_path
- quality-checks.mjs / iterator
- test-setup.js / @testing-library/jest-dom
- test_assistant_public_language.py
- .prettierrc.json / printWidth
- Project rules with protected first use evaluation / Confirmed frontend and private game authority bo
- within_deadline() / assistant_query()
- Isolated offline CPU NLP requirements / Pinned sentence transformers and Transformers dependencies
- FakeSocket / .close()
- Pinned backend dependency manifest / Pinned Argon2 and cryptography security dependencies
- React main.jsx module entry and root mount / Stack Moko Baby frontend HTML entry

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 120 edges
2. `normalize()` - 86 edges
3. `execute()` - 80 edges
4. `one()` - 74 edges
5. `Context` - 70 edges
6. `Assistant` - 67 edges
7. `now()` - 56 edges
8. `Stack Moko Baby canonical internal documentation index` - 48 edges
9. `useApp()` - 47 edges
10. `Stack Moko Baby step-by-step implementation and acceptance gates` - 44 edges

## Surprising Connections (you probably didn't know these)
- `Implemented administrator question review in Settings and at /admin/question-review` --references--> `QuestionReview()`  [INFERRED]
  docs/implementation-plan.md → frontend/src/pages/QuestionReview.jsx
- `Migration 006 preserves original frozen labels while saving reviewer decisions` --references--> `evaluation_case_reviews`  [EXTRACTED]
  docs/implementation-plan.md → backend/migrations/006_evaluation_review.sql
- `main()` --uses--> `Settings`  [INFERRED]
  scripts/export-registration-qr.py → backend/app/config.py
- `audit()` --uses--> `Context`  [INFERRED]
  docs/nlp-evaluation/audit_lab_context.py → backend/app/assistant.py
- `publish()` --calls--> `manifest()`  [INFERRED]
  docs/nlp-evaluation/summarize_history_lab.py → backend/experiment_history.py

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
- **Prepared325AI candidates remain isolated unreviewed and unscored** — docs_nlp_evaluation_candidate_v2_preparation_candidate_preparation, docs_nlp_evaluation_candidate_v2_preparation_candidate_status, docs_nlp_evaluation_candidate_v2_preparation_collision_audit, docs_nlp_evaluation_candidate_v2_preparation_review_unset, docs_nlp_evaluation_candidate_v2_preparation_evaluation_isolation, docs_nlp_evaluation_candidate_v2_preparation_followup_scoring [EXTRACTED 1.00]
- **History experiment evidence remains consumed regression; latercandidateauthoring doesnotimply revieworaccuracy** — docs_nlp_evaluation_history_lab_20261120_history_report, docs_nlp_evaluation_history_lab_20261120_history_measured, docs_nlp_evaluation_history_lab_20261120_coverage_failure, docs_nlp_evaluation_history_lab_20261120_admission_bottleneck, docs_nlp_evaluation_history_lab_20261120_history_no_promotion, docs_nlp_evaluation_history_lab_20261120_final_pending [EXTRACTED 1.00]
- **Frozen first-use evidence and consumed regression lifecycle** — docs_ai_system_rules_unseen_protocol, docs_nlp_evaluation_holdout_v1_holdout_isolation, docs_nlp_evaluation_holdout_v1_consumption_ledger, docs_nlp_routing_repair_frozen_replay [EXTRACTED 1.00]
- **Guarded public language to fresh read-only facts** — docs_nlp_routing_repair_pre_projection_guards, docs_nlp_routing_repair_lexical_projection, docs_nlp_routing_repair_topical_check, docs_nlp_routing_repair_deterministic_path, docs_admin_assistant_backend_facts [EXTRACTED 1.00]
- **Durable committed state survives missed responses without duplicate effects** — docs_device_recovery_consecutive_immutable_journal_receipts_and_scoped_uptime, docs_live_updates_transaction_committed_event_revision_and_durable_outbox, docs_schema_utc_millisecond_time_canonical_hash_and_transaction_boundaries [INFERRED 0.85]
- **Shared primitives and live semantic tokens preserve design during incremental migration** — docs_tailwind_ui_semantic_inline_aliases_resolve_live_application_tokens, docs_tailwind_ui_layered_migration_without_tailwind_preflight_reset, docs_tailwind_ui_incremental_shared_primitive_form_and_recovery_migration, docs_tailwind_ui_selector_controlled_admin_dark_mode_covers_radix_portals [INFERRED 0.85]

## Communities (75 total, 13 thin omitted)

### Community 0 - "api() / AppContext.jsx"
Cohesion: 0.07
Nodes (42): AdminAssistant(), send(), submit(), answerLabels, Evidence(), suggestions, mocks, openChat() (+34 more)

### Community 1 - "run.py / experiment_history.py"
Cohesion: 0.12
Nodes (27): manifest(), prepare(), run(), sha(), text(), DenseModel, fit_temperature(), loss() (+19 more)

### Community 2 - "json"
Cohesion: 0.08
Nodes (16): build(), wording(), measure(), main(), fetch(), main(), canonical(), main() (+8 more)

### Community 3 - "Candidate evaluation preparation, review and first-use chronology / Initial five-candidate local mea"
Cohesion: 0.05
Nodes (46): Prepare candidate questions before independent review without claiming adjudication, Blinded AI agreed with 323 of 325 proposed labels and adjudicated two differences, 119candidate questions have typed prior context, 176English149Taglish candidate annotations, Candidate evaluation preparation, review and first-use chronology, Authoring-stage packet contained 325 AI-written questions across 13 intents, 18offlinechecks Ruff and rejectionofunreviewed packet actualchecks, Zero exact usable-normalized reference collisions lexical matches or internalduplicates (+38 more)

### Community 4 - "icons.jsx / Registration.jsx"
Cohesion: 0.07
Nodes (48): ArrowLeft, ArrowRight, CalendarDays, CheckCircle2, CircuitBoard, Cpu, Eye, EyeOff (+40 more)

### Community 5 - "assistant.py / re"
Cohesion: 0.12
Nodes (19): conversational_reply(), composed_social(), parse(), greeting_answer(), interaction_rows(), interaction_social(), interaction_text(), interaction_words() (+11 more)

### Community 6 - "assistant.py"
Cohesion: 0.09
Nodes (36): constrained_route(), Intent, intent_payload(), MemoryPreferences, requested_metrics(), resolve_routing(), routing_input(), RoutingPlan (+28 more)

### Community 7 - "create_app() / subject()"
Cohesion: 0.11
Nodes (40): require_boot(), create_app(), admin_session(), admissions(), analytics(), assistant_forget_memory(), assistant_memory(), assistant_prepare() (+32 more)

### Community 8 - "V11 language coverage and topical scope repair / Analytics-v1 runtime and development AI system rule"
Cohesion: 0.05
Nodes (28): Stack Intelligence local administrator analytics guide, Explicit owner-reviewed current-version routing examples, Dashboard Settings houses model memory and training controls, Analytics-v1 runtime and development AI system rules, Explicit current measures override history and contradictory model labels, Student identity raw questions and private values excluded from model context, Eight bounded allowlisted read-only analytics operations, Dashboard visual contract with Tailwind integration (+20 more)

### Community 9 - "Assistant / Question"
Cohesion: 0.12
Nodes (25): Assistant, Question, run(), test_new_social_turns_work_with_ollama_disabled_and_preserve_context(), scenario(), test_specific_reported_greeting_through_the_service_without_ollama(), scenario(), test_explicit_request_bypasses_a_busy_inference_gate() (+17 more)

### Community 10 - "test_device_recovery.py / RecoveryEmulator"
Cohesion: 0.18
Nodes (25): RecoveryEmulator, emulator_setup(), fence(), fence_receipt(), resolution(), setup(), start_event(), test_a_new_boot_invalidates_an_old_fence_and_changed_storage_blocks_never_started() (+17 more)

### Community 11 - "main.py / recovery_emulator.py"
Cohesion: 0.10
Nodes (18): APIInput, BootRegistration, JournalEvent, Placement, RecoveryReason, RecoveryResolution, Result, cabinet_state() (+10 more)

### Community 12 - "check_quality.py / main()"
Cohesion: 0.12
Nodes (15): Settings, make_engine(), bounded_receive(), main(), receive(), start_api(), percentile(), serve() (+7 more)

### Community 13 - "Boot-bound device recovery"
Cohesion: 0.06
Nodes (9): Stack Moko Baby backend, Device command delivery and review holds, Espressif NVS commit and error guarantees, Espressif timer zero after deep sleep, MariaDB transaction scoped FOR UPDATE locks, Boot-bound device recovery, Local React and backend setup, Stack Moko Baby — MySQL data model (+1 more)

### Community 14 - "test_assistant_training.py / test_assistant_learning.py"
Cohesion: 0.08
Nodes (28): interpretation_choices(), retrieve(), seed_examples(), _seed_examples(), semantic_features(), signature(), compatible(), Proposal (+20 more)

### Community 15 - "Context / test_assistant.py"
Cohesion: 0.14
Nodes (27): compose(), endpoint(), normalize(), empty_summary(), fixture_data(), test_explaining_privacy_does_not_allow_identity_retrieval(), test_average_score_question_does_not_return_a_distribution_report(), test_empty_selection_keeps_rates_unavailable() (+19 more)

### Community 17 - "test_player_flow.py / post()"
Cohesion: 0.13
Nodes (26): compose_all(), test_absent_device_results_are_not_inferred_from_registrations(), test_all_sources_are_separate_and_players_are_deduplicated(), revision(), test_global_revisions_and_idempotent_operations(), test_live_rejects_missing_or_foreign_origin(), test_live_requires_the_right_authenticated_role(), test_logout_revokes_existing_socket_and_commands_are_rejected() (+18 more)

### Community 18 - "test_nlp_lab.py / data.py"
Cohesion: 0.09
Nodes (21): TrainingTarget, route_label(), Observer, predict(), balanced_cases(), partitions(), find(), union() (+13 more)

### Community 19 - "useApp"
Cohesion: 0.12
Nodes (26): AdminOnly(), App(), PlayerOnly(), UpdateStatus(), Entry(), ScanGate(), PublicHeader(), loadScannerApi() (+18 more)

### Community 20 - "evaluate_holdout.py / replay_consumed_holdout.py"
Cohesion: 0.17
Nodes (16): check(), evaluate(), ObservedAssistant, score(), evaluator_fingerprint(), runtime_fingerprint(), sha(), verify_frozen() (+8 more)

### Community 21 - "frontend/package.json / dependencies"
Cohesion: 0.09
Nodes (29): dependencies, @fontsource-variable/open-sans@5.3.0, @fortawesome/fontawesome-free@7.3.1, html5-qrcode@2.3.8, qr-scanner@1.4.2, qrcode.react@4.2.0, @radix-ui/react-dialog@1.3.1, @radix-ui/react-dropdown-menu@2.2.1 (+21 more)

### Community 22 - "one() / device_recovery.py"
Cohesion: 0.20
Nodes (15): acknowledge(), CommandAcknowledgement, hold_for_review(), current_boot(), journal(), quarantine(), recovery_view(), register_boot() (+7 more)

### Community 23 - "Cross-system quality audit"
Cohesion: 0.07
Nodes (4): Stack Moko Baby — functional specification, Durable browser updates, Player QR scanner, Cross-system quality audit

### Community 24 - "Reviewed routing examples privacy workflow and planned evaluation review page / Implemented administ"
Cohesion: 0.06
Nodes (27): System grounded learning retrieval and development corpora, Optimistic revision current public context confirmation and409staleapproval, 1000recordsperowner25perpage bounded parameterized statement-deadline queries, Future evaluation UI confirm correct reject versioneddecisions navigation progressfilters, Predictions hidden during pre-evaluation label review, Future evaluation UI question proposedlabel typedprior expectedstate explanations notes, No player identities private chats or credentials in future review UI, Evaluation cases stay separate from owner private chat training examples (+19 more)

### Community 25 - "holdout_audit.py / prepare_candidate_holdout.py"
Cohesion: 0.16
Nodes (18): build_rows(), feature_key(), freeze(), inventory(), overlap_audit(), previous_context(), reference_questions(), text_key() (+10 more)

### Community 26 - "Stack Moko Baby canonical internal documentation index / Local Graphify setup and freshness guide"
Cohesion: 0.09
Nodes (17): Local Graphify setup and freshness guide, Consumed replay accepted 146 of 325, including 7 of 25 follow-ups, Frozen core service accepted 130 of 325 AI-adjudicated synthetic cases, Private QR registration queue tickets and authenticated staff views, Confirmed React JavaScript Tailwind FastAPI XAMPP stack, Consumed regression135of325 with135clarifications open NLP gate, AI-adjudicated routing and behavior accepted 130 of 325 cases, including zero of 25 follow-ups, LED matrix physical button game and required private student ID (+9 more)

### Community 27 - "History shortcut offline representation and training experiment / Verified remaining software releas"
Cohesion: 0.05
Nodes (48): 40of120supported blocked upstream;84of130admitted31unknown14scope1measurement, 285originaltraining plus792historyvariants1077rows zero new independent questions, Synthetic variants add no missing subtypes language diversity or independent families, Augmentedpolicy answerszero question-onlypolicy answersone of120supported, Collection was empty at history run;later325AI candidates filled independentreviewpending, Frozen multilingual E5 hierarchical heads history and question-only ablations, Retained protocol variants heads predictions and14offlinechecks, AugmentedE5 ordinary61of130 stress47of120 vsoriginal63and14 (+40 more)

### Community 28 - "Queue.jsx / Machines.jsx"
Cohesion: 0.19
Nodes (25): actions, DeviceRecovery(), ArrowUpRight, ChevronLeft, Download, Pause, Play, UsersRound (+17 more)

### Community 29 - "Confirmed React.js Tailwind UI integration and conventions / Dashboard visual contract with Tailwind"
Cohesion: 0.10
Nodes (10): Official Tailwind Vite installation, Confirmed React.js Tailwind UI integration and conventions, Tailwind imports prefix and Preflight reset guidance, Tailwind inline theme aliases, Tailwind selector controlled dark mode, Access flow contrast mobile and verification refinement passes, Documented current Edge accessibility unit and production checks, Historical eight-page sample review evidence (+2 more)

### Community 30 - "Card() / Analytics.jsx"
Cohesion: 0.17
Nodes (22): ActivityChart(), axis, ChartTip(), LevelChart(), OutcomesChart(), ScoreChart(), Clock3, Target (+14 more)

### Community 31 - "assistant_training.py / evaluate_routing.py"
Cohesion: 0.15
Nodes (9): inspect(), corpus_digest(), model_json(), canonical(), context_version(), Review, TrainingStore, evaluate() (+1 more)

### Community 32 - "Overview.jsx / Leaderboard.jsx"
Cohesion: 0.21
Nodes (21): Check, ChevronDown, ChevronRight, Medal, X, PlayerList(), Shell(), tabs (+13 more)

### Community 33 - "Current QR player flow and administrator access / Explicit Queue-page simulator action sequence"
Cohesion: 0.15
Nodes (17): Authenticated synthetic-tested device integration boundary, Completed-round-only source-matched player leaderboard, Current QR player flow and administrator access, Durable win loss alerts with focus-refresh polling, Explicit Queue-page simulator action sequence, Owner-only persistent ticket across refreshes, Preserved Sourcio-derived player styling and font symbols, Private cabinetState and queueState waiting reasons (+9 more)

### Community 34 - "Stack Moko Baby step-by-step implementation and acceptance gates / Source-backed decisions and open "
Cohesion: 0.08
Nodes (26): Post-consumption corrections preserve originalresult new annotationversion, Planned21November dedicated admin evaluationcase review page not implemented, Stack Moko Baby step-by-step implementation and acceptance gates, Identity before queue verifiedresults before AI adaptive difficultydeferred, Deterministic engine shared fixtures immutable rules and hardwarelatency, Repeatable ReactPython XAMPP environment and Graphify, Firmwarepersistentjournal backend replay and atomic terminalresults, Confirmed ReactJavaScript Tailwind4shared UI incremental styling (+18 more)

### Community 35 - "test_assistant_generalization.py / security.py"
Cohesion: 0.17
Nodes (8): replay(), simulated_result(), seed_scores(), test_api_answers_scores_not_a_wrong_model_or_saved_subject(), test_player_score_sql_is_paginated_and_keeps_source_evidence(), test_terminal_duration_cannot_extend_beyond_the_ending_placement(), test_shared_scoring_vectors(), test_timeout_and_tamper_rejection()

### Community 37 - "execute() / database.py"
Cohesion: 0.13
Nodes (6): MemoryStore, execute(), routing(), test_forget_has_csrf_and_prevents_old_inflight_memory_from_returning(), test_preferences_are_private_and_memory_can_be_disabled(), test_readiness_requires_applied_migrations_and_schema()

### Community 38 - "schema.sql / staff_users"
Cohesion: 0.25
Nodes (18): ai_admin_memory, ai_requests, ai_training_examples, audit_logs, auth_sessions, device_commands, device_events, events (+10 more)

### Community 39 - "QuestionReview.jsx / QuestionReview()"
Cohesion: 0.15
Nodes (17): actions, Correction(), changeTopic(), subtypesFor(), decisions, describeContext(), kinds, labelTarget() (+9 more)

### Community 41 - "devDependencies / vite.config.js"
Cohesion: 0.12
Nodes (16): devDependencies, jsdom@31.0.1, prettier@3.10.1, tailwindcss@4.3.5, @tailwindcss/vite@4.3.5, @testing-library/react@16.3.3, @testing-library/user-event@14.6.10, vite@8.3.8 (+8 more)

### Community 42 - "001_initial.sql / game_sessions"
Cohesion: 0.28
Nodes (16): ai_requests, audit_logs, auth_sessions, device_commands, device_events, events, game_sessions, machines (+8 more)

### Community 43 - "@playwright/test / flows.spec.js"
Cohesion: 0.13
Nodes (5): errors, @axe-core/playwright@4.14.0, @playwright/test@1.65.1, @axe-core/playwright, @playwright/test

### Community 44 - "analytics.py / uuid"
Cohesion: 0.24
Nodes (8): clean(), collect(), collect_all(), _collect_snapshot(), _operations(), select(), stamp(), test_emulator_refuses_corrupt_journal_before_contacting_device()

### Community 45 - "test_quality_audit.py / test_ai_machine_readiness_agrees_with_dashboard_when_cabinet_is_unavailable("
Cohesion: 0.15
Nodes (6): replace(), test_ai_machine_readiness_agrees_with_dashboard_when_cabinet_is_unavailable(), test_chunked_body_limit_cannot_be_bypassed_without_content_length(), test_fresh_disabled_simulator_cannot_accept_a_new_assignment(), test_malformed_login_text_or_unknown_fields_fail_without_server_errors(), test_unknown_subject_cannot_be_replaced_with_event_data()

### Community 46 - "evaluation_review.py / live.py"
Cohesion: 0.18
Nodes (7): Annotation, CaseReview, packet(), proposed(), read_reviews(), save_review(), evaluation_decision()

### Community 47 - "test_device_commands.py / reserve()"
Cohesion: 0.28
Nodes (12): command_row(), reserve(), test_expired_unknown_start_never_becomes_an_automatic_no_show(), test_invalid_or_stale_receipts_cannot_change_the_command(), test_other_machine_commands_and_maintenance_cannot_be_bypassed(), test_polling_is_authorized_repeatable_and_contains_no_player_identity(), test_receipt_survives_application_recreation_and_emulator_lost_ack(), post() (+4 more)

### Community 49 - "dev.mjs / main()"
Cohesion: 0.17
Nodes (10): backend, backendOnly, frontend, health(), main(), owned, portInUse(), root (+2 more)

### Community 50 - "now() / all_rows()"
Cohesion: 0.20
Nodes (18): all_rows(), one(), poll_commands(), requires_review(), active(), call_next(), context(), device_commands() (+10 more)

### Community 51 - "LiveHub / check()"
Cohesion: 0.24
Nodes (4): LiveHub, restart(), test_slow_clients_coalesce_and_connection_caps_are_bounded(), check()

### Community 52 - "test_history_experiment.py / training_variants()"
Cohesion: 0.25
Nodes (8): question_only(), QuestionOnly, training_variants(), test_augmentation_cannot_ingest_calibration_comparison_or_blocked_rows(), test_existing_contextual_examples_are_never_relabelled_or_given_wrong_subject(), test_history_variants_keep_original_question_target_and_family(), test_question_only_features_do_not_change_with_any_validated_prior_subject(), training_row()

### Community 53 - "device_boots / 002_player_flow.sql"
Cohesion: 0.24
Nodes (7): entry_grants, login_attempts, player_notifications, qr_links, device_boots, device_journal_events, device_recovery_conflicts

### Community 55 - "build_language_lexicon.py / build()"
Cohesion: 0.23
Nodes (4): build(), digest(), Links, word_form()

### Community 56 - "package.json / scripts"
Cohesion: 0.18
Nodes (10): engines, node, name, private, scripts, dev, dev:backend, dev:frontend (+2 more)

### Community 57 - "Context"
Cohesion: 0.13
Nodes (16): automatic_scope(), basic_response(), Context, continuation(), knowledge_response(), preference_reply(), scope_payload(), render() (+8 more)

### Community 58 - "staff_users / evaluation_case_reviews"
Cohesion: 0.29
Nodes (3): ai_admin_memory, ai_training_examples, evaluation_case_reviews

### Community 60 - "register() / verify_csrf()"
Cohesion: 0.14
Nodes (12): boundaries(), entry(), login(), register(), session(), canonical_origin(), origin_allowed(), csrf_for() (+4 more)

### Community 61 - "scripts / build"
Cohesion: 0.25
Nodes (8): scripts, build, dev, dev:frontend, format, preview, test, test:browser

### Community 62 - "review-pages.mjs / ref_node_path"
Cohesion: 0.25
Nodes (6): directory, errors, height, results, routes, width

### Community 66 - "test_assistant_public_language.py"
Cohesion: 0.20
Nodes (5): lexical_resource(), test_development_wording_preserves_public_content_or_rejects_locally(), test_polysemous_word_does_not_silently_change_a_measure(), test_public_dictionary_is_word_only_filtered_and_content_addressed(), test_scope_rejection_stops_before_router_and_analytics()

### Community 68 - ".prettierrc.json / printWidth"
Cohesion: 0.40
Nodes (4): printWidth, semi, singleQuote, trailingComma

### Community 70 - "within_deadline() / assistant_query()"
Cohesion: 0.50
Nodes (3): assistant_query(), within_deadline(), request()

### Community 71 - "Isolated offline CPU NLP requirements / Pinned sentence transformers and Transformers dependencies"
Cohesion: 0.50
Nodes (4): Pinned sentence transformers and Transformers dependencies, Isolated offline CPU NLP requirements, SetFit 1.1.3 offline dependency, CPU Torch 2.9.1 offline dependency

### Community 75 - "Pinned backend dependency manifest / Pinned Argon2 and cryptography security dependencies"
Cohesion: 0.67
Nodes (3): Pinned Argon2 and cryptography security dependencies, Pinned backend dependency manifest, Pinned FastAPI SQLAlchemy PyMySQL Uvicorn runtime

## Knowledge Gaps
- **241 isolated node(s):** `answerLabels`, `suggestions`, `mocks`, `mocks`, `state` (+236 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 569 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create_app()` connect `create_app() / subject()` to `test_assistant_generalization.py / security.py`, `request_limits.py`, `execute() / database.py`, `within_deadline() / assistant_query()`, `assistant.py / re`, `Assistant / Question`, `main.py / recovery_emulator.py`, `analytics.py / uuid`, `check_quality.py / main()`, `test_assistant_training.py / test_assistant_learning.py`, `evaluation_review.py / live.py`, `now() / all_rows()`, `LiveHub / check()`, `one() / device_recovery.py`, `Context`, `register() / verify_csrf()`, `assistant_training.py / evaluate_routing.py`?**
  _High betweenness centrality (0.003) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `create_app()` (e.g. with `Question` and `Proposal`) actually correct?**
  _`create_app()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `answerLabels`, `suggestions`, `mocks` to the rest of the system?**
  _241 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `api() / AppContext.jsx` be split into smaller, more focused modules?**
  _Cohesion score 0.06939890710382514 - nodes in this community are weakly interconnected._
- **Why does `Assistant` connect `Assistant / Question` to `execute() / database.py`, `analytics.py / uuid`, `test_assistant_training.py / test_assistant_learning.py`, `now() / all_rows()`, `test_nlp_lab.py / data.py`, `Context`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **Should `run.py / experiment_history.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11591836734693878 - nodes in this community are weakly interconnected._
- **Why does `Stack Intelligence local administrator analytics guide` connect `V11 language coverage and topical scope repair / Analytics-v1 runtime and development AI system rule` to `Candidate evaluation preparation, review and first-use chronology / Initial five-candidate local mea`, `NLP request grounding research implementation and checks / Current explicit measure and operation pr`, `Conversational behavior expansion / Bounded full-utterance social composition grammar`, `Cross-system quality audit`, `Reviewed routing examples privacy workflow and planned evaluation review page / Implemented administ`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._