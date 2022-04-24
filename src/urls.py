"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')),



    # Users
    path('users/', include('users.urls', 'users')),
    # Users APIs
    path('api/users/', include('users.api.urls', 'users_api')),

    # Vendor
    path('vendor/', include('vendor.urls', 'vendor')),
    # Vendor APIs
    path('api/vendor/', include('vendor.api.urls', 'vendor_api')),

    # Products
    path('products/', include('products.urls', 'products')),
    # Products APIs
    path('api/products/', include('products.api.urls', 'products_api')),

    # Payment
    path('payment/', include('payment.urls', 'payment')),
    # Products APIs
    path('api/payment/', include('payment.api.urls', 'payment_api')),

    # Categories
    path('categories/', include('categories.urls', 'categories')),
    # Categories APIs
    path('api/categories/', include('categories.api.urls', 'categories_api')),

    # Orders
    path('orders/', include('orders.urls', 'orders')),
    # Orders APIs
    path('api/orders/', include('orders.api.urls', 'orders_api')),

    # Gifts
    path('gifts/', include('gifts.urls', 'gifts')),
    # Gifts APIs
    path('api/gifts/', include('gifts.api.urls', 'gifts-apis')),

    # Django Arabic URLS
    path('django-arabic', include('django_admin_arabic.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [
        # This for debugging
        path('__debug__/', include(debug_toolbar.urls)),
        # Swagger UI
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]

from django.conf.urls.i18n import i18n_patterns

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    # If no prefix is given, use the default language
    prefix_default_language=True
)
