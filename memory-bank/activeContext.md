# Active Context

## Current Focus
- Initial project setup and requirements gathering
- Understanding the Zerodha Kite Connect API for trade monitoring and order execution
- Planning the system architecture and component design
- Setting up the development environment for both backend and frontend

## Recent Changes
- 2023-09-05: Initial project requirements documented
- 2023-09-05: Updated memory bank with detailed project information
- 2023-09-05: Defined system architecture and component relationships

## Next Steps
1. Set up basic Flask project structure
   - Create necessary directories and files
   - Initialize Flask application
   - Configure basic routes

2. Implement account configuration loading
   - Create accounts_config.json structure
   - Implement account manager component
   - Set up Kite API authentication

3. Develop trade monitoring component
   - Connect to Kite WebSocket API
   - Parse and process trade updates
   - Implement WebSocket server for frontend

4. Develop frontend dashboard
   - Set up React application
   - Implement WebSocket client
   - Create trade display table with sorting

5. Implement trade copying logic
   - Filter trades based on criteria
   - Scale orders based on position size multipliers
   - Handle order placement and retries

6. Implement Google Sheets export
   - Set up Google Sheets authentication
   - Implement export service
   - Connect to frontend selection

## Active Decisions
- Deciding on state management approach for frontend (Redux vs Context API)
- Evaluating different approaches for handling WebSocket reconnection
- Considering options for local data storage for trade history
- Determining the best approach for error handling and retry mechanism
- Exploring options for handling Kite API rate limits 