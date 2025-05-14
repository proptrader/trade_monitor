# Background and Motivation
The project is moving to a SPA/HTMX navigation model for a more app-like experience. The navigation bar will now include a Trades tab (for live/all trades) and a Dashboard tab (for summary/overview). The main page will be blank. All navigation will use HTMX for partial updates, and active tab styling will be managed via JavaScript.

# Key Challenges and Analysis
- Ensuring all content routes return partials, not full HTML pages.
- Updating all navigation and JS to use `/trades` instead of `/dashboard` for the trades tab.
- Implementing a summary dashboard for account/trade stats.
- Managing active tab styling in a SPA context.

# High-level Task Breakdown
- [ ] Update navigation bar in `base.html`:
    - Add "Trades" tab after "Dashboard".
    - Use `hx-get`, `hx-target`, and `hx-push-url` for all tabs.
    - Set `href` to `/dashboard`, `/trades`, `/accounts`, `/logs` as appropriate.
- [ ] Update Flask routes:
    - `/dashboard` returns summary/overview partial (active accounts, trades per account, trades copied).
    - `/trades` returns live/all trades tabbed interface partial.
    - `/` returns a blank partial.
- [ ] Update all navigation and JS references from `/dashboard` to `/trades` for the trades tab.
- [ ] Implement JavaScript logic to update active tab styling on click.
- [ ] Ensure all content pages are returned as partials (not full HTML).
- [ ] Test navigation, content loading, and active tab styling.

# Project Status Board
- [ ] Navigation bar updated with SPA/HTMX and Trades tab
- [ ] Flask routes updated for partials and new tab structure
- [ ] Dashboard summary implemented
- [ ] Trades tab (live/all trades) implemented at `/trades`
- [ ] Active tab styling works with SPA navigation
- [ ] Main page blank
- [ ] All navigation and content tested

# Executor's Feedback or Assistance Requests
- Awaiting confirmation to proceed with implementation steps as per plan.

# Lessons
- For SPA/HTMX navigation, always use partials and manage active tab state via JS.
- Update all references when renaming routes (e.g., `/dashboard` to `/trades`).
