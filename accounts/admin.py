from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile


class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'first_name', 'last_name', 'username', 'role', 'verification_status', 'is_verified', 'is_staff']
    list_filter = ('role', 'is_verified', 'verification_status')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'username', 'role')}),
        ('Verification', {'fields': ('verification_document', 'is_verified', 'verification_status', 'verification_notes')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'username', 'role', 'password1', 'password2'),
        }),
    )
    search_fields = ['email', 'username']

    actions = ['approve_organisers', 'reject_organisers']

    def approve_organisers(self, request, queryset):
        queryset.filter(role='organiser').update(is_verified=True, verification_status='approved')
        self.message_user(request, 'Selected organisers have been approved.')
    approve_organisers.short_description = 'Approve selected organisers'

    def reject_organisers(self, request, queryset):
        queryset.filter(role='organiser').update(is_verified=False, verification_status='rejected')
        self.message_user(request, 'Selected organisers have been rejected.')
    reject_organisers.short_description = 'Reject selected organisers'


admin.site.register(User, UserAdmin)
admin.site.register(Profile)