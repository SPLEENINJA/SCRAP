import argparse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time, csv

def run_selenium_scraper(dict_args):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.doctolib.fr")
    wait = WebDriverWait(driver, 10)

    try:
        reject_btn = driver.find_element(By.ID, "didomi-notice-disagree-button")
        reject_btn.click()
        reject_btn.click()
        wait.until(EC.invisibility_of_element_located((By.ID, "didomi-notice-disagree-button")))
    except:
        pass

    time.sleep(2)


    specialite = dict_args.get("specialite", "")
    code_postal = dict_args.get("code_postal", "")
    prix_min = int(dict_args.get("prix_min", 0))
    prix_max = int(dict_args.get("prix_max", 999))
    max_results = int(dict_args.get("max_results", 10))

    place_input = driver.find_element(By.CSS_SELECTOR, "input.searchbar-input.searchbar-place-input")
    place_input.clear()
    place_input.send_keys(code_postal)
    place_input.send_keys(Keys.ENTER)
    time.sleep(2)

    search_input = driver.find_element(By.CSS_SELECTOR, "input.searchbar-input.searchbar-main-input")
    search_input.send_keys(specialite)
    search_input.send_keys(Keys.ENTER)
    time.sleep(5)

    wait.until(EC.element_to_be_clickable(By.CSS_SELECTOR("span button")))
    reject_btn.click((By.CSS_SELECTOR("span button")))

    time.sleep(10)

    practitioners = driver.find_elements(By.CSS_SELECTOR, "div.dl-search-result-presentation")
    time.sleep(5)

    # Résultats
    practitioners = driver.find_elements(By.CSS_SELECTOR, "div.dl-search-result-presentation")

    with open("resultats_medecins.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Nom", "Adresse", "Disponibilité", "Consultation", "Secteur", "Prix"])

        for p in practitioners[:args.max_results]:
            try:
                nom = p.find_element(By.CSS_SELECTOR, "h3").text
            except:
                nom = ""
            try:
                adresse = p.find_element(By.CSS_SELECTOR, "div.address").text
            except:
                adresse = ""
            try:
                dispo = p.find_element(By.CSS_SELECTOR, "div.availability").text
            except:
                dispo = ""
            try:
                consultation = p.find_element(By.CSS_SELECTOR, "div.activity-type").text
            except:
                consultation = ""
            try:
                secteur = p.find_element(By.XPATH, ".//div[contains(text(),'Secteur')]").text
            except:
                secteur = ""
            try:
                prix = p.find_element(By.XPATH, ".//div[contains(text(),'€')]").text
            except:
                prix = ""

            writer.writerow([nom, adresse, dispo, consultation, secteur, prix])

    driver.quit()
    print("CSV FAIT")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--specialite", type=str, required=True)
    parser.add_argument("--code_postal", type=str, required=True)
    parser.add_argument("--max_results", type=int, default=10)
    parser.add_argument("--date_debut", type=str)
    parser.add_argument("--date_fin", type=str)
    parser.add_argument("--assurance", type=str)
    parser.add_argument("--consultation", type=str)
    parser.add_argument("--prix_min", type=int)
    parser.add_argument("--prix_max", type=int)

    cli_args = vars(parser.parse_args())
    run_selenium_scraper(cli_args)

#