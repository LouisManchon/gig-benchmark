import json
import pika
import mysql.connector
from datetime import datetime

# --- Connexion à RabbitMQ ---
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue="odds")

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
    cote_dict = data["cotes"]
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute(
        """
        INSERT INTO odds (match_name, bookmaker, cote_1, cote_N, cote_2, trj, league, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            data["match"],
            data["bookmaker"],
            cote_dict.get("cote_1"),
            cote_dict.get("cote_N"),
            cote_dict.get("cote_2"),
            data["trj"],
            data["league"],
            now
        )
    )
    db.commit()
    print(f"💾 Enregistré en DB : {data}")

channel.basic_consume(queue="odds", on_message_callback=callback, auto_ack=True)
print("🔄 En attente de messages...")
channel.start_consuming()
