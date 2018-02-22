from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from apollo.views import home_page, static_page
from api.resources import ApiResource


urlpatterns = [
    url(r'^$', home_page, name='index'),
    url(r'^about$', static_page, {'page': 'about'}, name='about'),

    # Shot list
    url(r'^api/?$', ApiResource.as_view()),

    # Admin urls
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
