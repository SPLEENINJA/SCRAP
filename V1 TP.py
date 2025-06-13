from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://www.doctolib.fr")
wait = WebDriverWait(driver, 10)


try:
    reject_btn = driver.find_element(By.ID, "didomi-notice-disagree-button")
    reject_btn.click()
except:
    pass

# 3. Simulation de la recherche
time.sleep(2)
place_input = driver.find_element(By.CSS_SELECTOR, "input.searchbar-input.searchbar-place-input")
place_input.clear()
place_input.send_keys("75001")  # Code postal
time.sleep(2)
place_input.send_keys(Keys.TAB)
search_input = driver.find_element(By.CSS_SELECTOR, "input.searchbar-input.searchbar-query-input")
search_input.send_keys("dermato")
place_input.send_keys(Keys.TAB)
place_input.send_keys(Keys.ENTER)
total_results = wait.until(EC.presence_of_element_located((
    By.CSS_SELECTOR,
    "div[data-test='total-number-of-results']"
)))
 
print("Nombre de praticiens : ", total_results.text)
 
time.sleep(50)
 
driver.quit()
 # Attente du chargement des résultats

# # 4. Extraction des cartes de résultats
# practitioners = driver.find_elements(By.CSS_SELECTOR, "div.dl-search-result-presentation")

# # 5. Préparation des données CSV
# with open("medecins.csv", "w", newline='', encoding='utf-8') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow([
#         "Nom", "Disponibilité", "Consultation", "Secteur", "Prix", "Rue", "Code Postal", "Ville"
#     ])

#     for p in practitioners[:10]:  # Limite à 10 praticiens
#         try:
#             nom = p.find_element(By.CSS_SELECTOR, "h3").text
#         except:
#             nom = ""

#         try:
#             dispo = p.find_element(By.CSS_SELECTOR, "div.availability").text
#         except:
#             dispo = ""

#         try:
#             consultation = p.find_element(By.CSS_SELECTOR, "div.activity-type").text
#         except:
#             consultation = ""

#         try:
#             secteur = p.find_element(By.XPATH, ".//div[contains(text(),'Secteur')]").text
#         except:
#             secteur = ""

#         try:
#             prix = p.find_element(By.XPATH, ".//div[contains(text(),'€')]").text
#         except:
#             prix = ""

#         try:
#             adresse = p.find_element(By.CSS_SELECTOR, "div.address").text
#             lignes = adresse.split(",")
#             rue = lignes[0].strip() if len(lignes) > 0 else ""
#             cp_ville = lignes[1].strip().split(" ") if len(lignes) > 1 else ["", ""]
#             code_postal = cp_ville[0]
#             ville = " ".join(cp_ville[1:]) if len(cp_ville) > 1 else ""
#         except:
#             rue = code_postal = ville = ""

#         writer.writerow([nom, dispo, consultation, secteur, prix, rue, code_postal, ville])

# driver.quit()
