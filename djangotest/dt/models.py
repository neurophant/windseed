from django.db import models


class Record(models.Model):
    active = models.BooleanField(default=True)

    name = models.CharField(max_length=256, db_index=True, unique=True)
    description = models.TextField(null=True)

    class Meta:
        index_together = (
            ('active', 'name', ), )
