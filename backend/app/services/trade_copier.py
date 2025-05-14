import json
from flask import current_app
from ..utils.logger import log_info, log_error, log_success
from .kite_service import KiteService
import time

class TradeCopier:
    def __init__(self, kite_service):
        self.kite_service = kite_service
        self.is_replicating = False
        self._initialized = False
        self.allowed_types = {
            "order_types": ["MARKET", "LIMIT", "SL"],
            "product_types": ["MIS", "NRML"]
        }

    def _ensure_initialized(self):
        """Ensure the service is initialized with app context."""
        if not self._initialized:
            with current_app.app_context():
                self.load_allowed_order_types()
                self._initialized = True

    def load_allowed_order_types(self):
        """Load allowed order types from config file."""
        try:
            with open(current_app.config['ALLOWED_ORDER_TYPES_PATH'], 'r') as f:
                self.allowed_types = json.load(f)[0]
            log_info("Allowed order types loaded successfully")
        except Exception as e:
            log_error(f"Error loading allowed order types: {str(e)}")

    def is_order_allowed(self, order):
        """Check if an order type is allowed for replication."""
        self._ensure_initialized()
        return (
            order.get('order_type') in self.allowed_types['order_types'] and
            order.get('product') in self.allowed_types['product_types']
        )

    def start_replication(self):
        """Start trade replication."""
        self._ensure_initialized()
        self.is_replicating = True
        log_info("Trade replication started")

    def stop_replication(self):
        """Stop trade replication."""
        self._ensure_initialized()
        self.is_replicating = False
        log_info("Trade replication stopped")

    def on_order_update(self, order):
        """Handle order updates from primary account."""
        self._ensure_initialized()
        if not self.is_replicating:
            return

        if not self.is_order_allowed(order):
            log_info(f"Order {order.get('order_id')} skipped - type not allowed")
            return

        primary_account = self.kite_service.get_primary_account()
        if not primary_account:
            log_error("No primary account found")
            return

        # Skip if order is not from primary account
        if order.get('account_id') != primary_account:
            return

        # Replicate to other accounts
        for account_id, account in self.kite_service.accounts.items():
            if account_id == primary_account:
                continue

            # Scale quantity based on multiplier
            quantity = int(order.get('quantity', 0) * account.get('ps_multiplier', 1.0))
            if quantity == 0:
                continue

            # Prepare order parameters
            order_params = {
                'tradingsymbol': order.get('tradingsymbol'),
                'exchange': order.get('exchange'),
                'transaction_type': order.get('transaction_type'),
                'quantity': quantity,
                'order_type': order.get('order_type'),
                'product': order.get('product'),
                'price': order.get('price', 0)
            }

            # Add trigger price for SL orders
            if order.get('order_type') == 'SL':
                order_params['trigger_price'] = order.get('trigger_price')

            # Retry logic
            max_retries = 2
            for attempt in range(max_retries + 1):
                try:
                    order_id = self.kite_service.place_order(account_id, order_params)
                    if order_id:
                        log_success(
                            f"Order {order.get('order_id')} replicated to {account_id} "
                            f"as {order_id}"
                        )
                        break
                except Exception as e:
                    if attempt == max_retries:
                        log_error(
                            f"Failed to replicate order {order.get('order_id')} "
                            f"to {account_id} after {max_retries} attempts: {str(e)}"
                        )
                    else:
                        time.sleep(1)  # Wait before retry 