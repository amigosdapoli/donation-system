# donation-system (name yet to be defined)

[![Latest Release](https://img.shields.io/github/release/amigosdapoli/donation-system.svg?label=latest%20release)](https://github.com/amigosdapoli/donation-system/releases)
[![Travis-CI](https://travis-ci.org/amigosdapoli/donation-system.svg?branch=master)](https://travis-ci.org/amigosdapoli/donation-system)
[![Maintainability](https://api.codeclimate.com/v1/badges/2726dc794a5d74e9572c/maintainability)](https://codeclimate.com/github/amigosdapoli/donation-system/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/2726dc794a5d74e9572c/test_coverage)](https://codeclimate.com/github/amigosdapoli/donation-system/test_coverage)

Donation system is an open source project to help non profit organizations to easily collect and manage one-off and recurring donations via credit card, invoice or other payment methods. The project is being developed to help Amigos da Poli with the challenge making donations interface user friendly and easier to manage. 

Here is how the system will initially work: one page where donors can fill in information and register a one-off or a recurring donation and an admin page where the non profit fundraising responsible is able to easily consolidate all donation to the organization. 

The goal of this project is to help other endowment funds and non profits in general to have an effective and low cost donation system. As an open source project, we expect it can also help other non profit organizations to leverage financial resources and increase its impact in society. 

<p align="center">
  <img align="center" src="https://github.com/amigosdapoli/donation-system/raw/master/docs/img/donation_page.png" width="600">
</p>

# Installation

## Requirements

<<<<<<< HEAD
### If in Debian/Ubuntu
```
# Install Postgres
sudo apt-get update
sudo apt-get install python-dev libxml2-dev libxslt1-dev build-essential libssl-dev libffi-dev zlib1g-dev
sudo apt-get install postgresql postgresql-contrib 
sudo apt-get install python-pip

# Set up database
bash scripts/setup_database_linux.sh
```
=======
# Docker and docker compose
Install docker following the instructions for your plataform: https://docs.docker.com/install/
Don't forget the extra steps, so you don't have to root all you commands: https://docs.docker.com/install/linux/linux-postinstall/#manage-docker-as-a-non-root-user
Also, install docker compose: https://docs.docker.com/compose/install/
>>>>>>> 1921843... development: add docker image for faster start

Now, configure you stuff in the env file (`.env`)
```
GATEWAY_SANDBOX=<boolean>
MERCHANT_ID=<id>
MERCHANT_KEY=<key>
```

If you have to, you may also change some option for the postgres service: https://hub.docker.com/_/postgres/

Now, run:
```
docker-compose up -d
```
The first time, since the image isn't in the docker hub, it'll take some time.
The server will the be accessible in the URL `localhost:8000`

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
