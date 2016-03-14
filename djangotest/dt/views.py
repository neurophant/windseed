from django.shortcuts import render
from django.core.paginator import Paginator

from dt.models import Record, RecordPage


def index(request):
    page = int(request.GET.get('page', 1))

    records = Record.objects.filter(active=True).order_by('name')
    pages = Paginator(records, 48)

    '''
    records = pages.page(page).object_list
    '''
    records_pages = RecordPage.objects\
        .filter(page=page)\
        .select_related('record')

    return render(
        request,
        'records.html',
        dict(
            records=[record_page.record for record_page in records_pages],
            prev_page=pages.page(page).previous_page_number()
            if pages.page(page).has_previous() else None,
            next_page=pages.page(page).next_page_number()
            if pages.page(page).has_next() else None))
