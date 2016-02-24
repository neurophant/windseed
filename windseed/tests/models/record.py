import tornado.testing

from windseed import base, models


class RecordTestCase(base.Test):
    @tornado.testing.gen_test
    def test(self):
        record = models.Record.create(name='record 1')
        self.assertIsInstance(record, models.Record)
        self.assertEqual(record.name, 'record 1')

        updated = models.Record\
            .update(name='record 2')\
            .where(models.Record.uid == record.uid)\
            .execute()
        self.assertEqual(updated, 1)
        record = models.Record.get(models.Record.uid == record.uid)
        self.assertEqual(record.name, 'record 2')

        record.name = 'record 3'
        saved = record.save()
        self.assertEqual(saved, 1)
        record = models.Record.get(models.Record.uid == record.uid)
        self.assertEqual(record.name, 'record 3')

        record.delete_instance()
