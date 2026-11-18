-- Only schema-validated topic/filter/preferences, never raw messages or player facts.
CREATE TABLE IF NOT EXISTS ai_admin_memory (
  staff_user_id BIGINT UNSIGNED NOT NULL PRIMARY KEY,
  state_json JSON NOT NULL,
  revision BIGINT UNSIGNED NOT NULL DEFAULT 0,
  updated_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  CONSTRAINT fk_ai_memory_staff FOREIGN KEY (staff_user_id) REFERENCES staff_users(id)
) ENGINE=InnoDB;
