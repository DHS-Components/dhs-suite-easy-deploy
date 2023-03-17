#!/bin/bash
#set -e
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        CREATE USER db_user WITH ENCRYPTED PASSWORD 'password';
        CREATE DATABASE keycloak;
        GRANT ALL PRIVILEGES ON DATABASE keycloak TO db_user;
        ALTER DATABASE keycloak OWNER TO db_user;
EOSQL
