from __future__ import absolute_import, unicode_literals

import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university.settings')
app = Celery(
    'university',
    broker=os.getenv("REDIS_FOR_CELERY")
)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
