import tornado.gen
import tornado.ioloop

from windseed.settings import env, db
from windseed.apps.web.models import Record, RecordPage


@tornado.gen.coroutine
def main():
    db.pool.connect()

    Record.delete().execute()

    records = []
    for i in range(env.RECORD_COUNT):
        if i % 2 == 0:
            active = True
        else:
            active = False
        records.append(dict(
            active=active,
            name='record %d' % i,
            description='description %d' % i))
    with db.pool.atomic():
        Record.insert_many(records).execute()

    count = Record\
        .select()\
        .where(Record.active == True)\
        .count()
    per_page = env.RECORDS_PER_PAGE
    page_count = int(count/per_page) + int(bool(count % per_page))

    RecordPage.delete().execute()

    records_pages = []
    for page in range(1, page_count+1):
        records = Record\
            .select(Record.uid)\
            .where(Record.active == True)\
            .order_by(Record.name.asc())\
            .paginate(
                page,
                paginate_by=per_page)
        for record in records:
            records_pages.append(dict(record=record.uid, page=page))

    with db.pool.atomic():
        RecordPage.insert_many(records_pages).execute()

    if not db.pool.is_closed():
        db.pool.close()

    return


if __name__ == '__main__':
    ioloop = tornado.ioloop.IOLoop.instance().run_sync(main)
