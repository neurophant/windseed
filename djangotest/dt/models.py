from django.db import models


class Record(models.Model):
    active = models.BooleanField(default=True)

    name = models.CharField(max_length=256, db_index=True, unique=True)
    description = models.TextField(null=True)

    class Meta:
        index_together = (
            ('active', 'name', ), )


class RecordPage(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE, db_index=True,
                               unique=True)
    page = models.IntegerField(default=0, db_index=True)

    class Meta:
        unique_together = (('record', 'page', ), )
        index_together = (('record', 'page', ), )
