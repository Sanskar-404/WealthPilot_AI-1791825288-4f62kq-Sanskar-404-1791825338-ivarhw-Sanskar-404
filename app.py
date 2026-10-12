import streamlit as st
import pandas as pd
import plotly.express as px
from config import RISK_PROFILES, ASSET_CLASSES
from data.synthetic import generate_portfolios
from engine.orchestrator import OrchestratorAgent
from engine.backtest import run_backtest
from audit.logger import read_events

st.set_page_config(page_title="WealthPilot AI", page_icon="📈", layout="wide")
st.title("📈 WealthPilot AI")
st.caption("Autonomous portfolio rebalancing • Explainable multi-agent simulation • Synthetic data only")

with st.sidebar:
    st.header("Simulation controls")
    n = st.slider("Synthetic portfolios", 20, 500, 100, 20)
    risk_filter = st.selectbox("Risk category", ["All"] + list(RISK_PROFILES))
    month = st.selectbox("Simulation month", list(range(1, 13)), index=5)
    event = st.selectbox("Market event", ["None", "Market crash", "Regulatory change", "Client life event", "Tax harvesting window"])
    page = st.radio("Workspace", ["Overview", "Agent decision", "Backtesting", "Audit trail"])

portfolios = generate_portfolios(n, seed=7)
if risk_filter != "All":
    portfolios = [p for p in portfolios if p.risk_category == risk_filter]
engine = OrchestratorAgent()

if page == "Overview":
    a,b,c,d = st.columns(4)
    a.metric("Assets under management", "₹25,000 Cr", "Fictional mandate")
    b.metric("Client portfolios", "50,000", "Scaled synthetic sample")
    c.metric("Risk categories", "5", "Category-specific drift bands")
    d.metric("Agent roles", "6", "Orchestrator + specialists")
    st.subheader("Risk category policy")
    df = pd.DataFrame([{"Risk category": k, "Portfolios in mandate": v["portfolios"], "Equity %": v["Equity"]*100,
                        "Fixed income %": v["Fixed Income"]*100, "Alternatives %": v["Alternatives"]*100,
                        "Cash %": v["Cash"]*100, "Drift band %": v["band"]*100} for k,v in RISK_PROFILES.items()])
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.info("This prototype simulates the five risk categories and samples portfolios locally. It is not connected to live accounts or market feeds.")
    chart = px.bar(df, x="Risk category", y="Drift band %", title="Rebalancing tolerance by risk category")
    st.plotly_chart(chart, use_container_width=True)

elif page == "Agent decision":
    pmap = {p.portfolio_id: p for p in portfolios}
    if not pmap:
        st.warning("No portfolios in this category.")
    else:
        pid = st.selectbox("Portfolio", list(pmap))
        p = pmap[pid]
        st.write(f"**{p.risk_category}** · Value ₹{p.value_inr:,.0f} · Restricted assets: {', '.join(p.restricted_assets) or 'None'}")
        weights = pd.DataFrame({"Asset class": list(p.weights), "Current %": [x*100 for x in p.weights.values()],
                                "Target %": [RISK_PROFILES[p.risk_category][a]*100 for a in p.weights]})
        st.plotly_chart(px.bar(weights, x="Asset class", y=["Current %", "Target %"], barmode="group"), use_container_width=True)
        forced = st.checkbox("Human override: force a review")
        override_note = st.text_input("Override reason", "Advisor requested review")
        event_arg = None if event == "None" else event
        if st.button("Run multi-agent workflow", type="primary"):
            decision = engine.process(p, month=month, event=event_arg, force=forced, override_note=override_note)
            if decision is None:
                st.success("No trigger. Portfolio remains under monitoring.")
            else:
                st.session_state["last_decision"] = decision.to_dict()
                st.success(f"Decision {decision.decision_id} created · {decision.status}")
        raw = st.session_state.get("last_decision")
        if raw and raw["portfolio_id"] == pid:
            st.subheader("Proposed trades")
            st.dataframe(pd.DataFrame(raw["trades"]), use_container_width=True, hide_index=True)
            m = raw["metrics"]
            cols = st.columns(4)
            cols[0].metric("SAD", f"{m['sad_pct']:.2f}%")
            cols[1].metric("Gross turnover", f"{m['gross_turnover_pct']:.2f}%")
            cols[2].metric("Est. cost", f"₹{m['estimated_cost_inr']:,.0f}")
            cols[3].metric("Illustrative tax", f"₹{m['estimated_tax_inr']:,.0f}")
            for audience, label in [("client","Client explanation"),("advisor","Advisor explanation"),("compliance","Compliance explanation")]:
                with st.expander(label, expanded=audience=="client"):
                    st.write(raw["explanations"][audience])
            st.subheader("Pre-trade checks")
            st.json(raw["checks"])
            action = st.selectbox("Human review action", ["APPROVE", "REJECT", "OVERRIDE"])
            reviewer = st.text_input("Reviewer ID", "advisor-demo")
            note = st.text_input("Review note", "")
            if st.button("Record review"):
                from models import Decision
                # Audit review is recorded without executing any real trade.
                engine.review(Decision(**raw), action, reviewer, note)
                st.success("Review action appended to audit trail. No trades were executed.")

elif page == "Backtesting":
    st.subheader("Legacy vs WealthPilot agent — synthetic 12-month backtest")
    risk = st.selectbox("Backtest risk profile", list(RISK_PROFILES), index=2)
    scenario = st.selectbox("Market scenario", ["mixed", "normal", "crash"])
    if st.button("Run backtest", type="primary"):
        result = run_backtest(risk, scenario=scenario)
        st.session_state["backtest_result"] = result
    result = st.session_state.get("backtest_result", run_backtest(risk, scenario=scenario))
    st.dataframe(result, use_container_width=True)
    numeric = result.select_dtypes("number").reset_index().melt(id_vars="Strategy", var_name="Metric", value_name="Value")
    st.plotly_chart(px.bar(numeric, x="Metric", y="Value", color="Strategy", barmode="group", title="Strategy metric comparison"), use_container_width=True)
    st.warning("Backtest is synthetic and illustrative. Strategy differences are not proof of real-world alpha. Validate with survivorship-bias-free data, realistic tax lots, slippage and out-of-sample testing.")

else:
    st.subheader("Append-only simulation audit log")
    events = read_events()
    if events:
        df = pd.DataFrame(events)
        df["payload"] = df["payload"].apply(lambda x: str(x)[:500])
        st.dataframe(df.iloc[::-1], use_container_width=True, hide_index=True)
        st.download_button("Download audit log JSON", df.to_json(orient="records", indent=2), "wealthpilot_audit.json", "application/json")
    else:
        st.info("No audit events yet. Run an agent decision to populate the log.")
