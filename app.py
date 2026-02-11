import streamlit as st
import pandas as pd
import numpy as np
import time

# Iskra-konseptin mukainen ulkoasu
st.set_page_config(page_title="ISKRA | ISR Dashboard", layout="wide", initial_sidebar_state="expanded")

# Hersonin koordinaatit (Kherson TOT - Temporarily Occupied Territories)
KHERSON_LAT = 46.6394
KHERSON_LON = 32.6139

# --- ISTUNNON ALUSTUS ---
if 'log' not in st.session_state:
    st.session_state.log = []
if 'map_data' not in st.session_state:
    st.session_state.map_data = pd.DataFrame(columns=['lat', 'lon', 'weight'])

# --- SIVUPALKKI ---
st.sidebar.title("⚡ ISKRA SYSTEM")
st.sidebar.status("Connected to EW Sensors")
auto_mode = st.sidebar.toggle("Live Intelligence Ingestion", value=True)
refresh_speed = st.sidebar.slider("Scan Frequency (s)", 2, 10, 4)

if st.sidebar.button("Clear Tactical Data"):
    st.session_state.map_data = pd.DataFrame(columns=['lat', 'lon', 'weight'])
    st.session_state.log = []
    st.rerun()

# --- PÄÄNÄKYMÄ ---
st.title("Iskra: Geospatial Intelligence & Back-Casting")
st.markdown(f"**Sector:** Kherson Region | **Status:** Monitoring TOT (Temporarily Occupied Territories)")

# --- AUTOMAATIO-LOGIIKKA (Simuloidaan sensorisyötettä) ---
if auto_mode:
    # Luodaan uusi oletettu laukaisupiste (Back-casted point)
    new_lat = KHERSON_LAT + np.random.uniform(-0.012, 0.012)
    new_lon = KHERSON_LON + np.random.uniform(0.02, 0.045)
    
    new_row = pd.DataFrame({'lat': [new_lat], 'lon': [new_lon], 'weight': [1]})
    st.session_state.map_data = pd.concat([st.session_state.map_data, new_row], ignore_index=True)
    
    # Lisätään lokiin tapahtuma
    timestamp = time.strftime('%H:%M:%S')
    st.session_state.log.insert(0, f"[{timestamp}] Intercepted FPV feed: Back-casting successful. Confidence {np.random.randint(88,99)}%")

# --- KARTTA-OSIO ---
# Käytetään Streamlitin omaa natiivia karttaa (luotettavin)
st.subheader("Live Heatmap of Potential Launch Spots")
st.map(st.session_state.map_data, latitude='lat', longitude='lon', size=150, color='#FF4B4B')

# --- DASHBOARDIN ALAKERRAN KOLUMNI-JAOTELMA ---
st.divider()
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.subheader("Live Event Log")
    for entry in st.session_state.log[:5]:
        st.caption(entry)

with col2:
    st.subheader("ISR Analytics")
    if not st.session_state.map_data.empty:
        st.metric("Detected Launch Points", len(st.session_state.map_data))
        st.metric("Avg. System Confidence", f"{np.random.randint(92, 97)}%", "+1.2%")
    else:
        st.write("Awaiting data...")

with col3:
    st.subheader("Human-in-the-Loop")
    st.write("Vetted local volunteers reviewing intercepts.")
    if len(st.session_state.map_data) > 3:
        if st.button("Disseminate to DELTA"):
            st.balloons()
            st.success("Targeting insights sent to Unified Operational Picture")
    else:
        st.info("Insufficient data for target validation.")

# Automaattinen päivitys
if auto_mode:
    time.sleep(refresh_speed)
    st.rerun()
