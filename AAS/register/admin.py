from django.contrib import admin
from register.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms
# Register your models here.


class ARSUserAdmin(UserAdmin):

    # The fields to be used in displaying the CocoUser model.
    # These override the definitions on the base UserAdmin that reference specific fields on auth.User.
    list_display = ('id', 'username','first_name', 'last_name', 'email', 'is_admin')
    fieldsets = (
        (None, {'fields': ('username', )}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'date_joined', 'last_login',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'is_admin', 'is_client')}),
        
    )
    search_fields = ('id', 'email', 'first_name', 'last_name',)
    ordering = ('last_name', 'first_name',)

    class Meta:
        model = User


admin.site.register(User, ARSUserAdmin)