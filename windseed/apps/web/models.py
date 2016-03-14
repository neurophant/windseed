import peewee

from windseed.base.model import Model


class Record(Model):
    """
    Record db model:
        active - is record an active one

        name - record name
        description - record description
    """
    active = peewee.BooleanField(default=True)

    name = peewee.CharField(max_length=256, index=True, unique=True)
    description = peewee.TextField(null=True)

    class Meta:
        indexes = (
            (('active', 'name', ), True, ), )


class RecordPage(Model):
    """
    Records paginator db model:
        record - record foreign key
        page - page number
    """
    record = peewee.ForeignKeyField(
        Record,
        db_column='record',
        to_field='uid',
        related_name='record_records_pages',
        on_delete='CASCADE',
        index=True,
        unique=True)
    page = peewee.IntegerField(
        default=0,
        index=True,
        constraints=[peewee.Check('page >= 0'), ])

    class Meta:
        indexes = ((('record', 'page', ), True, ), )
        constraints = (peewee.SQL('UNIQUE (record, page)'), )
