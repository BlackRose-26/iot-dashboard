-- Explicitly selected sanitized routing inputs and human-reviewed labels only.
CREATE TABLE IF NOT EXISTS ai_training_examples (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  public_id CHAR(36) CHARACTER SET ascii COLLATE ascii_bin NOT NULL UNIQUE,
  staff_user_id BIGINT UNSIGNED NOT NULL,
  input_hash CHAR(64) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  input_json JSON NOT NULL,
  target_json JSON NOT NULL,
  status ENUM('pending','approved','rejected') NOT NULL DEFAULT 'pending',
  revision BIGINT UNSIGNED NOT NULL DEFAULT 0,
  context_version CHAR(64) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  policy_version VARCHAR(30) NOT NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  reviewed_at DATETIME(3) NULL,
  UNIQUE KEY uq_training_owner_input (staff_user_id,input_hash),
  KEY ix_training_owner_status (staff_user_id,status,context_version,id),
  CONSTRAINT fk_training_staff FOREIGN KEY (staff_user_id) REFERENCES staff_users(id)
) ENGINE=InnoDB;
