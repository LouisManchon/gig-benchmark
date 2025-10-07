"""
Service de gestion du scraping via RabbitMQ
"""
import json
from typing import Dict, Optional
from core.rabbitmq_config.rabbitmq_config import rabbitmq_config

class ScrapingService:
    """Service pour envoyer des tâches de scraping au worker"""
    
    # Liste de tous les scrapers disponibles
    AVAILABLE_SCRAPERS = {
        # Football
        'football.ligue_1': 'Ligue 1',
        'football.premier_league': 'Premier League',
        'football.la_liga': 'La Liga',
        'football.serie_a': 'Serie A',
        'football.bundesliga': 'Bundesliga',
        'football.champions_league': 'Champions League',
        
        # Basketball
        'basketball.nba': 'NBA',
        'basketball.euroleague': 'Euroleague',
        
        # Rugby
        'rugby.top14': 'Top 14',
        'rugby.6nations': '6 Nations',
        
        # Tennis
        'tennis.atp': 'ATP',
        'tennis.wta': 'WTA',
    }
    
    def __init__(self):
        self.rabbitmq = rabbitmq_config
        self.queue_name = 'scraping_tasks'
    
    def send_task(self, scraper: str, params: Optional[Dict] = None) -> Dict:
        """
        Envoie UNE tâche de scraping au worker
        
        Exemple: send_task('football.ligue_1')
        """
        if scraper not in self.AVAILABLE_SCRAPERS:
            return {
                'success': False,
                'error': f'Scraper inconnu: {scraper}'
            }
        
        if params is None:
            params = {}
        
        try:
            # Se connecter à RabbitMQ
            connection = self.rabbitmq.get_connection()
            channel = connection.channel()
            
            # Déclarer la queue
            channel.queue_declare(queue=self.queue_name, durable=True)
            
            # Créer le message
            message = {
                'scraper': scraper,
                'params': params
            }
            
            # Envoyer le message
            channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=json.dumps(message)
            )
            
            # Fermer la connexion
            connection.close()
            
            return {
                'success': True,
                'scraper': scraper,
                'league_name': self.AVAILABLE_SCRAPERS[scraper]
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_multiple_tasks(self, scrapers: list) -> Dict:
        """
        Envoie PLUSIEURS tâches de scraping
        
        Exemple: send_multiple_tasks(['football.ligue_1', 'football.la_liga'])
        """
        results = {
            'success': [],
            'failed': []
        }
        
        for scraper in scrapers:
            result = self.send_task(scraper)
            if result['success']:
                results['success'].append(scraper)
            else:
                results['failed'].append(scraper)
        
        return {
            'total': len(scrapers),
            'success_count': len(results['success']),
            'failed_count': len(results['failed']),
            'results': results
        }
    
    def get_available_scrapers(self) -> Dict:
        """Retourne la liste de tous les scrapers"""
        return {
            'count': len(self.AVAILABLE_SCRAPERS),
            'scrapers': self.AVAILABLE_SCRAPERS
        }
    
    def scrape_all_football(self) -> Dict:
        """Lance tous les championnats de FOOT"""
        scrapers = [
            'football.ligue_1',
            'football.premier_league',
            'football.la_liga',
            'football.serie_a',
            'football.bundesliga',
            'football.champions_league'
        ]
        return self.send_multiple_tasks(scrapers)
    
    def scrape_all_basketball(self) -> Dict:
        """Lance tous les championnats de BASKET"""
        scrapers = ['basketball.nba', 'basketball.euroleague']
        return self.send_multiple_tasks(scrapers)
    
    def scrape_all_rugby(self) -> Dict:
        """Lance tous les championnats de RUGBY"""
        scrapers = ['rugby.top14', 'rugby.6nations']
        return self.send_multiple_tasks(scrapers)
    
    def scrape_all_tennis(self) -> Dict:
        """Lance tous les championnats de TENNIS"""
        scrapers = ['tennis.atp', 'tennis.wta']
        return self.send_multiple_tasks(scrapers)
    
    def scrape_all(self) -> Dict:
        """Lance TOUS les scrapers"""
        return self.send_multiple_tasks(list(self.AVAILABLE_SCRAPERS.keys()))


# Instance globale pour l'utiliser dans les views
scraping_service = ScrapingService()