import importlib
from django.contrib.auth import authenticate
from users.models import User, Address
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, exceptions
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import transaction
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreatePasswordRetypeSerializer
from rest_framework.validators import UniqueValidator
from users.models import Vendor
from django.db import transaction
from djoser.conf import settings as djoser_settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

User = get_user_model()
rule_package, user_eligible_for_login = api_settings.USER_AUTHENTICATION_RULE.rsplit('.', 1)
login_rule = importlib.import_module(rule_package)

class UserCreateSerializer(UserCreatePasswordRetypeSerializer):
    phone_number = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all(),
                                        message=("Phone number already exists"))])

    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        fields = ('id', 'email', 'phone_number', 'first_name', 'last_name', 'agent_name', 'city', 'district', 'reg_as_vendor', 'password')



    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)

            if user.reg_as_vendor:
                # Create Vendor
                Vendor.objects.create(user=user)

            if djoser_settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user


class SignUpSerializer(serializers.ModelSerializer):

    re_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'first_name', 'last_name', 'avatar', 'password', 're_password', 'is_vendor']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    @transaction.atomic
    def save(self):
        is_vendor = False
        if 'is_vendor' in self.validated_data and self.validated_data['is_vendor']:
            is_vendor = True

        user = User(
            email=self.validated_data['email'],
            phone_number=self.validated_data['phone_number'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            avatar=self.validated_data['avatar'],
            is_vendor=is_vendor
        )

        password = self.validated_data['password']
        re_password = self.validated_data['re_password']

        if password != re_password:
            raise serializers.ValidationError({'password':'Password does not match.'})
        user.set_password(password)
        user.save()
        return user



class AuthTokenSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email_or_username = attrs.get('email_or_username')
        password = attrs.get('password')

        if email_or_username and password:
            # Check if user sent email
            if not validateEmail(email_or_username):
                try:
                    user_request = User.objects.get(username=email_or_username)
                except User.DoesNotExist:
                    msg = 'Unable to log in with provided credentials.'
                    raise serializers.ValidationError({
                        'status': 'error',
                        'message': msg
                    })

                email_or_username = user_request.email

            user = authenticate(email=email_or_username, password=password)

            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError({
                        'status': 'error',
                        'message': msg
                    })
            else:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError({
                    'status': 'error',
                    'message': msg
                })
        else:
            msg = 'Must include "email or username" and "password"'
            raise serializers.ValidationError({
                'status': 'error',
                'message': msg
            })

        attrs['user'] = user
        return attrs


def validateEmail( email ):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

class UserBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'phone_number', 'first_name', 'last_name')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'phone_number', 'first_name', 'last_name', 'agent_name', 'location', 'city', 'district', 'avatar', 'date_joined', 'last_login')


class AddressSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class AddressCreateSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('locality', 'city', 'zipcode', 'state', 'phone_number')

    def create(self, validated_data):
        user = self.context.get('request', None).user
        validated_data['user'] = user
        address = Address.objects.create(**validated_data)
        return address

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, data):
        # validators.validate_password(password=data, user=User)
        # return data

        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        user = User(**data)

        # get the password from the data
        password = data.get('password')

        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=user)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(RegisterUserSerializer, self).validate(data)


class TokenObtainPairCustomSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email =  attrs['email']
        password = attrs['password']

        try:
            request = self.context['request']
        except KeyError:
            pass

        # Check if user sent email
        if not validateEmail(email):
            try:
                user_request = User.objects.get(phone_number=email)
            except User.DoesNotExist:
                msg = 'Unable to log in with provided credentials.'
                raise exceptions.AuthenticationFailed(
                    msg
                )

            email = user_request.email

        self.user = authenticate(request=request, email=email, password=password)

        if not getattr(login_rule, user_eligible_for_login)(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )


        refresh = self.get_token(self.user)
        data = {}
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['is_vendor'] = self.user.is_active_vendor


        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
