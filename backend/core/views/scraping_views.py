# backend/core/views/scraping_views.py

from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import pika
import json
import os
import threading

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_PORT = int(os.environ.get('RABBITMQ_PORT', '5672'))
RABBITMQ_USER = os.environ.get('RABBITMQ_USER', 'gig_user')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD', 'gig_password_2025')

scraping_progress = {}
progress_lock = threading.Lock()

def send_scraping_task(scraper_name):
    """
    Envoie une tâche de scraping dans la queue RabbitMQ
    """
    try:
        print(f"🔌 Connexion à RabbitMQ: {RABBITMQ_HOST}:{RABBITMQ_PORT}")
        
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=credentials,
                connection_attempts=3,
                retry_delay=2
            )
        )
        
        print("✅ Connecté à RabbitMQ")
        
        channel = connection.channel()
        channel.queue_declare(queue='scraping_tasks', durable=True)
        
        print(f"📦 Queue 'scraping_tasks' déclarée")

        message = json.dumps({'scraper': scraper_name, 'params': {}})
        channel.basic_publish(
            exchange='',
            routing_key='scraping_tasks',
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)
        )
        
        print(f"✅ Tâche envoyée: {scraper_name}")
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur envoi task: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({'status': 'healthy', 'service': 'scraping-api'})


