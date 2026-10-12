# Architecture and design notes

## Agent sequence
1. Portfolio Monitoring Agent computes allocation drift, SAD and RMSD.
2. Trigger Evaluation Agent prioritises event-driven triggers, threshold breaches, then quarterly reviews.
3. Portfolio Analyst / Trade Generation Agent proposes target-directed buys and sells under turnover and restricted-asset rules.
4. Tax Optimisation Agent estimates tax from synthetic lots and uses an illustrative high-cost-lot-first policy.
5. Risk Assessment Agent checks long-only, turnover, cash and restricted-asset controls.
6. Compliance Verification Agent produces a versioned control result.
7. Explanation Generation Agent writes client, advisor and compliance narratives.
8. Orchestrator creates a decision and appends it to the audit log. Human review actions are logged separately.

## Core metrics
- Absolute drift per asset = actual weight − target weight
- SAD = sum of absolute asset-class drift
- RMSD = square root of mean squared asset-class drift
- Turnover = gross proposed trade value / portfolio value
- Costs = asset-specific basis-point estimate × proposed trade value

## Production hardening backlog
- Replace synthetic market data with licensed, timestamped market/custody feeds and stale-data gates.
- Use CVXPY or another validated solver for full constraint optimisation.
- Add instrument-level tax lots, holding periods, realised gain/loss netting and jurisdiction-specific rules.
- Add role-based access control, encrypted secrets, signed audit events, retention policy and tamper-evident storage.
- Implement event bus, durable queues, idempotency keys, retry policies and dead-letter queues.
- Add pre-trade limits, kill switch, circuit breakers, approval matrix and broker sandbox.
- Use out-of-sample historical backtests, walk-forward tests, stress tests and transaction-cost calibration.
- Validate all regulatory interpretations with qualified legal/compliance professionals.
