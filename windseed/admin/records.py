import peewee

import tornado.web
import tornado.gen
import tornado.escape

from windseed import settings, models, admin


class RecordsHandler(admin.Handler):
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
            count = peewee.SelectQuery(models.Record).count()
        except peewee.IntegrityError:
            count = 0

        page_count = int(count/settings.env.ADMIN_ITEMS_PER_PAGE) + \
            int(bool(count % settings.env.ADMIN_ITEMS_PER_PAGE))

        prev_page, page, next_page = self.paging(page, page_count)

        try:
            records = models.Record\
                .select()\
                .order_by(
                    models.Record.active.desc(),
                    models.Record.uts.desc())\
                .paginate(page, paginate_by=settings.env.ADMIN_ITEMS_PER_PAGE)
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
    @admin.authenticated
    def get(self):
        """
        Render records
        """
        self.render(
            'admin/records.html',
            user=self.user,
            **self.get_page_context())

    @tornado.gen.coroutine
    @admin.authenticated
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
                with settings.db.pool.atomic():
                    created = models.Record.create(
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
                with settings.db.pool.atomic():
                    updated = models.Record\
                        .update(
                            active=active,
                            name=name,
                            description=description)\
                        .where(models.Record.uid == uid)\
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
                with settings.db.pool.atomic():
                    deleted = models.Record\
                        .delete()\
                        .where(models.Record.uid == uid)\
                        .execute()
            except peewee.IntegrityError:
                deleted = None

            if deleted:
                self.ajax_page('delete')
            else:
                self.ajax_empty('not_deleted')
        else:
            self.ajax_empty('not_command')
