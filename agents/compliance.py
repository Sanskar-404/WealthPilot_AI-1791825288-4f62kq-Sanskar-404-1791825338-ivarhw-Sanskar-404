class ComplianceVerificationAgent:
    name = "Compliance Verification Agent"

    def verify(self, portfolio, risk_result):
        checks = dict(risk_result["checks"])
        checks["human_approval_required_flag"] = not portfolio.prior_approval_required
        checks["simulated_mode_only"] = True
        return {"checks": checks, "approved_for_simulation": all(checks.values()), "rule_version": "WEALTHPILOT-SIM-1.0"}
