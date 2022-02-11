from django.urls import path
from .views import GiftList

app_name = 'gifts'

urlpatterns = [
    path('', GiftList.as_view(), name='gifts'),
]
