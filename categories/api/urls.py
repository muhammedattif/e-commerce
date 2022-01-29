from django.urls import path
from .views import CategoryList, BrandList
app_name = 'categories'

urlpatterns = [
    path('', CategoryList.as_view(), name='categories'),
    path('brands/', BrandList.as_view(), name='brands')
  ]
