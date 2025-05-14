# Trade Monitor Application

A real-time trade monitoring and replication system for Zerodha accounts.

## Features

- Real-time trade monitoring from primary account
- Automatic trade replication to secondary accounts with position scaling
- Centralized account management
- Custom trade tagging
- Google Sheets export functionality
- Comprehensive logging system

## Tech Stack

### Backend
- Flask (Python)
- Kite Connect API (Zerodha)
- gspread (Google Sheets integration)
- Server-Sent Events (SSE) for real-time updates

### Frontend
- HTMX
- Tailwind CSS
- Server-Sent Events (SSE) for real-time updates

## Project Structure

```
trade-monitor/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   └── utils/
│   ├── config/
│   ├── logs/
│   ├── requirements.txt
│   └── run.py
└── frontend/
    ├── static/
    ├── templates/
    └── app.py
```

## Setup Instructions

### Backend Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure accounts:
- Copy `config/accounts_config.example.json` to `config/accounts_config.json`
- Update with your Zerodha account details

4. Configure Google Sheets:
- Place your Google Sheets credentials file in `config/`

5. Run the backend:
```bash
python run.py
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run the frontend:
```bash
python app.py
```

## Configuration Files

### accounts_config.json
```json
[
  {
    "account_id": "RA0165",
    "api_key": "your_api_key",
    "secret_api_key": "your_secret_key",
    "access_token": "your_access_token",
    "request_token": "your_request_token",
    "ps_multiplier": 1.0,
    "primary": true
  }
]
```

### allowed_order_types.json
```json
[
  {
    "order_types": ["MARKET", "LIMIT", "SL"],
    "product_types": ["MIS", "NRML"]
  }
]
```

## API Endpoints

### Accounts
- GET `/api/accounts` - List all accounts
- POST `/api/accounts/connect` - Connect to an account
- PUT `/api/accounts/{account_id}` - Update account details

### Trades
- GET `/api/trades` - List all trades
- POST `/api/trades/replicate` - Start trade replication
- POST `/api/trades/stop` - Stop trade replication
- POST `/api/trades/export` - Export trades to Google Sheets

### Logs
- GET `/api/logs` - Stream logs via SSE

## Error Handling

The application implements comprehensive error handling:
- Kite API errors
- Connection failures
- Trade replication errors
- Google Sheets export errors

All errors are logged and displayed to the user with appropriate messages.

## Logging

Logs are stored in `backend/logs/app.log` with the following levels:
- INFO: General information
- WARNING: Non-critical issues
- ERROR: Critical issues
- SUCCESS: Successful operations 