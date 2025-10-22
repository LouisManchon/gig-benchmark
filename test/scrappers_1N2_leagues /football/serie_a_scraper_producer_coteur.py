import time
import json
import pika
import dateparser
import re
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

def safe_float(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return None


def perform_scrapping():

    # --- Selenium ---
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # --- URL Seria A ---
    url = "https://www.coteur.com/cotes/foot/italie/serie-a"
    driver.get(url)
    try:
        # wait charging page
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".d-flex[data-name]"))
        )
    except Exception:
        None


    # had match links
    link_elements = driver.find_elements(By.CSS_SELECTOR, "a.text-decoration-none")
    match_links = []
    for elem in link_elements:
        href = elem.get_attribute("href")
        if href:
            if href.startswith("/"):
                href = "https://www.coteur.com" + href
            match_links.append(href)

    print(f"Number of matchs : {len(match_links)}")


    # browse matches
    for match_url in match_links:
        try:
            driver.get(match_url)
            time.sleep(3)

            try:
                title_element = driver.find_element(By.CSS_SELECTOR, ".page-title")
                title = title_element.text.strip()
                print("Match name :", title)

            except Exception as e:
                print("Error, no match name :", e)
                title = None

            # match date
            date_obj = None
            try:
                    span_elems = driver.find_elements(By.CSS_SELECTOR, "span.small")

                    for idx, span in enumerate(span_elems):
                        text_content = span.get_attribute("textContent")

                        if not text_content or text_content.strip() == "":
                            continue

                        # clean spaces
                        text_clean = re.sub(r'\s+', ' ', text_content).strip()

                        # search date with regex
                        match = re.search(r'\d{1,2}\s\w+\s\d{4}\sà\s\d{1,2}:\d{2}', text_clean)
                        if match:
                            date_str = match.group()
                            date_obj = dateparser.parse(date_str)
                            break

                    if not date_obj:
                        print("Error: No date match.")
            except Exception as e:
                    print("Error: date can't be parsed.", e)

            # name match
            # match_elem = driver.find_element(By.CSS_SELECTOR, ".page-title")
            # match_name = match_elem.text.strip()

            # name bookmakers
            rows = driver.find_elements(By.CSS_SELECTOR, ".d-flex[data-name]")
            for row in rows:
                bookmaker = row.get_attribute("data-name")
                odds = row.find_elements(By.CSS_SELECTOR, ".border.odds-col")
                try:
                    payout_elem = driver.find_element(By.CSS_SELECTOR, "div.border.bg-warning.payout")
                    payout = payout_elem.text.strip()
                except:
                    payout = None

                cote_dict = {}
                if len(odds) >= 3:
                    cote_dict["cote_1"] = safe_float(odds[0].text.strip())
                    cote_dict["cote_N"] = safe_float(odds[1].text.strip())
                    cote_dict["cote_2"] = safe_float(odds[2].text.strip())

                # trj calcul

                if cote_dict["cote_1"] and cote_dict["cote_N"] and cote_dict["cote_2"]:
                    trj = round((1 / (1/cote_dict["cote_1"] + 1/cote_dict["cote_N"] + 1/cote_dict["cote_2"])) * 100, 2)
                else:
                    trj = None

                # publish in Rabbit
                message = {
                    "match": title,
                    "match_date": date_obj.strftime("%Y-%m-%d %H:%M:%S") if date_obj else None,
                    "bookmaker": bookmaker,
                    "cotes": cote_dict,
                    "trj": trj,
                    "league": "Serie A",
                    "sport": "football"
                }
                channel.basic_publish(exchange="", routing_key="odds", body=json.dumps(message))
                print(f"📤 Send : {message}")

        except Exception as e:
            print("⚠️ Error scraping :", e)

    driver.quit()
    connection.close()

perform_scrapping()
