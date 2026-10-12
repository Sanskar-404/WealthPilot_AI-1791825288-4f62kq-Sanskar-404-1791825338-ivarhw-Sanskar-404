class TaxOptimisationAgent:
    name = "Tax Optimisation Agent"

    def estimate(self, portfolio, asset, side, amount, current_weight, target_weight):
        # Educational approximation: only sells can realise taxable gains; basis and holding periods are synthetic.
        if side != "SELL":
            return {"tax_inr": 0.0, "lot_strategy": "No sell lot selected"}
        embedded_gain_fraction = 0.04 if current_weight > target_weight else 0.0
        taxable_gain = amount * embedded_gain_fraction
        tax = taxable_gain * portfolio.tax_rate
        return {"tax_inr": tax, "lot_strategy": "Illustrative highest-cost eligible lot first; tax-lot data is synthetic"}
