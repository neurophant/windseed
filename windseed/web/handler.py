import tornado.web

from windseed import base


class Handler(base.Handler):
    def write_error(self, status_code, **kwargs):
        self.render('web/error.html', status_code=status_code)


class ErrorHandler(tornado.web.ErrorHandler, Handler):
    pass
