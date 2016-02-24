import datetime

import peewee

from windseed import settings


class Model(peewee.Model):
    """
    Common db model:
        uid - primary key
        uts - timestamp (auto on creation)
    """
    uid = peewee.PrimaryKeyField(unique=True, index=True)
    uts = peewee.DateTimeField(default=datetime.datetime.now, index=True)

    class Meta:
        database = settings.db.pool
        order_by = ('-uts', )
