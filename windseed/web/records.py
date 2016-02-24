import peewee

import tornado.web
import tornado.gen
import tornado.escape

from windseed import settings, models, web


class RecordsHandler(web.Handler):
    """
    Records: /
    """
    def get_page_context(self):
        """
        Return current page context
        """
        try:
            page = int(self.get_argument('page', 1))
        except ValueError:
            page = 1

        try:
            count = models.Record\
                .select()\
                .where(models.Record.active == True)\
                .count()
        except peewee.IntegrityError:
            count = 0

        per_page = settings.env.RECORDS_PER_PAGE
        page_count = int(count/per_page) + int(bool(count % per_page))

        prev_page, page, next_page = self.paging(page, page_count)

        try:
            records = models.Record\
                .select()\
                .where(models.Record.active == True)\
                .order_by(models.Record.name.asc())\
                .paginate(
                    page,
                    paginate_by=per_page)
        except peewee.IntegrityError:
            records = []

        return dict(records=records,
                    page_count=page_count,
                    prev_page=prev_page,
                    page=page,
                    next_page=next_page)

    @tornado.web.addslash
    @tornado.gen.coroutine
    def get(self):
        """
        Render records
        """
        self.render(
            'web/records.html',
            **self.get_page_context())
