import tornado.gen
import tornado.ioloop

from windseed import settings, models


@tornado.gen.coroutine
def main():
    settings.db.pool.connect()

    user = models.User.create(
        active=True,
        superuser=True,
        email=settings.env.SUPERUSER_EMAIL,
        password=settings.env.SUPERUSER_PASSWORD)

    if not user:
        print(None)
        return

    print(user.uid, user.uts, user.active, user.superuser, user.email,
          user.check_password(password=settings.env.SUPERUSER_PASSWORD))

    if not settings.db.pool.is_closed():
        settings.db.pool.close()

    return


if __name__ == '__main__':
    ioloop = tornado.ioloop.IOLoop.instance().run_sync(main)
