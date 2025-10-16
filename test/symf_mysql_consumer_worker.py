import json
import pika
import mysql.connector
from datetime import datetime

# --- Connexion à RabbitMQ ---
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue="cotes")

# --- Connexion à MySQL ---
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="cotes_db"
)
cursor = db.cursor()

def callback(ch, method, properties, body):
    data = json.loads(body)
    cote_dict = data.get("cotes")
    
    # On ajoute la date de scrap
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Si le message indique "scrape", on lance le scraper externe
    if data.get("action") == "scrape":
        print("🔄 Scraping déclenché par Symfony...")
        import subprocess
        subprocess.run(["python3", "/home/dougdoug/gig-benchmark/test/symf_ligue1_scraper_producer_coteur.py"])
        return

    # insert data
    cursor.execute(
        """
        INSERT INTO cotes (match_name, bookmaker, cote_1, cote_N, cote_2, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            data.get("match"),
            data.get("bookmaker"),
            cote_dict.get("cote_1"),
            cote_dict.get("cote_N"),
            cote_dict.get("cote_2"),
            now
        )
    )
    db.commit()
    print(f"💾 Enregistré en DB : {data}")

channel.basic_consume(queue="cotes", on_message_callback=callback, auto_ack=True)
print("🔄 En attente de messages...")
channel.start_consuming()
