from flask import Flask
from flask_cors import CORS
import os
from pathlib import Path

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Ensure required directories exist
    Path("logs").mkdir(exist_ok=True)
    Path("config").mkdir(exist_ok=True)

    # Load configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        ACCOUNTS_CONFIG_PATH="config/accounts_config.json",
        ALLOWED_ORDER_TYPES_PATH="config/allowed_order_types.json",
        TAGS_PATH="config/tags.json",
        GOOGLE_SHEETS_CREDENTIALS="config/heroic-muse-377907-482b72703bd0.json",
        LOG_FILE="logs/app.log"
    )

    # Register blueprints
    from .routes import accounts, trades, logs
    app.register_blueprint(accounts.bp)
    app.register_blueprint(trades.bp)
    app.register_blueprint(logs.bp)

    return app 