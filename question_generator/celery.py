# question_generator/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'question_generator.settings')

app = Celery('question_generator')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
