import pandas as pd
import streamlit as st
from Data import data
from Charts import Visualize
from Prediction import prediction

def Main(df):
    path = r"Dataset/df_cleaned.csv"
    df_cleaned = pd.read_csv(path, low_memory=False)
    df.columns = df.columns.str.lstrip('_*#').str.strip()

    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "Home"

    # Sidebar UI with uniform-width navigation buttons
    with st.sidebar:
        st.title("Navigation")
        
        # Set page via radio buttons
        selected = st.radio(
            "",
            ["🏠 Home", "📊 Data", "📈 Charts", "🤖 Prediction"],
            index=["Home", "Data", "Charts", "Prediction"].index(st.session_state.page),
            label_visibility="collapsed"
        )
        st.session_state.page = selected.split(" ", 1)[1]  # Extract actual page name

        # CSS for styling the radio buttons
        st.markdown("""
            <style>
                .stRadio > div {
                    flex-direction: column;
                }
                .stRadio div[role="radiogroup"] label {
                    background-color: #1f2937;
                    padding: 0.6rem 1rem;
                    margin-bottom: 8px;
                    width: 100%;
                    border-radius: 10px;
                    border: 1px solid #4b5563;
                    font-weight: 500;
                    color: white;
                    cursor: pointer;
                    transition: background 0.3s ease;
                }
                .stRadio div[role="radiogroup"] label:hover {
                    background-color: #374151;
                }
                .stRadio div[role="radiogroup"] input:checked + div {
                    background-color: #4b5563;
                }
            </style>
        """, unsafe_allow_html=True)

    # Page Routing
    if st.session_state.page == "Home":
    # Enhanced CSS for dark-themed styling and larger header
        st.markdown("""
    <style>
    h2 {
        font-size: 36px;
        font-weight: 800;
        color: #ff4b4b;
        margin-bottom: 30px;
        text-align: center;
    }

    .info-box {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 35px;
        border-radius: 15px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        max-width: 950px;
        margin: auto;
    }

    .info-box h3 {
        font-size: 24px;
        color: #f1f5f9;
        margin-bottom: 20px;
        font-weight: 700;
    }

    .info-box p {
        font-size: 1.15rem;
        color: #cbd5e1;
        line-height: 1.8;
        margin-bottom: 18px;
    }

    body {
        background-color: #0f172a;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
        st.markdown('<h2 class="main-header">🔥 California Wildfire Damage Prediction System</h2>', unsafe_allow_html=True)

        # Info Box
        st.markdown("""
        <div class="info-box">
            <h3>📍 Predicting Building Vulnerability to California Wildfires</h3>
            <p>🔥 This powerful dashboard uses machine learning to predict the likelihood of damage to buildings during wildfire events.</p>
            <p>🌿 It considers structural features, environmental conditions, and location-based risk factors.</p>
            <p>🛡️ Built to empower property owners, emergency responders, and insurers with insights to act before disaster strikes.</p>
        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.page == "Data":
        data(df, df_cleaned)

    elif st.session_state.page == "Charts":
        Visualize(df_cleaned)

    elif st.session_state.page == "Prediction":
        prediction()
