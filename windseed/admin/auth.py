import tornado.web
import tornado.gen

from windseed import settings, models, admin


def authenticated(func):
    """
    Execute target function if authenticated, redirect to login page otherwise
    """
    def decorated(self, *args, **kwargs):
        if not self.user:
            self.redirect(settings.urls.admin_login)
        else:
            return func(self, *args, **kwargs)

    return decorated


def unauthenticated(func):
    """
    Execute target function if not authenticated, redirect to dashboard
    otherwise
    """
    def decorated(self, *args, **kwargs):
        if self.user:
            self.redirect(settings.urls.admin_dashboard)
        else:
            return func(self, *args, **kwargs)

    return decorated


class LoginHandler(admin.Handler):
    """
    Login: /admin/login/
    """
    @tornado.web.addslash
    @tornado.gen.coroutine
    @unauthenticated
    def get(self):
        """
        Render login page
        """
        self.render('admin/login.html')

    @tornado.gen.coroutine
    @unauthenticated
    def post(self):
        """
        Process login form and authenticate user if credentials are valid,
        redirect back to login page otherwise
        """
        email = self.get_argument('email')
        password = self.get_argument('password')

        try:
            user = models.User.get(models.User.email == email)
        except models.User.DoesNotExist:
            user = None

        if user:
            if user.active and user.superuser and \
                    user.check_password(password=password):
                self.set_secure_cookie('user', user.email)
                self.redirect(settings.urls.admin_dashboard)
            else:
                self.redirect(settings.urls.admin_login)
        else:
            self.redirect(settings.urls.admin_login)


class LogoutHandler(admin.Handler):
    """
    Logout: /admin/logout/
    """
    @tornado.web.addslash
    @tornado.gen.coroutine
    @authenticated
    def get(self):
        """
        Clear user authentication and redirect to login page
        """
        self.clear_cookie('user')
        self.redirect(settings.urls.admin_login)
