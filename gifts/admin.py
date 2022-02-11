from django.contrib import admin
from .models import PromoCode, Redemption, FixedDiscount, PercentageDiscount, PromoCodeRule, PromoCodeCondition

class PromoCodeConfig(admin.ModelAdmin):
    model = PromoCode

    readonly_fields = ('number_of_uses', 'discount_type', 'discount_object_id', 'discount_object')

admin.site.register(PromoCode, PromoCodeConfig)
admin.site.register(PromoCodeRule)
admin.site.register(PromoCodeCondition)
admin.site.register(Redemption)
admin.site.register(FixedDiscount)
admin.site.register(PercentageDiscount)
