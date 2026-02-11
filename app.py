import streamlit as st
import pandas as pd
import numpy as np
import time

# Iskra Branding
st.set_page_config(page_title="ISKRA | ISR Dashboard", layout="wide")

# Koordinaatit (Hersonin rintama)
# Dnepr-joen itäpuoli (TOT - Miehitetty alue)
TOT_LAT_RANGE = (46.58, 46.70)
TOT_LON_RANGE = (32.70, 32.85)

# --- ISTUNNON ALUSTUS ---
if 'log' not in st.session_state:
    st.session_state.log = []
if 'map_data' not in st.session_state:
    # Käytetään yhtä saraketta värille (Hex-muoto on vakain)
    st.session_state.map_data = pd.DataFrame(columns=['lat', 'lon', 'type', 'hex_color', 'size'])

# --- SIVUPALKKI ---
st.sidebar.title("⚡ ISKRA SYSTEM")
st.sidebar.info("Sector: Kherson Frontline")
auto_mode = st.sidebar.toggle("Live Ingestion", value=True)
refresh_speed = st.sidebar.slider("Scan Speed (s)", 2, 10, 5)

if st.sidebar.button("Clear Tactical Data"):
    st.session_state.map_data = pd.DataFrame(columns=['lat', 'lon', 'type', 'hex_color', 'size'])
    st.session_state.log = []
    st.rerun()

# --- AUTOMAATIO-LOGIIKKA ---
if auto_mode:
    # 1. Laukaisupaikka ITÄPUOLELLE (Punainen)
    launch_lat = np.random.uniform(TOT_LAT_RANGE[0], TOT_LAT_RANGE[1])
    launch_lon = np.random.uniform(TOT_LON_RANGE[0], TOT_LON_RANGE[1])
    
    # 2. Drone-havainto (Valkoinen)
    drone_lat = launch_lat + np.random.uniform(-0.01, 0.01)
    drone_lon = launch_lon - np.random.uniform(0.04, 0.08) 
    
    # Lisätään data. Käytetään heksakoodeja merkkijonoina.
    new_rows = pd.DataFrame([
        {'lat': launch_lat, 'lon': launch_lon, 'type': 'Launch Spot', 'hex_color': '#FF0000', 'size': 350},
        {'lat': drone_lat, 'lon': drone_lon, 'type': 'Drone Intercept', 'hex_color': '#FFFFFF', 'size': 100}
    ])
    
    st.session_state.map_data = pd.concat([st.session_state.map_data, new_rows], ignore_index=True)
    
    # Lokikirjaus
    timestamp = time.strftime('%H:%M:%S')
    st.session_state.log.insert(0, f"[{timestamp}] Trajectory back-casted: Origin at {launch_lon:.3f}E (TOT)")

# --- KARTTA ---
st.subheader("Tactical Situation: Back-Casting Launch Origins")
st.markdown("_Red Dots = Predicted Launch Sites (East Bank) | White Dots = Drone Intercepts (Airborne)_")

# st.map lukee 'hex_color' sarakkeen suoraan, kunhan se annetaan merkkijonona
st.map(st.session_state.map_data, 
       latitude='lat', 
       longitude='lon', 
       size='size',
       color='hex_color')

# --- ANALYYSIPANEELI ---
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("System Logs")
    for entry in st.session_state.log[:3]:
        st.caption(entry)

with col2:
    st.subheader("Intelligence Metrics")
    launch_count = len(st.session_state.map_data[st.session_state.map_data['type'] == 'Launch Spot'])
    st.metric("Confirmed Launch Clusters", launch_count)
    st.caption("AI performing horizon triangulation on intercepted POV video.")

with col3:
    st.subheader("Human-in-the-loop")
    st.write("Vetted local volunteers reviewing intercepts.")
    if len(st.session_state.map_data) > 4:
        if st.button("Disseminate to DELTA"):
            st.success("Targeting insights sent to Unified Operational Picture.")
            st.balloons()
    else:
        st.info("Gathering more data for validation...")

if auto_mode:
    time.sleep(refresh_speed)
    st.rerun()
