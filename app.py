import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# Iskra Branding & Layout
st.set_page_config(page_title="Iskra Demo", layout="wide")
st.title("⚡ ISKRA - Intelligence, Surveillance, and Reconnaissance")
st.markdown("Heatmapping potential FPV drone launch spots through video back-casting.")

# 1. Ingestion Simulation
st.sidebar.header("Data Collection")
drone_input = st.sidebar.number_input("Detected drone feeds", 10, 500, 100)
conf_threshold = st.sidebar.slider("AI Confidence Threshold", 0.0, 1.0, 0.7)

# 2. Simulated Back-casted Data (Kherson area coordinates)
view_state = pdk.ViewState(latitude=46.63, longitude=32.61, zoom=12, pitch=45)

# Generate points weighted towards potential launch clusters
data = pd.DataFrame({
    'lat': np.random.normal(46.64, 0.015, drone_input),
    'lon': np.random.normal(32.62, 0.015, drone_input),
    'confidence': np.random.uniform(0.1, 1.0, drone_input)
})
filtered_data = data[data['confidence'] >= conf_threshold]

# 3. Layers for Visualization
heatmap = pdk.Layer(
    "HeatmapLayer", filtered_data, get_position=["lon", "lat"],
    get_weight="confidence", radius_pixels=70
)
points = pdk.Layer(
    "ScatterplotLayer", filtered_data, get_position=["lon", "lat"],
    get_color=[255, 0, 0, 200], get_radius=120
)

# 4. Main View
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/dark-v10",
    initial_view_state=view_state,
    layers=[heatmap, points]
))

# 5. Concept Implementation - Vetted Volunteers
st.divider()
st.subheader("Volunteer Moderation Hub (Tier 1 & 2)")
c1, c2 = st.columns(2)
with c1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aerial_view_of_Kherson.jpg", 
             caption="Back-casting: Landmark analysis in progress")
with c2:
    st.write("Vetted local volunteers are validating this sector's findings.")
    if st.button("Disseminate to DELTA System"):
        st.success("Target coordinates integrated into the Single Operational Picture.")
