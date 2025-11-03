from django.db import migrations
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json

def create_periodic_task(apps, schema_editor):
    schedule, created = CrontabSchedule.objects.get_or_create(
        minute='0',
        hour='*/6',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*',
        timezone='Europe/Paris'
    )
    
    
    PeriodicTask.objects.get_or_create(
        name='Scraping automatique toutes les 6h',
        defaults={
            'task': 'auto_scrape_all_leagues',
            'crontab': schedule,
            'enabled': True,
            'description': 'Scrape automatiquement Ligue 1, Premier League, La Liga, Serie A et Bundesliga'
        }
    )

def remove_periodic_task(apps, schema_editor):
    PeriodicTask.objects.filter(name='Scraping automatique toutes les 6h').delete()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
        ('django_celery_beat', '__latest__'),
    ]

    operations = [
        migrations.RunPython(create_periodic_task, remove_periodic_task),
    ]
