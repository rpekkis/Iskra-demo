import streamlit as st
import pandas as pd
import numpy as np
import time

# Iskra Branding
st.set_page_config(page_title="ISKRA | ISR Dashboard", layout="wide")

# Tarkennetut koordinaatit: Dnepr-joen ETELÄPUOLI (Miehitetty alue / TOT)
# Khersonin kaupunki on n. 46.64, 32.61. Joki kulkee tässä välissä.
TOT_LAT_RANGE = (46.50, 46.61) # Selkeästi etelämpänä
TOT_LON_RANGE = (32.65, 32.85) # Itään/Kaakkoon kaupungista

# --- ISTUNNON ALUSTUS ---
if 'log' not in st.session_state:
    st.session_state.log = []
if 'map_data' not in st.session_state:
    st.session_state.map_data = pd.DataFrame(columns=['lat', 'lon', 'type', 'hex_color', 'size'])

# --- SIVUPALKKI ---
st.sidebar.title("⚡ ISKRA SYSTEM")
st.sidebar.info("Sector: Kherson Frontline (South Bank Monitoring)")
auto_mode = st.sidebar.toggle("Live Ingestion", value=True)
refresh_speed = st.sidebar.slider("Scan Speed (s)", 2, 10, 5)

if st.sidebar.button("Clear Tactical Data"):
    st.session_state.map_data = pd.DataFrame(columns=['lat', 'lon', 'type', 'hex_color', 'size'])
    st.session_state.log = []
    st.rerun()

# --- AUTOMAATIO-LOGIIKKA ---
if auto_mode:
    # 1. Laukaisupaikka ETELÄPUOLELLE (Punainen)
    launch_lat = np.random.uniform(TOT_LAT_RANGE[0], TOT_LAT_RANGE[1])
    launch_lon = np.random.uniform(TOT_LON_RANGE[0], TOT_LON_RANGE[1])
    
    # 2. Drone-havainto (Valkoinen) - sijoitetaan joen päälle tai lähelle kaupunkia
    # Drone lentää etelästä pohjoiseen/luoteeseen
    drone_lat = launch_lat + np.random.uniform(0.02, 0.04) 
    drone_lon = launch_lon - np.random.uniform(0.02, 0.05)
    
    new_rows = pd.DataFrame([
        {'lat': launch_lat, 'lon': launch_lon, 'type': 'Launch Spot', 'hex_color': '#FF0000', 'size': 400},
        {'lat': drone_lat, 'lon': drone_lon, 'type': 'Drone Intercept', 'hex_color': '#FFFFFF', 'size': 120}
    ])
    
    st.session_state.map_data = pd.concat([st.session_state.map_data, new_rows], ignore_index=True)
    
    # Lokikirjaus
    timestamp = time.strftime('%H:%M:%S')
    st.session_state.log.insert(0, f"[{timestamp}] Trajectory back-casted to South Bank (Occupied)")

# --- KARTTA ---
st.subheader("Tactical Situation: Back-Casting Launch Origins")
st.markdown("_Red Dots = Launch Sites (South Bank/Occupied) | White Dots = Drone Intercepts (Airborne)_")

# Piirretään kartta. Jos havaintoja ei näy, tarkista zoom-taso (Streamlit optimoi sen automaattisesti)
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
    st.metric("Confirmed Clusters", launch_count)
    st.caption("Monitoring launch signatures across the Dnipro river.")

with col3:
    st.subheader("Human-in-the-Loop")
    if len(st.session_state.map_data) > 4:
        if st.button("Disseminate to DELTA"):
            st.success("Targeting insights sent.")
            st.balloons()
    else:
        st.write("Gathering data...")

if auto_mode:
    time.sleep(refresh_speed)
    st.rerun()
