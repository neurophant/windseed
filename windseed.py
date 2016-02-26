import tornado.gen
import tornado.web
import tornado.ioloop
import tornado.httpserver

from windseed.settings import env, urls
from windseed.apps.web import handlers as web_handlers


class Windseed(tornado.web.Application):
    """
    Our main application
    """
    def __init__(self):
        settings_ = dict(
            template_path=env.TEMPLATE_PATH,
            static_path=env.STATIC_PATH,
            cookie_secret=env.COOKIE_SECRET,
            xsrf_cookies=env.XSRF_COOKIES,
            debug=env.DEBUG,
            autoreload=env.AUTORELOAD,
            default_handler_class=web_handlers.ErrorHandler,
            default_handler_args=dict(status_code=404), )

        tornado.web.Application.__init__(self, urls.routes, **settings_)


def main():
    ioloop = tornado.ioloop.IOLoop.instance()

    http_server = tornado.httpserver.HTTPServer(Windseed())
    http_server.listen(8000, 'localhost')

    ioloop.start()


if __name__ == '__main__':
    main()
