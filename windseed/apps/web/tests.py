import tornado.testing

from windseed.base.test import Test
from windseed.apps.web.models import Record


class RecordTestCase(Test):
    @tornado.testing.gen_test
    def test(self):
        record = Record.create(name='record 1')
        self.assertIsInstance(record, Record)
        self.assertEqual(record.name, 'record 1')

        updated = Record\
            .update(name='record 2')\
            .where(Record.uid == record.uid)\
            .execute()
        self.assertEqual(updated, 1)
        record = Record.get(Record.uid == record.uid)
        self.assertEqual(record.name, 'record 2')

        record.name = 'record 3'
        saved = record.save()
        self.assertEqual(saved, 1)
        record = Record.get(Record.uid == record.uid)
        self.assertEqual(record.name, 'record 3')

        record.delete_instance()
