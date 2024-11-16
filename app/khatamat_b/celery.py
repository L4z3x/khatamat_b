from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'khatamat_b.settings')

app = Celery('khatamat_b')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()