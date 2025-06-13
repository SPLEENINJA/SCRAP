from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
 
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://www.doctolib.fr/")
 
 
try :
    reject_btn = driver.find_element(By.ID, "didomi-notice-disagree-button")
    reject_btn.click()
except:
    pass

time.sleep(2)
place_input = driver.find_element(By.CSS_SELECTOR, "input.searchbar-input.searchbar-place-input")
place_input.clear()
place_input.send_keys("75001")
place_input.send_keys(Keys.ENTER)
time.sleep(3)
 
total_results = driver.find_element(By.CSS_SELECTOR, "div[data-test='total-number-of-results']")
print("Found results count: ", total_results.text)
driver.quit()
 
 
 