from django.contrib import admin
from .models import Product, ProductImage, Feature, FeatureOption, Review, Favorite
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

class FeatureOptionInline(NestedStackedInline):
    model = FeatureOption
    can_delete = True
    verbose_name_plural = 'Options'
    fk_name = 'feature'


class FeatureInline(NestedStackedInline):
    model = Feature
    extra = 1
    can_delete = True
    verbose_name_plural = 'Features'
    fk_name = 'product'
    inlines = [FeatureOptionInline]


class ReviewConfig(admin.ModelAdmin):
    model = Review

    list_filter = ('user', 'product', 'rate', 'likes', 'dislikes', 'creation')
    list_display = ('user', 'product', 'rate', 'likes', 'dislikes', 'creation')

class ProductConfig(NestedModelAdmin):
    model = Product

    list_filter = ('vendor', 'name', 'price', 'discount', 'creation')
    list_display = ('vendor', 'name', 'price', 'discount', 'creation')


admin.site.register(Review, ReviewConfig)
admin.site.register(Product, ProductConfig)
admin.site.register(Feature)
admin.site.register(FeatureOption)
admin.site.register(ProductImage)
admin.site.register(Favorite)
