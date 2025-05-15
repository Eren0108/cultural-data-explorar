import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import plotly.express as px
from PIL import Image
import os

# Page config
st.set_page_config(page_title="Heritage Sites", page_icon="🏛️", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('data/heritage_sites.csv')

heritage_sites = load_data()

# Title and introduction
st.title("🏛️ Heritage Sites")
st.write("Explore cultural heritage sites from around the world.")

# Sidebar filters
st.sidebar.header("Filters")

# Country filter
countries = ['All'] + sorted(heritage_sites['Country'].unique().tolist())
selected_country = st.sidebar.selectbox('Select Country', countries)

# Type filter
site_types = ['All'] + sorted(heritage_sites['Type'].unique().tolist())
selected_type = st.sidebar.selectbox('Select Site Type', site_types)

# Filter data
filtered_sites = heritage_sites.copy()
if selected_country != 'All':
    filtered_sites = filtered_sites[filtered_sites['Country'] == selected_country]
if selected_type != 'All':
    filtered_sites = filtered_sites[filtered_sites['Type'] == selected_type]

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    # Map
    st.subheader("📍 Location Map")
    m = folium.Map(location=[filtered_sites['Latitude'].mean(), 
                           filtered_sites['Longitude'].mean()],
                  zoom_start=2)
    
    for idx, row in filtered_sites.iterrows():
        folium.Marker(
            [row['Latitude'], row['Longitude']],
            popup=f"<b>{row['Name']}</b><br>{row['Description'][:100]}...",
            tooltip=row['Name']
        ).add_to(m)
    
    folium_static(m)

with col2:
    # Statistics
    st.subheader("📊 Statistics")
    
    # Count by type
    type_counts = filtered_sites['Type'].value_counts()
    fig = px.pie(values=type_counts.values, 
                names=type_counts.index,
                title='Distribution by Type')
    st.plotly_chart(fig, use_container_width=True)
    
    # Count by country
    country_counts = filtered_sites['Country'].value_counts().head(10)
    fig = px.bar(x=country_counts.index,
                y=country_counts.values,
                title='Top 10 Countries by Number of Sites')
    st.plotly_chart(fig, use_container_width=True)

# Detailed list
st.subheader("📜 Site Details")
for idx, site in filtered_sites.iterrows():
    with st.expander(f"{site['Name']} - {site['Country']}"):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Try to load and display the image
            image_path = f"assets/images/heritage/{site['Name'].lower().replace(' ', '_')}.jpg"
            if os.path.exists(image_path):
                try:
                    image = Image.open(image_path)
                    st.image(image, caption=site['Name'])
                except Exception as e:
                    st.error(f"Error loading image: {e}")
            else:
                st.info("No image available")
        
        with col2:
            st.write(f"**Type:** {site['Type']}")
            st.write(f"**Location:** {site['Location']}")
            st.write(f"**Year Established:** {site['Year']}")
            st.write(f"**Description:**")
            st.write(site['Description']) 