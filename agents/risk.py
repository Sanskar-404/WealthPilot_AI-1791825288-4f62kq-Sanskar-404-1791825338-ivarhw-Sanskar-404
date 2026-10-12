class RiskAssessmentAgent:
    name = "Risk Assessment Agent"

    def assess(self, portfolio, analysis, trades):
        gross_turnover = sum(t["amount_inr"] for t in trades) / max(portfolio.value_inr, 1)
        cash_buy = sum(t["amount_inr"] for t in trades if t["asset_class"] == "Cash" and t["side"] == "BUY")
        cash_sell = sum(t["amount_inr"] for t in trades if t["asset_class"] == "Cash" and t["side"] == "SELL")
        checks = {
            "long_only": all(w >= 0 for w in portfolio.weights.values()),
            "turnover_within_20pct": gross_turnover <= .200001,
            "cash_reserve_non_negative": portfolio.weights.get("Cash", 0) - cash_sell / max(portfolio.value_inr, 1) >= -1e-9,
            "restricted_assets_excluded": all(t["asset_class"] not in portfolio.restricted_assets for t in trades),
            "trade_list_non_empty": len(trades) > 0
        }
        checks["all_checks_pass"] = all(checks.values())
        return {"checks": checks, "gross_turnover_pct": gross_turnover * 100, "estimated_cost_inr": sum(t["estimated_cost_inr"] for t in trades),
                "estimated_tax_inr": sum(t["estimated_tax_inr"] for t in trades)}
