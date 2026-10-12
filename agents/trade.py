from config import ASSET_CLASSES, TRANSACTION_COST_BPS, DEFAULT_TURNOVER_LIMIT
from agents.tax import TaxOptimisationAgent

class TradeGenerationAgent:
    name = "Trade Generation Agent"

    def generate(self, portfolio, analysis, turnover_limit=DEFAULT_TURNOVER_LIMIT):
        target, drift = analysis["target"], analysis["drift"]
        tax_agent = TaxOptimisationAgent()
        raw = []
        for asset in ASSET_CLASSES:
            delta = target[asset] - portfolio.weights[asset]
            if asset in portfolio.restricted_assets:
                continue
            amount = abs(delta) * portfolio.value_inr
            if amount < max(1000, portfolio.value_inr * 0.002):
                continue
            side = "BUY" if delta > 0 else "SELL"
            cost = amount * TRANSACTION_COST_BPS[asset] / 10000
            tax = tax_agent.estimate(portfolio, asset, side, amount, portfolio.weights[asset], target[asset])
            raw.append({"portfolio_id": portfolio.portfolio_id, "asset_class": asset, "side": side, "amount_inr": amount,
                        "current_weight": portfolio.weights[asset], "target_weight": target[asset],
                        "estimated_cost_inr": cost, "estimated_tax_inr": tax["tax_inr"],
                        "rationale": f"Move {asset} toward target allocation; {tax['lot_strategy']}"})
        # Scale trade set to turnover cap. Gross turnover counts both buys and sells.
        gross = sum(t["amount_inr"] for t in raw)
        cap = portfolio.value_inr * turnover_limit
        if gross > cap and gross > 0:
            factor = cap / gross
            for t in raw:
                t["amount_inr"] *= factor
                t["estimated_cost_inr"] *= factor
                t["estimated_tax_inr"] *= factor
                t["rationale"] += "; scaled to turnover budget"
        return raw