@api_view(['POST'])
@permission_classes([AllowAny])
def trigger_scraping(request):
    """
    Déclenche un scraping
    Body: {"scraper": "football.ligue_1"}
    """
    scraper = request.data.get('scraper')

    if not scraper:
        sport = request.data.get('sport')
        league = request.data.get('league')
        
        if sport and league:
            # Cas "all leagues"
            if league == 'all':
                # Router vers la fonction appropriée
                if sport == 'football':
                    return scrape_all_football(request)
                elif sport == 'basketball':
                    return scrape_all_basketball(request)
                elif sport == 'rugby':
                    return scrape_all_rugby(request)
                elif sport == 'tennis':
                    return scrape_all_tennis(request)
                else:
                    return Response(
                        {'success': False, 'error': f'Sport inconnu: {sport}'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                # Cas ligue spécifique
                scraper = f"{sport}.{league}"
    
    if not scraper:
        return Response(
            {'success': False, 'error': 'scraper or (sport + league) required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    # Envoie la tâche dans RabbitMQ
    success = send_scraping_task(scraper)
    
    if success:
        return Response({
            'success': True
        })
    else:
        return Response(
            {'success': False, 'error': 'Erreur lors de l\'envoi de la tâche'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def scrape_all_football(request):
    """Lance tous les scrapers de football"""
    scrapers = [
        'football.ligue_1',
        'football.premier_league',
        'football.la_liga',
        'football.serie_a',
        'football.bundesliga',
        'football.champions_league'
    ]
    
    tasks_sent = []
    errors = []
    
    for scraper in scrapers:
        if send_scraping_task(scraper):
            tasks_sent.append(scraper)
        else:
            errors.append(scraper)
    
    return Response({
        'success': len(errors) == 0,
        'message': f'{len(tasks_sent)} scrapers lancés',
        'tasks_sent': tasks_sent,
        'errors': errors
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def scrape_all_basketball(request):
    scrapers = ['basketball.nba', 'basketball.euroleague']
    tasks_sent = []
    for scraper in scrapers:
        if send_scraping_task(scraper):
            tasks_sent.append(scraper)
    
    return Response({
        'success': True,
        'message': f'{len(tasks_sent)} scrapers basketball lancés',
        'tasks_sent': tasks_sent
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def scrape_all_rugby(request):
    scrapers = ['rugby.top14']
    tasks_sent = []
    for scraper in scrapers:
        if send_scraping_task(scraper):
            tasks_sent.append(scraper)
    
    return Response({
        'success': True,
        'message': f'{len(tasks_sent)} scrapers rugby lancés',
        'tasks_sent': tasks_sent
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def scrape_all_tennis(request):
    scrapers = ['tennis.atp']
    tasks_sent = []
    for scraper in scrapers:
        if send_scraping_task(scraper):
            tasks_sent.append(scraper)
    
    return Response({
        'success': True,
        'message': f'{len(tasks_sent)} scrapers tennis lancés',
        'tasks_sent': tasks_sent
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def update_scraping_progress(request):
    try:
        data = request.data
        scraper = data.get('scraper')
        
        print(f"📊 Réception progression pour {scraper}")
        
        if scraper:
            # ✅ Verrou pour éviter les conflits
            with progress_lock:
                scraping_progress[scraper] = {
                    'status': data.get('status', 'running'),
                    'current': data.get('current', 0),
                    'total': data.get('total', 0),
                    'message': data.get('message', ''),
                    'current_match': data.get('current_match'),
                    'bookmakers_count': data.get('bookmakers_count', 0),
                    'matches_scraped': data.get('matches_scraped', 0),
                    'odds_sent': data.get('odds_sent', 0),
                }
                print(f"✅ Sauvegardé: current={scraping_progress[scraper]['current']}/{scraping_progress[scraper]['total']}")
        
        return Response({'success': True})
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        return Response({'success': False}, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_scraping_progress(request):
    try:
        scraper = request.query_params.get('scraper')

        if scraper:
            # ✅ Lecture avec verrou
            with progress_lock:
                if scraper in scraping_progress:
                    data = scraping_progress[scraper].copy()  # ← Copie pour éviter les modifications
                    return Response(data)

        return Response({
            'status': 'idle',
            'current': 0,
            'total': 0,
            'message': 'Aucun scraping en cours'
        })

    except Exception as e:
        print(f"❌ ERREUR: {e}")
        return Response({'status': 'idle', 'current': 0, 'total': 0})


@api_view(['GET'])
@permission_classes([AllowAny])
def get_auto_scraping_status(request):
    """
    Récupère le statut du scraping automatique avec la prochaine exécution
    """
    try:
        from django_celery_beat.models import PeriodicTask
        from datetime import timedelta
        from django.utils import timezone

        task = PeriodicTask.objects.filter(name='Scraping automatique toutes les 6h').first()

        if task:
            next_run = None
            if task.enabled:
                # Utiliser la méthode schedule de Celery Beat pour calculer la prochaine exécution
                now = timezone.now()

                if task.crontab:
                    # Si c'est un crontab, calculer la prochaine exécution basée sur le crontab
                    # Le crontab est: 0 */6 * * * (minute 0, toutes les 6h)
                    # Donc: 00:00, 06:00, 12:00, 18:00 (en timezone du crontab)

                    # Convertir en timezone du crontab (Europe/Paris)
                    import pytz
                    # task.crontab.timezone peut être soit un string soit un objet ZoneInfo
                    if isinstance(task.crontab.timezone, str):
                        tz = pytz.timezone(task.crontab.timezone)
                    else:
                        # C'est déjà un objet timezone
                        tz = task.crontab.timezone
                    now_local = now.astimezone(tz)

                    # Trouver la prochaine heure parmi 0, 6, 12, 18
                    current_hour = now_local.hour
                    next_hours = [0, 6, 12, 18]

                    # Trouver la prochaine heure
                    next_hour = None
                    for h in next_hours:
                        if h > current_hour or (h == current_hour and now_local.minute < 1):
                            next_hour = h
                            break

                    # Si aucune heure trouvée aujourd'hui, prendre la première heure demain
                    if next_hour is None:
                        next_run = now_local.replace(hour=next_hours[0], minute=0, second=0, microsecond=0) + timedelta(days=1)
                    else:
                        next_run = now_local.replace(hour=next_hour, minute=0, second=0, microsecond=0)

                    # Convertir en UTC pour l'API
                    next_run = next_run.astimezone(pytz.UTC).isoformat()

                elif task.interval:
                    # Si c'est un interval, ajouter l'intervalle à la dernière exécution
                    if task.last_run_at:
                        next_run = task.last_run_at + timedelta(seconds=task.interval.every)
                        next_run = next_run.isoformat()
                    else:
                        # Si jamais exécutée, exécuter maintenant
                        next_run = now.isoformat()

            return Response({
                'success': True,
                'enabled': task.enabled,
                'last_run_at': task.last_run_at.isoformat() if task.last_run_at else None,
                'next_run_at': next_run
            })
        else:
            return Response({
                'success': False,
                'error': 'Tâche de scraping automatique non trouvée'
            }, status=404)

    except Exception as e:
        print(f"❌ Error getting auto scraping status: {e}")
        import traceback
        traceback.print_exc()
        return Response({
            'success': False,
            'error': str(e)
        }, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def toggle_auto_scraping(request):
    """
    Active/Désactive le scraping automatique
    Body: {"enabled": true/false}
    """
    try:
        from django_celery_beat.models import PeriodicTask

        enabled = request.data.get('enabled')

        if enabled is None:
            return Response({
                'success': False,
                'error': 'Le paramètre "enabled" est requis'
            }, status=400)

        task = PeriodicTask.objects.filter(name='Scraping automatique toutes les 6h').first()

        if task:
            task.enabled = enabled
            task.save()

            status_text = 'activé' if enabled else 'désactivé'
            print(f"✅ Scraping automatique {status_text}")

            return Response({
                'success': True,
                'enabled': task.enabled,
                'message': f'Scraping automatique {status_text}'
            })
        else:
            return Response({
                'success': False,
                'error': 'Tâche de scraping automatique non trouvée'
            }, status=404)

    except Exception as e:
        print(f"❌ Error toggling auto scraping: {e}")
        import traceback
        traceback.print_exc()
        return Response({
            'success': False,
            'error': str(e)
        }, status=500)
