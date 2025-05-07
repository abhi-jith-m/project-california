import pandas as pd
import streamlit as st


def data(df, df_cleaned):
    st.markdown("""

        <style>
        .main-title {
            font-size: 36px !important;
            font-family: 'Arial', sans-serif;
            font-weight: bold;
            color: #D72638;
            text-align: center;
            padding: 15px;
        }
        
        .section-title {
            font-size: 24px !important;
            font-weight: bold;
            color: #3B3B98;
            margin-top: 20px;
            padding-bottom: 5px;
            border-bottom: 2px solid #3B3B98;
        }
        
        .highlight-text {
            font-size: 18px;
            font-weight: bold;
            color: #FF6600;
        }

        .dataframe-container {
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            padding: 10px;
            background-color: #F8F9FA;
        }
        
        .expander-title {
            font-size: 20px;
            font-weight: bold;
            color: #4CAF50;
        }
        </style>
    """, unsafe_allow_html=True)

    # Title
    st.markdown('<p class="main-title">📊 Data Exploration</p>', unsafe_allow_html=True)

    # ✅ Creating Tabs
    tab1, tab2 = st.tabs(['Dataset', 'Preprocessing'])

    # 📌 Dataset Tab
    with tab1:
        st.markdown('<p class="section-title">📂 Raw Dataset</p>', unsafe_allow_html=True)
        st.dataframe(df)

        st.markdown('<p class="section-title">📜 Dataset Information</p>', unsafe_allow_html=True)
    
        df_info = pd.DataFrame({
                'Columns': df.columns.tolist(),
                "Null Count": df.isna().sum().values,
                "Dtype": df.dtypes.values,
            })
        st.dataframe(df_info, use_container_width=True)

        st.markdown('<p class="section-title">📊 Summary Statistics</p>', unsafe_allow_html=True)
       
        st.dataframe(df.describe(), use_container_width=True)

    # 📌 Preprocessing Tab
    with tab2:
        st.markdown('<p class="section-title">🔍 Missing Value Analysis</p>', unsafe_allow_html=True)

        # Finding Missing Values
        missing_cols = df.columns[df.isna().mean() * 100 > 50]
        
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<p class="highlight-text">🛑 Missing Value Count</p>', unsafe_allow_html=True)
            df_missing_summary = df[missing_cols].isna().sum().reset_index()
            df_missing_summary.columns = ['Columns', 'Missing Count']
            st.dataframe(df_missing_summary.sort_values(by='Missing Count', ascending=False).reset_index(drop=True), use_container_width=True)

        with col2:
            st.markdown('<p class="highlight-text">📉 Missing Value Percentage</p>', unsafe_allow_html=True)
            df_missing_percent = df[missing_cols].isna().mean() * 100
            df_missing_percent = df_missing_percent.reset_index()
            df_missing_percent.columns = ['Columns', 'Missing Percent']
            st.dataframe(df_missing_percent.sort_values(by='Missing Percent', ascending=False).reset_index(drop=True), use_container_width=True)

    
        with st.expander('🛠 Handling Missing Values', expanded=False):
            st.write("To be implemented...")

        st.markdown('<p class="section-title">✅ Cleaned Dataset</p>', unsafe_allow_html=True)
        st.dataframe(df_cleaned.drop('Unnamed: 0', axis=1), use_container_width=True)
