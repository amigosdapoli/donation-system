# donation-system (name yet to be defined)

[![Latest Release](https://img.shields.io/github/release/amigosdapoli/donation-system.svg?label=latest%20release)](https://github.com/amigosdapoli/donation-system/releases)
[![travis-ci](https://travis-ci.org/amigosdapoli/donation-system.svg?branch=master)](https://travis-ci.org/amigosdapoli/donation-system)
[![Maintainability](https://api.codeclimate.com/v1/badges/2726dc794a5d74e9572c/maintainability)](https://codeclimate.com/github/amigosdapoli/donation-system/maintainability)

Donation system is an open source project to help non profit organizations to easily collect and manage one-off and recurring donations via credit card, invoice or other payment methods. The project is being developed to help Amigos da Poli with the challenge making donations interface user friendly and easier to manage. 

Here is how the system will initially work: one page where donors can fill in information and register a one-off or a recurring donation and an admin page where the non profit fundraising responsible is able to easily consolidate all donation to the organization. 

The goal of this project is to help other endowment funds and non profits in general to have an effective and low cost donation system. As an open source project, we expect it can also help other non profit organizations to leverage financial resources and increase its impact in society. 

<p align="center">
  <img align="center" src="https://github.com/amigosdapoli/donation-system/raw/master/docs/img/donation_page.png" width="600">
</p>

# Installation

## Start
```bash
# Clone repo
git clone https://github.com/amigosdapoli/donation-system.git
cd donation-system/

# Install requirements 
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```
## If in Debian/Ubuntu
```
# Install Postgres
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib 

# Set up database
bash scripts/etup_database_linux.sh
```

## If in Mac
```
# Install Postgres
brew update
brew install postgresql

# Start the postgres service
pg_ctl -D /usr/local/var/postgres start && brew services start postgresql

# Set up database
psql postgres
=>CREATE DATABASE poscad;
=>CREATE USER admin WITH PASSWORD 'admin' ;
=>ALTER ROLE admin SET client_encoding TO 'utf8';
=>ALTER ROLE admin SET default_transaction_isolation TO 'read committed';
=>ALTER ROLE admin SET timezone TO 'UTC-3';
=>GRANT ALL PRIVILEGES ON DATABASE poscad TO admin;
```

## Continue
```
# Run start database
python manage.py makemigrations
python manage.py migrate

#Run application
python manage.py runserver

```
TODO using docker? Vagrant?

# Payment Gateways
Payment gateways will follow a pattern so we can add different services if needed.

## Available gateways
* MaxiPago
TODO List different payment methods
## Creating new gateways

## Configuring payment gateway
Set the following environment variables
```
GATEWAY_SANDBOX=<boolean>
MERCHANT_ID=<id>
MERCHANT_KEY=<key>
```

# Contributing

To contribute:
1. Fork it
2. Create your feature branch ('git checkout -b <feature name>')
3. Commit your changes ('git commit -am 'Add some feature')
4. Push to the branch ('git push origin my-new-feature')
5. Create a new Pull request

# License
