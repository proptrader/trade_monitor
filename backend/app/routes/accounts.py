from flask import Blueprint, jsonify, request, current_app
from ..services.kite_service import KiteService
from ..utils.logger import log_info, log_error, log_success

bp = Blueprint('accounts', __name__, url_prefix='/api/accounts')
kite_service = KiteService()

@bp.route('/', methods=['GET'])
def get_accounts():
    """Get all accounts."""
    try:
        kite_service._ensure_initialized()
        accounts = list(kite_service.accounts.values())
        return jsonify(accounts)
    except Exception as e:
        log_error(f"Error getting accounts: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/<account_id>/connect', methods=['POST'])
def connect_account(account_id):
    """Connect to a Kite account."""
    try:
        request_token = request.json.get('request_token')
        if not request_token:
            return jsonify({"error": "Request token is required"}), 400

        if kite_service.connect_account(account_id, request_token):
            return jsonify({"message": "Account connected successfully"})
        else:
            return jsonify({"error": "Failed to connect account"}), 500
    except Exception as e:
        log_error(f"Error connecting account {account_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/<account_id>', methods=['PUT'])
def update_account(account_id):
    """Update account details."""
    try:
        account = kite_service.accounts.get(account_id)
        if not account:
            return jsonify({"error": "Account not found"}), 404

        data = request.json
        if 'request_token' in data:
            if kite_service.connect_account(account_id, data['request_token']):
                return jsonify({"message": "Account updated successfully"})
            else:
                return jsonify({"error": "Failed to update account"}), 500
        else:
            return jsonify({"error": "No valid update data provided"}), 400
    except Exception as e:
        log_error(f"Error updating account {account_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500 