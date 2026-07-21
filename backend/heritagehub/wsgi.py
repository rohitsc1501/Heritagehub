"""WSGI config for HeritageHub project."""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heritagehub.settings')
application = get_wsgi_application()
