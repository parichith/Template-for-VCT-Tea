import os

from django.core.wsgi import get_wsgi_application

# This gets the WSGI module callable.

# https://wsgi.readthedocs.io/en/latest/

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

application = get_wsgi_application()
