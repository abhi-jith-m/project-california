import streamlit as st
import pandas as pd
from Main import Main

# ✅ Set page configuration (Only once)
st.set_page_config(
    page_title="Fire Damage Prediction",
    page_icon="🔥",
    layout="wide"
)

# ✅ Initialize session state page variable only if not already set
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ✅ Load your dataset
path = r"Dataset/california.csv"
df = pd.read_csv(path, low_memory=False)

# ✅ Call Main layout function
Main(df)
