from django.contrib import admin

from api.models import Shot


@admin.register(Shot)
class ShotAdmin(admin.ModelAdmin):

    list_display = ('created', 'term_01', 'term_02', 'term_03', 'water_sensor')

    fieldsets = (
        ('Info', {
            'fields': ('term_01', 'term_02', 'term_03', 'water_sensor')
        }),
    )
