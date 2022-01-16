from django.contrib import admin
from .models import Product, ProductImage, Feature, FeatureAttribute, Review
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

class FeatureAttributeInline(NestedStackedInline):
    model = FeatureAttribute
    can_delete = True
    verbose_name_plural = 'Attributes'
    fk_name = 'feature'


class FeatureInline(NestedStackedInline):
    model = Feature
    extra = 1
    can_delete = True
    verbose_name_plural = 'Features'
    fk_name = 'product'
    inlines = [FeatureAttributeInline]


class ReviewConfig(admin.ModelAdmin):
    model = Review

    list_filter = ('user', 'product', 'rate', 'likes', 'dislikes', 'creation')
    list_display = ('user', 'product', 'rate', 'likes', 'dislikes', 'creation')

class ProductConfig(NestedModelAdmin):
    model = Review

    list_filter = ('provider', 'name', 'description', 'price', 'quantity', 'discount', 'creation', 'data')
    list_display = ('provider', 'name', 'description', 'price', 'quantity', 'discount', 'creation', 'data')

    inlines = [FeatureInline]

admin.site.register(Review, ReviewConfig)

admin.site.register(Product, ProductConfig)
admin.site.register(Feature)
admin.site.register(FeatureAttribute)
admin.site.register(ProductImage)
