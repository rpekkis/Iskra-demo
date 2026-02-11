import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import time

# Iskra Branding
st.set_page_config(page_title="Iskra Autonomous ISR", layout="wide")

# Hersonin koordinaatit
KHERSON_LAT = 46.6394
KHERSON_LON = 32.6139

st.title("⚡ ISKRA - Autonomous Drone Intelligence")
st.markdown("Automated back-casting from live sensor feeds. Monitoring Kherson TOT sector.")

# Alustetaan historia session_stateen
if 'history' not in st.session_state:
    st.session_state.history = []

# --- SIVUPALKKI ---
st.sidebar.header("System Controls")
run_auto = st.sidebar.toggle("Enable Autonomous Monitoring", value=True)
scan_speed = st.sidebar.slider("Scan Speed (Seconds)", 2, 10, 5)

if st.sidebar.button("🧹 Clear Intelligence Data"):
    st.session_state.history = []
    st.rerun()

# --- AUTOMAATIO-LOGIIKKA ---
if run_auto:
    # Simuloidaan uusi havainto vihollisen puolelta
    new_point = {
        'lat': KHERSON_LAT + np.random.uniform(-0.015, 0.015),
        'lon': KHERSON_LON + np.random.uniform(0.02, 0.05),
        'id': len(st.session_state.history) + 1,
        'time': time.strftime('%H:%M:%S')
    }
    st.session_state.history.append(new_point)
    # Pidetään historia kohtuullisena
    if len(st.session_state.history) > 20:
        st.session_state.history.pop(0)

# --- KARTAN LUONTI (FOLIUM) ---
# Luodaan peruskartta (OpenStreetMap toimii aina ilman avaimia)
m = folium.Map(location=[KHERSON_LAT, KHERSON_LON + 0.02], zoom_start=12, tiles="OpenStreetMap")

# Lisätään havainnot kartalle
for p in st.session_state.history:
    # Viiva kaupungista havaintopisteeseen (Back-casting viiva)
    folium.PolyLine(
        locations=[[KHERSON_LAT, KHERSON_LON], [p['lat'], p['lon']]],
        color="red",
        weight=2,
        opacity=0.5
    ).add_to(m)
    
    # Itse havaintopiste (Heatmap-piste)
    folium.CircleMarker(
        location=[p['lat'], p['lon']],
        radius=10,
        color="orange",
        fill=True,
        fill_color="red",
        popup=f"Drone ID: {p['id']} Detected at {p['time']}"
    ).add_to(m)

# Näytetään kartta
st_folium(m, width="100%", height=500)

# --- DASHBOARD ---
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Live Sensor Feed")
    st.write(f"Active Drones Tracked: {len(st.session_state.history)}")
    if st.session_state.history:
        st.info(f"Latest intercept: {st.session_state.history[-1]['time']}")

with col2:
    st.subheader("Back-Casting Engine")
    if st.session_state.history:
        st.metric("AI Confidence", f"{np.random.randint(85, 99)}%", "High")
        st.caption("Triangulating origin using horizon analysis.")

with col3:
    st.subheader("Intelligence Output")
    if len(st.session_state.history) > 5:
        st.success("Launch Cluster Identified")
        st.button("Export to DELTA System")
    else:
        st.warning("Gathering baseline data...")

# Automaattinen päivitys
if run_auto:
    time.sleep(scan_speed)
    st.rerun()
