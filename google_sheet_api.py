import os
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# The ID and range of your spreadsheet.
load_dotenv()
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
RANGE_NAME = 'Sheet1!A:C' # A, B, C for 'name', 'age', 'occupation'

class GoogleSheetsAPI:
    service = None

    def __init__(self):
        self.service = self.get_google_sheets_service()
        if not self.service:
            raise RuntimeError("Failed to initialize Google Sheets service.")

    def get_google_sheets_service(self):
        """
        Authenticates and returns a service object to interact with the Google Sheets API.
        This function should be called once to get the service object for all subsequent
        API calls.
        """
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        creds = None
        token_path = 'google_tokens/token.json'
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0, open_browser=False)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('sheets', 'v4', credentials=creds)
            return service
        except Exception as error:
            print(f"An error occurred: {error}")
            return None

    def find_person_by_name(self, name_to_find):
        """
        Checks if a name exists in the spreadsheet.
        Returns the person's data as a dictionary if found, otherwise returns None.
        """
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        values = result.get('values', [])
        
        if not values:
            return None

        headers = values[0]
        existing_rows = values[1:]
        
        try:
            name_col_index = headers.index('name')
        except ValueError:
            print("Error: 'name' column not found in the sheet headers.")
            return None

        for row in existing_rows:
            if len(row) > name_col_index and row[name_col_index].lower() == name_to_find.lower():
                return dict(zip(headers, row))
        
        return None

    def insert_person_data(self, name, age=None, occupation=None):
        """
        Checks if a person exists by name. If not, it inserts a new entry.
        Returns the person's data if found, or the newly inserted data.
        """
        found_person = self.find_person_by_name(name)

        if found_person:
            raise ValueError(f"Person '{name}' already exists in the sheet.")
        else:
            if age is None or occupation is None:
                raise ValueError("Age and Occupation must be provided for a new entry.")
            
            new_row = [name, age, occupation]
            body = {'values': [new_row]}
            sheet = self.service.spreadsheets()
            result = sheet.values().append(
                spreadsheetId=SPREADSHEET_ID,
                range=RANGE_NAME,
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            if result.get('updates', {}).get('updatedRows', 0) > 0:
                return {"name": name, "age": age, "occupation": occupation}
            else:
                raise RuntimeError("Failed to insert new person data.")


# --- Main script execution ---
if __name__ == '__main__':
    try:
        google_sheets = GoogleSheetsAPI()
        # Example 1: Check for an existing person
        person_to_check = "John Doe"
        found_data = google_sheets.find_person_by_name(person_to_check)
        print(f"\nResult of checking for '{person_to_check}':")
        print(found_data)

        # Example 2: Add a new person
        new_person_data = google_sheets.insert_person_data(
            name="Mary Johnsonnn", 
            age=25, 
            occupation="Data Scientist"
        )
        print(f"\nResult of adding new person:")
        print(new_person_data)

        # Example 3: Try to add a new person without providing all required info
        try:
            google_sheets.insert_person_data(name="Incomplete Entry")
        except ValueError as e:
            print(f"\nCorrectly caught an error: {e}")
    except Exception as e:
        print(f"An error occurred during execution: {e}")