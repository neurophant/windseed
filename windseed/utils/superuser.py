import tornado.gen
import tornado.ioloop

from windseed.settings import env, db
from windseed.apps.admin.models import User


@tornado.gen.coroutine
def main():
    db.pool.connect()

    user = User.create(
        active=True,
        superuser=True,
        email=env.SUPERUSER_EMAIL,
        password=env.SUPERUSER_PASSWORD)

    if not user:
        print(None)
        return

    print(user.uid, user.uts, user.active, user.superuser, user.email,
          user.check_password(password=env.SUPERUSER_PASSWORD))

    if not db.pool.is_closed():
        db.pool.close()

    return


if __name__ == '__main__':
    ioloop = tornado.ioloop.IOLoop.instance().run_sync(main)
