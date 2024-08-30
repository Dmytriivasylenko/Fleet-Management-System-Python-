from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Налаштування Django для використання Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fleet')


app = Celery('fleet')

# Налаштування Celery
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

