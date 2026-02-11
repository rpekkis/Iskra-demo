import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import time

# Iskra Branding
st.set_page_config(page_title="Iskra Autonomous ISR", layout="wide")

# Hersonin koordinaatit
KHERSON_LAT = 46.6394
KHERSON_LON = 32.6139

st.title("⚡ ISKRA - Autonomous Drone Intelligence")
st.markdown("Automated back-casting from live sensor feeds. Monitoring Kherson TOT sector.")

# Alustetaan historia, jos sitä ei ole
if 'history_list' not in st.session_state:
    st.session_state.history_list = []

# --- SIVUPALKKI ---
st.sidebar.header("System Controls")
run_automation = st.sidebar.toggle("Enable Autonomous Monitoring", value=True)
speed = st.sidebar.slider("Scan Speed (Seconds)", 2, 10, 5)

if st.sidebar.button("🧹 Clear Intelligence Data"):
    st.session_state.history_list = []
    st.rerun()

# --- AUTOMAATIO-LOGIIKKA ---
# Luodaan uusi havainto automaattisesti jos toggle on päällä
if run_automation:
    # Simuloidaan havaintoa
    new_lat = KHERSON_LAT + np.random.uniform(-0.015, 0.015)
    new_lon = KHERSON_LON + np.random.uniform(0.02, 0.05)
    
    # Lisätään historiaan
    st.session_state.history_list.append({
        'lat': new_lat,
        'lon': new_lon,
        'confidence': np.random.uniform(0.7, 0.98)
    })
    
    # Pidetään historia hallittavana (viimeiset 50 havaintoa)
    if len(st.session_state.history_list) > 50:
        st.session_state.history_list.pop(0)

# --- VISUALISOINTI ---
# Käytetään varmempaa karttapohjaa (Light/Dark ilman avainvaatimusta)
view_state = pdk.ViewState(
    latitude=KHERSON_LAT,
    longitude=KHERSON_LON + 0.02,
    zoom=11,
    pitch=40
)

layers = []

# 1. Historiallinen Heatmap (Kumulatiivinen data)
if st.session_state.history_list:
    h_df = pd.DataFrame(st.session_state.history_list)
    layers.append(pdk.Layer(
        "HeatmapLayer",
        h_df,
        get_position=["lon", "lat"],
        get_weight="confidence",
        radius_pixels=80,
        opacity=0.8,
    ))

# 2. Viimeisin havainto - Animaatio-kaari
if st.session_state.history_list:
    latest = st.session_state.history_list[-1]
    arc_data = [{'start': [latest['lon'], latest['lat']], 'end': [KHERSON_LON, KHERSON_LAT]}]
    layers.append(pdk.Layer(
        "ArcLayer",
        data=arc_data,
        get_source_position="start",
        get_target_position="end",
        get_source_color=[255, 0, 0, 200],
        get_target_color=[0, 255, 255, 200],
        get_width=6,
    ))

# KARTTA - Käytetään standardia Dark-tyyliä joka on vakaampi
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/dark-v10", 
    initial_view_state=view_state,
    layers=layers,
))

# --- DASHBOARD ---
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Live Sensor Feed")
    st.write(f"Active Drones Detected: {len(st.session_state.history_list)}")
    if st.session_state.history_list:
        st.metric("Latest Signal Strength", f"{np.random.randint(60, 99)}%", "Stable")
    st.info("Continuous video interception active...")

with col2:
    st.subheader("Back-Casting Engine")
    if st.session_state.history_list:
        conf = st.session_state.history_list[-1]['confidence'] * 100
        st.metric("AI Confidence Score", f"{conf:.1f}%")
        st.progress(conf/100)
    st.caption("Triangulating origin points using geospatial horizon landmarks.")

with col3:
    st.subheader("Intelligence Output")
    if len(st.session_state.history_list) > 5:
        st.success("Targeting Clusters Identified")
        st.write("Data ready for DELTA system integration.")
    else:
        st.warning("Collecting baseline data...")

# Automaattinen päivitys
if run_automation:
    time.sleep(speed)
    st.rerun()
