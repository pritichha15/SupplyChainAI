import streamlit as st
import pandas as pd
import joblib

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="AI Supply Chain Digital Twin",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS (YOUR LUXURY UI KEPT)
# --------------------------------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700&family=Cormorant+Garamond:wght@500;600;700&display=swap');

.stApp {
    background:
        radial-gradient(circle at 15% 20%, rgba(37,99,235,0.25), transparent 40%),
        radial-gradient(circle at 85% 30%, rgba(212,175,55,0.12), transparent 45%),
        radial-gradient(circle at 50% 90%, rgba(56,189,248,0.10), transparent 50%),
        linear-gradient(180deg, #05070f 0%, #0b1220 50%, #070a12 100%);
    font-family: 'Manrope', sans-serif;
    color: #e5e7eb;
}

h1 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 44px !important;
    color: #f8fafc;
}

h2, h3 {
    font-family: 'Manrope', sans-serif;
    color: #cbd5e1;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    border-radius: 16px;
    padding: 18px;
    border: 1px solid rgba(148,163,184,0.18);
}

[data-testid="stMetricValue"] {
    font-size: 22px;
    font-weight: 700;
    color: #f8fafc;
}

div.stButton > button {
    background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 40%, #d4af37 120%);
    color: white;
    border-radius: 12px;
    height: 52px;
    font-weight: 600;
}

input, select {
    font-family: 'Manrope', sans-serif;
    background: rgba(255,255,255,0.04) !important;
    border-radius: 12px !important;
    color: #e5e7eb !important;
}

.summary-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(148,163,184,0.18);
    padding: 18px;
    border-radius: 14px;
    line-height: 1.8;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------
model = joblib.load("rf_delay_predictor.pkl")

# --------------------------------------------------
# EXPLAINABILITY
# --------------------------------------------------
def explain_prediction(traffic, demand_pressure, environmental_risk, inventory):
    reasons = []

    if traffic == "Heavy":
        reasons.append("Heavy Traffic Conditions")
    elif traffic == "Detour":
        reasons.append("Route Diversion Detected")

    if demand_pressure > 3:
        reasons.append("High Demand Pressure")

    if environmental_risk > 2000:
        reasons.append("Adverse Environmental Conditions")

    if inventory < 200:
        reasons.append("Low Inventory Availability")

    return reasons

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown("# AI Supply Chain Digital Twin")
st.markdown("Real-Time Logistics Risk Monitoring Dashboard")

st.divider()

# --------------------------------------------------
# INPUTS
# --------------------------------------------------
left, right = st.columns(2)

with left:
    inventory = st.number_input("Inventory Level", min_value=0, value=500)
    temperature = st.number_input("Temperature (°C)", value=30.0)
    waiting_time = st.number_input("Waiting Time (minutes)", min_value=0, value=20)

with right:
    traffic = st.selectbox("Traffic Status", ["Clear", "Detour", "Heavy"])
    humidity = st.number_input("Humidity (%)", value=60.0)
    demand_forecast = st.number_input("Demand Forecast", min_value=0, value=1000)

# --------------------------------------------------
# PREDICTION
# --------------------------------------------------
if st.button("Analyze Logistics Risk"):

    traffic_map = {"Clear": 0, "Detour": 1, "Heavy": 2}
    traffic_risk = traffic_map[traffic]

    demand_pressure = demand_forecast / (inventory + 1)
    environmental_risk = temperature * humidity

    input_data = pd.DataFrame([{
        "Latitude": 0,
        "Longitude": 0,
        "Inventory_Level": inventory,
        "Temperature": temperature,
        "Humidity": humidity,
        "Waiting_Time": waiting_time,
        "User_Transaction_Amount": 1000,
        "User_Purchase_Frequency": 5,
        "Asset_Utilization": 80,
        "Demand_Forecast": demand_forecast,
        "Traffic_Risk": traffic_risk,
        "Demand_Pressure": demand_pressure,
        "Environmental_Risk": environmental_risk
    }])

    probability = model.predict_proba(input_data)[0][1]

    # --------------------------------------------------
    # RISK CLASSIFICATION
    # --------------------------------------------------
    if probability >= 0.75:
        risk_icon = "🔺"
        risk_label = "HIGH RISK"
        bar_color = "#ef4444"
    elif probability >= 0.40:
        risk_icon = "🟠"
        risk_label = "MEDIUM RISK"
        bar_color = "#f59e0b"
    else:
        risk_icon = "🟢"
        risk_label = "LOW RISK"
        bar_color = "#22c55e"

    # --------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------
    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Delay Probability",
            f"{risk_icon} {probability:.1%} ({risk_label})"
        )

    with c2:
        st.metric(
            "Risk Level",
            risk_label
        )

    with c3:
        st.metric(
            "Traffic Status",
            traffic
        )

    st.divider()

    # --------------------------------------------------
    # COLORED PROGRESS BAR
    # --------------------------------------------------
    st.subheader("Risk Assessment")

    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 10px;
    ">
        <div style="
            width: 100%;
            background: #1f2937;
            border-radius: 10px;
            height: 18px;
            overflow: hidden;
        ">
            <div style="
                width: {probability * 100}%;
                height: 18px;
                background: {bar_color};
                transition: 0.5s;
            "></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write(f"{risk_icon} Predicted delay probability: {probability:.1%}")

    st.divider()

    # --------------------------------------------------
    # EXPLANATIONS
    # --------------------------------------------------
    st.subheader("Primary Risk Drivers")

    reasons = explain_prediction(
        traffic,
        demand_pressure,
        environmental_risk,
        inventory
    )

    if reasons:
        for r in reasons:
            st.info(r)
    else:
        st.success("No significant operational risk drivers detected.")

    st.divider()

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------
    st.subheader("Digital Twin Summary")

    summary_html = f"""
    <div class="summary-box">
        <b>Inventory Level:</b> {inventory}<br>
        <b>Traffic Status:</b> {traffic}<br>
        <b>Temperature:</b> {temperature} °C<br>
        <b>Humidity:</b> {humidity} %<br>
        <b>Waiting Time:</b> {waiting_time} minutes<br>
        <b>Demand Forecast:</b> {demand_forecast}
    </div>
    """

    st.markdown(summary_html, unsafe_allow_html=True)