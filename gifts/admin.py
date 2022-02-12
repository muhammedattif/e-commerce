from django.contrib import admin
from .models import PromoCode, Redemption, FixedDiscount, PercentageDiscount, PromoCodeRule, AllowedUsersRule, UsageRule, ValidityRule, ConditionRule
from gifts.actions import rollback_and_delete_selected_redemptions

class PromoCodeConfig(admin.ModelAdmin):
    model = PromoCode

class RedemptionConfig(admin.ModelAdmin):
    model = Redemption
    actions = [rollback_and_delete_selected_redemptions]


admin.site.register(PromoCode, PromoCodeConfig)
admin.site.register(PromoCodeRule)
admin.site.register(AllowedUsersRule)
admin.site.register(UsageRule)
admin.site.register(ValidityRule)
admin.site.register(ConditionRule)
admin.site.register(Redemption, RedemptionConfig)
admin.site.register(FixedDiscount)
admin.site.register(PercentageDiscount)
