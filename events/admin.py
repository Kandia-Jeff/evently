from django.contrib import admin
from .models import Event, EventUpdate


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organiser', 'category', 'date', 'status')
    list_filter = ('status', 'category')
    search_fields = ('title', 'organiser__username')
    actions = ['approve_events', 'reject_events']

    def approve_events(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, 'Selected events have been approved.')
    approve_events.short_description = 'Approve selected events'

    def reject_events(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, 'Selected events have been rejected.')
    reject_events.short_description = 'Reject selected events'


@admin.register(EventUpdate)
class EventUpdateAdmin(admin.ModelAdmin):
    list_display = ('event', 'created_at')