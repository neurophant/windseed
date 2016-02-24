import tornado.gen
import tornado.ioloop

from windseed import settings, models


@tornado.gen.coroutine
def main():
    tables = [
        models.User,
        models.Record, ]

    settings.db.pool.connect()

    settings.db.pool.drop_tables(tables, safe=True, cascade=True)
    settings.db.pool.create_tables(tables, safe=True)

    if not settings.db.pool.is_closed():
        settings.db.pool.close()

    return


if __name__ == '__main__':
    ioloop = tornado.ioloop.IOLoop.instance().run_sync(main)
