from flask import Blueprint, Response, current_app
from ..utils.logger import log_info, log_error, log_success
import json
import time
import os

bp = Blueprint('logs', __name__, url_prefix='/api/logs')

@bp.route('/stream', methods=['GET'])
def stream_logs():
    """Stream logs via SSE."""
    # Check if log file exists
    log_file = current_app.config['LOG_FILE']
    if not os.path.exists(log_file):
        log_error(f"Log file not found: {log_file}")
        return Response(
            json.dumps({'error': 'Log file not found'}),
            mimetype='application/json',
            status=404
        )

    def generate():
        try:
            # Get initial file size
            file_size = os.path.getsize(log_file)
            with open(log_file, 'r') as f:
                # Skip to end of file
                f.seek(file_size)
                
                while True:
                    line = f.readline()
                    if line:
                        # Parse log line
                        try:
                            timestamp, level, message = line.strip().split(' - ', 2)
                            log_entry = {
                                'timestamp': timestamp,
                                'level': level,
                                'message': message
                            }
                            yield f"data: {json.dumps(log_entry)}\n\n"
                        except Exception as e:
                            log_error(f"Failed to parse log line: {str(e)}")
                            # Skip malformed log lines
                            continue
                    else:
                        # No new lines, wait before checking again
                        time.sleep(0.1)
        except Exception as e:
            log_error(f"Error streaming logs: {str(e)}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    # Set headers for SSE with CORS
    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'X-Accel-Buffering': 'no',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

    return Response(
        generate(),
        mimetype='text/event-stream',
        headers=headers
    )

@bp.route('/history', methods=['GET'])
def get_log_history():
    """Get recent log history."""
    try:
        log_file = current_app.config['LOG_FILE']
        if not os.path.exists(log_file):
            log_error("Log file not found")
            return Response(
                json.dumps({
                    'error': 'Log file not found',
                    'details': 'The log file has not been created yet.'
                }),
                mimetype='application/json',
                status=404
            )

        file_size = os.path.getsize(log_file)
        if file_size == 0:
            log_info("Empty log file found")
            return Response(
                json.dumps({
                    'logs': [],
                    'message': 'No logs available yet. New logs will appear automatically.'
                }),
                mimetype='application/json'
            )

        # Read last 100 lines of logs
        logs = []
        with open(log_file, 'r') as f:
            # Read all lines and get last 100
            lines = f.readlines()[-100:]
            for line in lines:
                try:
                    timestamp, level, message = line.strip().split(' - ', 2)
                    logs.append({
                        'timestamp': timestamp,
                        'level': level,
                        'message': message
                    })
                except Exception as e:
                    log_error(f"Failed to parse log line: {str(e)}")
                    continue

        if not logs:
            return Response(
                json.dumps({
                    'logs': [],
                    'message': 'No valid logs found. New logs will appear automatically.'
                }),
                mimetype='application/json'
            )

        return Response(
            json.dumps({'logs': logs}),
            mimetype='application/json'
        )
    except Exception as e:
        error_msg = f"Error getting log history: {str(e)}"
        log_error(error_msg)
        return Response(
            json.dumps({
                'error': error_msg,
                'details': 'Please check server logs for more information.'
            }),
            mimetype='application/json',
            status=500
        ) 