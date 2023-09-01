import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ZaurCloud.settings')
app = Celery('Loader')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
