import gspread
from  gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials
import datetime

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("leaderboard_credentials.json", scope)
client = gspread.authorize(creds)

SHEET_NAME = "QOTD Leaderboard"  

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


sheet = client.open(SHEET_NAME).sheet1  

today_date = datetime.datetime.today().strftime("%d-%m-%Y")

existing_dates = sheet.col_values(2)[5:] 

print("Existing dates in sheet:", existing_dates)
print("Today's date:", today_date)

if today_date in existing_dates:
    print(f"Data for {today_date} already exists. Skipping update.")
    exit(0)

used_rows = set()
for col in range(2, 10):
    col_data = sheet.col_values(col)
    used_rows.update(range(6, len(col_data) + 1))

next_row = 6
while next_row in used_rows:
    next_row += 1

print("Next available row for new data:", next_row)


print("\n TESTING MODE: Using dummy data instead of scraping\n")

leaderboard = {
    "EM": "7",
    "LG": "8", 
    "RH": "6",
    "SG": "9",
    "SH": "7",
    "TM": "8",
    "TW": "5"
}

expected_players = ["EM", "LG", "RH", "SG", "SH", "TM", "TW"]

new_row = [today_date]  
for player in expected_players:
    score = leaderboard.get(player, "-")
    if score.isdigit():  
        new_row.append(int(score))  
    else:
        new_row.append(score)  

print("new_row Type: \n", type(new_row), "new_row: ", new_row)
print("New row to be added:", new_row)

sheet.update(f"B{next_row}:I{next_row}", [new_row])
format_cell_range(sheet, f"B{next_row}:I{next_row}", fmt)