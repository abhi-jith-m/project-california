import streamlit as st

# Set page configuration - MUST BE FIRST STREAMLIT COMMAND

import joblib
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

import gdown
import os
file_id = '18QM9AiAUroch0BFeFk2Fi5q0e5Wft1ym'
url = f'https://drive.google.com/uc?id={file_id}'
output_path = 'Dataset/random_forest.joblib'
if not os.path.exists(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Ensure directory exists
    gdown.download(url, output_path, quiet=False)
    print(f"✅ File downloaded to: {os.path.abspath(output_path)}")
else:
    print(f"⚠ File already exists at: {os.path.abspath(output_path)} - Skipping download.")

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 36px;
        font-weight: bold;
        color: #FF5733;
        text-align: center;
        margin-bottom: 20px;
    }
    .sub-header {
        font-size: 24px;
        font-weight: bold;
        color: #333;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .info-box {
        background-color: #F0F2F6;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .prediction-box {
        background-color: #E6F3FF;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-top: 20px;
    }
    .stButton>button {
        background-color: #FF5733;
        color: white;
        font-weight: bold;
        width: 100%;
        padding: 10px;
    }
    .category-container {
        background-color: #F8F9FA;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

def prediction():
    # Display app header
    st.markdown('<p class="main-header">🔥 Fire Damage Prediction System</p>', unsafe_allow_html=True)
    
    # App description
    
    try:
        # Load data and models
        with st.spinner("Loading models and data..."):
            df = pd.read_csv('Dataset/names.csv')
            df1 = pd.read_csv('Dataset/df_cleaned.csv')
            rf_classifier = joblib.load('Dataset/random_forest.joblib')
            with open("label_encoders.pkl", "rb") as f:
                label_encoders = pickle.load(f)
            sc_loaded = joblib.load("scaler.pkl")
            
            # Clean data
            df1.drop(['Unnamed: 0', 'Damage', 'City', 'County', 'Community', "Street Name", 'Street Number'], 
                    inplace=True, axis=1)
            df1_cols = list(df1.columns)
            train_cols = list(df['Columns'].unique())
            
            catcols = [
                'Street Type (e.g. road, drive, lane, etc.)',
                'State',
                'CAL FIRE Unit',
                'Incident Name',
                'Structure Type',
                'Roof Construction',
                'Vent Screen',
                'Exterior Siding',
                'Hazard Type',
                'Structure Category',
                'Eaves',
                'Window Pane',
                'Deck/Porch On Grade',
                'Deck/Porch Elevated',
                'Patio Cover/Carport Attached to Structure',
                'Fence Attached to Structure',
            ]
            
            cols_ = [
                "Hazard Type", "Structure Category", "Eaves", "Window Pane",
                "Deck/Porch On Grade", "Deck/Porch Elevated",
                "Patio Cover/Carport Attached to Structure", "Fence Attached to Structure"
            ]
            
        # Initialize input storage
        s = {}
        
        # Create main form
        with st.form("prediction_form"):
                # Create two columns for the layout
                col1, col2 = st.columns(2)
                
                # Group categorical inputs into logical sections
                with col1:
                    st.markdown('<p class="sub-header">Structure Information</p>', unsafe_allow_html=True)
                    with st.container(border=True):
                        for i in ['Structure Type', 'Structure Category', 'CAL FIRE Unit', 'State']:
                            if i in catcols and i in df1_cols:
                                unique = sorted(list(df1[i].unique()))
                                s[i] = st.selectbox(i, unique, key=f'select_{i}')
                
                    st.markdown('<p class="sub-header">Construction Details</p>', unsafe_allow_html=True)
                    with st.container(border=True):
                        for i in ['Roof Construction', 'Exterior Siding', 'Eaves', 'Window Pane', 'Vent Screen']:
                            if i in catcols and i in df1_cols:
                                unique = sorted(list(df1[i].unique()))
                                s[i] = st.selectbox(i, unique, key=f'select_{i}')
                
                with col2:
                    st.markdown('<p class="sub-header">Location Properties</p>', unsafe_allow_html=True)
                    with st.container(border=True):
                        for i in ['Street Type (e.g. road, drive, lane, etc.)', 'Incident Name']:
                            if i in catcols and i in df1_cols:
                                unique = sorted(list(df1[i].unique()))
                                s[i] = st.selectbox(i, unique, key=f'select_{i}')
                    
                    st.markdown('<p class="sub-header">Additional Structures</p>', unsafe_allow_html=True)
                    with st.container(border=True):
                        for i in ['Deck/Porch On Grade', 'Deck/Porch Elevated', 
                                'Patio Cover/Carport Attached to Structure', 'Fence Attached to Structure']:
                            if i in catcols and i in df1_cols:
                                unique = sorted(list(df1[i].unique()))
                                s[i] = st.selectbox(i, unique, key=f'select_{i}')
                    
                    st.markdown('<p class="sub-header">Hazard Information</p>', unsafe_allow_html=True)
                    with st.container(border=True):
                        for i in ['Hazard Type']:
                            if i in catcols and i in df1_cols:
                                unique = sorted(list(df1[i].unique()))
                                s[i] = st.selectbox(i, unique, key=f'select_{i}')
                
                # Add numerical inputs
                st.markdown('<p class="sub-header">Numerical Parameters</p>', unsafe_allow_html=True)
                num_cols = [j for j in train_cols if j not in catcols and j in df1_cols]
                
                # Create a multi-column layout for numerical inputs
                num_col1, num_col2 = st.columns(2)
                
                for idx, j in enumerate(num_cols):
                    # Calculate min and max values for each numerical column
                    min_val = float(df1[j].min()) if j in df1_cols else 0.0
                    max_val = float(df1[j].max()) if j in df1_cols else 100.0
                    default_val = float(df1[j].median()) if j in df1_cols else 0.0
                    
                    # Alternate between columns
                    if idx % 2 == 0:
                        with num_col1:
                            s[j] = st.number_input(
                                j, 
                                min_value=min_val,
                                max_value=max_val,
                                value=default_val,
                                step=0.1,
                                format="%.2f"
                            )
                    else:
                        with num_col2:
                            s[j] = st.number_input(
                                j, 
                                min_value=min_val,
                                max_value=max_val,
                                value=default_val,
                                step=0.1,
                                format="%.2f"
                            )
                
                # Submit button
                submit_button = st.form_submit_button(label="Generate Prediction")
            
            # If form is submitted
                if submit_button:
                 with st.spinner("Processing prediction..."):
                    # Prepare array for prediction
                    arr = np.zeros(len(train_cols))
                    
                    for key, value in s.items():
                        if key in train_cols and key not in cols_:
                            if isinstance(value, str):
                                one_hot_key = f"{key}_{value}"
                                if one_hot_key in train_cols:
                                    arr[train_cols.index(one_hot_key)] = 1
                            else:
                                arr[train_cols.index(key)] = value
                        elif key in cols_:
                            if value in label_encoders[key].classes_:
                                arr[train_cols.index(key)] = label_encoders[key].transform([value])[0]
                            else:
                                arr[train_cols.index(key)] = -1
                    
                    # Create dataframe and transform
                    arr_df = pd.DataFrame([arr], columns=train_cols)
                    arr_scaled = sc_loaded.transform(arr_df)
                    
                    # Make prediction
                    prediction = rf_classifier.predict(arr_scaled)
                    prediction_proba = rf_classifier.predict_proba(arr_scaled)
                    
                    # Display prediction
                    st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
                    
                    if prediction[0] == 1:
                        st.error("⚠️ **HIGH RISK**: The structure is predicted to sustain damage in case of fire.")
                        st.markdown(f"Confidence: {prediction_proba[0][1]*100:.2f}%")
                    else:
                        st.success("✅ **LOW RISK**: The structure is predicted to resist damage in case of fire.")
                        st.markdown(f"Confidence: {prediction_proba[0][0]*100:.2f}%")
                    
                    # Feature importance visualization
                    
                
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.write("Please ensure all required files are in the correct location.")

if __name__ == "__main__":
    prediction()