import os
from backend.config.celery import Celery

# Définir le module de settings Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

app = Celery('gig_benchmark')

# Configuration depuis les settings Django avec le namespace CELERY
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-découverte des tâches dans toutes les apps installées
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')