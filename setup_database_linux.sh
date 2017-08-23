#! /bin/sh
	
sudo -u postgres psql -c "CREATE DATABASE poscad;"
sudo -u postgres psql -c "CREATE USER admin WITH PASSWORD 'admin' ;"
sudo -u postgres psql -c "ALTER ROLE admin SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE admin SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE admin SET timezone TO 'UTC-3';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE poscad TO admin;"