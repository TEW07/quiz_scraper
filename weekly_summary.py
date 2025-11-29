import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("leaderboard_credentials.json", scope)
client = gspread.authorize(creds)

SHEET_NAME = "QOTD Leaderboard"
sheet = client.open(SHEET_NAME).sheet1

print("✅ Successfully connected to Google Sheets!")
print(f"📊 Sheet name: {sheet.title}")
print(f"📊 Total rows: {sheet.row_count}")
print(f"📊 Total columns: {sheet.col_count}")
cell = sheet.find("TM")
print(cell)