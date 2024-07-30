from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Ustawienie domyślnego modułu ustawień Django dla Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myRAG.settings')

app = Celery('myRAG')

# Użycie ustawień Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatyczne odkrywanie zadań w aplikacjach zainstalowanych w Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

