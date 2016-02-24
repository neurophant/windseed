import tornado.web
import tornado.gen

from windseed import admin


class DashboardHandler(admin.Handler):
    """
    Dashboard: /admin/
    """
    @tornado.web.addslash
    @tornado.gen.coroutine
    @admin.authenticated
    def get(self):
        """
        Render dashboard
        """
        self.render('admin/dashboard.html', user=self.user)
