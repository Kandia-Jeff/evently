from django.contrib import admin
from .models import Event, EventUpdate


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organiser', 'category', 'date', 'status')
    list_filter = ('status', 'category')
    search_fields = ('title', 'organiser__username')
    actions = ['approve_events', 'reject_events']

    def approve_events(self, request, queryset):
        from accounts.emails import send_event_approved_email
        for event in queryset:
            event.status = 'approved'
            event.save()
            send_event_approved_email(event)
        self.message_user(request, 'Selected events have been approved and organisers notified.')
    approve_events.short_description = 'Approve selected events'

    def reject_events(self, request, queryset):
        from accounts.emails import send_event_rejected_email
        for event in queryset:
            event.status = 'rejected'
            event.save()
            send_event_rejected_email(event)
        self.message_user(request, 'Selected events have been rejected and organisers notified.')
    reject_events.short_description = 'Reject selected events'


@admin.register(EventUpdate)
class EventUpdateAdmin(admin.ModelAdmin):
    list_display = ('event', 'created_at')