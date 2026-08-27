import streamlit as st
import requests

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="AutoValue AI",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_URL = "http://127.0.0.1:8000/predict"

# ---------------------------------------------------------
# Premium Custom Styling
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        /* Main page */
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(31, 41, 55, 0.12), transparent 30%),
                radial-gradient(circle at top right, rgba(59, 130, 246, 0.10), transparent 28%),
                linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
        }

        .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        /* Hide Streamlit chrome */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Hero */
        .hero {
            background:
                linear-gradient(
                    135deg,
                    rgba(15, 23, 42, 0.98),
                    rgba(30, 41, 59, 0.96)
                );
            border-radius: 26px;
            padding: 42px 44px;
            margin-bottom: 28px;
            box-shadow: 0 22px 55px rgba(15, 23, 42, 0.14);
            position: relative;
            overflow: hidden;
        }

        .hero::after {
            content: "";
            position: absolute;
            width: 260px;
            height: 260px;
            right: -80px;
            top: -80px;
            border-radius: 50%;
            background: radial-gradient(
                circle,
                rgba(96, 165, 250, 0.30),
                rgba(96, 165, 250, 0)
            );
        }

        .hero-badge {
            display: inline-block;
            padding: 7px 12px;
            border-radius: 999px;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.12);
            color: #bfdbfe;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 18px;
        }

        .hero-title {
            color: white;
            font-size: 46px;
            line-height: 1.08;
            font-weight: 800;
            letter-spacing: -1.2px;
            margin: 0 0 12px 0;
        }

        .hero-subtitle {
            color: #cbd5e1;
            font-size: 17px;
            line-height: 1.65;
            max-width: 730px;
            margin-bottom: 22px;
        }

        .tech-row {
            display: flex;
            flex-wrap: wrap;
            gap: 9px;
        }

        .tech-pill {
            padding: 7px 11px;
            border-radius: 999px;
            background: rgba(255,255,255,0.07);
            border: 1px solid rgba(255,255,255,0.10);
            color: #e2e8f0;
            font-size: 12px;
            font-weight: 600;
        }

        /* Cards */
        .section-card {
            background: rgba(255,255,255,0.92);
            border: 1px solid #e2e8f0;
            border-radius: 22px;
            padding: 24px;
            box-shadow: 0 12px 35px rgba(15, 23, 42, 0.06);
            margin-bottom: 18px;
        }

        .section-title {
            font-size: 20px;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 4px;
        }

        .section-subtitle {
            font-size: 13px;
            color: #64748b;
            margin-bottom: 18px;
        }

        /* Result card */
        .result-card {
            background:
                linear-gradient(
                    135deg,
                    rgba(15, 23, 42, 0.99),
                    rgba(30, 41, 59, 0.97)
                );
            border-radius: 24px;
            padding: 30px;
            box-shadow: 0 18px 45px rgba(15, 23, 42, 0.16);
            margin-top: 14px;
            color: white;
        }

        .result-label {
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            font-size: 12px;
            font-weight: 700;
        }

        .result-price {
            font-size: 48px;
            font-weight: 850;
            letter-spacing: -1px;
            margin-top: 8px;
            margin-bottom: 4px;
        }

        .result-note {
            color: #cbd5e1;
            font-size: 14px;
            line-height: 1.55;
        }

        /* Stat cards */
        .stat-card {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 18px;
            padding: 18px;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
            min-height: 110px;
        }

        .stat-label {
            color: #64748b;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            font-weight: 700;
            margin-bottom: 6px;
        }

        .stat-value {
            color: #0f172a;
            font-size: 20px;
            font-weight: 800;
        }

        .stat-desc {
            color: #64748b;
            font-size: 12px;
            margin-top: 4px;
        }

        /* Flow */
        .flow-wrap {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            align-items: center;
            justify-content: center;
            margin-top: 10px;
        }

        .flow-box {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 15px;
            padding: 12px 16px;
            color: #0f172a;
            font-size: 13px;
            font-weight: 700;
            box-shadow: 0 6px 18px rgba(15,23,42,0.04);
        }

        .flow-arrow {
            color: #94a3b8;
            font-size: 18px;
            font-weight: 900;
        }

        /* Button */
        .stButton > button {
            width: 100%;
            border-radius: 15px;
            padding: 0.95rem 1rem;
            font-weight: 800;
            font-size: 16px;
            border: none;
            background: linear-gradient(135deg, #0f172a, #334155);
            color: white;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.15);
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 14px 30px rgba(15, 23, 42, 0.20);
        }

        /* Inputs */
        .stTextInput input,
        .stNumberInput input,
        div[data-baseweb="select"] > div {
            border-radius: 12px !important;
        }

        /* Remove excess spacing */
        div[data-testid="stVerticalBlock"] > div {
            gap: 0.75rem;
        }

        /* Mobile */
        @media (max-width: 800px) {
            .hero-title {
                font-size: 34px;
            }

            .hero {
                padding: 28px 24px;
            }

            .result-price {
                font-size: 38px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Hero Section
# ---------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">AI-Powered Automotive Valuation</div>

        <div class="hero-title">
            AutoValue AI
        </div>

        <div class="hero-subtitle">
            Estimate a vehicle's selling price using machine learning.
            Enter the vehicle profile below and the system will send the
            structured data to a FastAPI inference service powered by a
            trained Random Forest regression model.
        </div>

        <div class="tech-row">
            <span class="tech-pill">Python</span>
            <span class="tech-pill">Scikit-Learn</span>
            <span class="tech-pill">Random Forest</span>
            <span class="tech-pill">FastAPI</span>
            <span class="tech-pill">Streamlit</span>
            <span class="tech-pill">REST API</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Intro Row
# ---------------------------------------------------------
left_intro, right_intro = st.columns([1.5, 1])

with left_intro:
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Vehicle Valuation Workspace</div>
            <div class="section-subtitle">
                Provide the vehicle's market and ownership details to generate
                a real-time predicted selling price.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right_intro:
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Model Pipeline</div>
            <div class="section-subtitle">
                Structured input → API → ML preprocessing → prediction
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# Main Input Form
# ---------------------------------------------------------
st.markdown(
    """
    <div class="section-card">
        <div class="section-title">Vehicle Details</div>
        <div class="section-subtitle">
            Enter the attributes used by the trained price-prediction model.
        </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2, gap="large")

with col1:
    car_name = st.text_input(
        "Vehicle name",
        value="swift",
        help="Use the vehicle name format present in the training dataset.",
    )

    year = st.number_input(
        "Model year",
        min_value=1990,
        max_value=2026,
        value=2014,
        step=1,
    )

    present_price = st.number_input(
        "Current market price (lakhs)",
        min_value=0.0,
        value=5.59,
        step=0.1,
        format="%.2f",
    )

    kms_driven = st.number_input(
        "Kilometers driven",
        min_value=0,
        value=40000,
        step=1000,
    )

with col2:
    fuel_type = st.selectbox(
        "Fuel type",
        ["Petrol", "Diesel", "CNG"],
    )

    seller_type = st.selectbox(
        "Seller type",
        ["Dealer", "Individual"],
    )

    transmission = st.selectbox(
        "Transmission",
        ["Manual", "Automatic"],
    )

    owner_label = st.selectbox(
        "Ownership history",
        [
            "0 (First Owner)",
            "1 (Second Owner)",
            "3 (Third Owner)",
        ],
    )

owner = int(owner_label.split()[0])

payload = {
    "Car_Name": str(car_name),
    "Year": int(year),
    "Present_Price": float(present_price),
    "Kms_Driven": int(kms_driven),
    "Fuel_Type": str(fuel_type),
    "Seller_Type": str(seller_type),
    "Transmission": str(transmission),
    "Owner": int(owner),
}

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Action Area
# ---------------------------------------------------------
st.write("")

predict_clicked = st.button(
    "Generate AI Price Estimate",
    use_container_width=True,
)

# ---------------------------------------------------------
# Result Logic
# ---------------------------------------------------------
if predict_clicked:
    with st.spinner("Analyzing vehicle profile and running model inference..."):
        try:
            res = requests.post(API_URL, json=payload, timeout=20)

            if res.status_code == 200:
                data = res.json()
                pred = data.get("prediction_price")

                if pred is None:
                    st.warning(
                        "The API responded successfully, but no prediction value was found."
                    )

                    with st.expander("View API response"):
                        st.json(data)

                else:
                    st.markdown(
                        f"""
                        <div class="result-card">
                            <div class="result-label">
                                Estimated Selling Price
                            </div>

                            <div class="result-price">
                                ₹ {pred:.2f} Lakhs
                            </div>

                            <div class="result-note">
                                Machine-learning estimate generated from the
                                selected vehicle attributes using the trained
                                Random Forest regression pipeline.
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.write("")

                    stat1, stat2, stat3 = st.columns(3)

                    with stat1:
                        st.markdown(
                            """
                            <div class="stat-card">
                                <div class="stat-label">Model</div>
                                <div class="stat-value">Random Forest</div>
                                <div class="stat-desc">
                                    Regression-based price prediction
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    with stat2:
                        st.markdown(
                            """
                            <div class="stat-card">
                                <div class="stat-label">Input Profile</div>
                                <div class="stat-value">8 Features</div>
                                <div class="stat-desc">
                                    Vehicle, market and ownership data
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    with stat3:
                        st.markdown(
                            """
                            <div class="stat-card">
                                <div class="stat-label">Inference</div>
                                <div class="stat-value">FastAPI</div>
                                <div class="stat-desc">
                                    Real-time REST API prediction
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

            else:
                st.error(
                    f"The prediction API returned status code {res.status_code}."
                )

                with st.expander("View API error response"):
                    st.code(res.text)

        except requests.exceptions.RequestException as e:
            st.error(
                "Unable to connect to the prediction API. "
                "Make sure the FastAPI server is running on port 8000."
            )

            with st.expander("Technical details"):
                st.code(str(e))

# ---------------------------------------------------------
# How It Works
# ---------------------------------------------------------
st.write("")
st.write("")

st.markdown(
    """
    <div class="section-card">
        <div class="section-title">How the prediction works</div>
        <div class="section-subtitle">
            A complete model-to-application inference pipeline.
        </div>

        <div class="flow-wrap">
            <div class="flow-box">Vehicle Inputs</div>
            <div class="flow-arrow">→</div>
            <div class="flow-box">FastAPI</div>
            <div class="flow-arrow">→</div>
            <div class="flow-box">Feature Processing</div>
            <div class="flow-arrow">→</div>
            <div class="flow-box">Random Forest</div>
            <div class="flow-arrow">→</div>
            <div class="flow-box">Price Estimate</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown(
    """
    <div style="
        text-align:center;
        color:#94a3b8;
        font-size:12px;
        margin-top:24px;
        padding-bottom:10px;
    ">
        Machine Learning • FastAPI • Streamlit • Python
    </div>
    """,
    unsafe_allow_html=True,
)
