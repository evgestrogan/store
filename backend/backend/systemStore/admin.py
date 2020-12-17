from django.contrib import admin
from .models import Product, ProductPhoto, Category, Order


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('title', )
    list_display = ('title', )


class ProductPhotoAdmin(admin.StackedInline):
    model = ProductPhoto
    extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Settings django-admin for new user table"""
    fieldsets = (
        (None, {'fields': ('title', 'weight', 'price', 'category', 'description', 'vendor_code', 'presence', )}),
    )
    list_display = ('title', 'weight', 'price', 'category', 'presence', )
    inlines = [ProductPhotoAdmin]


class DescriptionProductOrderAdmin(admin.TabularInline):
    model = Order.product.through
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'status', )}),
    )
    list_display = ('user', 'get_count_products', 'status', 'created',)
    inlines = [DescriptionProductOrderAdmin]
