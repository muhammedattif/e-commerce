from django.contrib import admin
from .models import Product, ProductImage, Review

class ReviewConfig(admin.ModelAdmin):
    model = Review

    list_filter = ('user', 'product', 'rate', 'likes', 'dislikes', 'creation')
    list_display = ('user', 'product', 'rate', 'likes', 'dislikes', 'creation')

admin.site.register(Review, ReviewConfig)

admin.site.register(Product)
admin.site.register(ProductImage)
