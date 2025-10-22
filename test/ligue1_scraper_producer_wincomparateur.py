import time
import json
import pika
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

# --- URL Ligue 1 ---
url = "https://www.wincomparator.com/fr-fr/pronostics/football/france/ligue-1-123/"
driver.get(url)
try:
    match_elem = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.cursor-pointer.w-full.xl\\:border-r.border-primary-grayborder"))
    )
    match = match_elem.text.strip()
except:
    print("⚠️ Impossible de récupérer le titre du match :", url)


match_divs = driver.find_elements(By.CSS_SELECTOR, "div.cursor-pointer.w-full.xl\\:border-r.border-primary-grayborder")

match_urls = []

# --- Récupérer tous les liens de matchs ---
for div in match_divs:
    onclick_value = div.get_attribute("onclick")  # ex: location.href='/fr-fr/pronostics/paris-fc-lorient-7856808/'
    if onclick_value and "location.href=" in onclick_value:
        # Extraire ce qui est entre les quotes
        path = onclick_value.split("'")[1]  # prend le 2ème élément du split
        if path:  # vérifie que ce n'est pas vide
            # Construire l'URL pour ton site
            new_url = "https://www.wincomparator.com/fr-fr/pronostics" + path  # remplace par ton domaine
            match_urls.append(new_url)

print(f"📌 Nombre de matchs trouvés : {len(match_urls)}")


# --- Parcourir les matchs ---
for match_url in match_urls:
    try:
        driver.get(match_url)
        time.sleep(3)

        # Récupérer le nom du match
        try:
            match_title_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "span.text-gray-700.dark\\:text-white.text-sm.font-semibold")
            )
        )
            match_title = match_title_elem.text.strip()
            print("Match title:", match_title)
        except:
            print("⚠️ Impossible de récupérer le titre du match")

        # Récupérer les bookmakers
        rows = driver.find_elements(By.CSS_SELECTOR, ".self-stretch.flex-col.justify-start.items-start.gap-2.flex.w-full")
        for row in rows:
            img = row.find_element(By.CSS_SELECTOR, "img.mx-auto.hidden.md\\:block.rounded-md")
            bookmaker = img.get_attribute("alt")
            odds = row.find_elements(By.CSS_SELECTOR, "div.text-center.text-sky-950.text-base.font-bold.leading-normal.w-full")

            cote_dict = {}
            if len(odds) >= 3:
                cote_dict["cote_1"] = odds[0].text.strip()
                cote_dict["cote_N"] = odds[1].text.strip()
                cote_dict["cote_2"] = odds[2].text.strip()

            # Publier dans RabbitMQ
            message = {"match": match_name, "bookmaker": bookmaker, "cotes": cote_dict}
            channel.basic_publish(exchange="", routing_key="cotes", body=json.dumps(message))
            print(f"📤 Envoyé : {message}")

    except Exception as e:
        print("⚠️ Erreur scraping :", e)

driver.quit()
connection.close()
