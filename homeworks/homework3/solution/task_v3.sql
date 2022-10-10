-- Предложите решение с изменением структуры данных и запроса
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX IF NOT EXISTS idx_users_id           ON users_user    USING hash(UPPER(id::text));
CREATE INDEX IF NOT EXISTS idx_users_company_id   ON users_user    USING hash(company_id);
CREATE INDEX IF NOT EXISTS idx_users_job_id       ON users_user    USING hash(job_id);

CREATE INDEX IF NOT EXISTS idx_users_first_name   ON users_user    USING gin(UPPER(first_name) gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_users_last_name    ON users_user    USING gin(UPPER(last_name) gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_users_fio          ON users_user    USING gin(UPPER(last_name || ' ' || first_name || ' ' || second_name) gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_users_phone_number ON users_user    USING gin(UPPER(phone_number) gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_users_email        ON users_user    USING gin(UPPER(email) gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_company_title      ON users_company USING gin(UPPER(title) gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_job_title          ON users_job     USING gin(UPPER(title) gin_trgm_ops);

-- Изменение запроса

SELECT users_user.id,
       users_user.first_name,
       users_user.second_name,
       users_user.last_name,
       users_user.email,
       users_user.address,
       users_user.phone_number,
       users_user.company_id,
       users_user.job_id,
       (users_user.last_name || ' ' || users_user.first_name || ' ' || users_user.second_name) AS fio
FROM users_user
WHERE UPPER(users_user.id::text) = UPPER('Иванов') OR
      UPPER(users_user.last_name || ' ' || users_user.first_name || ' ' || users_user.second_name) LIKE UPPER('%Иванов%') OR
      UPPER(users_user.phone_number::text) LIKE UPPER('%Иванов%') OR
      UPPER(users_user.email::text) LIKE UPPER('%Иванов%') OR
      users_user.company_id = ANY ((
          SELECT ARRAY (
              SELECT id FROM users_company WHERE UPPER(users_company.title) LIKE UPPER('%Иванов%')
          )
      )::bigint[]) OR
      users_user.job_id = ANY ((
          SELECT ARRAY (
              SELECT id FROM users_job WHERE UPPER(users_job.title) LIKE UPPER('%Иванов%')
          )
      )::bigint[])
ORDER BY fio ASC;