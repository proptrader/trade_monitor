from app import create_app
from app.utils.logger import setup_logger

app = create_app()

with app.app_context():
    logger = setup_logger()

if __name__ == '__main__':
    app.run(debug=True, port=5000) 