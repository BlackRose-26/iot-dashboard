-- Stack Moko Baby candidate schema: XAMPP MariaDB 10.11 / MySQL-compatible InnoDB.
-- Apply only to an empty development database; migrate with Alembic thereafter.
-- This file does not provision users or contain real player data.
CREATE DATABASE IF NOT EXISTS stack_moko_baby
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE stack_moko_baby;
SET time_zone = '+00:00';

CREATE TABLE events (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  public_id CHAR(36) CHARACTER SET ascii COLLATE ascii_bin NOT NULL UNIQUE,
  code VARCHAR(40) CHARACTER SET ascii COLLATE ascii_bin NOT NULL UNIQUE,
  name VARCHAR(120) NOT NULL,
  timezone VARCHAR(64) NOT NULL DEFAULT 'Asia/Manila',
  status ENUM('draft','open','paused','closed') NOT NULL DEFAULT 'draft',
  starts_at DATETIME(3) NOT NULL,
  ends_at DATETIME(3) NOT NULL,
  revision BIGINT UNSIGNED NOT NULL DEFAULT 0,
  settings JSON NOT NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT ck_event_dates CHECK (ends_at > starts_at)
) ENGINE=InnoDB;

CREATE TABLE players (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  public_id CHAR(36) CHARACTER SET ascii COLLATE ascii_bin NOT NULL UNIQUE,
  public_code VARCHAR(20) CHARACTER SET ascii COLLATE ascii_bin NOT NULL UNIQUE,
  nickname VARCHAR(24) NOT NULL,
  notice_version VARCHAR(30) NOT NULL,
  notice_ack_at DATETIME(3) NOT NULL,
  anonymized_at DATETIME(3) NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
) ENGINE=InnoDB;

CREATE TABLE student_identities (
  player_id BIGINT UNSIGNED PRIMARY KEY,
  institution_code VARCHAR(40) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  id_lookup BINARY(32) NOT NULL,
  lookup_key_version SMALLINT UNSIGNED NOT NULL,
  encrypted_id VARBINARY(512) NOT NULL,
  nonce BINARY(12) NOT NULL,
  auth_tag BINARY(16) NOT NULL,
  encryption_key_version SMALLINT UNSIGNED NOT NULL,
  purge_after DATETIME(3) NOT NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  UNIQUE KEY uq_identity_lookup (institution_code, lookup_key_version, id_lookup),
  KEY ix_identity_purge (purge_after),
  CONSTRAINT fk_identity_player FOREIGN KEY (player_id) REFERENCES players(id)
) ENGINE=InnoDB;

CREATE TABLE staff_users (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(80) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('operator','admin') NOT NULL,
  enabled BOOLEAN NOT NULL DEFAULT TRUE,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
) ENGINE=InnoDB;

CREATE TABLE auth_sessions (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  token_hash BINARY(32) NOT NULL UNIQUE,
  csrf_token_hash BINARY(32) NOT NULL,
  player_id BIGINT UNSIGNED NULL,
  staff_user_id BIGINT UNSIGNED NULL,
  expires_at DATETIME(3) NOT NULL,
  revoked_at DATETIME(3) NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  KEY ix_auth_expiry (expires_at),
  CONSTRAINT fk_auth_player FOREIGN KEY (player_id) REFERENCES players(id),
  CONSTRAINT fk_auth_staff FOREIGN KEY (staff_user_id) REFERENCES staff_users(id),
  CONSTRAINT ck_auth_subject CHECK ((player_id IS NULL) <> (staff_user_id IS NULL))
) ENGINE=InnoDB;

CREATE TABLE rulesets (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(50) CHARACTER SET ascii COLLATE ascii_bin NOT NULL UNIQUE,
  version SMALLINT UNSIGNED NOT NULL,
  config JSON NOT NULL,
  config_hash BINARY(32) NOT NULL UNIQUE,
  created_by BIGINT UNSIGNED NOT NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT fk_rules_staff FOREIGN KEY (created_by) REFERENCES staff_users(id)
) ENGINE=InnoDB;

