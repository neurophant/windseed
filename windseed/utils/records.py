import tornado.gen
import tornado.ioloop

from windseed.settings import db
from windseed.apps.web.models import Record


@tornado.gen.coroutine
def main():
    db.pool.connect()

    with db.pool.atomic():
        for i in range(10000):
            if i % 2 == 0:
                active = True
            else:
                active = False
            Record.create(active=active, name='record %d' % i,
                          description='description %d' % i)

    if not db.pool.is_closed():
        db.pool.close()

    return


if __name__ == '__main__':
    ioloop = tornado.ioloop.IOLoop.instance().run_sync(main)
