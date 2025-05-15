import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Cultural Data Explorer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and introduction
st.title("🌍 Cultural Data Explorer")
st.write("""
Welcome to the Cultural Data Explorer! This application allows you to explore cultural heritage sites, 
events, and art forms from around the world. Use the navigation menu on the left to explore different aspects 
of cultural data.
""")

# Load data
@st.cache_data
def load_data():
    heritage_sites = pd.read_csv('data/heritage_sites.csv')
    cultural_events = pd.read_csv('data/cultural_events.csv')
    art_forms = pd.read_csv('data/art_forms.csv')
    return heritage_sites, cultural_events, art_forms

heritage_sites, cultural_events, art_forms = load_data()

# Dashboard layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("🗺️ Global Distribution of Heritage Sites")
    
    # Create map
    m = folium.Map(location=[20, 0], zoom_start=2)
    
    # Add markers for heritage sites
    for idx, row in heritage_sites.iterrows():
        folium.Marker(
            [row['Latitude'], row['Longitude']],
            popup=f"<b>{row['Name']}</b><br>{row['Type']}",
            tooltip=row['Name']
        ).add_to(m)
    
    folium_static(m)

with col2:
    # Quick stats
    st.subheader("📊 Quick Statistics")
    
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    
    with stats_col1:
        st.metric("Heritage Sites", len(heritage_sites))
    with stats_col2:
        st.metric("Cultural Events", len(cultural_events))
    with stats_col3:
        st.metric("Art Forms", len(art_forms))
    
    # Heritage sites by type
    fig = px.pie(
        heritage_sites['Type'].value_counts().reset_index(),
        values='count',
        names='Type',
        title='Heritage Sites by Type'
    )
    st.plotly_chart(fig, use_container_width=True)

# Featured sections
st.subheader("🎯 Featured Sections")

feat_col1, feat_col2, feat_col3 = st.columns(3)

with feat_col1:
    st.markdown("""
    ### 🏛️ Heritage Sites
    Explore historical and cultural landmarks from around the world. 
    Features include:
    - Interactive map visualization
    - Filtering by country and type
    - Detailed information and images
    """)

with feat_col2:
    st.markdown("""
    ### 🎭 Cultural Events
    Discover festivals and cultural events worldwide. 
    Features include:
    - Timeline visualization
    - Date-based filtering
    - Event details and photos
    """)

with feat_col3:
    st.markdown("""
    ### 🎨 Art Forms
    Learn about traditional and contemporary art forms. 
    Features include:
    - Popularity rankings
    - Regional distribution
    - Detailed descriptions and images
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Created with ❤️ using Streamlit</p>
    <p>Data sources: Various cultural heritage databases and organizations</p>
</div>
""", unsafe_allow_html=True) 