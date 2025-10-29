# scraping/src/football/ligue_1.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import json
import re
import dateparser
import pika
import os
import requests

BACKEND_URL = os.environ.get('BACKEND_URL', 'http://backend:8000')

def safe_float(val):
    """Convert value in float"""
    try:
        return float(val)
    except (ValueError, TypeError):
        return None

def send_progress_update(scraper_name, data):
    """Send update progress to backend"""
    try:
        url = f'{BACKEND_URL}/api/scraping/progress'
        payload = {
            'scraper': scraper_name,
            **data
        }
        
        print(f"📤 Envoi progression à {url}")
        print(f"   Payload: {payload}")
        
        response = requests.post(url, json=payload, timeout=2)
        
        print(f"📥 Réponse: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✅ Progression envoyée avec succès")
        else:
            print(f"⚠️ Erreur status {response.status_code}: {response.text}")
            
    except requests.exceptions.Timeout:
        print(f"⚠️ Timeout lors de l'envoi de la progression")
    except requests.exceptions.ConnectionError as e:
        print(f"⚠️ Erreur de connexion: {e}")
    except Exception as e:
        print(f"⚠️ Erreur inattendue: {type(e).__name__}: {e}")

def scrape_top14():
    """Scrape all top 14 matches"""
    
    print("\n" + "="*60)
    print("DÉMARRAGE DU SCRAPING - TOP 14")
    print("="*60)
    
    connection = None
    channel = None
    driver = None
    
    try:
        # Connexion RabbitMQ
        credentials = pika.PlainCredentials('gig_user', 'gig_password_2025')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
        )
        channel = connection.channel()
        channel.queue_declare(queue='odds', durable=True)
        print("Connecté à RabbitMQ")

        print("\n📋 Configuration Chrome...")
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.page_load_strategy = 'eager'
        print("✅ Options configurées")
        
        # Connexion Selenium Remote
        driver = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',
            options=options
        )
        driver.set_page_load_timeout(60)
        driver.set_script_timeout(60)
        driver.implicitly_wait(10)
        print("Connect to Selenium")

        # Go to page Top 14
        url = "https://www.coteur.com/cotes/rugby/france/top-14"
        print(f"\n{url}")
        driver.get(url)
        time.sleep(3)
        
        # Accept cookies
        try:
            cookie_btn = driver.find_element(By.ID, "cookie_consent_use_all_cookies")
            cookie_btn.click()
            time.sleep(1)
        except:
            pass
        
        # retrieve all matches links
        link_elements = driver.find_elements(By.CSS_SELECTOR, "a.text-decoration-none")
        match_links = []
        for elem in link_elements:
            href = elem.get_attribute("href")
            if href and "/cote/" in href:
                if href.startswith("/"):
                    href = "https://www.coteur.com" + href
                match_links.append(href)
        
        match_links = list(set(match_links))
        total_matches = len(match_links)
        print(f"{total_matches} matches found\n")
        
        # SCRAP ALL MATCHES
        matches_scraped = 0
        odds_sent = 0
        
        for i, match_url in enumerate(match_links, 1):
            print(f"\n{'='*60}")
            print(f"MATCH {i}/{len(match_links)}")
            print(f"{'='*60}")

            scraper_name = 'rugby.top14'
            
            try:
                driver.get(match_url)
                time.sleep(5)
                
                # Retrieve match title
                try:
                    title_element = driver.find_element(By.CSS_SELECTOR, ".page-title")
                    title = title_element.text.strip()
                    print(f"{title}")

                    send_progress_update(scraper_name, {
                        'status': 'running',
                        'current': i,
                        'total': total_matches,
                        'message': f'Scraping match {i}/{total_matches}',
                        'current_match': title,
                        'bookmakers_count': 0
                    })
                except:
                    print("Pas de titre, skip")
                    continue
                
                # Retrieve date
                date_obj = None
                try:
                    span_elems = driver.find_elements(By.CSS_SELECTOR, "span.small")
                    for span in span_elems:
                        text_content = span.get_attribute("textContent")
                        if text_content:
                            text_clean = re.sub(r'\s+', ' ', text_content).strip()
                            match_date = re.search(r'\d{1,2}\s\w+\s\d{4}\sà\s\d{1,2}:\d{2}', text_clean)
                            if match_date:
                                date_str = match_date.group()
                                date_obj = dateparser.parse(date_str)
                                break
                except:
                    pass
                
                # Retrieve all bookmakers
                rows = driver.find_elements(By.CSS_SELECTOR, ".d-flex[data-name]")
                bookmakers_count = len(rows)
                print(f"{bookmakers_count} bookmakers")

                send_progress_update(scraper_name, {
                    'status': 'running',
                    'current': i,
                    'total': total_matches,
                    'message': f'Scraping match {i}/{total_matches}',
                    'current_match': title,
                    'bookmakers_count': bookmakers_count
                })
                
                for row in rows:
                    bookmaker = row.get_attribute("data-name")
                    odds = row.find_elements(By.CSS_SELECTOR, ".border.odds-col")
                    
                    if len(odds) >= 3:
                        cote_dict = {
                            "cote_1": safe_float(odds[0].text.strip()),
                            "cote_N": safe_float(odds[1].text.strip()),
                            "cote_2": safe_float(odds[2].text.strip())
                        }
                        
                        # Calculate RTP
                        if cote_dict["cote_1"] and cote_dict["cote_N"] and cote_dict["cote_2"]:
                            trj = round((1 / (1/cote_dict["cote_1"] + 1/cote_dict["cote_N"] + 1/cote_dict["cote_2"])) * 100, 2)
                        else:
                            trj = None
                        
                        # Create message
                        message = {
                            "match": title,
                            "match_date": date_obj.strftime("%Y-%m-%d %H:%M:%S") if date_obj else None,
                            "bookmaker": bookmaker,
                            "cotes": cote_dict,
                            "trj": trj,
                            "league": "Top 14",
                            "sport": "rugby"
                        }
                        
                        # Send to RabbitMQ
                        channel.basic_publish(
                            exchange='',
                            routing_key='odds',
                            body=json.dumps(message),
                            properties=pika.BasicProperties(delivery_mode=2)
                        )
                        
                        print(f"{bookmaker}: {cote_dict['cote_1']}/{cote_dict['cote_N']}/{cote_dict['cote_2']} (TRJ: {trj}%)")
                        odds_sent += 1
                
                matches_scraped += 1
                
            except Exception as e:
                print(f"Erreur: {e}")
                continue

        send_progress_update(scraper_name, {
            'status': 'completed',
            'current': total_matches,
            'total': total_matches,
            'message': f'Scraping finished: {matches_scraped} matchs, {odds_sent} odds',
            'matches_scraped': matches_scraped,
            'odds_sent': odds_sent
        })
        
        print(f"\n{'='*60}")
        print(f"SCRAPING TERMINÉ")
        print(f"{'='*60}")
        print(f"Matchs scrapés: {matches_scraped}/{len(match_links)}")
        print(f"Cotes envoyées: {odds_sent}")
        print(f"{'='*60}\n")
        
        return {
            "status": "success",
            "matches_scraped": matches_scraped,
            "odds_sent": odds_sent
        }
        
    except Exception as e:
        print(f"\nERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        return None
        
    finally:
        if driver:
            driver.quit()
        if connection:
            connection.close()