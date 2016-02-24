# Windseed

Extendable skeleton for developing web applications using [Tornado]
(https://github.com/tornadoweb/tornado) and [peewee]
(https://github.com/coleifer/peewee)


# Prerequisites

Ubuntu 14.10, PostgreSQL 9.3, Python 3.5+, nginx, Supervisor


# Structure

- backups/ - folder for pg_dump

- conf/ - config files for nginx/supervisor for dev and prod:
  - dev-nginx.conf - nginx config for development
  - dev-supervisord.conf - supervisor config for development (just to test
                           everything works)
  - prod-nginx.conf - nginx production config
  - prod-supervisord.conf - supervisor config for production

- scripts/ - various bash scripts including project settings within environment
             variables:
  - backup.sh - create pg_dump in backups folder
  - env.sh - contains all environment variables for project
  - superuser.sh - create superuser
  - supervisor.sh - script for supervisor
  - tables.sh - drop database, crate database and create db tables
  - tests.sh - run tests
  - windseed.sh - run application

- static/ - project static files, mainly Bootstrap 3, robots.txt, admin styles

- windseed/ - windseed module:
  - admin/ - admin application:
    - auth.py - auth decorators and login/logout handlers
    - dashboard.py - dashboard handler
    - handler.py - base admin handler derived from base handler
    - records.py - records list and CRUD handlers
  - base/ - base classes:
    - handler.py - base handler class
    - model.py - base model class
    - test.py - base test class
  - models/ - project models
    - record.py - record db model
    - user.py - user db model
  - settings/ - project settings
    - db.py - postgresql database pool
    - env.py - environment variables from env.sh and paths
    - urls.py - project urls
  - templates/ - project templates:
    - admin/ - admin application templates
    - web/ - web application templates
  - tests/ - tests:
    - models/ - tests for models
  - utils/ - utilities:
    - superuser.py - create superuser
    - tables.py - create tables
  - web/ - web application:
    - handler.py - base web handler derived from base handler
    - records.py - records list handler
    - sitemap.py - sitemap handler

- windseed.py - Windseed Tornado application


# Install Python 3.5+

sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get update
sudo apt-get install python3.5 python3.5-venv python3.5-dev


# Setup environment and packages

pyvenv-3.5 .env
source .env/bin/activate
pip install -r requirements.txt


# Generate cookie secret

openssl rand -base64 40
and put it to env.sh


# Run

bash scripts/tables.sh - create db and tables
bash scripts/superuser.sh - create superuser
bash scripts/tests.sh - run tests
bash scripts/windseed.sh - run project


# Nginx

sudo apt-get install nginx
sudo cp conf/prod-nginx.conf /etc/nginx/nginx.conf
sudo service nginx restart


# Nginx file limits

/etc/security/limits.conf:
  soft nofile 16384
  hard nofile 16384

/etc/sysctl.conf:
  fs.file-max = 16384

/etc/pam.d/common-session:
  session required pam_limits.so


# SSL certificate

sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout windseed.key -out windseed.crt


# Supervisor

sudo apt-get install supervisor
pgrep -fl supervisor
sudo service supervisor start
sudo cp conf/supervisord.conf /etc/supervisor/supervisord.conf
sudo supervisord -c conf/supervisord.conf
sudo service supervisor restart

sudo unlink /tmp/supervisor.sock
kill related processes
