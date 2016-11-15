from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.staticfiles.templatetags.staticfiles import static as static_file

from api.models import Shot


@admin.register(ShotType)
class ShotTypeAdmin(admin.ModelAdmin):

    list_display = ('icon_image', 'title', 'volume', 'measure', 'degree')
    ordering = ('title',)

    fieldsets = (
        (_('Info'), {
            'fields': ('title', ('volume', 'measure'), 'degree')
        }),
    )
