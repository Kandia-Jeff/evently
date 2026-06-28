from django.contrib import admin
from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['event__title', 'user__username']


admin.site.register(Feedback, FeedbackAdmin)