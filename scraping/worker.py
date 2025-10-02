import time
import json
import pika
import mysql.connector
import os

# Configuration from environment variables
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'gig_user')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'gig_password')

DB_HOST = os.getenv('DB_HOST', 'db')
DB_NAME = os.getenv('DB_NAME', 'gig_benchmark')
DB_USER = os.getenv('DB_USER', 'gig_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'gig_password')

# RabbitMQ connection
print(f"Connecting to RabbitMQ at {RABBITMQ_HOST}...")
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
)
channel = connection.channel()
channel.queue_declare(queue='scraping_tasks')
print("Connected to RabbitMQ successfully")

# MySQL connection
print(f"Connecting to MySQL at {DB_HOST}...")
db = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)
print("Connected to MySQL successfully")

# Listening loop
print("Waiting for scraping tasks...")
while True:
    time.sleep(10)
    print("Worker is active...")