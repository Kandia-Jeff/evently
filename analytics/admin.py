from django.contrib import admin
from .models import EventView


@admin.register(EventView)
class EventViewAdmin(admin.ModelAdmin):
    list_display = ('event', 'viewed_at')
    list_filter = ('event',)