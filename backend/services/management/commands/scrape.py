import json
import pika
import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Trigger scraping task via RabbitMQ'

    def add_arguments(self, parser):
        parser.add_argument(
            'scraper',
            type=str,
            help='Scraper to run (e.g., football.ligue_1, football.la_liga)'
        )

    def handle(self, *args, **options):
        scraper = options['scraper']
        
        RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'gig_user')
        RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'gig_password_2025')
        
        self.stdout.write(f'Sending scraping task: {scraper}')
        
        try:
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters('rabbitmq', credentials=credentials)
            )
            channel = connection.channel()
            channel.queue_declare(queue='scraping_tasks', durable=True)
            
            message = json.dumps({'scraper': scraper})
            channel.basic_publish(
                exchange='',
                routing_key='scraping_tasks',
                body=message,
                properties=pika.BasicProperties(delivery_mode=2)
            )
            
            self.stdout.write(self.style.SUCCESS(f'Task sent successfully: {scraper}'))
            connection.close()
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error sending task: {str(e)}'))