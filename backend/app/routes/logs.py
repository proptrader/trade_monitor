from flask import Blueprint, Response, current_app
from ..utils.logger import log_info, log_error, log_success
import json
import time
import os

bp = Blueprint('logs', __name__, url_prefix='/api/logs')

@bp.route('/stream', methods=['GET'])
def stream_logs():
    """Stream logs via SSE."""
    def generate():
        # Get initial file size
        file_size = os.path.getsize(current_app.config['LOG_FILE'])
        with open(current_app.config['LOG_FILE'], 'r') as f:
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
                    except:
                        # Skip malformed log lines
                        continue
                else:
                    time.sleep(0.1)

    return Response(generate(), mimetype='text/event-stream') 