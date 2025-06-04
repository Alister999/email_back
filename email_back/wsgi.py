import os
from django.core.wsgi import get_wsgi_application
import logging

logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'email_back.settings')

application = get_wsgi_application()