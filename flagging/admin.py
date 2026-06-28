from django.contrib import admin
from .models import Flag


class FlagAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'fl_status', 'created_at']
    list_filter = ['fl_status']
    search_fields = ['event__title', 'user__username']


admin.site.register(Flag, FlagAdmin)