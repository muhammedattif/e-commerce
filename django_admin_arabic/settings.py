import string
from django.conf import settings


SITE_INDEX_TITLE = getattr(settings, 'SITE_INDEX_TITLE', 'Site Administration')
SITE_TITLE = getattr(settings, 'SITE_TITLE', 'Django site admin')
SITE_HEADER = getattr(settings, 'SITE_HEADER', 'Django Administration')
