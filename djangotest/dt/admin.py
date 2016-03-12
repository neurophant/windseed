from django.contrib import admin
from dt.models import Record


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    pass
