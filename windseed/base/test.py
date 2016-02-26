import tornado.testing

from windseed.settings import db


class Test(tornado.testing.AsyncTestCase):
    """
    Common test case
    """
    def setUp(self):
        """
        Prepare db connection pool
        """
        db.pool.connect()

        super().setUp()

    def tearDown(self):
        """
        Close db connection pool
        """
        if not db.pool.is_closed():
            db.pool.close()

        super().tearDown()
