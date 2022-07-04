from django.contrib import admin
from handbooks.models import Handbook, HandbookElement


@admin.register(Handbook)
class HandbookAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'start_at']
    list_filter = ['handbook_id']
    sortable_by = ['start_at']


@admin.register(HandbookElement)
class HandbookElementAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'value']
    list_filter = ['element_code']
    sortable_by = ['handbook_id.start_at']
