from rest_framework.views import APIView
from rest_framework.response import Response
from gifts.models import PromoCode
class GiftList(APIView):

    def get(self, request):
        promo_code = request.user.promocode_set.first()
        print(promo_code.is_active())
        print(promo_code.is_expired())
        print(promo_code.is_valid())
        print(promo_code.is_limit_reached())
        print(promo_code.is_owner(request.user))
        print(promo_code.is_owner_limit_reached(request.user))
        # print(promo_code.redeem(request.user))
        print(promo_code.rules)
        print(promo_code.rules.allowed_categories.all())
        print(promo_code.rules.allowed_brands.all())
        print(promo_code.check_conditions())

        return Response({'1':1})
