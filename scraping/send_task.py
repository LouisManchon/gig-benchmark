#!/usr/bin/env python3
import pika
import json
import sys

if len(sys.argv) < 2:
    print("Usage: python send_task.py <scraper_name>")
    print("Exemple: python send_task.py football.ligue_1")
    sys.exit(1)

scraper = sys.argv[1]

credentials = pika.PlainCredentials('gig_user', 'gig_password_2025')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='rabbitmq',
        port=5672,
        credentials=credentials
    )
)
channel = connection.channel()
channel.queue_declare(queue='scraping_tasks', durable=True)

message = json.dumps({'scraper': scraper, 'params': {}})
channel.basic_publish(
    exchange='',
    routing_key='scraping_tasks',
    body=message,
    properties=pika.BasicProperties(delivery_mode=2)
)

print(f"Tâche envoyée: {scraper}")
connection.close()
