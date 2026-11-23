-- Preserve classic results. Only subsequent assignments use matrix-v1.
INSERT IGNORE INTO rulesets(code,version,config,config_hash,created_by)
SELECT 'matrix-v1',1,'{"base_step_ms":60,"code":"matrix-v1","columns":16,"foundation_x":5,"initial_width":6,"levels":15,"minimum_step_ms":50,"perfect_bonus":0,"round_limit_ms":60000,"row_points":1,"step_decrease_ms":10}',
UNHEX('f73ce2ee4d1f607b6ea97038a534c7521a9305ee9ada3e2d418029cf866a58a4'),id FROM staff_users ORDER BY id LIMIT 1;

UPDATE events SET settings=JSON_SET(settings,'$.active_ruleset','matrix-v1'),revision=revision+1 WHERE code='acs-day';
