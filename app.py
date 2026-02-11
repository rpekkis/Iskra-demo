import streamlit as st
import pandas as pd
import numpy as np
import time

# Iskra Branding
st.set_page_config(page_title="ISKRA | ISR Dashboard", layout="wide")

# Koordinaattipisteet (Hersonin rintama)
KHERSON_CITY = [46.6394, 32.6139] # Länsiranta (Ukrainan hallussa)
# Dnepr-joen itäpuoli (TOT - Miehitetty alue) alkaa n. pituudesta 32.65 ->
TOT_LAT_RANGE = (46.55, 46.70)
TOT_LON_RANGE = (32.68, 32.85)

# --- ISTUNNON ALUSTUS ---
if 'log' not in st.session_state:
    st.session_state.log = []
if 'map_data' not in st.session_state:
    # Erotetaan Drone (ilmassa) ja Launch Spot (maassa)
    st.session_state.map_data = pd.DataFrame(columns=['lat', 'lon', 'type', 'color', 'size'])

# --- SIVUPALKKI ---
st.sidebar.title("⚡ ISKRA SYSTEM")
st.sidebar.info("Sector: Kherson Frontline")
auto_mode = st.sidebar.toggle("Live Ingestion", value=True)
refresh_speed = st.sidebar.slider("Scan Speed (s)", 2, 10, 5)

if st.sidebar.button("Clear Tactical Data"):
    st.session_state.map_data = pd.DataFrame(columns=['lat', 'lon', 'type', 'color', 'size'])
    st.session_state.log = []
    st.rerun()

# --- AUTOMAATIO-LOGIIKKA (Realistinen sijoittelu) ---
if auto_mode:
    # 1. Luodaan laukaisupaikka joen ITÄPUOLELLE (Punainen ympyrä)
    launch_lat = np.random.uniform(*TOT_LAT_RANGE)
    launch_lon = np.random.uniform(*TOT_LON_RANGE)
    
    # 2. Luodaan drone-havainto hieman lähemmäs kaupunkia (Valkoinen piste)
    drone_lat = launch_lat + np.random.uniform(-0.01, 0.01)
    drone_lon = launch_lon - np.random.uniform(0.01, 0.03) # Drone liikkuu länteen kohti Hersonia
    
    # Lisätään molemmat kartalle
    new_rows = pd.DataFrame([
        {'lat': launch_lat, 'lon': launch_lon, 'type': 'Launch Spot', 'color': '#FF0000', 'size': 300}, # Punainen = Kohde
        {'lat': drone_lat, 'lon': drone_lon, 'type': 'Drone Intercept', 'color': '#FFFFFF', 'size': 80}   # Valkoinen = Havainto
    ])
    
    st.session_state.map_data = pd.concat([st.session_state.map_data, new_rows], ignore_index=True)
    
    # Lokikirjaus
    timestamp = time.strftime('%H:%M:%S')
    st.session_state.log.insert(0, f"[{timestamp}] New trajectory back-casted to East Bank (TOT).")

# --- KARTTA-OSIO ---
st.subheader("Tactical Situation: Back-Casting Launch Origins")
st.markdown("_Red = Predicted Launch Site (East Bank) | White = Intercepted Drone (Airborne)_")

# Käytetään Streamlitin omaa karttaa väreillä ja kooilla
st.map(st.session_state.map_data, 
       latitude='lat', 
       longitude='lon', 
       size='size', 
       color='color')

# --- ANALYYSIPANEELI ---
st.divider()
c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("System Logs")
    for entry in st.session_state.log[:3]:
        st.caption(entry)

with c2:
    st.subheader("Intelligence Metrics")
    launch_count = len(st.session_state.map_data[st.session_state.map_data['type'] == 'Launch Spot'])
    st.metric("Confirmed Launch Clusters", launch_count)
    st.write(f"Monitoring occupied sector: {TOT_LON_RANGE[0]}E - {TOT_LON_RANGE[1]}E")

with col3 := c3:
    st.subheader("Human Safari Prevention")
    st.write("Target data validation for counter-battery fire.")
    if st.button("Disseminate to DELTA"):
        st.success("Coordinates sent to Artillery Units")

if auto_mode:
    time.sleep(refresh_speed)
    st.rerun()
