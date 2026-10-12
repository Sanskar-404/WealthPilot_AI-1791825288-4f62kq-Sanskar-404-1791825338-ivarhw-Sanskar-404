from agents.monitor import PortfolioMonitoringAgent
from agents.triggers import TriggerEvaluationAgent
from agents.trade import TradeGenerationAgent
from agents.risk import RiskAssessmentAgent
from agents.compliance import ComplianceVerificationAgent
from agents.explain import ExplanationGenerationAgent
from models import Decision
from audit.logger import log_event

class OrchestratorAgent:
    name = "Orchestrator Agent"

    def __init__(self):
        self.monitor = PortfolioMonitoringAgent()
        self.trigger = TriggerEvaluationAgent()
        self.trade = TradeGenerationAgent()
        self.risk = RiskAssessmentAgent()
        self.compliance = ComplianceVerificationAgent()
        self.explain = ExplanationGenerationAgent()

    def process(self, portfolio, month=1, event=None, force=False, override_note=None):
        analysis = self.monitor.analyze(portfolio)
        trigger = self.trigger.evaluate(analysis, month, event)
        if force:
            trigger = {"trigger_type": "Human override: " + (override_note or "manual review"), "priority": "HIGH", "rebalance": True}
        if not trigger["rebalance"]:
            log_event("MONITOR_ONLY", portfolio.portfolio_id, {"trigger": trigger, "drift": analysis["drift"]})
            return None
        trades = self.trade.generate(portfolio, analysis)
        risk = self.risk.assess(portfolio, analysis, trades)
        compliance = self.compliance.verify(portfolio, risk)
        explanations = self.explain.generate(portfolio, analysis, trigger, trades, risk, compliance)
        requires_approval = portfolio.prior_approval_required or not compliance["approved_for_simulation"]
        status = "PENDING_HUMAN_APPROVAL" if requires_approval else "PROPOSED_SIMULATION_ONLY"
        decision = Decision.create(portfolio_id=portfolio.portfolio_id, trigger_type=trigger["trigger_type"],
            priority=trigger["priority"], status=status, drift=analysis["drift"], trades=trades,
            metrics={"sad_pct": analysis["sad"]*100, "rmsd_pct": analysis["rmsd"]*100,
                     "gross_turnover_pct": risk["gross_turnover_pct"], "estimated_cost_inr": risk["estimated_cost_inr"],
                     "estimated_tax_inr": risk["estimated_tax_inr"], "portfolio_value_inr": portfolio.value_inr},
            explanations=explanations, checks=compliance["checks"])
        log_event("DECISION_CREATED", portfolio.portfolio_id, decision.to_dict())
        return decision

    def review(self, decision, action, reviewer, note=""):
        if action not in ("APPROVE", "REJECT", "OVERRIDE"):
            raise ValueError("Action must be APPROVE, REJECT, or OVERRIDE")
        result = {"decision_id": decision.decision_id, "action": action, "reviewer": reviewer, "note": note}
        log_event("HUMAN_REVIEW", decision.portfolio_id, result)
        return result
