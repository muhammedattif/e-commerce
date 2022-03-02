from django.urls import path, include
from .views import (
SignIn,
SignUp,
Profile,
BaseAddressListCreateView,
ChangePasswordView,
ResetPasswordConfirmView,
FavoriteListAddView,
FavoriteDestroyView,
TokenObtainPairCustomView
)

app_name = 'users'

urlpatterns = [
    # Authentication Routes
    path('signin', SignIn.as_view(), name="signin"),
    path('signup', SignUp.as_view(), name="singup"),
    path('profile/', Profile.as_view(), name="profile"),
    path('profile/addresses/', BaseAddressListCreateView.as_view(), name="addresses"),

    path('favorites/', FavoriteListAddView.as_view(), name="favorite-list-add"),
    path('favorites/<int:id>/', FavoriteDestroyView.as_view(), name="remove-from-favorite"),

    # Change Password
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

    # Reset Password
    path('reset-password/', include('django_rest_passwordreset.urls', namespace='reset-password')),
    path('reset_password/confirm/', ResetPasswordConfirmView.as_view(), name='reset-password-confirm'),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/jwt/custom/create/', TokenObtainPairCustomView.as_view()),
  ]
