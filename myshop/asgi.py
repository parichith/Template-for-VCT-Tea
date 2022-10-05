import os

from django.core.asgi import get_asgi_application

# This gets the ASGI module callable.
# Where WSGI was purely synchronous, ASGI is both asynchronous and synchronous

# https://asgi.readthedocs.io/en/latest/

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

application = get_asgi_application()
