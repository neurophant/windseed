"""This module contains base constants, that needed for windseed`s
functionality. In other words, its a project-wide settings.

It takes values from environment variables, so you must define them.
"""

from os import path, getenv

# Main

DEBUG = getenv('DEBUG', True)
AUTORELOAD = getenv('AUTORELOAD', True)

# Paths

BASE_PATH = path.join(path.dirname(__file__), '../../')
STATIC_PATH = path.join(BASE_PATH, 'static')
TEMPLATE_PATH = path.join(BASE_PATH, 'templates')

# Host & User

DOMAIN = getenv('WINDSEED_DOMAIN')
SUPERUSER_EMAIL = getenv('WINDSEED_SUPERUSER_EMAIL')
SUPERUSER_PASSWORD = getenv('WINDSEED_SUPERUSER_PASSWORD')

# Cookies

COOKIE_SECRET = getenv('WINDSEED_COOKIE_SECRET')  # secret key for secret cookie
XSRF_COOKIES = getenv('XSRF_COOKIES', True)

# DataBase

DBNAME = getenv('WINDSEED_DBNAME')
MAX_CONNECTIONS = int(getenv('WINDSEED_MAX_CONNECTIONS', 8))
STALE_TIMEOUT = int(getenv('WINDSEED_STALE_TIMEOUT', 30))
USER = getenv('WINDSEED_USER')
PASSWORD = getenv('WINDSEED_PASSWORD')
HOST = getenv('WINDSEED_HOST', 'localhost')
PORT = getenv('WINDSEED_PORT', 5432)

# Items per page

RELATED_ITEMS_PER_PAGE = int(getenv('WINDSEED_RELATED_ITEMS_PER_PAGE', 10))
ADMIN_ITEMS_PER_PAGE = int(getenv('WINDSEED_ADMIN_ITEMS_PER_PAGE', 10))

RECORDS_PER_PAGE = int(getenv('WINDSEED_RECORDS_PER_PAGE', 10))
SITEMAP_PER_PAGE = int(getenv('WINDSEED_SITEMAP_PER_PAGE', 10))
