from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import gspread
from  gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials
import time
import datetime

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("leaderboard_credentials.json", scope)
client = gspread.authorize(creds)

SHEET_NAME = "QOTD Leaderboard"  
sheet = client.open(SHEET_NAME).sheet1  

fmt = cellFormat(
    backgroundColor=color(1, 1, 1),
    textFormat=textFormat(
        bold=False,
        foregroundColor=color(0, 0, 0)
    ),
    horizontalAlignment='CENTER',
    borders=Borders(
        top=Border('SOLID', color(0, 0, 0)),
        bottom=Border('SOLID', color(0, 0, 0)),
        left=Border('SOLID', color(0, 0, 0)),
        right=Border('SOLID', color(0, 0, 0))
    ))

today_date = datetime.datetime.today().strftime("%d-%m-%Y")

existing_dates = sheet.col_values(2)[5:] 

print("Existing dates in sheet:", existing_dates)
print("Today's date:", today_date)

if today_date in existing_dates:
    print(f"Data for {today_date} already exists. Skipping update.")
    exit(0)

used_rows = set()
for col in range(2, 10):  # Columns B to I (2 to 9)
    col_data = sheet.col_values(col)
    used_rows.update(range(6, len(col_data) + 1))

next_row = 6
while next_row in used_rows:
    next_row += 1

print("Next available row for new data:", next_row)

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
    score = leaderboard.get(player, "-")
    if score.isdigit():  
        new_row.append(int(score))  
    else:
        new_row.append(score)  


print("New row to be added:", new_row)

sheet.update(f"B{next_row}:I{next_row}", [new_row])
format_cell_range(sheet, f"B{next_row}:I{next_row}", fmt)

print(f"Successfully added scores for {today_date} in row {next_row}.")



