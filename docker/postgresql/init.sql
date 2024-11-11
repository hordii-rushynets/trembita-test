DO
$do$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'trembita') THEN
      CREATE DATABASE trembita;
   END IF;
END
$do$;

DO
$do$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'trembita') THEN
      CREATE USER trembita WITH PASSWORD 'qwerty123';
      GRANT ALL PRIVILEGES ON DATABASE trembita TO trembita;
      ALTER USER trembita CREATEDB;
   END IF;
END
$do$;
