from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")  
chrome_options.add_argument("--disable-dev-shm-usage")  

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://quizoftheday.co.uk/league/ZE2TJ06KZZ2048")
time.sleep(5)

rows = driver.find_elements(By.CSS_SELECTOR, "#leagueScores tbody tr")
for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    initials = cells[0].text
    score = cells[1].text
    print(f"Initials: {initials}, Score: {score}")

driver.quit()


