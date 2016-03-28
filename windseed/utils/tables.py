import tornado.gen
import tornado.ioloop

from windseed.settings import db
from windseed.apps.admin.models import User
from windseed.apps.web.models import Record, RecordPage


@tornado.gen.coroutine
def main():
    tables = [
        User,
        Record,
        RecordPage, ]

    db.pool.connect()

    db.pool.drop_tables(tables, safe=True, cascade=True)
    db.pool.create_tables(tables, safe=True)

    if not db.pool.is_closed():
        db.pool.close()

    return


if __name__ == '__main__':
    ioloop = tornado.ioloop.IOLoop.instance().run_sync(main)
