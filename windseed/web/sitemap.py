import peewee

import tornado.web
import tornado.gen
import tornado.escape

from windseed import settings, models, web


class SitemapHandler(web.Handler):
    """
    Sitemap: /sitemap/
    """
    def get_page_context(self):
        """
        Return current page context
        """
        try:
            records = models.Record\
                .select()\
                .where(models.Record.active == True)\
                .paginate(1, paginate_by=settings.env.SITEMAP_PER_PAGE)
        except peewee.IntegrityError:
            records = []

        return dict(records=records)

    @tornado.gen.coroutine
    def get(self):
        """
        Render sitemap
        """
        self.set_header('Content-Type', 'text/xml')
        self.render(
            'web/sitemap.xml',
            **self.get_page_context())
