from django.contrib import admin
from .models import Category, Brand
# from nested_inline.admin import NestedStackedInline, NestedModelAdmin


class CategoryConfig(admin.ModelAdmin):
    model = Category

    list_display = ('name',)
    ordering = ('name',)
    list_per_page = 20


class BrandConfig(admin.ModelAdmin):
    model = Brand
    list_display = ('name',)
    ordering = ('name',)
    list_per_page = 20

admin.site.register(Category, CategoryConfig)
admin.site.register(Brand, BrandConfig)
