# Windseed

Extendable skeleton for developing web applications using [Tornado]
(https://github.com/tornadoweb/tornado) and [peewee]
(https://github.com/coleifer/peewee)


## Prerequisites

- Ubuntu 14.10
- PostgreSQL 9.3
- Python 3.5+
- nginx
- Supervisor


## Structure

- **backups/** - folder for pg_dump to save dump using bash/backup.sh

- **bash/** - various bash scripts including project settings within environment
             variables:
  - **backup.sh** - create pg_dump in backups folder
  - **env.sh** - contains all environment variables for project
  - **superuser.sh** - create superuser
  - **supervisor.sh** - script for supervisor
  - **tables.sh** - drop database, crate database and create db tables
  - **tests.sh** - run tests
  - **windseed.sh** - run application

- **conf/** - config files for nginx/supervisor for dev and prod:
  - **dev-nginx.conf** - nginx config for development
  - **dev-supervisord.conf** - supervisor config for development (just to test
                           everything works)
  - **prod-nginx.conf** - nginx production config
  - **prod-supervisord.conf** - supervisor config for production

- **djangotest/** - similar project in Django to compare performance

- **static/** - project static files, mainly Bootstrap 3, robots.txt, admin styles

- **templates/** - project templates

- **windseed/** - windseed package:
  - **apps/** - project's applications folder, each app within its folder has:
    - **handlers.py** - app handlers
    - **models.py** - app models
    - **tests.py** - app tests
    - **urls.py** - app URLs and routes
  - **base/** - base classes:
    - **handler.py** - base handler class
    - **model.py** - base model class
    - **test.py** - base test class
  - **settings/** - project settings
    - **db.py** - postgresql database pool
    - **env.py** - environment variables from env.sh and paths
    - **urls.py** - project routes
  - **utils/** - project utilities:
    - **superuser.py** - create superuser
    - **tables.py** - create tables

- **windseed.py** - Windseed Tornado application


## Install Python 3.5+
```
sudo add-apt-repository ppa:fkrull/deadsnakes

sudo apt-get update

sudo apt-get install python3.5 python3.5-venv python3.5-dev
```

## Setup environment and packages

```
pyvenv-3.5 .env

source .env/bin/activate

pip install -r requirements.txt
```

## Generate cookie secret

```
openssl rand -base64 40
```
and put it to **env.sh**


## Run

```
bash scripts/tables.sh - create db and tables

bash scripts/superuser.sh - create superuser

bash scripts/tests.sh - run tests

bash scripts/windseed.sh - run project
```

## Nginx

```
sudo apt-get install nginx

sudo cp conf/prod-nginx.conf /etc/nginx/nginx.conf

sudo service nginx restart
```

## Ubuntu/nginx file limits

**/etc/security/limits.conf**:
```
soft nofile 16384

hard nofile 16384
```

**/etc/sysctl.conf**:
```
fs.file-max = 16384
```

**/etc/pam.d/common-session**:
```
session required pam_limits.so
```

## SSL certificate

```
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout windseed.key -out windseed.crt
```

## Supervisor

```
sudo apt-get install supervisor

pgrep -fl supervisor

sudo service supervisor start

sudo cp conf/supervisord.conf /etc/supervisor/supervisord.conf

sudo supervisord -c conf/supervisord.conf

sudo service supervisor restart

sudo unlink /tmp/supervisor.sock

kill related processes
```

## Performance

- Intel® Pentium(R) CPU 2117U @ 1.80GHz × 2
- 4 Gb RAM
- Ubuntu 14.10 x64

- Django 1.9.4
- uwsgi 2.0.12
- Tornado 4.2.1

Select 48 active records at 104 page of 105 pages total (10 000 records)

Testing with ab (Apache Benchmark) with various number of requests (n) and
concurrency level (c):
```
ab -n <n> -c <c> http://localhost:8000/?page=104
```

Django:
```
DEBUG=False

uwsgi --module=djangotest.wsgi:application --env DJANGO_SETTINGS_MODULE=djangotest.settings --http=127.0.0.1:8000 --master --processes <process number>
```

Tornado:
```
DEBUG=False

bash bash/windseed.sh
```

Time per request (mean)/Failed requests

Django + uWSGI (1 process)

| --- | --- | --- | --- |
| | n=100 | n=1000 | n=10000 |
| c=1 | 57ms/0 | 57ms/0 | 57ms/0 |
| c=100 | 58ms/0 | 57ms/0 | 57ms/0 |
| c=500 | - | 64ms/313 | 60ms/3623 |
