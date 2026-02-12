import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

# --- Konfiguraatio ---
st.set_page_config(page_title="ISKRA | Intelligence Snapshot", layout="wide")

KHERSON_LAT, KHERSON_LON = 46.6394, 32.6139

# Käytetään session_statea, jotta pisteet eivät muutu vaikka sivu latautuisi, 
# ellet itse halua päivittää niitä (R-näppäin).
if 'static_data' not in st.session_state:
    targets = []
    
    # 1. PUNAISET KESKITTYMÄT (Strike Zones)
    # Rypäs 1: Oleshky/Hersonin itäpuoli
    for i in range(6):
        targets.append({
            'pos': [46.620 + np.random.uniform(-0.004, 0.004), 32.715 + np.random.uniform(-0.004, 0.004)],
            'obs': [46.660 + np.random.uniform(-0.005, 0.005), 32.610 + np.random.uniform(-0.005, 0.005)],
            'color': 'red'
        })
    
    # Rypäs 2: Syvemmällä TOT-alueella (Radensk akseli)
    for i in range(5):
        targets.append({
            'pos': [46.545 + np.random.uniform(-0.006, 0.006), 32.840 + np.random.uniform(-0.006, 0.006)],
            'obs': [46.645 + np.random.uniform(-0.005, 0.005), 32.625 + np.random.uniform(-0.005, 0.005)],
            'color': 'red'
        })

    # 2. KELTAISET HAJAHAVAINNOT (Unverified Intercepts)
    for i in range(12):
        targets.append({
            'pos': [np.random.uniform(46.52, 46.66), np.random.uniform(32.66, 32.90)],
            'obs': [np.random.uniform(46.64, 46.68), np.random.uniform(32.59, 32.64)],
            'color': 'orange'
        })
    st.session_state.static_data = targets

# --- UI ---
st.title("ISKRA | Battlefield Intelligence Snapshot")
st.markdown("Target Acquisition Layer: **Sector Kherson-South** | Deployment: Live Operational Data")

# Kartta - Kiinteä zoom ja sijainti
m = folium.Map(location=[46.60, 32.75], 
               zoom_start=11, 
               tiles='cartodbpositron',
               zoom_control=False,
               scrollWheelZoom=False,
               dragging=False)

for t in st.session_state.static_data:
    # Drone havaintopiste (pieni sininen)
    folium.CircleMarker(location=t['obs'], radius=2, color='blue', fill=True, opacity=0.4).add_to(m)
    
    # Laukaisupaikka (Backcasted)
    folium.CircleMarker(location=t['pos'], 
                        radius=9 if t['color'] == 'red' else 6, 
                        color=t['color'], 
                        fill=True, 
                        fill_opacity=0.8).add_to(m)
    
    # Backcasting-vektori
    folium.PolyLine(locations=[t['obs'], t['pos']], 
                    color=t['color'], 
                    weight=1.5, 
                    dash_array='5, 5', 
                    opacity=0.5).add_to(m)

# Piirretään kartta ilman välkkymistä
st_folium(m, width="100%", height=750, key="screenshot_map")

# Dashboard-metriikat screenshotin alareunaan
st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Confirmed Clusters", "2 Strike Zones")
c2.metric("Pending Analysis", "12 Points")
c3.metric("AI Confidence Avg.", "94.8%")
c4.metric("Data Freshness", "Real-time")
