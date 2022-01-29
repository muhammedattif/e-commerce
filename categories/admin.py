from django.contrib import admin
from .models import Category, Brand
from nested_inline.admin import NestedStackedInline, NestedModelAdmin


class CategoryConfig(NestedModelAdmin):
    model = Category

    list_display = ('name',)


admin.site.register(Category)
admin.site.register(Brand)
