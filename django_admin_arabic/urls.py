from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .settings import (
SITE_INDEX_TITLE,
SITE_TITLE,
SITE_HEADER
)
app_name = 'django_admin_arabic'

urlpatterns = [

]

admin.site.index_title = _(SITE_INDEX_TITLE)
admin.site.site_title = _(SITE_TITLE)
admin.site.site_header = _(SITE_HEADER)
