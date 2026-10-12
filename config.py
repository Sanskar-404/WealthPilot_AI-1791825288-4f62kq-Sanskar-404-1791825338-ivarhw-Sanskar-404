RISK_PROFILES = {
    "Ultra-Conservative": {"Equity": 0.15, "Fixed Income": 0.60, "Alternatives": 0.10, "Cash": 0.15, "band": 0.020, "portfolios": 5000},
    "Conservative":       {"Equity": 0.30, "Fixed Income": 0.45, "Alternatives": 0.12, "Cash": 0.13, "band": 0.025, "portfolios": 12000},
    "Balanced":           {"Equity": 0.50, "Fixed Income": 0.30, "Alternatives": 0.12, "Cash": 0.08, "band": 0.030, "portfolios": 18000},
    "Aggressive":         {"Equity": 0.70, "Fixed Income": 0.15, "Alternatives": 0.10, "Cash": 0.05, "band": 0.040, "portfolios": 10000},
    "Ultra-Aggressive":   {"Equity": 0.85, "Fixed Income": 0.05, "Alternatives": 0.07, "Cash": 0.03, "band": 0.050, "portfolios": 5000},
}
ASSET_CLASSES = ["Equity", "Fixed Income", "Alternatives", "Cash"]
ASSET_RETURN = {"Equity": 0.115, "Fixed Income": 0.065, "Alternatives": 0.075, "Cash": 0.035}
ASSET_VOL = {"Equity": 0.19, "Fixed Income": 0.055, "Alternatives": 0.13, "Cash": 0.008}
DEFAULT_PORTFOLIO_VALUE = 2_500_000
TRANSACTION_COST_BPS = {"Equity": 12, "Fixed Income": 8, "Alternatives": 15, "Cash": 1}
DEFAULT_TURNOVER_LIMIT = 0.20
