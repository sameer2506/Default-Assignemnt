import string

import gspread as gspread
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account


class GoogleSheetManager:
    credentials = ""
    sheet_id = ""
    client = None
    DEFAULT_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    def __init__(self, credentials_path, sheet_id, scopes=DEFAULT_SCOPES):
        self.sheet_id = sheet_id
        self._init_credentials(credentials_path=credentials_path, scopes=scopes)

    def _init_credentials(self, credentials_path, scopes):
        self.credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=scopes)
        self.client = gspread.Client(auth=self.credentials)

    def start_session(self):
        self.client.session = AuthorizedSession(self.credentials)

    def close_session(self):
        if self.client.session is not None:
            self.client.session.close()

    def _get_worksheet(self, wsheet_number):
        sheet = self.client.open_by_key(self.sheet_id)
        worksheet = sheet.get_worksheet(wsheet_number)
        return worksheet

    @staticmethod
    def _build_range(row_number, col_count):
        range_text = "A{0}:{1}{2}".format(row_number, string.ascii_uppercase[col_count - 1], row_number)
        return range_text

    # Create methods

    def append_rows(self, row_values, worksheet_number=0):
        worksheet = self._get_worksheet(worksheet_number)
        return worksheet.append_rows(row_values)
