import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

# --- Konfiguraatio ---
st.set_page_config(page_title="ISKRA | Intelligence Snapshot", layout="wide")

KHERSON_LAT, KHERSON_LON = 46.6394, 32.6139

# --- Staattisen datan luonti ---
def generate_static_data():
    targets = []
    
    # 1. PUNAISET KESKITTYMÄT (Heatmap Clusters)
    # Cluster A: Oleshky pohjoinen
    for i in range(5):
        targets.append({
            'pos': [46.625 + np.random.uniform(-0.005, 0.005), 32.720 + np.random.uniform(-0.005, 0.005)],
            'obs': [46.660 + np.random.uniform(-0.01, 0.01), 32.610 + np.random.uniform(-0.01, 0.01)],
            'color': 'red', 'label': 'Confirmed Launch Site'
        })
    
    # Cluster B: Radensk eteläpuoli
    for i in range(4):
        targets.append({
            'pos': [46.550 + np.random.uniform(-0.008, 0.008), 32.850 + np.random.uniform(-0.008, 0.008)],
            'obs': [46.640 + np.random.uniform(-0.01, 0.01), 32.630 + np.random.uniform(-0.01, 0.01)],
            'color': 'red', 'label': 'Confirmed Launch Site'
        })

    # 2. KELTAISET HAJAHAVAINNOT (Noise/Pending)
    for i in range(8):
        targets.append({
            'pos': [np.random.uniform(46.50, 46.68), np.random.uniform(32.65, 32.95)],
            'obs': [np.random.uniform(46.63, 46.69), np.random.uniform(32.58, 32.65)],
            'color': 'orange', 'label': 'Awaiting Validation'
        })
        
    return targets

# --- UI ---
st.title("ISKRA | Battlefield Intelligence Snapshot")
st.subheader("Target Acquisition Layer: Sector Kherson-South")

# Kartta
m = folium.Map(location=[KHERSON_LAT - 0.05, KHERSON_LON + 0.15], 
               zoom_start=11, 
               tiles='cartodbpositron')

data = generate_static_data()

for t in data:
    # Havaintopiste (Pieni sininen)
    folium.CircleMarker(location=t['obs'], radius=2, color='blue', fill=True, opacity=0.3).add_to(m)
    
    # Laukaisupaikka
    folium.CircleMarker(location=t['pos'], 
                        radius=8 if t['color'] == 'red' else 6, 
                        color=t['color'], 
                        fill=True, 
                        fill_opacity=0.7,
                        popup=t['label']).add_to(m)
    
    # Backcasting-vektori
    folium.PolyLine(locations=[t['obs'], t['pos']], 
                    color=t['color'], 
                    weight=1.5, 
                    dash_array='5, 5', 
                    opacity=0.4).add_to(m)

# Piirretään kartta
st_folium(m, width="100%", height=700)

# Alaosan selite screenshotia varten
c1, c2, c3 = st.columns(3)
c1.metric("Validated Battery Clusters", "2 Areas")
c2.metric("Active Ingress Vectors", "17 Intercepts")
c3.metric("System Confidence", "96.4%")

st.info("Visualized: Point of Launch backcasted from signal intercept. Red zones indicate high-probability strike zones.")
