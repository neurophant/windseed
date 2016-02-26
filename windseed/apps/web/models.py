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
