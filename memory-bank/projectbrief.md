# Project Brief

## Project Scope
- Develop a Trade Monitor application that monitors trades across multiple Zerodha trading accounts
- Enable trade copying from a primary account to other accounts with position size scaling
- Provide a real-time dashboard to view trade activities across all accounts
- Allow users to select trades, tag them, and export them to Google Sheets
- Create a responsive web application with a backend in Flask and frontend in React

## Key Requirements
### Functional Requirements
- Monitor real-time trade data from multiple Zerodha accounts
- Copy trades from a primary account to secondary accounts with adjustable position size multipliers
- Only copy trades matching specific criteria (order types, product type MIS)
- Display trades in a real-time updating table with checkboxes for selection
- Allow tagging selected trades with a Trade ID
- Export selected trades to Google Sheets
- Implement retry mechanism for failed trade copies

### Non-functional Requirements
- Real-time updates using WebSockets
- Secure handling of account credentials
- Responsive and intuitive user interface
- Proper error handling and user feedback
- Logging for debugging and audit purposes

### Technical Constraints
- Must use Flask for the backend
- Must use React for the frontend
- Must integrate with Zerodha's Kite Connect API
- Must use gspread for Google Sheets integration
- Must use WebSockets for real-time data

## Success Criteria
- Users can monitor trades from multiple accounts in real-time
- Users can copy trades from a primary account to other accounts with correct position sizing
- Users can select, tag, and export trades to Google Sheets
- The application is responsive and intuitive to use
- The system handles errors gracefully and provides useful feedback to users
- All trade copies and exports are properly logged 