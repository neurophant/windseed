import tornado.gen
import tornado.web
import tornado.ioloop
import tornado.httpserver

from windseed import settings, admin, web


class Windseed(tornado.web.Application):
    """
    Our main application
    """
    def __init__(self):
        handlers = [
            (settings.urls.admin_login+'?', admin.LoginHandler),
            (settings.urls.admin_logout+'?', admin.LogoutHandler),
            (settings.urls.admin_dashboard+'?', admin.DashboardHandler),
            (settings.urls.admin_records+'?', admin.RecordsHandler),
            (settings.urls.web_records+'?', web.RecordsHandler),
            (settings.urls.web_sitemap+'?', web.SitemapHandler), ]

        settings_ = dict(
            template_path=settings.env.TEMPLATE_PATH,
            static_path=settings.env.STATIC_PATH,
            cookie_secret=settings.env.COOKIE_SECRET,
            xsrf_cookies=settings.env.XSRF_COOKIES,
            debug=settings.env.DEBUG,
            autoreload=settings.env.AUTORELOAD,
            default_handler_class=web.ErrorHandler,
            default_handler_args=dict(status_code=404), )

        tornado.web.Application.__init__(self, handlers, **settings_)


def main():
    ioloop = tornado.ioloop.IOLoop.instance()

    http_server = tornado.httpserver.HTTPServer(Windseed())
    http_server.listen(8000, 'localhost')

    ioloop.start()


if __name__ == '__main__':
    main()
