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
channel.queue_declare(queue="odds")


def perform_scrapping():
    # --- Selenium ---
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # --- URL Champions League ---
    url = "https://www.coteur.com/cotes/foot/europe/ligue-des-champions"
    driver.get(url)
    try:
        # wait charging page
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".event-team"))
        )
        print("✅ Page chargée, les éléments de matchs sont présents.")
    except:
        print("⚠️ Impossible de charger les éléments de la page :", url)


    # had match links
    link_elements = driver.find_elements(By.CSS_SELECTOR, "a.text-decoration-none")
    match_links = []
    for elem in link_elements:
        href = elem.get_attribute("href")
        if href:
            if href.startswith("/"):
                href = "https://www.coteur.com" + href
            match_links.append(href)

    print(f"📌 Nombre de matchs trouvés : {len(match_links)}")


    # browse matches
    for match_url in match_links:
        try:
            driver.get(match_url)
            time.sleep(3)

            # wait for title of the match

            try:
                title_element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".page-title"))
                )
                title = title_element.text.strip()
                print("✅ Titre trouvé :", title)

            except Exception as e:
                print("⚠️ Erreur scraping : impossible de trouver .page-title :", e)
                title = None

            # name match

            # match_elem = driver.find_element(By.CSS_SELECTOR, ".page-title")
            # match_name = match_elem.text.strip()

            # name bookmakers
            rows = driver.find_elements(By.CSS_SELECTOR, ".d-flex[data-name]")
            for row in rows:
                bookmaker = row.get_attribute("data-name")
                odds = row.find_elements(By.CSS_SELECTOR, ".border.odds-col")

                cote_dict = {}
                if len(odds) >= 3:
                    cote_dict["cote_1"] = float(odds[0].text.strip())
                    cote_dict["cote_N"] = float(odds[1].text.strip())
                    cote_dict["cote_2"] = float(odds[2].text.strip())

                # publish in Rabbit
                message = {
                    "match": title,
                    "bookmaker": bookmaker,
                    "cotes": cote_dict,
                    "trj": round((1 / (1/cote_dict["cote_1"] + 1/cote_dict["cote_N"] + 1/cote_dict["cote_2"])) * 100, 2),
                    "league": "Champions League",
                    "sport": "football"
                }
                channel.basic_publish(exchange="", routing_key="odds", body=json.dumps(message))
                print(f"📤 Envoyé : {message}")

        except Exception as e:
            print("⚠️ Erreur scraping :", e)

    driver.quit()
    connection.close()

perform_scrapping()