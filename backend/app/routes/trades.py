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
    """Get trade history for an account."""
    try:
        account_id = request.args.get('account_id')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 50))
        
        if not account_id:
            return jsonify({"error": "Account ID is required"}), 400

        # Get trades for the current date
        today = datetime.now().strftime('%Y-%m-%d')
        account_trades = [
            trade for trade in trades 
            if trade.get('account_id') == account_id 
            and trade.get('date') == today
        ]

        # Sort by timestamp (newest first)
        account_trades.sort(key=lambda x: x.get('timestamp', 0), reverse=True)

        # Paginate
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_trades = account_trades[start_idx:end_idx]

        return jsonify({
            'trades': paginated_trades,
            'has_more': end_idx < len(account_trades),
            'total': len(account_trades)
        })
    except Exception as e:
        log_error(f"Error getting trade history: {str(e)}")
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
    """Export trades to Google Sheets."""
    try:
        data = request.json
        selected_trades = data.get('trades', [])
        tag = data.get('tag')

        if not selected_trades:
            return jsonify({"error": "No trades selected"}), 400
        if not tag:
            return jsonify({"error": "Tag is required"}), 400

        if sheets_service.export_trades(selected_trades, tag):
            return jsonify({"message": "Trades exported successfully"})
        else:
            return jsonify({"error": "Failed to export trades"}), 500
    except Exception as e:
        log_error(f"Error exporting trades: {str(e)}")
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