**AI Supply Chain Digital Twin**

An AI-powered logistics risk prediction system that forecasts shipment delays using machine learning and visualizes risk through an interactive Streamlit dashboard.

-> **Features**

- Predict shipment delay probability using ML
- Real-time risk classification (Low / Medium / High)
- Feature engineering:
  - Traffic Risk
  - Demand Pressure
  - Environmental Risk
- Interactive Streamlit dashboard
- Explainable AI risk drivers



-> **Tech Stack**

- Python
- Pandas
- Scikit-learn
- Random Forest
- Streamlit
- Joblib


-> **Model Performance**

- Accuracy: ~74.5%
- Focus: Improving recall for delay detection
- Key insight: Traffic is the strongest predictor

-> **How to Run**

1. Install dependencies
2. Run the Streamlit app

streamlit run app.py

3. Open in browser

After running the command, Streamlit will show a local URL like:

http://localhost:8501

Open it in your browser.

4. Use the app

- Enter logistics inputs (inventory, traffic, temperature, etc.)
- Click **Analyze Logistics Risk**
- View results:
  - Delay Probability
  - Risk Level (Low / Medium / High)
  - Primary Risk Drivers
  - Digital Twin Summary

