from playhouse.pool import PooledPostgresqlDatabase

from windseed import settings


pool = PooledPostgresqlDatabase(
    settings.env.DBNAME,
    max_connections=settings.env.MAX_CONNECTIONS,
    stale_timeout=settings.env.STALE_TIMEOUT,
    user=settings.env.USER,
    password=settings.env.PASSWORD,
    host=settings.env.HOST,
    port=settings.env.PORT)
