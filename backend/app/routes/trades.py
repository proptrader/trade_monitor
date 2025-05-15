from flask import Blueprint, jsonify, request, current_app, Response
from ..services.kite_service import KiteService
from ..services.trade_copier import TradeCopier
from ..services.sheets_service import SheetsService
from ..utils.logger import log_info, log_error, log_success
import json
import time
from datetime import datetime

bp = Blueprint('trades', __name__, url_prefix='/api/trades')
kite_service = KiteService()
trade_copier = TradeCopier(kite_service)
sheets_service = SheetsService()

# Store trades in memory (in a real app, use a database)
trades = []

@bp.route('/', methods=['GET'])
def get_trades():
    """Get all trades."""
    try:
        return jsonify(trades)
    except Exception as e:
        log_error(f"Error getting trades: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/stream', methods=['GET'])
def stream_trades():
    """Stream trades via SSE."""
    def generate():
        while True:
            # Get new trades
            new_trades = [trade for trade in trades if trade.get('timestamp', 0) > time.time() - 1]
            if new_trades:
                yield f"data: {json.dumps({'type': 'live_trade', 'trades': new_trades})}\n\n"
            time.sleep(1)

    return Response(generate(), mimetype='text/event-stream')

@bp.route('/history', methods=['GET'])
def get_trade_history():
    """Get trade history for an account using Kite API."""
    try:
        account_id = request.args.get('account_id')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 50))
        if not account_id:
            log_error("[Trades API] Account ID is required for trade history.")
            return jsonify({"error": "Account ID is required"}), 400
        trades = kite_service.get_trades_for_account(account_id)
        # Sort by timestamp (newest first)
        trades.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
        # Paginate
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_trades = trades[start_idx:end_idx]
        log_info(f"[Trades API] Returning {len(paginated_trades)} trades for account {account_id} (page {page})")
        return jsonify({
            'trades': paginated_trades,
            'has_more': end_idx < len(trades),
            'total': len(trades)
        })
    except Exception as e:
        log_error(f"[Trades API] Error getting trade history: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/replicate', methods=['POST'])
def start_replication():
    """Start trade replication."""
    try:
        primary_account = kite_service.get_primary_account()
        if not primary_account:
            return jsonify({"error": "No primary account found"}), 400

        # Start ticker for primary account
        if not kite_service.start_ticker(primary_account, trade_copier.on_order_update):
            return jsonify({"error": "Failed to start ticker"}), 500

        trade_copier.start_replication()
        return jsonify({"message": "Trade replication started"})
    except Exception as e:
        log_error(f"Error starting trade replication: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/stop', methods=['POST'])
def stop_replication():
    """Stop trade replication."""
    try:
        primary_account = kite_service.get_primary_account()
        if primary_account:
            kite_service.stop_ticker(primary_account)

        trade_copier.stop_replication()
        return jsonify({"message": "Trade replication stopped"})
    except Exception as e:
        log_error(f"Error stopping trade replication: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/export', methods=['POST'])
def export_trades():
    """Export selected trades to Google Sheets by trade ID (fetching from Kite API)."""
    try:
        log_info("[Export API] Export request received")
        
        # Check content type to handle both JSON and form data
        if request.is_json:
            log_info("[Export API] Processing JSON request")
            data = request.json
            trade_ids = data.get('trades', [])
            tag = data.get('tag')
            account_id = data.get('account_id')
        else:
            log_info("[Export API] Processing form data request")
            # Handle form data
            trade_ids = request.form.get('trades', '')
            tag = request.form.get('tag', '')
            account_id = request.form.get('account_id', '')
            
            # Handle different trade_ids formats
            if trade_ids:
                if isinstance(trade_ids, str):
                    # Try to parse as JSON first
                    try:
                        trade_ids = json.loads(trade_ids)
                        log_info(f"[Export API] Parsed trade_ids from JSON string: {len(trade_ids)} trades")
                    except json.JSONDecodeError:
                        # If not JSON, try comma-separated string
                        if ',' in trade_ids:
                            trade_ids = [id.strip() for id in trade_ids.split(',') if id.strip()]
                            log_info(f"[Export API] Parsed trade_ids from comma-separated string: {len(trade_ids)} trades")
                        else:
                            # Single trade ID
                            trade_ids = [trade_ids]
                            log_info(f"[Export API] Using single trade ID: {trade_ids[0]}")
                else:
                    log_error("[Export API] Unexpected trade_ids format")
                    trade_ids = []
        
        # Log the received data
        log_info(f"[Export API] Received data - tag: {tag}, account_id: {account_id}, trade_ids count: {len(trade_ids) if trade_ids else 0}")
        
        # Validate request data
        if not trade_ids:
            log_error("[Export API] No trades selected")
            return jsonify({"error": "No trades selected"}), 400
        if not tag:
            log_error("[Export API] Tag is required")
            return jsonify({"error": "Tag is required"}), 400
        
        # If no account ID is provided, try to determine from the trades
        if not account_id:
            log_info("[Export API] No account ID provided, attempting to find from trade data")
            # Try to get account ID from the first trade if available
            all_accounts = kite_service.get_active_accounts()
            if all_accounts:
                account_id = all_accounts[0]['account_id']
                log_info(f"[Export API] Using first active account: {account_id}")
            else:
                log_error("[Export API] No active accounts found")
                return jsonify({"error": "No active account available"}), 400
            
        # Log account active status
        account = next((acc for acc in kite_service.get_active_accounts() if acc['account_id'] == account_id), None)
        if account:
            log_info(f"[Export API] Account {account_id} is active")
        else:
            log_error(f"[Export API] Account {account_id} is not active or not found")
            
        # Fetch all trades for the account
        log_info(f"[Export API] Fetching trades for account {account_id}")
        all_trades = kite_service.get_trades_for_account(account_id)
        log_info(f"[Export API] Found {len(all_trades)} total trades for account {account_id}")
        
        # Filter for selected trades
        selected_trades = [trade for trade in all_trades if trade['trade_id'] in trade_ids]
        log_info(f"[Export API] Selected {len(selected_trades)} trades for export")
        
        if not selected_trades:
            log_error(f"[Export API] No trades found for selected IDs: {trade_ids}")
            return jsonify({"error": "No matching trades found for export."}), 400
        
        # Export to Google Sheets
        log_info(f"[Export API] Exporting {len(selected_trades)} trades to Google Sheets with tag: {tag}")
        if sheets_service.export_trades(selected_trades, tag):
            log_success(f"[Export API] Successfully exported {len(selected_trades)} trades for account {account_id}")
            return jsonify({"message": f"Successfully exported {len(selected_trades)} trades"})
        else:
            log_error(f"[Export API] Failed to export trades for account {account_id}")
            return jsonify({"error": "Failed to export trades"}), 500
    except Exception as e:
        log_error(f"[Export API] Error exporting trades: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/tags', methods=['GET'])
def get_tags():
    """Get all tags."""
    try:
        tags = sheets_service.get_all_tags()
        return jsonify(tags)
    except Exception as e:
        log_error(f"Error getting tags: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/dashboard/overview', methods=['GET'])
def dashboard_overview():
    """Return dashboard overview stats: active accounts and trades executed per account."""
    try:
        active_accounts = kite_service.get_active_accounts()
        trades_executed = kite_service.get_trades_executed_counts()
        return jsonify({
            'active_accounts': len(active_accounts),
            'trades_executed': trades_executed
        })
    except Exception as e:
        log_error(f"[Dashboard API] Error getting overview: {str(e)}")
        return jsonify({'error': str(e)}), 500 