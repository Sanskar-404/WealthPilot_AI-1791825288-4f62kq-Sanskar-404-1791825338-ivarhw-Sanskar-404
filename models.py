from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from datetime import datetime, timezone
import uuid

def now_iso():
    return datetime.now(timezone.utc).isoformat()

@dataclass
class Portfolio:
    portfolio_id: str
    client_name: str
    risk_category: str
    value_inr: float
    weights: Dict[str, float]
    restricted_assets: List[str]
    tax_rate: float = 0.20
    last_rebalance_month: int = 1
    prior_approval_required: bool = False

@dataclass
class Trade:
    portfolio_id: str
    asset_class: str
    side: str
    amount_inr: float
    current_weight: float
    target_weight: float
    estimated_cost_inr: float
    estimated_tax_inr: float
    rationale: str

@dataclass
class Decision:
    decision_id: str
    portfolio_id: str
    trigger_type: str
    priority: str
    status: str
    drift: Dict[str, float]
    trades: List[dict]
    metrics: dict
    explanations: dict
    checks: dict
    created_at: str

    @classmethod
    def create(cls, **kwargs):
        kwargs.setdefault("decision_id", "REB-" + uuid.uuid4().hex[:10].upper())
        kwargs.setdefault("created_at", now_iso())
        return cls(**kwargs)

    def to_dict(self):
        return asdict(self)
