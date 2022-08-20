from re import search
from . import models
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from . import forms
# Register your models here.


class UserProfileAdmin(SimpleHistoryAdmin):
    form = forms.UserDetailAdminForm
    ordering = ['user']
    list_display = ['user', 'gender', 'country_code',
                    'mobile', 'dob', 'active_user', 'created_from']
    search_fields = ['mobile', 'created_from', 'country_code']
    list_per_page = 20


class IpAddressAdmin(admin.ModelAdmin):
    list_display = ['ip', 'create_date', 'continent', 'country',
                    'country_code', 'region', 'region_code', 'city']
    search_fields = ['ip', 'city', 'country']
    ordering = ['-create_date']
    list_per_page = 20


admin.site.register(models.UserProfile)
admin.site.register(models.IpAddress)
