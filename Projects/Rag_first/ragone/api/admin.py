from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


admin.site.register(Document)
admin.site.register(DocumentChunk)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Fields to display in the user list
    list_display = ('username', 'email', 'is_staff', 'is_active')
    # Fields to filter by
    list_filter = ('is_staff', 'is_active')
    # Fields to use in the add/change user form
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    # Fields to show when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
