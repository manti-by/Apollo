import logging

from django.http import Http404
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from api.models import Shot

logger = logging.getLogger('app')


@login_required
def home_page(request):
    try:
        user = request.user
        return render_to_response('index.html', {'user': user})
    except Exception as e:
        logger.exception(e)
        raise Http404


def static_page(request, page):
    try:
        user = None
        if request.user.is_authenticated:
            user = request.user.profiles.as_dict()
        return render_to_response('static/%s.html' % page, {'user': user})
    except Exception as e:
        logger.exception(e)
        raise Http404

