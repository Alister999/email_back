"""Standart WSGI module"""
import os
import logging
from django.core.wsgi import get_wsgi_application

logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'email_back.settings')

application = get_wsgi_application()
