import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import current_app
from ..utils.logger import log_info, log_error, log_success
import json

class SheetsService:
    def __init__(self):
        self.client = None
        self.sheet = None
        self._initialized = False

    def _ensure_initialized(self):
        """Ensure the service is initialized with app context."""
        if not self._initialized:
            with current_app.app_context():
                self.initialize_client()
                self._initialized = True

    def initialize_client(self):
        """Initialize Google Sheets client."""
        try:
            scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                current_app.config['GOOGLE_SHEETS_CREDENTIALS'],
                scope
            )
            self.client = gspread.authorize(credentials)
            self.sheet = self.client.open("CDS").sheet1
            log_info("Google Sheets client initialized successfully")
        except Exception as e:
            log_error(f"Error initializing Google Sheets client: {str(e)}")
            self.client = None
            self.sheet = None

    def export_trades(self, trades, tag):
        """Export trades to Google Sheets."""
        self._ensure_initialized()
        if not self.sheet:
            log_error("Google Sheets client not initialized")
            return False

        try:
            # Prepare data
            data = []
            for trade in trades:
                row = [
                    trade.get('order_id', ''),
                    trade.get('account_id', ''),
                    trade.get('tradingsymbol', ''),
                    trade.get('quantity', ''),
                    trade.get('price', ''),
                    trade.get('order_type', ''),
                    trade.get('product', ''),
                    trade.get('timestamp', ''),
                    tag
                ]
                data.append(row)

            # Append to sheet
            self.sheet.append_rows(data)
            log_success(f"Successfully exported {len(trades)} trades to Google Sheets")
            return True
        except Exception as e:
            log_error(f"Error exporting trades to Google Sheets: {str(e)}")
            return False

    def get_all_tags(self):
        """Get all tags from the sheet."""
        self._ensure_initialized()
        if not self.sheet:
            return []

        try:
            # Get all values from the tag column (last column)
            all_values = self.sheet.get_all_values()
            if not all_values:
                return []

            # Extract unique tags
            tags = set()
            for row in all_values[1:]:  # Skip header
                if row and row[-1]:  # Check if row exists and has a tag
                    tags.add(row[-1])
            return sorted(list(tags))
        except Exception as e:
            log_error(f"Error getting tags from Google Sheets: {str(e)}")
            return [] 