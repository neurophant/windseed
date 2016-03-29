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

Testing with [wrk] (https://github.com/wg/wrk):

- 10 000, 100 000, 1 000 000 records in table
- 1 minute test with 1 minute timeout
- 1 and 10 threads
- From 10 to 100 connections with step of 10 connections
- Pagination using OFFSET and pagination using pagination table
- First and last page
- Sorted by name
- Compare Windseed and [Windseed-Django] (https://github.com/embali/windseed-django) 
apps with similar functionality

Start wrk
```
wrk -t1 -c10 -d1m --timeout 1m "http://localhost:8000/?page=1"
```

Start Windseed
```
bash bash/windseed.sh
```

Start Windseed-Django
```
uwsgi --module=djangotest.wsgi:application
      --env DJANGO_SETTINGS_MODULE=djangotest.settings
      --http=127.0.0.1:8000
      --processes 1
```

<br/><br/>
**100 000 records**

<br/>
Windseed

| | c10 | c20 | c30 | c40 | c50 | c60 | c70 | c80 | c90 | c100 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **t1, OFFSET, first page** | 12.64 ms | 12.84 ms | 12.51 ms | 12.35 ms | 12.54 ms | 12.49 ms | 12.53 ms | 12.45 ms | 12.79 ms | 12.90 ms |
| **t1, OFFSET, last page** | 340.91 ms | 348.84 ms | 379.75 ms | 400.00 ms | 447.76 ms | 483.87 ms | 495.87 ms | 545.45 ms | 588.24 ms | 600.00 ms |
| **t1, table, first page** | 33.78 ms | 13.59 ms | 13.87 ms | 13.82 ms | 13.69 ms | 14.00 ms | 13.73 ms | 14.08 ms | 14.11 ms | 13.99 ms |
| **t1, table, last page** | 14.55 ms | 14.34 ms | 14.11 ms | 14.87 ms | 14.19 ms | 15.03 ms | 15.80 ms | 14.49 ms | 15.67 ms | 15.97 ms |

<br/>
Windseed-Django

| | c10 | c20 | c30 | c40 | c50 | c60 | c70 | c80 | c90 | c100 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **t1, OFFSET, first page** | 33.92 ms | 33.67 ms | 33.50 ms | 32.95 ms | 34.05 ms | 33.90 ms | 33.78 ms | 33.94 ms | 34.05 ms | 35.84 ms |
| **t1, OFFSET, last page** | 402.68 ms | 392.16 ms | 416.67 ms | 441.18 ms | 480.00 ms | 508.47 ms | 555.56 ms | 618.56 ms | 740.74 ms | 800.00 ms |
| **t1, table, first page** | 60.98 ms | 23.93 ms | 24.86 ms | 24.84 ms | 23.97 ms | 24.92 ms | 24.58 ms | 25.06 ms | 26.64 ms | 24.74 ms |
| **t1, table, last page** | 25.02 ms | 23.73 ms | 24.35 ms | 24.59 ms | 24.59 ms | 24.93 ms | 25.13 ms | 24.39 ms | 24.36 ms | 24.52 ms |

<br/>
![t1, OFFSET, first page](/benchmarks/20160329064401.png?raw=true "t1, OFFSET, first page")
