from django.contrib.auth import authenticate
from users.models import User, Address
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import transaction
from django.contrib.auth import get_user_model
User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):

    re_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'avatar', 'password', 're_password', 'is_vendor']
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
            username=self.validated_data['username'],
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
        fields = ('id', 'email', 'username', 'first_name', 'last_name')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'location', 'avatar', 'date_joined', 'last_login')


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



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

class TokenObtainPairCustomSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['is_vendor'] = self.user.is_vendor


        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
