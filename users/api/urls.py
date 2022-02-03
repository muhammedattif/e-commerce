from django.urls import path, include
from .views import SignIn, SignUp, Profile, BaseAddressListCreateView, ChangePasswordView, ResetPasswordConfirmView
app_name = 'users'

urlpatterns = [
    # Authentication Routes
    path('signin', SignIn.as_view(), name="signin"),
    path('signup', SignUp.as_view(), name="singup"),
    path('profile/', Profile.as_view(), name="profile"),
    path('profile/addresses/', BaseAddressListCreateView.as_view(), name="addresses"),

    # Change Password
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

    # Reset Password
    path('reset-password/', include('django_rest_passwordreset.urls', namespace='reset-password')),
    path('reset_password/confirm/', ResetPasswordConfirmView.as_view(), name='reset-password-confirm'),
  ]
