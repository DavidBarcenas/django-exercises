from django.contrib import admin

from .models import Category, Type, Product


class TypeAdmin(admin.ModelAdmin):
    list_display = ("id", "title")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title")


admin.site.register(Type, TypeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
