from django.contrib import admin

from account.models import UserRegister


@admin.register(UserRegister)
class UserRegister(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')

