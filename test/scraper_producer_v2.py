# scraper_producer.py
import time
import json
import pika
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# --- RabbitMQ ---
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue="cotes")

# --- Selenium ---
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# --- URL à scraper ---
url = "https://www.coteur.com/cote/strasbourg-marseille-1545864"   # page des matchs
driver.get(url)
time.sleep(5)

# Récupérer le match

match_elem = driver.find_element(By.CSS_SELECTOR, ".page-title")  # trouver le nom du match
match = match_elem.text.strip()

# --- Scraping ---
rows = driver.find_elements(By.CSS_SELECTOR, ".d-flex[data-name]")  # trouver bookmakers
print(f"📌 Nombre de bookmakers trouvés : {len(rows)}")

for row in rows:
    try:
        bookmaker = row.get_attribute("data-name")
        print("👉 Bookmaker trouvé :", bookmaker)
        odds = row.find_elements(By.CSS_SELECTOR, ".border.odds-col")
        print("👉 Nombre de cotes trouvées :", len(odds))
        cote_dict = {}
        if len(odds) >= 3:
            cote_dict["cote_1"] = odds[0].text.strip()
            cote_dict["cote_N"] = odds[1].text.strip()
            cote_dict["cote_2"] = odds[2].text.strip()

        # Publier dans RabbitMQ
        message = {"match": match, "bookmaker": bookmaker, "cotes": cote_dict}
        channel.basic_publish(exchange="", routing_key="cotes", body=json.dumps(message))
        print(f"📤 Envoyé : {message}")
    except Exception as e:
        print("⚠️ Erreur scraping :", e)

driver.quit()
connection.close()
