import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os

# Page config
st.set_page_config(page_title="Art Forms", page_icon="🎨", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('data/art_forms.csv')

art_forms = load_data()

# Title and introduction
st.title("🎨 Art Forms")
st.write("Explore traditional and contemporary art forms from different cultures.")

# Sidebar filters
st.sidebar.header("Filters")

# Region filter
regions = ['All'] + sorted(art_forms['Region'].unique().tolist())
selected_region = st.sidebar.selectbox('Select Region', regions)

# Category filter
categories = ['All'] + sorted(art_forms['Category'].unique().tolist())
selected_category = st.sidebar.selectbox('Select Category', categories)

# Filter data
filtered_arts = art_forms.copy()
if selected_region != 'All':
    filtered_arts = filtered_arts[filtered_arts['Region'] == selected_region]
if selected_category != 'All':
    filtered_arts = filtered_arts[filtered_arts['Category'] == selected_category]

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    # Popularity chart
    st.subheader("📈 Popularity by Art Form")
    fig = px.bar(
        filtered_arts.sort_values('Popularity', ascending=False),
        x='Name',
        y='Popularity',
        color='Category',
        title='Art Forms by Popularity'
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Statistics
    st.subheader("📊 Statistics")
    
    # Distribution by category
    category_counts = filtered_arts['Category'].value_counts()
    fig = px.pie(
        values=category_counts.values,
        names=category_counts.index,
        title='Distribution by Category'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Average popularity by category
    avg_popularity = filtered_arts.groupby('Category')['Popularity'].mean()
    fig = px.bar(
        x=avg_popularity.index,
        y=avg_popularity.values,
        title='Average Popularity by Category'
    )
    st.plotly_chart(fig, use_container_width=True)

# Detailed list
st.subheader("📜 Art Form Details")
for idx, art in filtered_arts.iterrows():
    with st.expander(f"{art['Name']} - {art['Region']}"):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Try to load and display the image
            image_path = f"assets/images/art/{art['Name'].lower().replace(' ', '_')}.jpg"
            if os.path.exists(image_path):
                try:
                    image = Image.open(image_path)
                    st.image(image, caption=art['Name'])
                except Exception as e:
                    st.error(f"Error loading image: {e}")
            else:
                st.info("No image available")
        
        with col2:
            st.write(f"**Category:** {art['Category']}")
            st.write(f"**Region:** {art['Region']}")
            st.write(f"**Time Period:** {art['Time_Period']}")
            st.write(f"**Popularity Score:** {art['Popularity']}/10")
            st.write(f"**Description:**")
            st.write(art['Description']) 