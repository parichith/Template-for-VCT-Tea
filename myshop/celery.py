import os
from celery import Celery

# Celery cannot be made functional under the current OS used to build this website.
# Hence, this website cannot perform asynchronous tasks as of yet.

# sets the default Django settings module for the 'celery' program.

# https://docs.celeryproject.org/en/stable/

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')


app = Celery('myshop')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
