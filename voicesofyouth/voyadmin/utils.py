from django.conf import settings
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator


def get_paginator(queryset, page=1, items_per_page=None):
    items_per_page = items_per_page or settings.ITEMS_PER_PAGE
    paginator = Paginator(queryset, items_per_page)
    try:
        paginator = paginator.page(page)
    except PageNotAnInteger:
        paginator = paginator.page(1)
    except EmptyPage:
        # Invalid page number. We send the last page.
        paginator = paginator.page(paginator.num_pages)

    return paginator
