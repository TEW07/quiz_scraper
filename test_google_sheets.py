from oauth2client.service_account import ServiceAccountCredentials
import gspread

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("leaderboard_credentials.json", scope)
client = gspread.authorize(creds)

sheet = client.open("TestLeader").sheet1 

data = sheet.get_all_values()[:6]  
print("First 5 rows of the sheet:")
for row in data:
    print(row)
