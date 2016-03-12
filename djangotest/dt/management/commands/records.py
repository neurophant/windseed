from django.core.management.base import BaseCommand
from dt.models import Record


class Command(BaseCommand):
    help = 'Creates 10000 records'

    def handle(self, *args, **options):
        records = []

        for i in range(10000):
            if i % 2 == 0:
                active = True
            else:
                active = False
            records.append(Record(active=active, name='record %d' % i,
                                  description='description %d' % i))
        Record.objects.bulk_create(records)
