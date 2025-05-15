import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os
from datetime import datetime

# Page config
st.set_page_config(page_title="Cultural Events", page_icon="🎭", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/cultural_events.csv')
    df['Start_Date'] = pd.to_datetime(df['Start_Date'])
    df['End_Date'] = pd.to_datetime(df['End_Date'])
    return df

events = load_data()

# Title and introduction
st.title("🎭 Cultural Events")
st.write("Discover cultural events and festivals from around the world.")

# Sidebar filters
st.sidebar.header("Filters")

# Country filter
countries = ['All'] + sorted(events['Country'].unique().tolist())
selected_country = st.sidebar.selectbox('Select Country', countries)

# Event type filter
event_types = ['All'] + sorted(events['Type'].unique().tolist())
selected_type = st.sidebar.selectbox('Select Event Type', event_types)

# Date range filter
min_date = events['Start_Date'].min().date()
max_date = events['End_Date'].max().date()
date_range = st.sidebar.date_input(
    'Select Date Range',
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Filter data
filtered_events = events.copy()
if selected_country != 'All':
    filtered_events = filtered_events[filtered_events['Country'] == selected_country]
if selected_type != 'All':
    filtered_events = filtered_events[filtered_events['Type'] == selected_type]
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_events = filtered_events[
        (filtered_events['Start_Date'].dt.date >= start_date) &
        (filtered_events['End_Date'].dt.date <= end_date)
    ]

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    # Timeline
    st.subheader("📅 Event Timeline")
    fig = px.timeline(
        filtered_events,
        x_start='Start_Date',
        x_end='End_Date',
        y='Name',
        color='Type',
        title='Event Timeline'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Statistics
    st.subheader("📊 Statistics")
    
    # Events by type
    type_counts = filtered_events['Type'].value_counts()
    fig = px.pie(
        values=type_counts.values,
        names=type_counts.index,
        title='Distribution by Event Type'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Events by country
    country_counts = filtered_events['Country'].value_counts().head(10)
    fig = px.bar(
        x=country_counts.index,
        y=country_counts.values,
        title='Top 10 Countries by Number of Events'
    )
    st.plotly_chart(fig, use_container_width=True)

# Detailed list
st.subheader("📜 Event Details")
for idx, event in filtered_events.iterrows():
    with st.expander(f"{event['Name']} - {event['Country']}"):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Try to load and display the image
            image_path = f"assets/images/events/{event['Name'].lower().replace(' ', '_')}.jpg"
            if os.path.exists(image_path):
                try:
                    image = Image.open(image_path)
                    st.image(image, caption=event['Name'])
                except Exception as e:
                    st.error(f"Error loading image: {e}")
            else:
                st.info("No image available")
        
        with col2:
            st.write(f"**Type:** {event['Type']}")
            st.write(f"**Location:** {event['Location']}, {event['Country']}")
            st.write(f"**Dates:** {event['Start_Date'].strftime('%B %d, %Y')} - {event['End_Date'].strftime('%B %d, %Y')}")
            st.write(f"**Description:**")
            st.write(event['Description']) 