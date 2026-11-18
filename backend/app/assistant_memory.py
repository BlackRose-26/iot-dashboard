"""Per-staff structured conversation memory; never stores message text or game facts."""
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from .database import execute, one


class MemoryStore:
    def __init__(self, engine, schema):
        self.engine, self.schema = engine, schema

    def load(self, staff_id):
        if self.engine is None: return self.schema(), 0, False
        try:
            with self.engine.connect() as connection:
                row = one(connection, 'SET STATEMENT max_statement_time=1 FOR SELECT revision,state_json FROM ai_admin_memory WHERE staff_user_id=:staff', staff=staff_id)
            if row is None: return self.schema(), 0, True
            if not isinstance(row['state_json'],str) or len(row['state_json']) > 16384:
                return self.schema(), 0, False
            return self.schema.model_validate_json(row['state_json']), row['revision'], True
        except (SQLAlchemyError, ValidationError, ValueError, TypeError):
            return self.schema(), 0, False

    def save(self, staff_id, state, revision):
        if self.engine is None: return False
        # Revalidate before writing; callers cannot add arbitrary messages/keys.
        safe = self.schema.model_validate(state.model_dump()).model_dump_json()
        try:
            with self.engine.begin() as connection:
                execute(connection, '''SET STATEMENT max_statement_time=1 FOR INSERT IGNORE INTO ai_admin_memory
                    (staff_user_id,state_json,revision) VALUES(:staff,:empty,0)''', staff=staff_id, empty=self.schema().model_dump_json())
                result = execute(connection, '''SET STATEMENT max_statement_time=1 FOR UPDATE ai_admin_memory
                    SET state_json=:state,revision=revision+1 WHERE staff_user_id=:staff AND revision=:revision''',
                    staff=staff_id, state=safe, revision=revision)
                return result.rowcount == 1
        except SQLAlchemyError:
            return False

    def forget(self, staff_id):
        # Keep only a revision tombstone, so an older in-flight reply cannot revive memory.
        with self.engine.begin() as connection:
            execute(connection, '''SET STATEMENT max_statement_time=1 FOR INSERT INTO ai_admin_memory
                (staff_user_id,state_json,revision) VALUES(:staff,:empty,1)
                ON DUPLICATE KEY UPDATE state_json=VALUES(state_json),revision=revision+1''',
                staff=staff_id, empty=self.schema().model_dump_json())
        return {'available': True, 'remembered': 0, 'preferences': {'language': None, 'detailed': None}, 'context': None}
