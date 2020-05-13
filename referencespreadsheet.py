import gspread
from oauth2client.service_account import ServiceAccountCredentials
# from oauth2client.client import SignedJWTAssertionCredentials




# scope = ['https://spreadsheets.google.com/feeds']
scope = ['https://spreadsheets.google.com/feeds' + ' ' +'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# try:
#     book = client.open('Legislators 2017')
# except Exception as e:
#     print("Error opening the the Workbook. Stacktrace:\n{}".format(e))
        
# try:
#     sheet = book.sheet1
# except Exception as e:
#     print("Error opening the Sheet in the Workbook. Stacktrace:\n{}".format(e))


sheet = client.open('Legislators 2017').sheet1

legislators = sheet.get_all_records()

print("legislators Data Type: {}".format(type(legislators)))
print(legislators)
