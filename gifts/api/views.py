from rest_framework.views import APIView
from rest_framework.response import Response
from gifts.models import PromoCode
from categories.models import Brand, Category
from gifts.utils import PromoCodeConfig

class GiftList(APIView):

    def get(self, request):
        brands = Brand.objects.all()
        categories = Category.objects.all()
        conditions = [{'operator': '>', 'price': 1000}, {'operator': '<', 'price': 2000}]
        config = PromoCodeConfig(
                discount_type='fixed',
                amount=10000,
                users=request.user,
                all_users=True,
                brands=brands,
                categories=categories
            )
        promo_code = PromoCode.objects.create_promo_code(config=config)
        print(promo_code.is_valid(user=request.user))
        # promo_code = PromoCode.objects.prefetch_related('rules__usage__parent_rule','rules__allowed_users__users').filter(rules__allowed_users__users__in=[request.user]).first()
        print(promo_code.is_active)
        print(promo_code.is_expired)
        print(promo_code.is_valid)
        print(promo_code.is_limit_reached)
        print(promo_code.is_eligible_for_user(request.user))
        print(promo_code.is_user_limit_reached(request.user))
        print(promo_code.redeem(request.user))
        print(promo_code.rules)
        print(promo_code.rules.allowed_categories.all())
        print(promo_code.rules.allowed_brands.all())
        print(promo_code.check_conditions())
        print(PromoCode.objects.expired())
        print(PromoCode.objects.owner(user=request.user))

        return Response({'1':1})
