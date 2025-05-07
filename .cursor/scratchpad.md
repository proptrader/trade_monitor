# Project Scratchpad

## Background and Motivation
The Trade Monitor application aims to help traders manage multiple trading accounts efficiently. The system will monitor trades across Zerodha accounts, enable copying trades from a primary account to secondary accounts with position size scaling, and allow exporting selected trades to Google Sheets for analysis or record-keeping.

## Key Challenges and Analysis
1. **Zerodha API Integration**: Need to understand and implement Kite Connect API for trade monitoring and order execution.
2. **Real-time Updates**: Implementing WebSocket for real-time trade data updates to the frontend.
3. **Trade Copying Logic**: Ensuring accurate position sizing when copying trades across accounts.
4. **Error Handling**: Implementing retry mechanism for failed trade copies.
5. **Data Management**: Organizing trade data for selection, tagging, and export.

## High-level Task Breakdown
1. **Set up Project Structure**
   - Initialize Flask backend
   - Initialize React frontend
   - Set up development environment
   - Success criteria: Basic application structure with routes and components

2. **Implement Account Management**
   - Create accounts_config.json structure with primary flag
   - Implement account loading and validation
   - Set up Kite API authentication
   - Success criteria: Successfully load account details and authenticate with Kite API

3. **Develop Trade Monitoring**
   - Connect to Kite WebSocket for real-time updates
   - Implement trade event processing
   - Set up WebSocket server for frontend updates
   - Success criteria: Receive and process trade updates from Kite, push to frontend

4. **Create Frontend Dashboard**
   - Implement React components for trade display
   - Create tabbed interface with most recent trades at top
   - Implement trade selection with checkboxes
   - Success criteria: Display real-time trade data with proper sorting and selection

5. **Implement Trade Copying**
   - Filter trades based on order types and PRODUCT_MIS
   - Scale orders based on account multipliers
   - Implement order placement with error handling and retries
   - Success criteria: Successfully copy eligible trades to secondary accounts

6. **Develop Google Sheets Export**
   - Set up Google Sheets authentication
   - Implement export functionality for selected trades
   - Support trade tagging with Trade ID
   - Success criteria: Export selected trades to Google Sheets "CDS" sheet

## Project Status Board
- [ ] Set up Project Structure
- [ ] Implement Account Management
- [ ] Develop Trade Monitoring
- [ ] Create Frontend Dashboard
- [ ] Implement Trade Copying
- [ ] Develop Google Sheets Export

## Current Status / Progress Tracking
Project is in initial planning phase. Requirements have been documented, system architecture has been defined, and memory bank has been updated with project information.

## Executor's Feedback or Assistance Requests
No feedback or assistance requests at this time, as implementation has not yet started.

## Lessons
- Trade copying should be filtered by both order type and product type (PRODUCT_MIS)
- Trade retry mechanism is required for failed trade copies
- Primary account should be identified with a "primary" flag in the configuration 