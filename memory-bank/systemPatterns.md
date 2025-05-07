# System Patterns

## Architecture
- **Client-Server Architecture**:
  - Flask backend providing REST API and WebSocket server
  - React frontend consuming API and WebSocket events
  
- **Event-Driven Architecture**:
  - WebSocket events for real-time trade updates
  - Event listeners for trade copying logic

- **Main Components**:
  - Account Manager: Handles account configuration and authentication
  - Trade Monitor: Connects to Kite WebSocket and monitors trades
  - Trade Copier: Copies trades from primary to secondary accounts
  - Export Service: Handles export of selected trades to Google Sheets
  - Frontend Dashboard: Displays trades and provides user interface

## Design Patterns
- **Observer Pattern**: WebSocket implementation for real-time updates
- **Factory Pattern**: Creating trade objects from API responses
- **Strategy Pattern**: Different strategies for trade copying based on order types
- **Facade Pattern**: Simplified interface to the complex subsystems (Kite API, Google Sheets)
- **Repository Pattern**: For managing trade data and account configurations

## Component Relationships
- **Account Manager**:
  - Loads account configuration from JSON
  - Establishes Kite API sessions for each account
  - Provides account information to other components

- **Trade Monitor**:
  - Subscribes to Kite WebSocket for all accounts
  - Receives trade updates and notifies Trade Copier
  - Pushes updates to frontend via Flask-SocketIO

- **Trade Copier**:
  - Receives trade notifications from Trade Monitor
  - Filters trades based on configured criteria
  - Scales orders based on position size multipliers
  - Places orders on secondary accounts
  - Implements retry logic for failed orders

- **Export Service**:
  - Receives export requests from frontend
  - Formats selected trades for Google Sheets
  - Uses gspread to update the "CDS" sheet

- **Frontend Components**:
  - Trade Dashboard: Displays real-time trade data
  - Selection Panel: Allows selecting and tagging trades
  - Export Panel: Handles export requests

## Data Flow
- **Trade Monitoring Flow**:
  1. Kite WebSocket sends trade updates to backend
  2. Backend processes and stores trade information
  3. Backend sends updates to frontend via WebSocket
  4. Frontend updates UI in real-time

- **Trade Copying Flow**:
  1. Primary account executes a trade
  2. Trade Monitor detects the trade
  3. Trade Copier checks if trade meets copy criteria
  4. If criteria met, Trade Copier scales order for each secondary account
  5. Trade Copier places orders on secondary accounts
  6. Results are logged and reported back to frontend

- **Export Flow**:
  1. User selects trades and adds optional Trade ID tag
  2. User initiates export
  3. Frontend sends export request to backend
  4. Backend formats data and updates Google Sheet
  5. Success/failure notification sent back to frontend

- **Data Validation**:
  - Validate trade parameters before copying
  - Validate account configuration on startup
  - Validate export requests before processing 