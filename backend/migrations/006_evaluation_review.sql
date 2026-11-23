-- Append-only human annotations for synthetic evaluation cases.
CREATE TABLE IF NOT EXISTS evaluation_case_reviews (
  staff_user_id BIGINT UNSIGNED NOT NULL,
  packet_version CHAR(64) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  case_id VARCHAR(80) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  revision INT UNSIGNED NOT NULL,
  decision ENUM('confirm','correct','reject') NOT NULL,
  annotation JSON NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (staff_user_id,packet_version,case_id,revision),
  CONSTRAINT fk_evaluation_reviewer FOREIGN KEY (staff_user_id) REFERENCES staff_users(id)
) ENGINE=InnoDB;

