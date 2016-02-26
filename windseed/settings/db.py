from playhouse.pool import PooledPostgresqlDatabase

from windseed.settings import env


pool = PooledPostgresqlDatabase(
    env.DBNAME,
    max_connections=env.MAX_CONNECTIONS,
    stale_timeout=env.STALE_TIMEOUT,
    user=env.USER,
    password=env.PASSWORD,
    host=env.HOST,
    port=env.PORT)
