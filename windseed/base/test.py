import tornado.testing

from windseed import settings


class Test(tornado.testing.AsyncTestCase):
    """
    Common test case
    """
    def setUp(self):
        """
        Prepare db connection pool
        """
        settings.db.pool.connect()

        super().setUp()

    def tearDown(self):
        """
        Close db connection pool
        """
        if not settings.db.pool.is_closed():
            settings.db.pool.close()

        super().tearDown()
