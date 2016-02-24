from windseed import base


class Handler(base.Handler):
    def write_error(self, status_code, **kwargs):
        self.render('admin/error.html', status_code=status_code)
