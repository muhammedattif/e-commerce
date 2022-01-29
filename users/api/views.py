from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import renderers
from rest_framework import parsers
from rest_framework.authtoken import views as auth_views
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema
from django.http import JsonResponse
from .serializers import AuthTokenSerializer, SignUpSerializer, UserSerializer, AddressSerilaizer, AddressCreateSerilaizer
from django.core.exceptions import ValidationError


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
