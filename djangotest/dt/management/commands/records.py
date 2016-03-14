from django.core.management.base import BaseCommand
from django.core.paginator import Paginator

from dt.models import Record, RecordPage


class Command(BaseCommand):
    help = 'Creates 1000000 records'

    def handle(self, *args, **options):
        records = []

        Record.objects.all().delete()

        for i in range(1000000):
            if i % 2 == 0:
                active = True
            else:
                active = False
            records.append(Record(active=active, name='record %d' % i,
                                  description='description %d' % i))
        Record.objects.bulk_create(records)

        RecordPage.objects.all().delete()

        records = Record.objects.filter(active=True).order_by('name')
        paginator = Paginator(records, 48)

        records_pages = []
        for page in range(1, paginator.num_pages+1):
            for record in paginator.page(page).object_list:
                records_pages.append(RecordPage(record=record, page=page))

        RecordPage.objects.bulk_create(records_pages)
