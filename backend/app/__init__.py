from flask import Flask
from flask_cors import CORS
import os
from pathlib import Path
from .utils.logger import setup_logger, log_info

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Get absolute paths
    BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOGS_DIR = os.path.join(BACKEND_DIR, "logs")
    CONFIG_DIR = os.path.join(BACKEND_DIR, "config")

    # Ensure required directories exist
    Path(LOGS_DIR).mkdir(exist_ok=True)
    Path(CONFIG_DIR).mkdir(exist_ok=True)

    # Load configuration with absolute paths
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        ACCOUNTS_CONFIG_PATH=os.path.join(CONFIG_DIR, "accounts_config.json"),
        ALLOWED_ORDER_TYPES_PATH=os.path.join(CONFIG_DIR, "allowed_order_types.json"),
        TAGS_PATH=os.path.join(CONFIG_DIR, "tags.json"),
        GOOGLE_SHEETS_CREDENTIALS=os.path.join(CONFIG_DIR, "heroic-muse-377907-482b72703bd0.json"),
        LOG_FILE=os.path.join(LOGS_DIR, "app.log"),
        INIT_TRACKER_PATH=os.path.join(CONFIG_DIR, "init_tracker.json")
    )

    with app.app_context():
        # Initialize logger
        setup_logger()
        log_info("Application started")
        log_info("Logger initialized")

        # Register blueprints
        from .routes import accounts, trades, logs
        app.register_blueprint(accounts.bp)
        app.register_blueprint(trades.bp)
        app.register_blueprint(logs.bp)

        log_info("Routes registered")

    return app 