CREATE TABLE machines (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  public_id CHAR(36) CHARACTER SET ascii COLLATE ascii_bin NOT NULL UNIQUE,
  event_id BIGINT UNSIGNED NOT NULL,
  code VARCHAR(40) CHARACTER SET ascii COLLATE ascii_bin NOT NULL UNIQUE,
  name VARCHAR(80) NOT NULL,
  device_token_hash BINARY(32) NOT NULL,
  enabled BOOLEAN NOT NULL DEFAULT TRUE,
  maintenance BOOLEAN NOT NULL DEFAULT FALSE,
  observed_state VARCHAR(30) NOT NULL DEFAULT 'unknown',
  observed_session_public_id CHAR(36) CHARACTER SET ascii COLLATE ascii_bin NULL,
  boot_id CHAR(36) CHARACTER SET ascii COLLATE ascii_bin NULL,
  uptime_ms BIGINT UNSIGNED NULL,
  firmware_version VARCHAR(64) NULL,
  last_seen_at DATETIME(3) NULL,
  health JSON NULL,
  revision BIGINT UNSIGNED NOT NULL DEFAULT 0,
  UNIQUE KEY uq_machine_event (event_id, id),
  CONSTRAINT fk_machine_event FOREIGN KEY (event_id) REFERENCES events(id)
) ENGINE=InnoDB;

CREATE TABLE queue_entries (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  public_id CHAR(36) CHARACTER SET ascii COLLATE ascii_bin NOT NULL UNIQUE,
  event_id BIGINT UNSIGNED NOT NULL,
  player_id BIGINT UNSIGNED NOT NULL,
  status ENUM('waiting','assigned','served','cancelled','expired') NOT NULL DEFAULT 'waiting',
  live_player_id BIGINT UNSIGNED GENERATED ALWAYS AS
    (CASE WHEN status IN ('waiting','assigned') THEN player_id ELSE NULL END) STORED,
  joined_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  closed_at DATETIME(3) NULL,
  revision BIGINT UNSIGNED NOT NULL DEFAULT 0,
  UNIQUE KEY uq_live_ticket (event_id, live_player_id),
  UNIQUE KEY uq_queue_binding (event_id, id, player_id),
  KEY ix_queue_fifo (event_id, status, joined_at, id),
  CONSTRAINT fk_queue_event FOREIGN KEY (event_id) REFERENCES events(id),
  CONSTRAINT fk_queue_player FOREIGN KEY (player_id) REFERENCES players(id)
) ENGINE=InnoDB;

CREATE TABLE game_sessions (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  public_id CHAR(36) CHARACTER SET ascii COLLATE ascii_bin NOT NULL UNIQUE,
  event_id BIGINT UNSIGNED NOT NULL,
  machine_id BIGINT UNSIGNED NOT NULL,
  queue_entry_id BIGINT UNSIGNED NOT NULL UNIQUE,
  player_id BIGINT UNSIGNED NOT NULL,
  ruleset_id BIGINT UNSIGNED NOT NULL,
  status ENUM('reserved','countdown','playing','awaiting_result','completed','expired','aborted','review')
    NOT NULL DEFAULT 'reserved',
  active_machine_id BIGINT UNSIGNED GENERATED ALWAYS AS
    (CASE WHEN status IN ('reserved','countdown','playing','awaiting_result','review')
      THEN machine_id ELSE NULL END) STORED,
  revision BIGINT UNSIGNED NOT NULL DEFAULT 1,
  reserved_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  ready_deadline_at DATETIME(3) NOT NULL,
  started_at DATETIME(3) NULL,
  completed_at DATETIME(3) NULL,
  received_at DATETIME(3) NULL,
  terminal_id CHAR(36) CHARACTER SET ascii COLLATE ascii_bin NULL UNIQUE,
  result_hash BINARY(32) NULL,
  outcome ENUM('win','loss') NULL,
  end_reason ENUM('target_reached','zero_overlap','timeout','operator_abort','power_loss','no_show','device_fault') NULL,
  duration_ms INT UNSIGNED NULL,
  score INT UNSIGNED NULL,
  highest_level SMALLINT UNSIGNED NULL,
  perfect_rows SMALLINT UNSIGNED NULL,
  overlap_total SMALLINT UNSIGNED NULL,
  attempted_width_total SMALLINT UNSIGNED NULL,
  invalidated_at DATETIME(3) NULL,
  invalidated_by BIGINT UNSIGNED NULL,
  invalidation_reason VARCHAR(300) NULL,
  UNIQUE KEY uq_active_machine (active_machine_id),
  UNIQUE KEY uq_session_machine (id, machine_id),
  KEY ix_session_ranking (event_id, ruleset_id, status, invalidated_at, score DESC, completed_at),
  KEY ix_session_player (player_id, completed_at),
  CONSTRAINT fk_session_event_machine FOREIGN KEY (event_id, machine_id)
    REFERENCES machines(event_id, id),
  CONSTRAINT fk_session_queue_player FOREIGN KEY (event_id, queue_entry_id, player_id)
    REFERENCES queue_entries(event_id, id, player_id),
  CONSTRAINT fk_session_rules FOREIGN KEY (ruleset_id) REFERENCES rulesets(id),
  CONSTRAINT fk_session_invalidator FOREIGN KEY (invalidated_by) REFERENCES staff_users(id),
  CONSTRAINT ck_session_completed CHECK (status <> 'completed' OR
    (outcome IS NOT NULL AND terminal_id IS NOT NULL AND result_hash IS NOT NULL
     AND completed_at IS NOT NULL AND received_at IS NOT NULL AND duration_ms IS NOT NULL
     AND score IS NOT NULL AND highest_level IS NOT NULL AND perfect_rows IS NOT NULL
     AND overlap_total IS NOT NULL AND attempted_width_total IS NOT NULL)),
  CONSTRAINT ck_session_accuracy CHECK (overlap_total IS NULL OR attempted_width_total IS NULL
    OR overlap_total <= attempted_width_total),
  CONSTRAINT ck_session_perfect CHECK (perfect_rows IS NULL OR highest_level IS NULL
    OR perfect_rows <= highest_level),
  CONSTRAINT ck_session_invalidation CHECK (invalidated_at IS NULL OR
    (invalidated_by IS NOT NULL AND invalidation_reason IS NOT NULL))
) ENGINE=InnoDB;

