# Test plan

Manual smoke tests:
1. `python main.py demo` creates a simulated decision and appends an audit event.
2. `python main.py backtest` prints two strategy rows and key performance metrics.
3. Launch `streamlit run app.py`; inspect overview risk table and charts.
4. In Agent decision, select a portfolio and run with an event.
5. Inspect all three explanation levels and pre-trade checks.
6. Record APPROVE / REJECT / OVERRIDE and confirm a `HUMAN_REVIEW` event appears in Audit trail.
7. Select a restricted asset profile and confirm no trade is generated for restricted asset classes.
8. Compare `Legacy quarterly` and `WealthPilot agent` across normal, mixed and crash synthetic scenarios.

Acceptance criteria:
- No live order execution or external API calls.
- All generated decisions have a unique ID, timestamp, trigger, metrics, explanations and checks.
- Human review records reviewer, action, note, timestamp and portfolio reference.
- Backtest produces metrics for both strategies.
- Dashboard clearly labels results synthetic/illustrative.
