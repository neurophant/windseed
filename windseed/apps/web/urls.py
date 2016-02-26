from windseed.apps.web import handlers


records = r'/'
sitemap = r'/sitemap/'

routes = [
    (records+'?', handlers.RecordsHandler),
    (sitemap+'?', handlers.SitemapHandler), ]
