from django.conf import settings
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from functools import reduce


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

    index = paginator.number - 1
    max_index = len(paginator.paginator.page_range)
    start_index = index - 4 if index >= 4 else 0
    end_index = index + 4 if index <= max_index - 4 else max_index
    paginator.page_range = list(paginator.paginator.page_range)[start_index:end_index]

    return paginator


round_bar_valids_percents = [x * 5 for x in range(0, 21)]
def radial_bar_round_down(value):
    return reduce(
        lambda current, next: next if value >= next else current,
        round_bar_valids_percents)
