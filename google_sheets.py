from googleapiclient.discovery import build
from google.oauth2 import service_account

# Path to your service account key file
SERVICE_ACCOUNT_FILE = 'path/to/your/service-account-file.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Initialize the Sheets API client
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)

SPREADSHEET_ID = '1DRscnQ3VQmTqlPq9ebLp2AxReKz2SOVFGbLq2wlte_U'
RANGE_NAME = 'Sheet1!A:D'

def save_user_data(username, email, mobile, payment_method):
    values = [[username, email, mobile, payment_method]]
    body = {
        'values': values
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption='RAW',
        body=body
    ).execute()
    return result

def get_user_data(username):
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME
    ).execute()
    values = result.get('values', [])
    for row in values:
        if row[0] == username:  # Assuming username is in the first column
            return {
                'username': row[0],
                'email': row[1],
                'mobile': row[2],
                'payment_method': row[3]
            }
    return None
