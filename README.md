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

Hardware:

- Intel® Core™ i7-5500U CPU @ 2.40GHz × 4
- 16 Gb RAM

Testing with [wrk] (https://github.com/wg/wrk):

- 10 000, 100 000, 1 000 000 records in table
- 1 minute test with 1 minute timeout
- 1 and 10 threads
- From 10 to 100 connections with step of 10 connections
- Pagination using SQL OFFSET and pagination using pagination table
- First and last page
- Sorted by name
- Compare Windseed and [Django] (https://github.com/embali/windseed-django) 
apps with similar functionality

Start wrk
```
wrk -t1 -c10 -d1m --timeout 1m "http://localhost:8000/?page=1"
```

Start Windseed
```
bash bash/windseed.sh
```

Start Django
```
uwsgi --module=djangotest.wsgi:application
      --env DJANGO_SETTINGS_MODULE=djangotest.settings
      --http=127.0.0.1:8000
      --processes 1
```

<br/><br/>
**10 000 records**

<br/>
Windseed

| | c10 | c20 | c30 | c40 | c50 | c60 | c70 | c80 | c90 | c100 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **t1, offset, first** | 4.35 | 4.21 | 4.26 | 4.15 | 4.29 | 4.36 | 4.38 | 4.18 | 4.49 | 4.38 |
| **t1, offset, last** | 21.17 | 20.40 | 21.15 | 21.17 | 21.25 | 20.54 | 20.48 | 21.03 | 21.37 | 21.22 |
| **t1, table, first** | 7.47 | 6.78 | 6.94 | 6.82 | 7.13 | 7.34 | 7.28 | 7.39 | 7.11 | 7.02 |
| **t1, table, last** | 6.97 | 6.75 | 6.91 | 6.64 | 6.59 | 7.10 | 7.22 | 7.08 | 7.02 | 7.07 |
| **t10, offset, first** | 4.44 | 4.07 | 3.99 | 4.19 | 4.10 | 4.05 | 4.28 | 4.27 | 4.26 | 3.95 |
| **t10, offset, last** | 20.17 | 19.97 | 20.01 | 20.23 | 20.55 | 20.77 | 20.74 | 20.45 | 20.55 | 20.94 |
| **t10, table, first** | 6.84 | 6.39 | 7.09 | 7.27 | 7.12 | 7.18 | 7.24 | 7.35 | 7.27 | 7.60 |
| **t10, table, last** | 7.51 | 7.04 | 7.24 | 7.40 | 7.34 | 7.31 | 7.17 | 7.60 | 7.73 | 7.73 |

<br/>
Django

| | c10 | c20 | c30 | c40 | c50 | c60 | c70 | c80 | c90 | c100 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **t1, offset, first** | 17.80 | 17.38 | 18.01 | 18.10 | 18.18 | 18.03 | 18.33 | 18.80 | 17.96 | 18.11 |
| **t1, offset, last** | 37.15 | 36.36 | 36.32 | 36.52 | 37.31 | 37.62 | 37.55 | 37.66 | 38.24 | 38.46 |
| **t1, table, first** | 18.36 | 17.16 | 17.26 | 17.62 | 17.30 | 17.25 | 17.40 | 17.41 | 17.27 | 17.46 |
| **t1, table, last** | 17.64 | 17.01 | 17.04 | 17.21 | 17.31 | 17.35 | 17.31 | 17.07 | 16.27 | 15.81 |
| **t10, offset, first** | 16.49 | 16.47 | 15.96 | 16.23 | 16.11 | 16.10 | 16.44 | 16.23 | 16.34 | 16.69 |
| **t10, offset, last** | 33.44 | 32.70 | 32.91 | 33.58 | 33.73 | 33.61 | 33.52 | 33.98 | 33.98 | 34.29 |
| **t10, table, first** | 16.04 | 15.16 | 15.89 | 15.43 | 15.58 | 15.77 | 16.03 | 18.46 | 18.46 | 18.52 |
| **t10, table, last** | 18.54 | 18.29 | 18.30 | 15.43 | 16.89 | 17.40 | 17.52 | 17.49 | 17.79 | 17.65 |

<br/>
![1 thread, offset pagination, first page](/charts/104/20160330115515.png?raw=true "1 thread, offset pagination, first page")

<br/>
![1 thread, offset pagination, last page](/charts/104/20160330120051.png?raw=true "1 thread, offset pagination, last page")

<br/>
![1 thread, table pagination, first page](/charts/104/20160330120639.png?raw=true "1 thread, table pagination, first page")

<br/>
![1 thread, table pagination, last page](/charts/104/20160330121024.png?raw=true "1 thread, table pagination, last page")

<br/>
![10 threads, offset pagination, first page](/charts/104/20160330124517.png?raw=true "10 threads, offset pagination, first page")

<br/>
![10 threads, offset pagination, last page](/charts/104/20160330124836.png?raw=true "10 threads, offset pagination, last page")

<br/>
![10 threads, table pagination, first page](/charts/104/20160330125228.png?raw=true "10 threads, table pagination, first page")

<br/>
![10 threads, table pagination, last page](/charts/104/20160330125539.png?raw=true "10 threads, table pagination, last page")

<br/><br/>
**100 000 records**

<br/>
Windseed

| | c10 | c20 | c30 | c40 | c50 | c60 | c70 | c80 | c90 | c100 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **t1, offset, first** | 12.64  | 12.84  | 12.51  | 12.35  | 12.54  | 12.49  | 12.53  | 12.45  | 12.79  | 12.90  |
| **t1, offset, last** | 340.91  | 348.84  | 379.75  | 400.00  | 447.76  | 483.87  | 495.87  | 545.45  | 588.24  | 600.00  |
| **t1, table, first** | 33.78  | 13.59  | 13.87  | 13.82  | 13.69  | 14.00  | 13.73  | 14.08  | 14.11  | 13.99  |
| **t1, table, last** | 14.55  | 14.34  | 14.11  | 14.87  | 14.19  | 15.03  | 15.80  | 14.49  | 15.67  | 15.97  |
| **t10, offset, first** | 12.47 | 12.60 | 12.56 | 12.76 | 12.76 | 12.67 | 12.64 | 12.47 | 12.61 | 14.21 |
| **t10, offset, last** | 355.03 | 365.85 | 387.10 | 413.79 | 483.87 | 512.82 | 560.75 | 606.06 | 666.67 | 833.33 |
| **t10, table, first** | 36.56 | 14.10 | 14.32 | 14.49 | 14.40 | 15.54 | 14.34 | 14.45 | 14.26 | 14.69 |
| **t10, table, last** | 14.97 | 14.23 | 14.26 | 14.29 | 14.30 | 14.31 | 14.45 | 14.65 | 14.50 | 14.12 |

<br/>
Django

| | c10 | c20 | c30 | c40 | c50 | c60 | c70 | c80 | c90 | c100 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **t1, offset, first** | 33.92  | 33.67  | 33.50  | 32.95  | 34.05  | 33.90  | 33.78  | 33.94  | 34.05  | 35.84  |
| **t1, offset, last** | 402.68  | 392.16  | 416.67  | 441.18  | 480.00  | 508.47  | 555.56  | 618.56  | 740.74  | 800.00  |
| **t1, table, first** | 60.98  | 23.93  | 24.86  | 24.84  | 23.97  | 24.92  | 24.58  | 25.06  | 26.64  | 24.74  |
| **t1, table, last** | 25.02  | 23.73  | 24.35  | 24.59  | 24.59  | 24.93  | 25.13  | 24.39  | 24.36  | 24.52  |
| **t10, offset, first** | 32.75 | 32.35 | 33.15 | 31.90 | 32.12 | 32.38 | 32.52 | 32.59 | 32.86 | 33.99 |
| **t10, offset, last** | 372.67 | 372.67 | 394.74 | 428.57 | 458.02 | 491.80 | 540.54 | 600.00 | 689.66 | 810.81 |
| **t10, table, first** | 55.05 | 23.10 | 23.32 | 23.36 | 23.45 | 23.56 | 23.68 | 23.81 | 23.83 | 24.09 |
| **t10, table, last** | 24.10 | 23.32 | 23.42 | 23.95 | 25.21 | 25.17 | 24.42 | 24.69 | 24.27 | 24.40 |

<br/>
![1 thread, offset pagination, first page](/charts/105/20160330033437.png?raw=true "1 thread, offset pagination, first page")

<br/>
![1 thread, offset pagination, last page](/charts/105/20160330034042.png?raw=true "1 thread, offset pagination, last page")

<br/>
![1 thread, table pagination, first page](/charts/105/20160330040018.png?raw=true "1 thread, table pagination, first page")

<br/>
![1 thread, table pagination, last page](/charts/105/20160330040436.png?raw=true "1 thread, table pagination, last page")

<br/>
![10 threads, offset pagination, first page](/charts/105/20160330040722.png?raw=true "10 threads, offset pagination, first page")

<br/>
![10 threads, offset pagination, last page](/charts/105/20160330041002.png?raw=true "10 threads, offset pagination, last page")

<br/>
![10 threads, table pagination, first page](/charts/105/20160330041221.png?raw=true "10 threads, table pagination, first page")

<br/>
![10 threads, table pagination, last page](/charts/105/20160330041456.png?raw=true "10 threads, table pagination, last page")

<br/><br/>
**1 000 000 records**

<br/>
Windseed

| | c10 | c20 | c30 | c40 | c50 | c60 | c70 | c80 | c90 | c100 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **t1, offset, first** | 95.69 | 94.15 | 98.36 | 107.33 | 110.50 | 119.52 | 115.61 | 126.05 | 123.46 | 126.85 |
| **t1, offset, last** | 405.41 | 348.84 | 357.14 | 375.00 | 465.12 | 413.79 | 483.87 | 545.45 | 526.32 | 600.00 |
| **t1, table, first** | 212.01 | 102.21 | 109.29 | 106.95 | 109.49 | 105.63 | 108.89 | 110.91 | 113.21 | 115.38 |
| **t1, table, last** | 116.73 | 100.50 | 101.52 | 103.63 | 105.45 | 106.95 | 108.11 | 110.50 | 113.64 | 115.38 |
| **t10, offset, first** | 102.04 | 107.53 | 102.39 | 102.92 | 106.19 | 107.72 | 110.29 | 110.29 | 114.50 | 119.28 |
| **t10, offset, last** | 408.16 | 320.86 | 340.91 | 357.14 | 382.17 | 410.96 | 476.19 | 521.74 | 555.56 | 582.52 |
| **t10, table, first** | 214.29 | 105.45 | 110.29 | 101.18 | 102.39 | 106.01 | 106.19 | 107.72 | 109.69 | 113.21 |
| **t10, table, last** | 114.72 | 99.01 | 98.85 | 101.35 | 103.99 | 103.45 | 106.38 | 111.11 | 112.36 | 128.76 |

<br/>
Django

| | c10 | c20 | c30 | c40 | c50 | c60 | c70 | c80 | c90 | c100 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **t1, offset, first** | 199.34 | 208.33 | 212.01 | 219.78 | 223.05 | 236.22 | 250.00 | 255.32 | 263.16 | 276.50 |
| **t1, offset, last** | 606.06 | 437.96 | 476.19 | 512.82 | 560.75 | 606.06 | 689.66 | 800.00 | 882.35 | 1071.43 |
| **t1, table, first** | 314.14 | 108.11 | 111.11 | 114.72 | 120.00 | 119.52 | 121.95 | 124.22 | 127.93 | 129.87 |
| **t1, table, last** | 132.45 | 109.09 | 111.32 | 112.57 | 116.96 | 119.05 | 123.46 | 131.29 | 132.16 | 131.00 |
| **t10, offset, first** | 198.02 | 204.78 | 212.01 | 219.78 | 230.77 | 243.90 | 247.93 | 262.01 | 271.49 | 289.86 |
| **t10, offset, last** | 625.00 | 422.54 | 458.02 | 495.87 | 535.71 | 588.24 | 659.34 | 750.00 | 857.14 | 983.61 |
| **t10, table, first** | 310.88 | 111.94 | 110.29 | 114.29 | 124.74 | 123.20 | 123.20 | 126.05 | 123.46 | 127.66 |
| **t10, table, last** | 137.30 | 117.19 | 117.19 | 116.96 | 123.46 | 126.85 | 126.05 | 131.00 | 131.00 | 131.00 |

<br/>
![1 thread, offset pagination, first page](/charts/106/.png?raw=true "1 thread, offset pagination, first page")

<br/>
![1 thread, offset pagination, last page](/charts/106/.png?raw=true "1 thread, offset pagination, last page")

<br/>
![1 thread, table pagination, first page](/charts/106/.png?raw=true "1 thread, table pagination, first page")

<br/>
![1 thread, table pagination, last page](/charts/106/.png?raw=true "1 thread, table pagination, last page")

<br/>
![10 threads, offset pagination, first page](/charts/106/.png?raw=true "10 threads, offset pagination, first page")

<br/>
![10 threads, offset pagination, last page](/charts/106/.png?raw=true "10 threads, offset pagination, last page")

<br/>
![10 threads, table pagination, first page](/charts/106/.png?raw=true "10 threads, table pagination, first page")

<br/>
![10 threads, table pagination, last page](/charts/106/.png?raw=true "10 threads, table pagination, last page")
