from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import datetime

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("leaderboard_credentials.json", scope)
client = gspread.authorize(creds)

SHEET_NAME = "QOTD Leaderboard"  
sheet = client.open(SHEET_NAME).sheet1  

today_date = datetime.datetime.today().strftime("%d-%m-%Y")  # UK format (DD-MM-YYYY)
existing_data = sheet.get_all_values()


existing_dates = sheet.col_values(2)[1:]  # Skip the header row

print("Existing dates in sheet:", existing_dates)
print("Today's date:", today_date)

if today_date in existing_dates:
    print(f"Data for {today_date} already exists. Skipping update.")
    exit(0)




chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")  
chrome_options.add_argument("--disable-dev-shm-usage")  

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

URL = "https://quizoftheday.co.uk/league/ZE2TJ06KZZ2048"
driver.get(URL)
time.sleep(5)

rows = driver.find_elements(By.CSS_SELECTOR, "#leagueScores tbody tr")
leaderboard = {}
for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    initials = cells[0].text.strip().upper()
    score = cells[1].text.strip()
    leaderboard[initials] = score

driver.quit()


expected_players = ["EM", "LG", "RH", "SG", "SH", "TM", "TW"]

new_row = [today_date]  
for player in expected_players:
    new_row.append(leaderboard.get(player, "-")) 

print("New row to be added:", new_row)

sheet.append_row(new_row, value_input_option="USER_ENTERED")
print(f"Successfully added scores for {today_date}.")


