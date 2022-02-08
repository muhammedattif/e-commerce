from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, renderers, parsers, exceptions
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.authtoken import views as auth_views
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema
from django.http import JsonResponse
from .serializers import AuthTokenSerializer, SignUpSerializer, UserSerializer, AddressSerilaizer, AddressCreateSerilaizer
from django.core.exceptions import ValidationError
from .serializers import ChangePasswordSerializer
from users.models import User
import src.utils as general_utils
from products.models import Favorite
from products.api.serializers import ProductsSerializer
from django_rest_passwordreset.views import ResetPasswordConfirm
from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.signals import pre_password_reset, post_password_reset
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.conf import settings
import products.utils as product_utils

class SignIn(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )

    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            content = {
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            }
            return Response(content)
        except:
            response = {}
            errors = serializer.errors
            for error in errors:
                response[error] = errors[error][0]
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class SignUp(APIView):

    permission_classes = ()

    def post(self, request, format=True):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token, created = Token.objects.get_or_create(user=user)
            response = {
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            }
        else:
            response = serializer.errors
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class Profile(APIView):

    def get(self, request):
        serializer = UserSerializer(request.user, many=False, context = {
          'request': request
        })
        return Response(serializer.data)

class Profile(APIView):

    def get(self, request):
        serializer = UserSerializer(request.user, many=False, context = {
          'request': request
        })
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        profile = serializer.save()
        serializer = UserSerializer(profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class BaseAddressListCreateView(APIView):
    def get(self, request):
        addresses = request.user.addresses.all()
        serializer = AddressSerilaizer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = AddressCreateSerilaizer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        address = serializer.save()
        serializer = AddressSerilaizer(address)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                error = general_utils.error('wrong_old_password')
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            success = general_utils.success('updated_successfully')
            return Response(success)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ResetPasswordConfirmView(ResetPasswordConfirm):

    def post(self, request, *args, **kwargs):
        data = {
        'token': request.data['token'],
        'password': request.data['password']
        }

        try:
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=False)
            password = serializer.validated_data['password']
            token = serializer.validated_data['token']
        except Exception as e:
            error = general_utils.error('invalid_url')
            return Response(error, status.HTTP_400_BAD_REQUEST)

        # find token
        reset_password_token = ResetPasswordToken.objects.filter(key=token).first()

        # change users password (if we got to this code it means that the user is_active)
        if reset_password_token.user.eligible_for_reset():
            pre_password_reset.send(sender=self.__class__, user=reset_password_token.user)
            try:
                # validate the password against existing validators
                validate_password(
                    password,
                    user=reset_password_token.user,
                    password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
                )
            except ValidationError as e:
                # raise a validation error for the serializer
                raise exceptions.ValidationError({
                    'password': e.messages
                })

            reset_password_token.user.set_password(password)
            reset_password_token.user.save()
            post_password_reset.send(sender=self.__class__, user=reset_password_token.user)

        # Delete all password reset tokens for this user
        ResetPasswordToken.objects.filter(user=reset_password_token.user).delete()

        success = general_utils.success('password_reset_successfully')
        return Response(success)


class FavoriteListAddView(APIView):

    def get(self, request):
        favorites = request.user.favorite.products.all()
        serializer = ProductsSerializer(favorites, many=True)
        return Response(serializer.data)

    def post(self, request):

        product_id = request.data['product_id']

        filter_kwargs = {
        'id': product_id
        }
        product, found, error = product_utils.get_product(filter_kwargs)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        favorites = request.user.favorite.products
        favorites.add(product)

        success = general_utils.success('updated_successfully')
        return Response(success)


class FavoriteDestroyView(APIView):

    def delete(self, request, id):

        filter_kwargs = {
        'id': id
        }

        product, found, error = product_utils.get_product(filter_kwargs)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        favorites = request.user.favorite.products
        favorites.remove(product)

        success = general_utils.success('updated_successfully')
        return Response(success)
