# WealthPilot AI — Autonomous Portfolio Rebalancing System

A runnable educational prototype of a multi-agent portfolio rebalancing platform for the fictional WealthPilot AI robo-advisor.

## Included
- Portfolio drift monitoring and risk-category-specific thresholds
- Threshold, calendar, and event-driven trigger evaluation
- Specialist-agent workflow: Orchestrator, Portfolio Analyst, Risk, Tax, Compliance, Explanation
- Constraint-aware proposed trade lists with cash, long-only, turnover, restricted-security and concentration checks
- Illustrative tax-lot-aware sell ordering and transaction-cost estimates
- Client, advisor, and compliance explanations
- Human override/approval with append-only JSONL audit events
- Synthetic 12-month backtest comparing a quarterly calendar legacy strategy against the agent strategy
- Streamlit dashboard and CLI demo
- Synthetic data only; no brokerage connection or live trading

## Quick start (Windows PowerShell)
```powershell
cd WealthPilot_AI
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```
If `py` is unavailable, use `python` instead.

## CLI demo
```powershell
python main.py demo
python main.py backtest
python main.py portfolios
```

## Important limitations
This is a simulation, not investment advice or a production trading system. It uses synthetic prices, simplified tax assumptions, and heuristic optimisation. Tax treatment and regulatory constraints are jurisdiction-, instrument-, and date-dependent. No order is routed to a broker. Production deployment would require validated market/custody feeds, robust optimisation, security controls, model validation, legal/compliance review, disaster recovery, monitoring, and approved execution integrations.

## Architecture
`data/` synthetic portfolio/price data • `agents/` specialist agents • `engine/` workflow and backtesting • `audit/` JSONL event trail • `app.py` dashboard.

## Success metrics
Backtest output reports annualised return, volatility, Sharpe ratio, maximum drawdown, turnover, estimated trading costs, average absolute drift, and number of rebalances. Results are generated from synthetic data and should not be interpreted as evidence of real-world outperformance.
