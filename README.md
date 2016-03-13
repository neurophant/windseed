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

- Tornado 4.2.1

- peewee 2.8.0

- Django 1.9.4

- uWSGI 2.0.12

Testing with ab (Apache Benchmark) with various number of requests (n),
concurrency level (c) and page (page):
```
ab -n <n> -c <c> -r http://localhost:8000/?page=<page>
```

Tornado:
```
DEBUG=False

bash bash/windseed.sh
```

Django:
```
DEBUG=False

uwsgi --module=djangotest.wsgi:application
      --env DJANGO_SETTINGS_MODULE=djangotest.settings
      --http=127.0.0.1:8000
      --processes <process number>
```

**Render page 1/105 (10 000 records total, 48 records per page)**

Tornado (1 process) - time per request (mean)

| | n=100 | n=1000 | n=2000 | n=5000 | n=10000 |
| --- | --- | --- | --- | --- | --- |
| **c=1** | 9 ms | 8 ms | 9 ms | 9 ms | 9 ms |
| **c=50** | 8 ms | 8 ms | 9 ms | 8 ms | 9 ms |
| **c=100** | 8 ms | 9 ms | 8 ms | 9 ms | 9 ms |
| **c=200** | - | 14 ms | 14 ms | 11 ms | 11 ms |
| **c=300** | - | 14 ms | 10 ms | 12 ms | 11 ms |
| **c=500** | - | 15 ms | 14 ms | 12 ms | 14 ms |

Tornado (1 process) - failed requests

| | n=100 | n=1000 | n=2000 | n=5000 | n=10000 |
| --- | --- | --- | --- | --- | --- |
| **c=1** | 0 | 0 | 0 | 0 | 0 |
| **c=50** | 0 | 0 | 0 | 0 | 0 |
| **c=100** | 0 | 0 | 0 | 0 | 0 |
| **c=200** | - | 0 | 0 | 0 | 43 |
| **c=300** | - | 0 | 12 | 26 | 114 |
| **c=500** | - | 0 | 126 | 343 | 424 |

Django + uWSGI (1 process) - time per request (mean)

| | n=100 | n=1000 | n=2000 | n=5000 | n=10000 |
| --- | --- | --- | --- | --- | --- |
| **c=1** | 25 ms | 25 ms | 24 ms | 23 ms | 24 ms |
| **c=50** | 24 ms | 23 ms | 23 ms | 25 ms | 23 ms |
| **c=100** | 23 ms | 24 ms | 24 ms | 23 ms | 23 ms |
| **c=200** | - | 35 ms | 43 ms | 41 ms | 56 ms |
| **c=300** | - | 91 ms | 34 ms | 47 ms | 40 ms |
| **c=500** | - | 56 ms | 31 ms | 38 ms | 32 ms |

Django + uWSGI (1 process) - failed requests

| | n=100 | n=1000 | n=2000 | n=5000 | n=10000 |
| --- | --- | --- | --- | --- | --- |
| **c=1** | 0 | 0 | 0 | 0 | 0 |
| **c=50** | 0 | 0 | 0 | 0 | 0 |
| **c=100** | 0 | 0 | 0 | 0 | 0 |
| **c=200** | - | 2 | 120 | 260 | 775 |
| **c=300** | - | 94 | 197 | 662 | 1209 |
| **c=500** | - | 65 | 312 | 869 | 2015 |

<br/>
**Render page 104/105 (10 000 records total, 48 records per page)**

Tornado (1 process) - time per request (mean)

| | n=100 | n=1000 | n=2000 | n=5000 | n=10000 |
| --- | --- | --- | --- | --- | --- |
| **c=1** | 42 ms | 42 ms | 42 ms | 42 ms | 42 ms |
| **c=50** | 43 ms | 42 ms | 42 ms | 42 ms | 42 ms |
| **c=100** | 43 ms | 42 ms | 42 ms | 42 ms | 42 ms |
| **c=200** | - | 66 ms | 53 ms | 41 ms | 41 ms |
| **c=300** | - | 58 ms | 54 ms | 46 ms | 40 ms |
| **c=500** | - | 54 ms | 52 ms | 41 ms | 37 ms |

Tornado (1 process) - failed requests

| | n=100 | n=1000 | n=2000 | n=5000 | n=10000 |
| --- | --- | --- | --- | --- | --- |
| **c=1** | 0 | 0 | 0 | 0 | 0 |
| **c=50** | 0 | 0 | 0 | 0 | 0 |
| **c=100** | 0 | 0 | 0 | 0 | 0 |
| **c=200** | - | 0 | 38 | 90 | 139 |
| **c=300** | - | 26 | 151 | 242 | 388 |
| **c=500** | - | 149 | 527 | 882 | 1233 |

Django + uWSGI (1 process) - time per request (mean)

| | n=100 | n=1000 | n=2000 | n=5000 | n=10000 |
| --- | --- | --- | --- | --- | --- |
| **c=1** | 58 ms | 57 ms | 57 ms | 57 ms | 56 ms |
| **c=50** | 58 ms | 57 ms | 57 ms | 57 ms | 57 ms |
| **c=100** | 58 ms | 57 ms | 57 ms | 57 ms | 57 ms |
| **c=200** | - | 130 ms | 94 ms | 117 ms | 131 ms |
| **c=300** | - | 83 ms | 67 ms | 95 ms | 80 ms |
| **c=500** | - | 68 ms | 76 ms | 62 ms | 55 ms |

Django + uWSGI (1 process) - failed requests

| | n=100 | n=1000 | n=2000 | n=5000 | n=10000 |
| --- | --- | --- | --- | --- | --- |
| **c=1** | 0 | 0 | 0 | 0 | 0 |
| **c=50** | 0 | 0 | 0 | 0 | 0 |
| **c=100** | 0 | 0 | 0 | 0 | 0 |
| **c=200** | - | 108 | 255 | 728 | 1745 |
| **c=300** | - | 172 | 348 | 1372 | 2362 |
| **c=500** | - | 304 | 672 | 1788 | 3284 |
