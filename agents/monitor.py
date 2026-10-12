from config import ASSET_CLASSES, RISK_PROFILES

class PortfolioMonitoringAgent:
    name = "Portfolio Monitoring Agent"

    def analyze(self, portfolio):
        profile = RISK_PROFILES[portfolio.risk_category]
        drift = {a: portfolio.weights[a] - profile[a] for a in ASSET_CLASSES}
        sad = sum(abs(v) for v in drift.values())
        rmsd = (sum(v*v for v in drift.values()) / len(drift)) ** 0.5
        breach = any(abs(drift[a]) > profile["band"] for a in ASSET_CLASSES if a != "Cash")
        return {"drift": drift, "sad": sad, "rmsd": rmsd, "breach": breach, "target": {a: profile[a] for a in ASSET_CLASSES}, "band": profile["band"]}
