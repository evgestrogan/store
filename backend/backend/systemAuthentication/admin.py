from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


class DescriptionProductUserAdmin(admin.TabularInline):
    model = User.product.through
    extra = 1


@admin.register(User)
class UserAdmin(UserAdmin):
    """Settings django-admin for new user table"""
    fieldsets = (
        (None, {'fields': ('username', 'password', 'last_name', 'first_name', 'middle_name', 'number_phone', 'email',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'groups'),
        }),
    )
    inlines = [DescriptionProductUserAdmin]
    filter_horizontal = ('groups',)
    list_display = ('username', 'last_name', 'first_name', 'middle_name', 'is_staff',)
    search_fields = ('username',)
