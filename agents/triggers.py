class TriggerEvaluationAgent:
    name = "Trigger Evaluation Agent"

    def evaluate(self, analysis, month, event=None):
        if event:
            return {"trigger_type": "Event-driven: " + event, "priority": "CRITICAL" if event in ("Market crash", "Regulatory change", "Concentration breach") else "HIGH", "rebalance": True}
        if analysis["breach"]:
            return {"trigger_type": "Threshold-based", "priority": "HIGH", "rebalance": True}
        if month in (3, 6, 9, 12):
            return {"trigger_type": "Calendar-based quarterly review", "priority": "MEDIUM", "rebalance": True}
        return {"trigger_type": "Monitor only", "priority": "LOW", "rebalance": False}
