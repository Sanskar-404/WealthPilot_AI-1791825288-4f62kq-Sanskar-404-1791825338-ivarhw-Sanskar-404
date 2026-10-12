import sys
from data.synthetic import generate_portfolios
from engine.orchestrator import OrchestratorAgent
from engine.backtest import run_backtest

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "demo"
    if cmd == "portfolios":
        for p in generate_portfolios(10):
            print(p.portfolio_id, p.risk_category, f"₹{p.value_inr:,.0f}", p.weights)
    elif cmd == "backtest":
        print(run_backtest().to_string())
    else:
        p = generate_portfolios(1, seed=41)[0]
        # Introduce visible drift for demo
        p.weights["Equity"] = min(.92, p.weights["Equity"] + .08)
        total = sum(p.weights.values()); p.weights = {k:v/total for k,v in p.weights.items()}
        decision = OrchestratorAgent().process(p, month=6, event="Market crash")
        print("WEALTHPILOT AI — DEMO DECISION")
        print("Portfolio:", p.portfolio_id, "| Risk:", p.risk_category)
        print("Decision:", decision.decision_id, "| Status:", decision.status, "| Trigger:", decision.trigger_type)
        print("\nMetrics:", decision.metrics)
        print("\nTrades:")
        for t in decision.trades: print(t["side"], t["asset_class"], f"₹{t['amount_inr']:,.0f}", "| tax est.", f"₹{t['estimated_tax_inr']:,.0f}")
        print("\nClient explanation:", decision.explanations["client"])
        print("\nAudit event appended to audit/audit_log.jsonl")

if __name__ == "__main__":
    main()
