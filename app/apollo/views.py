import logging

from django.http import Http404
from django.shortcuts import render_to_response

logger = logging.getLogger('app')


def home_page(request):
    try:
        return render_to_response('index.html')
    except Exception as e:
        logger.exception(e)
        raise Http404


def static_page(request, page):
    try:
        return render_to_response('%s.html' % page)
    except Exception as e:
        logger.exception(e)
        raise Http404
