CREATE TABLE device_boots (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  public_id CHAR(36) CHARACTER SET ascii COLLATE ascii_bin NOT NULL UNIQUE,
  machine_id BIGINT UNSIGNED NOT NULL,
  previous_boot_id BIGINT UNSIGNED NULL,
  storage_id CHAR(36) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  registration_hash BINARY(32) NOT NULL,
  last_sequence BIGINT UNSIGNED NOT NULL DEFAULT 0,
  last_uptime_ms BIGINT UNSIGNED NOT NULL,
  registered_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  last_seen_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  retired_at DATETIME(3) NULL,
  active_machine_id BIGINT UNSIGNED GENERATED ALWAYS AS (IF(retired_at IS NULL,machine_id,NULL)) STORED,
  UNIQUE KEY uq_current_device_boot (active_machine_id),
  CONSTRAINT fk_boot_machine FOREIGN KEY (machine_id) REFERENCES machines(id),
  CONSTRAINT fk_boot_previous FOREIGN KEY (previous_boot_id) REFERENCES device_boots(id)
) ENGINE=InnoDB;

ALTER TABLE device_commands
  MODIFY command_type ENUM('reserve','abort','reconcile','maintenance','fence') NOT NULL,
  ADD accepted_boot_id BIGINT UNSIGNED NULL,
  ADD accepted_uptime_ms BIGINT UNSIGNED NULL,
  ADD target_boot_id BIGINT UNSIGNED NULL,
  ADD CONSTRAINT fk_command_accepted_boot FOREIGN KEY (accepted_boot_id) REFERENCES device_boots(id),
  ADD CONSTRAINT fk_command_target_boot FOREIGN KEY (target_boot_id) REFERENCES device_boots(id);

CREATE TABLE device_journal_events (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  public_id CHAR(36) CHARACTER SET ascii COLLATE ascii_bin NOT NULL UNIQUE,
  boot_id BIGINT UNSIGNED NOT NULL,
  sequence_number BIGINT UNSIGNED NOT NULL,
  uptime_ms BIGINT UNSIGNED NOT NULL,
  session_id BIGINT UNSIGNED NOT NULL,
  command_id BIGINT UNSIGNED NOT NULL,
  phase ENUM('reserved','started','terminal','fenced_unstarted','fenced_interrupted') NOT NULL,
  payload_hash BINARY(32) NOT NULL,
  payload JSON NOT NULL,
  response_safe JSON NOT NULL,
  received_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  UNIQUE KEY uq_boot_sequence (boot_id,sequence_number),
  KEY ix_recovery_session (session_id,id),
  CONSTRAINT fk_journal_boot FOREIGN KEY (boot_id) REFERENCES device_boots(id),
  CONSTRAINT fk_journal_session FOREIGN KEY (session_id) REFERENCES game_sessions(id),
  CONSTRAINT fk_journal_command FOREIGN KEY (command_id) REFERENCES device_commands(id)
) ENGINE=InnoDB;

ALTER TABLE game_sessions ADD recovery_quarantined BOOLEAN NOT NULL DEFAULT FALSE;

CREATE TABLE device_recovery_conflicts (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  session_id BIGINT UNSIGNED NOT NULL,
  boot_id BIGINT UNSIGNED NOT NULL,
  attempted_event_id CHAR(36) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  sequence_number BIGINT UNSIGNED NOT NULL,
  phase VARCHAR(32) CHARACTER SET ascii NOT NULL,
  payload_hash BINARY(32) NOT NULL,
  reason VARCHAR(160) NOT NULL,
  received_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  CONSTRAINT fk_conflict_session FOREIGN KEY (session_id) REFERENCES game_sessions(id),
  CONSTRAINT fk_conflict_boot FOREIGN KEY (boot_id) REFERENCES device_boots(id)
) ENGINE=InnoDB;
