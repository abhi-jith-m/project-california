import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

def Visualize(df):
    df.drop(columns=['Unnamed: 0'],inplace=True)
    st.markdown("""
        <style>
        .main-title {
            font-size: 36px !important;
            font-family: 'Arial', sans-serif;
            font-weight: bold;
            color: #D72638;
            text-align: center;
            padding: 15px;
            margin-top:-55px !important;
            
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
    st.markdown('<p class="main-title">📈 Charts & Visualizations </p>',unsafe_allow_html=True)
    
    tabs=st.tabs(['Countplot','Scatterplot','Lineplot','Boxplot','Other plots'])
    with tabs[0]:
        st.write('')
        st.write('')
        st.markdown('<p class="section-title">🏆 Top 20 Cities by Occurrence</p>', unsafe_allow_html=True)
        top20 = df['City'].value_counts().head(20).index.tolist()
        
    
        fig = px.histogram(
           df[df['City'].isin(top20)] , 
            x='City', 
            histfunc="count", 
            text_auto=True, 
            color='City' # Adds color variation for categories
            )

        fig.update_layout(
                title=f"Top 20 Cities",
                xaxis_title='City',
                yaxis_title="Count",
                bargap=0.2,
                template="plotly_dark",  # Optional dark theme
            )

        st.plotly_chart(fig, use_container_width=True)
        st.write('')
        
        categorical_columns = ['Damage',
                                'Street Type (e.g. road, drive, lane, etc.)',
                                'County',
                                'Hazard Type',
                                'Structure Type',
                                'Structure Category',
                                'Roof Construction',
                                'Eaves',
                                'Vent Screen',
                                'Exterior Siding',
                                'Window Pane',
                                'Deck/Porch On Grade',
                                'Deck/Porch Elevated',
                                'Patio Cover/Carport Attached to Structure',
                                'Fence Attached to Structure']

        for col in categorical_columns:
            st.markdown(f'<p class="section-title">📊 Distribution of {col}</p>', unsafe_allow_html=True)
            
            # Create the countplot
            fig = px.histogram(df, x=col, histfunc="count", text_auto=True, color=col)
            
            # Update layout
            fig.update_layout(title=f"Count of {col}", xaxis_title=col, yaxis_title="Count", bargap=0.2)
            
            # Show plot in Streamlit
            st.plotly_chart(fig, use_container_width=True)
    with tabs[1]:
            st.write('')
            st.markdown(f'<p class="section-title">🌍 Geographic Distribution of Data</p>', unsafe_allow_html=True)
            fig = px.scatter(df,x="Latitude", y="Longitude",
                            color_discrete_sequence=['crimson'],)
            st.plotly_chart(fig, use_container_width=True)
            st.write('')
            
            st.markdown(f'<p class="section-title"> 🔥Geographic Distribution of Damage</p>', unsafe_allow_html=True)
            fig = px.scatter(df, x="Latitude", y="Longitude",
                        color='Damage',
                        hover_name="Damage",   
                        color_discrete_sequence=px.colors.qualitative.Safe,  
            )
            st.plotly_chart(fig, use_container_width=True)
            

            st.write('')
            df['City']=df['City'].str.strip().str.lower()
            st.markdown(f'<p class="section-title"> 🌆Geographic Distribution of City</p>', unsafe_allow_html=True)
            fig = px.scatter(df, x="Latitude", y="Longitude",
                        color='City',
                        hover_name="City",   
                        color_discrete_sequence=px.colors.qualitative.Prism, 
            )

            fig.update_layout(mapbox_style="carto-darkmatter")
            st.plotly_chart(fig, use_container_width=True)
            
            st.write('')
            
            st.markdown(f'<p class="section-title"> 🌆Geographic Distribution of Hazard Type</p>', unsafe_allow_html=True)
            fig = px.scatter(df, x="Latitude", y="Longitude",
                        color='Hazard Type',
                        hover_name="City",   
                        color_discrete_sequence=px.colors.qualitative.Set1, 
            )

            fig.update_layout(mapbox_style="carto-darkmatter")
            st.plotly_chart(fig, use_container_width=True)
            
            st.write('')
            
            df['Community']=df['Community'].str.strip().str.lower()
            st.markdown(f'<p class="section-title"> 🏙️ Community Distribution</p>', unsafe_allow_html=True)

            fig = px.scatter(df, x="Latitude", y="Longitude",
                        color='Community',
                        hover_name="Community",   
                        color_discrete_sequence=px.colors.qualitative.Prism, 
            )

            st.plotly_chart(fig, use_container_width=True)
            
            st.write('')
            st.markdown(f'<p class="section-title">🗺️ County-Wise Distribution</p>', unsafe_allow_html=True)

            df['County']=df['County'].str.strip().str.lower()
            fig = px.scatter(df, x="Latitude", y="Longitude",
                        color='County',
                        hover_name="County",   
                        color_discrete_sequence=px.colors.qualitative.Prism, 
            )

            st.plotly_chart(fig, use_container_width=True)
            
    with tabs[2]:
        
        st.write('')
        st.markdown(f'<p class="section-title">📅 Trend of Fire Incidents by Year Built</p>', unsafe_allow_html=True)
        yearly_trend = df['Year Built (parcel)'].value_counts().sort_index()
        fig = px.line(yearly_trend, x=yearly_trend.index, y=yearly_trend.values,
                    labels={'x': 'Year Built', 'y': 'Number of Incidents'},
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.write('')
       
        st.markdown(f'<p class="section-title">📈Trend of Average Assessed Value Over Years</p>', unsafe_allow_html=True)
        avg_value_trend = df.groupby('Year Built (parcel)')["Assessed Improved Value (parcel)"].mean().dropna()
        fig = px.line(avg_value_trend, x=avg_value_trend.index, y=avg_value_trend.values,
                    labels={'x': 'Year Built', 'y': 'Average Assessed Value'},
                    color_discrete_sequence=["#2ca02c"])

        st.plotly_chart(fig, use_container_width=True)
        
        st.write('')
        st.markdown(f'<p class="section-title">🏡 Growth of Total Assessed Property Value Over Time</p>', unsafe_allow_html=True)
        total_value_trend = df.groupby("Year Built (parcel)")["Assessed Improved Value (parcel)"].sum().dropna()
        fig = px.line(total_value_trend, x=total_value_trend.index, y=total_value_trend.values,
                    
                    labels={'x': 'Year Built', 'y': 'Total Assessed Value'},
                    color_discrete_sequence=["#ff7f0e"])

        st.plotly_chart(fig, use_container_width=True)

    with tabs[3]:
        
        st.write('')
        st.markdown(f'<p class="section-title">📆 Box Plot – Year Built Distribution Across Structure Categories</p>', unsafe_allow_html=True)
        fig = px.box(df, x="Structure Category", y="Year Built (parcel)")
        st.plotly_chart(fig)
        
        
        st.write('')
        st.markdown(f'<p class="section-title">🏗️ Box Plot – Assessed Value vs Structure Category</p>', unsafe_allow_html=True)
        fig = px.box(df, x="Structure Category", y="Assessed Improved Value (parcel)")
        st.plotly_chart(fig)
        
        st.write('')
        st.markdown(f'<p class="section-title">🎭 Box Plot – Finding Outliers in Assessed Values</p>', unsafe_allow_html=True)
        fig = px.box(df, y="Assessed Improved Value (parcel)")
        st.plotly_chart(fig)
        
    with tabs[4]:
        
        st.write('')
        st.markdown(f'<p class="section-title">🚨 Pie Chart – Proportion of Different Damage Categories</p>', unsafe_allow_html=True)
        fig = px.pie(df, names="Damage")
        st.plotly_chart(fig)
        
        st.write('')
        
        st.markdown(f'<p class="section-title">📏 Structure Height vs Damage Distribution</p>', unsafe_allow_html=True)
        fig = px.density_contour(df, x="Damage", y="Structure Type",color="Damage")
        st.plotly_chart(fig)


