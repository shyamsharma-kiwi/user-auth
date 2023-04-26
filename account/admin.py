from django.contrib import admin

from account.models import UserRegister


@admin.register(UserRegister)
class UserRegisterAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'password', 'otp', 'created_at', 'is_active']
    list_filter = ['first_name', 'last_name', 'email', 'is_active']
    search_fields = ['first_name', 'last_name', 'email']
    ordering = ['first_name']
    fieldsets = (
        ("Basic Details", {'fields': ('first_name', 'last_name', 'email', 'password')}),
        ("Permissions", {'fields': ('is_active',)}),
        ("OTP Verification", {'fields': ('otp',)})
    )
