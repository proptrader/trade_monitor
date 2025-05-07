# Technical Context

## Technologies
### Backend
- Flask (Python) - Web framework for the backend API
- Kite Connect API (Zerodha) - For brokerage operations and trade data
- Flask-SocketIO - For real-time updates using WebSockets
- gspread - For Google Sheets integration
- JSON - For configuration files

### Frontend
- React - JavaScript library for building the user interface
- Tailwind CSS - For styling the frontend components
- WebSocket client - For receiving real-time updates from the backend
- Data grid component - For displaying trade data with checkboxes

## Development Setup
### Backend Setup
1. Python 3.8+ environment
2. Install required packages:
   ```
   pip install flask flask-socketio kiteconnect gspread google-auth
   ```
3. Set up Zerodha Kite Connect API credentials
4. Configure Google Sheets API access using heroic-muse-377907-482b72703bd0.json

### Frontend Setup
1. Node.js and npm
2. Create React App:
   ```
   npx create-react-app trade-monitor-frontend
   cd trade-monitor-frontend
   npm install socket.io-client tailwindcss
   ```
3. Configure connection to backend WebSocket

## Technical Constraints
- Zerodha API rate limits and constraints
- WebSocket connection limitations
- Google Sheets API quotas and limitations
- Need to handle authentication token expiry for Zerodha API
- Must filter trades by specific criteria (order types, PRODUCT_MIS)
- Must implement retry mechanism for failed trade copies

## Infrastructure
### Development Environment
- Backend: localhost:5000
- Frontend: localhost:3000

### Configuration Files
- accounts_config.json:
  ```json
  [
    {
      "account_id": "account_1",
      "cred1": "kite_api_key",
      "cred2": "kite_access_token",
      "ps_multiplier": 1.0,
      "primary": true
    },
    {
      "account_id": "account_2",
      "cred1": "kite_api_key_2",
      "cred2": "kite_access_token_2",
      "ps_multiplier": 2.5,
      "primary": false
    }
  ]
  ```

- allowed_order_types.json:
  ```json
  {
    "order_types": ["MARKET", "LIMIT", "SL"]
  }
  ```

### Security
- Secure storage of API credentials
- Basic route protection for API endpoints 