class ExplanationGenerationAgent:
    name = "Explanation Generation Agent"

    def generate(self, portfolio, analysis, trigger, trades, risk, compliance):
        top = sorted(analysis["drift"].items(), key=lambda x: abs(x[1]), reverse=True)[0]
        buys = sum(t["amount_inr"] for t in trades if t["side"] == "BUY")
        sells = sum(t["amount_inr"] for t in trades if t["side"] == "SELL")
        costs = risk["estimated_cost_inr"] + risk["estimated_tax_inr"]
        client = (f"Your portfolio was reviewed because of {trigger['trigger_type'].lower()}. "
                  f"The largest allocation difference is {top[0]} ({top[1]*100:+.2f} percentage points from target). "
                  f"We propose purchases of about ₹{buys:,.0f} and sales of about ₹{sells:,.0f} to move closer to your chosen risk profile. "
                  f"Estimated trading costs and illustrative tax impact total ₹{costs:,.0f}. This is a simulated proposal, not an executed trade.")
        advisor = (f"{portfolio.portfolio_id} | {portfolio.risk_category} | SAD={analysis['sad']*100:.2f}% | "
                   f"RMSD={analysis['rmsd']*100:.2f}% | band={analysis['band']*100:.2f}% | "
                   f"trigger={trigger['trigger_type']} ({trigger['priority']}). Gross turnover={risk['gross_turnover_pct']:.2f}%; "
                   f"estimated transaction cost=₹{risk['estimated_cost_inr']:,.0f}; illustrative tax=₹{risk['estimated_tax_inr']:,.0f}.")
        comp = (f"Decision control record: portfolio={portfolio.portfolio_id}; trigger={trigger}; "
                f"drift={analysis['drift']}; checks={compliance['checks']}; rule_version={compliance['rule_version']}; "
                f"trades={len(trades)}; all checks pass={compliance['approved_for_simulation']}. "
                f"Tax, regulatory and holdings inputs are synthetic and require independent validation before production use.")
        return {"client": client, "advisor": advisor, "compliance": comp}
