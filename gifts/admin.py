from django.contrib import admin
from .models import PromoCode, Redemption, FixedDiscount, PercentageDiscount, PromoCodeRule, AllowedUsersRule, UsageRule, ValidityRule, ConditionRule

class PromoCodeConfig(admin.ModelAdmin):
    model = PromoCode


admin.site.register(PromoCode, PromoCodeConfig)
admin.site.register(PromoCodeRule)
admin.site.register(AllowedUsersRule)
admin.site.register(UsageRule)
admin.site.register(ValidityRule)
admin.site.register(ConditionRule)
admin.site.register(Redemption)
admin.site.register(FixedDiscount)
admin.site.register(PercentageDiscount)
