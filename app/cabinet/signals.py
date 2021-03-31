from django.conf import settings
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

from cabinet.models import Cabinet