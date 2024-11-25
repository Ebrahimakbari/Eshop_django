from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models



@admin.register(models.CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    # form = UserChangeForm
    # add_form = UserCreationForm

    list_display = ('email', 'username', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'phone_number', 'password1', 'password2'),}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)