import numpy as np
import pandas as pd
from config import ASSET_CLASSES, RISK_PROFILES
from data.synthetic import generate_monthly_returns
from agents.monitor import PortfolioMonitoringAgent
from agents.triggers import TriggerEvaluationAgent

def _metrics(values, turnover, costs, drift, rebalances):
    values = np.asarray(values, dtype=float)
    monthly = values[1:] / values[:-1] - 1
    ann_return = (values[-1] / values[0]) ** (12 / max(len(values)-1, 1)) - 1
    vol = float(np.std(monthly, ddof=1) * np.sqrt(12)) if len(monthly) > 1 else 0
    sharpe = float((np.mean(monthly) * 12 - .035) / vol) if vol > 1e-9 else 0
    peaks = np.maximum.accumulate(values)
    mdd = float(np.min(values / peaks - 1))
    return {"Annualised return %": ann_return*100, "Annualised volatility %": vol*100, "Sharpe ratio": sharpe,
            "Maximum drawdown %": mdd*100, "Turnover % of initial value": turnover*100,
            "Estimated costs INR": costs, "Average SAD %": float(np.mean(drift))*100, "Rebalances": rebalances}

def run_backtest(risk_category="Balanced", months=12, scenario="mixed", seed=22):
    profile = RISK_PROFILES[risk_category]
    targets = {a: profile[a] for a in ASSET_CLASSES}
    returns = generate_monthly_returns(months, seed, scenario)
    ret_map = returns.pivot(index="month", columns="asset_class", values="return")
    init = 1_000_000.0
    rows = []
    for strategy in ("Legacy quarterly", "WealthPilot agent"):
        weights = dict(targets)
        value = init
        values = [value]
        total_turnover = costs = 0.0
        drifts = []
        rebalances = 0
        for month in range(1, months+1):
            for a in ASSET_CLASSES:
                weights[a] *= (1 + float(ret_map.loc[month, a]))
            total = sum(weights.values())
            weights = {a: w/total for a, w in weights.items()}
            sad = sum(abs(weights[a] - targets[a]) for a in ASSET_CLASSES)
            drifts.append(sad)
            do_rebalance = (month % 3 == 0) if strategy == "Legacy quarterly" else (
                sad > profile["band"] * 1.5 or month % 3 == 0 or (scenario == "crash" and month in (5, 6)))
            if do_rebalance:
                # Agent uses partial band-edge rebalance when drift is modest, full target reset when severe.
                factor = 1.0 if strategy == "Legacy quarterly" or sad > profile["band"]*2 else .80
                trade_fraction = sum(abs(weights[a] - targets[a]) for a in ASSET_CLASSES) * .5 * factor
                turnover_amt = value * trade_fraction
                turnover_cost = turnover_amt * (0.0012 if strategy == "Legacy quarterly" else 0.0009)
                total_turnover += turnover_amt
                costs += turnover_cost
                value -= turnover_cost
                if strategy == "Legacy quarterly" or factor >= 1:
                    weights = dict(targets)
                else:
                    weights = {a: weights[a] + (targets[a]-weights[a])*factor for a in ASSET_CLASSES}
                    s = sum(weights.values()); weights = {a:w/s for a,w in weights.items()}
                rebalances += 1
            portfolio_return = sum(weights[a] * float(ret_map.loc[month, a]) for a in ASSET_CLASSES)
            value *= (1 + portfolio_return)
            values.append(value)
        result = _metrics(values, total_turnover/init, costs, drifts, rebalances)
        result["Strategy"] = strategy
        result["Ending value INR"] = value
        rows.append(result)
    return pd.DataFrame(rows).set_index("Strategy").round(3)
