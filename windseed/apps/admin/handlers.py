import peewee

import tornado.web
import tornado.gen

from windseed.settings import env, db, urls
from windseed.base import handler
from windseed.apps.admin.models import User
from windseed.apps.web.models import Record


class Handler(handler.Handler):
    def write_error(self, status_code, **kwargs):
        self.render('admin/error.html', status_code=status_code)


def authenticated(func):
    """
    Execute target function if authenticated, redirect to login page otherwise
    """
    def decorated(self, *args, **kwargs):
        if not self.user:
            self.redirect(urls.admin_login)
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
            self.redirect(urls.admin_dashboard)
        else:
            return func(self, *args, **kwargs)

    return decorated


class LoginHandler(Handler):
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
            user = User.get(User.email == email)
        except User.DoesNotExist:
            user = None

        if user:
            if user.active and user.superuser and \
                    user.check_password(password=password):
                self.set_secure_cookie('user', user.email)
                self.redirect(urls.admin_dashboard)
            else:
                self.redirect(urls.admin_login)
        else:
            self.redirect(urls.admin_login)


class LogoutHandler(Handler):
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
        self.redirect(urls.admin_login)


class DashboardHandler(Handler):
    """
    Dashboard: /admin/
    """
    @tornado.web.addslash
    @tornado.gen.coroutine
    @authenticated
    def get(self):
        """
        Render dashboard
        """
        self.render('admin/dashboard.html', user=self.user)


class RecordsHandler(Handler):
    """
    Records: /admin/records/
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
            count = peewee.SelectQuery(Record).count()
        except peewee.IntegrityError:
            count = 0

        page_count = int(count/env.ADMIN_ITEMS_PER_PAGE) + \
            int(bool(count % env.ADMIN_ITEMS_PER_PAGE))

        prev_page, page, next_page = self.paging(page, page_count)

        try:
            records = Record\
                .select()\
                .order_by(
                    Record.active.desc(),
                    Record.uts.desc())\
                .paginate(page, paginate_by=env.ADMIN_ITEMS_PER_PAGE)
        except peewee.IntegrityError:
            records = []

        return dict(records=records,
                    count=count,
                    page_count=page_count,
                    prev_page=prev_page,
                    page=page,
                    next_page=next_page)

    def ajax_page(self, status):
        """
        Return current page
        """
        record_list = tornado.escape.to_basestring(
            self.render_string(
                'admin/partials/_record_list.html',
                **self.get_page_context()))
        self.write(dict(status=status, record_list=record_list))

    def ajax_empty(self, status):
        """
        Return empty response
        """
        self.write(dict(status=status))

    @tornado.web.addslash
    @tornado.gen.coroutine
    @authenticated
    def get(self):
        """
        Render records
        """
        self.render(
            'admin/records.html',
            user=self.user,
            **self.get_page_context())

    @tornado.gen.coroutine
    @authenticated
    def post(self):
        """
        Create, update or delete a record
        """
        create = self.get_argument('create', None)
        update = self.get_argument('update', None)
        delete = self.get_argument('delete', None)

        uid = self.get_argument('uid', None)

        active = self.get_argument('active', None)
        active = True if active is not None else False

        name = self.get_argument('name', None)
        if name is not None:
            name = name.strip()
            if not name:
                name = None

        description = self.get_argument('description', None)

        if create is not None and \
                active is not None and \
                name is not None:
            try:
                with db.pool.atomic():
                    created = Record.create(
                        active=active,
                        name=name,
                        description=description)
            except peewee.IntegrityError:
                created = None

            if created:
                self.ajax_page('create')
            else:
                self.ajax_empty('not_created')
        elif update is not None and \
                uid is not None and \
                active is not None and \
                name is not None:
            try:
                with db.pool.atomic():
                    updated = Record\
                        .update(
                            active=active,
                            name=name,
                            description=description)\
                        .where(Record.uid == uid)\
                        .execute()
            except peewee.IntegrityError:
                updated = None

            if updated:
                self.ajax_page('update')
            else:
                self.ajax_empty('not_updated')
        elif delete is not None and \
                uid is not None:
            try:
                with db.pool.atomic():
                    deleted = Record\
                        .delete()\
                        .where(Record.uid == uid)\
                        .execute()
            except peewee.IntegrityError:
                deleted = None

            if deleted:
                self.ajax_page('delete')
            else:
                self.ajax_empty('not_deleted')
        else:
            self.ajax_empty('not_command')
