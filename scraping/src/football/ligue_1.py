import os          # AJOUTEZ CETTE LIGNE
import time
import json
import pika
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def connect_rabbitmq():
    """Connexion à RabbitMQ avec retry"""
    max_retries = 5
    for i in range(max_retries):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=os.getenv('RABBITMQ_HOST', 'rabbitmq'),
                    port=5672,
                    credentials=pika.PlainCredentials(
                        os.getenv('RABBITMQ_USER', 'gig_user'),
                        os.getenv('RABBITMQ_PASSWORD', 'gig_password_2025')
                    )
                )
            )
            return connection
        except Exception as e:
            print(f"Tentative {i+1}/{max_retries} - Erreur connexion RabbitMQ: {e}")
            if i < max_retries - 1:
                time.sleep(5)
            else:
                raise

def setup_chrome_driver():
    """Configuration du driver Chrome pour Docker"""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--disable-extensions")
    
    # Pour Docker, pas besoin de ChromeDriverManager
    return webdriver.Chrome(options=options)

def main():
    print("Démarrage du scraper Ligue 1...")
    
    # Connexion à RabbitMQ
    connection = connect_rabbitmq()
    channel = connection.channel()
    channel.queue_declare(queue="cotes", durable=True)
    print("Connexion RabbitMQ établie")
    
    # Configuration Selenium
    driver = setup_chrome_driver()
    print("Driver Chrome configuré")
    
    try:
        # URL Ligue 1
        url = "https://www.coteur.com/cotes/foot/france/ligue-1"
        driver.get(url)
        
        # Attendre que la page se charge
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".col-12"))
        )
        
        # Récupérer tous les liens de matchs
        link_elements = driver.find_elements(By.CSS_SELECTOR, "a.text-decoration-none")
        match_links = []
        
        for elem in link_elements:
            href = elem.get_attribute("href")
            if href:
                if href.startswith("/"):
                    href = "https://www.coteur.com" + href
                match_links.append(href)
        
        print(f"Nombre de matchs trouvés : {len(match_links)}")
        
        # Parcourir les matchs
        for match_url in match_links:
            try:
                driver.get(match_url)
                time.sleep(3)
                
                # Récupérer le nom du match
                match_elem = driver.find_element(By.CSS_SELECTOR, ".page-title")
                match_name = match_elem.text.strip()
                
                # Récupérer les bookmakers
                rows = driver.find_elements(By.CSS_SELECTOR, ".d-flex[data-name]")
                
                for row in rows:
                    bookmaker = row.get_attribute("data-name")
                    odds = row.find_elements(By.CSS_SELECTOR, ".border.odds-col")
                    
                    cote_dict = {}
                    if len(odds) >= 3:
                        cote_dict["cote_1"] = odds[0].text.strip()
                        cote_dict["cote_N"] = odds[1].text.strip()
                        cote_dict["cote_2"] = odds[2].text.strip()
                    
                    # Publier dans RabbitMQ
                    message = {
                        "match": match_name,
                        "bookmaker": bookmaker,
                        "cotes": cote_dict,
                        "timestamp": time.time()
                    }
                    
                    channel.basic_publish(
                        exchange="",
                        routing_key="cotes",
                        body=json.dumps(message),
                        properties=pika.BasicProperties(delivery_mode=2)  # Message persistant
                    )
                    print(f"Envoyé : {message}")
                    
            except Exception as e:
                print(f"Erreur scraping pour {match_url}: {e}")
                
    except Exception as e:
        print(f"Erreur générale : {e}")
    finally:
        driver.quit()
        connection.close()
        print("Scraper terminé")

# Point d'entrée pour le worker
def scrape_ligue_1(**kwargs):
    """
    Fonction appelée par worker.py
    """
    print("Démarrage du scraping Ligue 1 depuis le worker")
    try:
        # Appeler votre fonction main() existante
        main()
        
        return {
            'success': True,
            'league': 'Ligue 1',
            'message': 'Scraping terminé avec succès'
        }
    except Exception as e:
        print(f"Erreur: {e}")
        return {
            'success': False,
            'league': 'Ligue 1',
            'error': str(e)
        }


# Pour test standalone
if __name__ == "__main__":
    print("Test du scraper Ligue 1")
    result = scrape_ligue_1()
    print(f"Résultat: {result}")
