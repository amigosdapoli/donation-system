#! /bin/sh
	
psql -Uadmin -c "CREATE DATABASE poscad;"
psql -Uadmin -c "CREATE USER admin WITH PASSWORD 'admin' ;"
psql -Uadmin -c "ALTER ROLE admin SET client_encoding TO 'utf8';"
psql -Uadmin -c "ALTER ROLE admin SET default_transaction_isolation TO 'read committed';"
psql -Uadmin -c "ALTER ROLE admin SET timezone TO 'UTC-3';"
psql -Uadmin -c "GRANT ALL PRIVILEGES ON DATABASE poscad TO admin;"
psql -Uadmin -c "ALTER USER admin CREATEDB;"
