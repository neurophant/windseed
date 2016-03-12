import tornado.web

from windseed.settings import db


class Handler(tornado.web.RequestHandler):
    """
    Base request handler
    """
    def prepare(self):
        """
        Prepare db connection pool
        """
        db.pool.connect()

        return super().prepare()

    def on_finish(self):
        """
        Close db connection pool
        """
        if not db.pool.is_closed():
            db.pool.close()

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
