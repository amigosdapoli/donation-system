#! /bin/sh
	
psql -U admin -c "ALTER ROLE admin SET client_encoding TO 'utf8';"
psql -U admin -c "ALTER ROLE admin SET default_transaction_isolation TO 'read committed';"
psql -U admin -c "ALTER ROLE admin SET timezone TO 'UTC-3';"
psql -U admin -c "GRANT ALL PRIVILEGES ON DATABASE poscad TO admin;"