CREATE TABLE placements (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  session_id BIGINT UNSIGNED NOT NULL,
  sequence_no SMALLINT UNSIGNED NOT NULL,
  level_no SMALLINT UNSIGNED NOT NULL,
  candidate_x SMALLINT UNSIGNED NOT NULL,
  candidate_width SMALLINT UNSIGNED NOT NULL,
  support_x SMALLINT UNSIGNED NOT NULL,
  support_width SMALLINT UNSIGNED NOT NULL,
  overlap_width SMALLINT UNSIGNED NOT NULL,
  locked_at_ms INT UNSIGNED NOT NULL,
  UNIQUE KEY uq_placement_seq (session_id, sequence_no),
  UNIQUE KEY uq_placement_level (session_id, level_no),
  CONSTRAINT fk_placement_session FOREIGN KEY (session_id) REFERENCES game_sessions(id),
  CONSTRAINT ck_placement_positive CHECK (sequence_no > 0 AND level_no > 0
    AND candidate_width > 0 AND support_width > 0),
  CONSTRAINT ck_placement_overlap CHECK
    (overlap_width <= candidate_width AND overlap_width <= support_width)
) ENGINE=InnoDB;

CREATE TABLE device_events (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  public_id CHAR(36) CHARACTER SET ascii COLLATE ascii_bin NOT NULL UNIQUE,
  session_id BIGINT UNSIGNED NOT NULL,
  machine_id BIGINT UNSIGNED NOT NULL,
  sequence_no INT UNSIGNED NOT NULL,
  event_type ENUM('countdown_started','play_started','progress','interrupted') NOT NULL,
  payload JSON NOT NULL,
  payload_hash BINARY(32) NOT NULL,
  received_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  UNIQUE KEY uq_device_event_seq (session_id, sequence_no),
  CONSTRAINT fk_device_event_binding FOREIGN KEY (session_id, machine_id)
    REFERENCES game_sessions(id, machine_id)
) ENGINE=InnoDB;

