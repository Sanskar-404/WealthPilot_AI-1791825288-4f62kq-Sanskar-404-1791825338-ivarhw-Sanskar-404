import numpy as np
import pandas as pd
from config import RISK_PROFILES, ASSET_CLASSES, DEFAULT_PORTFOLIO_VALUE, ASSET_RETURN, ASSET_VOL
from models import Portfolio

def generate_portfolios(n=100, seed=7):
    rng = np.random.default_rng(seed)
    names = list(RISK_PROFILES)
    probs = np.array([RISK_PROFILES[x]["portfolios"] for x in names], dtype=float)
    probs /= probs.sum()
    portfolios = []
    for i in range(n):
        risk = rng.choice(names, p=probs)
        profile = RISK_PROFILES[risk]
        target = np.array([profile[a] for a in ASSET_CLASSES], dtype=float)
        noise = rng.normal(0, 0.018, len(target))
        weights = np.maximum(target + noise, 0.005)
        weights /= weights.sum()
        portfolios.append(Portfolio(
            portfolio_id=f"WP-{i+1:05d}",
            client_name=f"Client {i+1:05d}",
            risk_category=risk,
            value_inr=float(DEFAULT_PORTFOLIO_VALUE * rng.lognormal(0, .45)),
            weights=dict(zip(ASSET_CLASSES, weights.tolist())),
            restricted_assets=(["Alternatives"] if rng.random() < .08 else []),
            tax_rate=float(rng.choice([.10, .20, .30])),
            last_rebalance_month=int(rng.integers(1, 12)),
            prior_approval_required=bool(rng.random() < .04)
        ))
    return portfolios

def generate_monthly_returns(months=12, seed=22, scenario="mixed"):
    rng = np.random.default_rng(seed)
    rows = []
    for m in range(months):
        stress = scenario == "crash" and m in (4, 5)
        for asset in ASSET_CLASSES:
            mu = ASSET_RETURN[asset] / 12
            sd = ASSET_VOL[asset] / np.sqrt(12)
            ret = rng.normal(mu, sd)
            if stress and asset == "Equity":
                ret -= .12
            if scenario == "mixed" and m == 5 and asset == "Equity":
                ret -= .16
            if scenario == "mixed" and m == 6 and asset == "Fixed Income":
                ret -= .025
            rows.append({"month": m+1, "asset_class": asset, "return": float(ret)})
    return pd.DataFrame(rows)
