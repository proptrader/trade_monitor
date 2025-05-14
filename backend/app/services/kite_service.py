from kiteconnect import KiteConnect, KiteTicker
import json
from flask import current_app
from ..utils.logger import log_info, log_error, log_success
import time
import traceback

class KiteService:
    def __init__(self):
        self.accounts = {}
        self.tickers = {}
        self._initialized = False

    def _ensure_initialized(self):
        """Ensure the service is initialized with app context."""
        if not self._initialized:
            with current_app.app_context():
                self.load_accounts()
                self._initialized = True

    def load_accounts(self):
        """Load accounts from config file."""
        log_info("[KiteService] Loading accounts from config file...")
        try:
            with open(current_app.config['ACCOUNTS_CONFIG_PATH'], 'r') as f:
                self.accounts = {acc['account_id']: acc for acc in json.load(f)}
            log_info(f"[KiteService] Accounts loaded: {[a for a in self.accounts.keys()]}")
        except Exception as e:
            log_error(f"[KiteService] Error loading accounts: {str(e)}\n{traceback.format_exc()}")
            self.accounts = {}

    def save_accounts(self):
        """Save accounts to config file."""
        log_info("[KiteService] Saving accounts to config file...")
        try:
            with open(current_app.config['ACCOUNTS_CONFIG_PATH'], 'w') as f:
                json.dump(list(self.accounts.values()), f, indent=2)
            log_info(f"[KiteService] Accounts saved: {[a for a in self.accounts.keys()]}")
        except Exception as e:
            log_error(f"[KiteService] Error saving accounts: {str(e)}\n{traceback.format_exc()}")

    def connect_account(self, account_id, request_token):
        """Connect to a Kite account using request token."""
        self._ensure_initialized()
        log_info(f"[KiteService] Attempting to connect account: {account_id}")
        try:
            account = self.accounts.get(account_id)
            if not account:
                log_error(f"[KiteService] Account {account_id} not found in config.")
                raise ValueError(f"Account {account_id} not found")

            log_info(f"[KiteService] Using API key: {account['api_key']} for account: {account_id}")
            log_info(f"[KiteService] Request token received for account {account_id}: {bool(request_token)}")
            kite = KiteConnect(api_key=account['api_key'])
            log_info(f"[KiteService] Calling generate_session for account: {account_id}")
            data = kite.generate_session(
                request_token=request_token,
                api_secret=account['secret_api_key']
            )
            log_info(f"[KiteService] generate_session successful for account: {account_id}")
            
            account['access_token'] = data['access_token']
            account['request_token'] = request_token
            self.save_accounts()
            
            log_success(f"[KiteService] Successfully connected account {account_id}")
            return True
        except Exception as e:
            log_error(f"[KiteService] Error connecting account {account_id}: {str(e)}\n{traceback.format_exc()}")
            return False

    def get_kite_instance(self, account_id):
        """Get KiteConnect instance for an account."""
        self._ensure_initialized()
        account = self.accounts.get(account_id)
        if not account or not account.get('access_token'):
            return None

        try:
            kite = KiteConnect(api_key=account['api_key'])
            kite.set_access_token(account['access_token'])
            return kite
        except Exception as e:
            log_error(f"Error creating Kite instance for {account_id}: {str(e)}")
            return None

    def start_ticker(self, account_id, on_order_update):
        """Start KiteTicker for an account."""
        self._ensure_initialized()
        account = self.accounts.get(account_id)
        if not account or not account.get('access_token'):
            return False

        try:
            kite = self.get_kite_instance(account_id)
            if not kite:
                return False

            ticker = KiteTicker(account['api_key'], account['access_token'])
            ticker.on_order_update = on_order_update
            ticker.connect(threaded=True)
            self.tickers[account_id] = ticker
            log_success(f"Started ticker for account {account_id}")
            return True
        except Exception as e:
            log_error(f"Error starting ticker for {account_id}: {str(e)}")
            return False

    def stop_ticker(self, account_id):
        """Stop KiteTicker for an account."""
        self._ensure_initialized()
        ticker = self.tickers.get(account_id)
        if ticker:
            try:
                ticker.close()
                del self.tickers[account_id]
                log_info(f"Stopped ticker for account {account_id}")
            except Exception as e:
                log_error(f"Error stopping ticker for {account_id}: {str(e)}")

    def place_order(self, account_id, order_params):
        """Place an order for an account."""
        self._ensure_initialized()
        kite = self.get_kite_instance(account_id)
        if not kite:
            return None

        try:
            order_id = kite.place_order(**order_params)
            log_success(f"Order placed successfully for account {account_id}")
            return order_id
        except Exception as e:
            log_error(f"Error placing order for {account_id}: {str(e)}")
            return None

    def get_primary_account(self):
        """Get the primary account ID."""
        self._ensure_initialized()
        for account_id, account in self.accounts.items():
            if account.get('primary'):
                return account_id
        return None

    def get_trades_for_account(self, account_id):
        """
        Fetches all executed trades for the given account using the Kite API.
        - No date filtering is needed; Kite API returns only current date's trades.
        - Handles authentication, logging, and error checking.
        - Returns a list of trades in the format expected by the frontend.
        """
        self._ensure_initialized()
        account = self.accounts.get(account_id)
        if not account or not account.get('access_token'):
            log_error(f"[KiteService] No access token for account {account_id}")
            return []
        try:
            kite = self.get_kite_instance(account_id)
            if not kite:
                log_error(f"[KiteService] Could not get Kite instance for {account_id}")
                return []
            all_orders = kite.orders()
            trades = [
                {
                    "trade_id": order["order_id"],
                    "account_id": account_id,
                    "symbol": order["tradingsymbol"],
                    "quantity": order["quantity"],
                    "price": order["average_price"],
                    "order_type": order["order_type"],
                    "product_type": order["product"],
                    "timestamp": str(order["order_timestamp"]),
                }
                for order in all_orders
                if order["status"] == "COMPLETE"
            ]
            log_info(f"[KiteService] Fetched {len(trades)} trades for account {account_id}")
            return trades
        except Exception as e:
            log_error(f"[KiteService] Error fetching trades for account {account_id}: {str(e)}")
            return [] 