CREATE TABLE device_commands (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  public_id CHAR(36) CHARACTER SET ascii COLLATE ascii_bin NOT NULL UNIQUE,
  machine_id BIGINT UNSIGNED NOT NULL,
  session_id BIGINT UNSIGNED NULL,
  command_type ENUM('reserve','abort','reconcile','maintenance') NOT NULL,
  expected_revision BIGINT UNSIGNED NOT NULL,
  payload JSON NOT NULL,
  status ENUM('pending','accepted','applied','rejected','expired') NOT NULL DEFAULT 'pending',
  receipt_hash BINARY(32) NULL,
  rejection_code VARCHAR(60) NULL,
  issued_by BIGINT UNSIGNED NULL,
  expires_at DATETIME(3) NOT NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  acknowledged_at DATETIME(3) NULL,
  applied_at DATETIME(3) NULL,
  KEY ix_command_delivery (machine_id, status, created_at),
  CONSTRAINT fk_command_machine FOREIGN KEY (machine_id) REFERENCES machines(id),
  CONSTRAINT fk_command_binding FOREIGN KEY (session_id, machine_id)
    REFERENCES game_sessions(id, machine_id),
  CONSTRAINT fk_command_staff FOREIGN KEY (issued_by) REFERENCES staff_users(id)
) ENGINE=InnoDB;

CREATE TABLE request_receipts (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  actor_scope VARCHAR(100) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  operation VARCHAR(80) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  idempotency_key VARCHAR(80) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  request_hash BINARY(32) NOT NULL,
  response_status SMALLINT UNSIGNED NOT NULL,
  response_safe JSON NOT NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  UNIQUE KEY uq_request_receipt (actor_scope, operation, idempotency_key)
) ENGINE=InnoDB;

CREATE TABLE audit_logs (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  event_id BIGINT UNSIGNED NULL,
  staff_user_id BIGINT UNSIGNED NULL,
  action VARCHAR(80) NOT NULL,
  entity_type VARCHAR(50) NOT NULL,
  entity_public_id CHAR(36) CHARACTER SET ascii COLLATE ascii_bin NULL,
  reason VARCHAR(300) NULL,
  details_safe JSON NOT NULL,
  request_id CHAR(36) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  KEY ix_audit_time (event_id, created_at),
  CONSTRAINT fk_audit_event FOREIGN KEY (event_id) REFERENCES events(id),
  CONSTRAINT fk_audit_staff FOREIGN KEY (staff_user_id) REFERENCES staff_users(id)
) ENGINE=InnoDB;

CREATE TABLE ai_requests (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  public_id CHAR(36) CHARACTER SET ascii COLLATE ascii_bin NOT NULL UNIQUE,
  event_id BIGINT UNSIGNED NOT NULL,
  staff_user_id BIGINT UNSIGNED NOT NULL,
  ruleset_id BIGINT UNSIGNED NULL,
  policy_version VARCHAR(30) NOT NULL,
  model_identifier VARCHAR(100) NULL,
  status ENUM('ok','no_data','refused','timeout','provider_error','invalid_output') NOT NULL,
  window_start DATETIME(3) NOT NULL,
  window_end DATETIME(3) NOT NULL,
  tools_used JSON NOT NULL,
  input_tokens INT UNSIGNED NULL,
  output_tokens INT UNSIGNED NULL,
  latency_ms INT UNSIGNED NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT fk_ai_event FOREIGN KEY (event_id) REFERENCES events(id),
  CONSTRAINT fk_ai_staff FOREIGN KEY (staff_user_id) REFERENCES staff_users(id),
  CONSTRAINT fk_ai_rules FOREIGN KEY (ruleset_id) REFERENCES rulesets(id),
  CONSTRAINT ck_ai_window CHECK (window_end > window_start)
) ENGINE=InnoDB;

CREATE TABLE outbox_events (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  public_id CHAR(36) CHARACTER SET ascii COLLATE ascii_bin NOT NULL UNIQUE,
  event_id BIGINT UNSIGNED NOT NULL,
  event_revision BIGINT UNSIGNED NOT NULL,
  event_type VARCHAR(60) NOT NULL,
  entity_public_id CHAR(36) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  payload_safe JSON NOT NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  published_at DATETIME(3) NULL,
  attempts INT UNSIGNED NOT NULL DEFAULT 0,
  next_attempt_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  KEY ix_outbox_pending (published_at, next_attempt_at, id),
  KEY ix_outbox_revision (event_id, event_revision),
  CONSTRAINT fk_outbox_event FOREIGN KEY (event_id) REFERENCES events(id)
) ENGINE=InnoDB;
