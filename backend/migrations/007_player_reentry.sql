-- Operator-issued, one-time re-entry tokens (24 Nov 2026). They restore a player's own
-- ticket session after a lost phone, cleared browser or a new tunnel hostname (player
-- cookies are tied to the old hostname). Stored hashed, single use, short-lived, audited.
CREATE TABLE IF NOT EXISTS player_reentry_tokens (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  token_hash BINARY(32) NOT NULL UNIQUE,
  player_id BIGINT UNSIGNED NOT NULL,
  issued_by BIGINT UNSIGNED NOT NULL,
  expires_at DATETIME(3) NOT NULL,
  used_at DATETIME(3) NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  KEY ix_reentry_player (player_id),
  CONSTRAINT fk_reentry_player FOREIGN KEY (player_id) REFERENCES players(id),
  CONSTRAINT fk_reentry_staff FOREIGN KEY (issued_by) REFERENCES staff_users(id)
) ENGINE=InnoDB;
