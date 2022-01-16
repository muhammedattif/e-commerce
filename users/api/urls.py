from django.urls import path, include
from .views import SignIn, SignUp, Profile, BaseAddressListCreateView
app_name = 'users'

urlpatterns = [
    # Authentication Routes
    path('signin', SignIn.as_view(), name="signin"),
    path('signup', SignUp.as_view(), name="singup"),
    path('profile/', Profile.as_view(), name="profile"),
    path('profile/addresses/', BaseAddressListCreateView.as_view(), name="addresses")
  ]
