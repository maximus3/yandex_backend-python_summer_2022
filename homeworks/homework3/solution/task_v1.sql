-- Укажите дополнительные индексы
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX IF NOT EXISTS idx_users_id ON users_user USING hash(UPPER(id::text));
CREATE INDEX IF NOT EXISTS idx_users_first_name ON users_user USING gin(UPPER(first_name) gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_users_last_name ON users_user USING gin(UPPER(last_name) gin_trgm_ops);