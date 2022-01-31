from django.contrib import admin
from .models import Product, ProductImage, Feature, FeatureAttribute, FeatureAttributesMap, Review
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

    list_filter = ('vendor', 'name', 'price', 'discount', 'creation')
    list_display = ('vendor', 'name', 'price', 'discount', 'creation')

class FeatureAttributesMapConfig(admin.ModelAdmin):
    model = FeatureAttributesMap

    list_filter = ('product', 'quantity')
    list_display = ('product', 'quantity')

    def get_queryset(self, request):
        queryset = super(FeatureAttributesMapConfig, self).get_queryset(request)
        queryset = queryset.select_related('product').prefetch_related('attributes')
        return queryset




admin.site.register(Review, ReviewConfig)
admin.site.register(Product, ProductConfig)
admin.site.register(Feature)
admin.site.register(FeatureAttribute)
admin.site.register(FeatureAttributesMap, FeatureAttributesMapConfig)
admin.site.register(ProductImage)
