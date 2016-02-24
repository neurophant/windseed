import tornado.web

from windseed import settings


class Handler(tornado.web.RequestHandler):
    """
    Base request handler
    """
    @property
    def user(self):
        """
        Current user property
        """
        return self.get_current_user()

    def get_current_user(self):
        """
        Current user
        """
        user_cookie = self.get_secure_cookie('user')

        if user_cookie:
            return user_cookie

        return None

    def prepare(self):
        """
        Prepare db connection pool
        """
        settings.db.pool.connect()

        return super().prepare()

    def on_finish(self):
        """
        Close db connection pool
        """
        if not settings.db.pool.is_closed():
            settings.db.pool.close()

        return super().on_finish()

    def paging(self, page, page_count):
        """
        Return paging options
        """
        if page > page_count:
            page = page_count

        if page < 1:
            page = 1

        if page > 1:
            prev_page = page - 1
        else:
            prev_page = None

        if page < page_count:
            next_page = page + 1
        else:
            next_page = None

        return prev_page, page, next_page
