from django.contrib.admin import ModelAdmin
from django.utils import timezone


# ========================
def rollback_and_delete_selected_redemptions(modeladmin, request, queryset):
    for redemption in queryset:
        redemption.delete()
    ModelAdmin.message_user(modeladmin, request, "Promo Codes reseted!")


def delete_expired_coupons(modeladmin, request, queryset):
    count = 0
    for coupon in queryset:
        expiration_date = coupon.ruleset.validity.expiration_date
        if timezone.now() >= expiration_date:
            coupon.delete()
            count += 1

    ModelAdmin.message_user(modeladmin, request, "{0} Expired coupons deleted!".format(count))


# Actions short descriptions
# ==========================
rollback_and_delete_selected_redemptions.short_description = "Delete Selected Redemptions and Rollback Back Promo Codes"
delete_expired_coupons.short_description = "Delete expired coupons"
