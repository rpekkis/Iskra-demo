import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import time

st.set_page_config(page_title="ISKRA | ISR System", layout="wide")

# --- MAANTIETEEN MÄÄRITTELY ---
KHERSON_LAT, KHERSON_LON = 46.6394, 32.6139
TOT_LAT_RANGE = (46.50, 46.61) # Eteläpuoli (Miehitetty)
TOT_LON_RANGE = (32.65, 32.85)

# --- ALUSTUS ---
if 'map_data' not in st.session_state:
    st.session_state.map_data = pd.DataFrame(columns=['lat', 'lon', 'type', 'confidence', 'color'])
if 'current_fpv' not in st.session_state:
    st.session_state.current_fpv = {"id": "N/A", "status": "Scanning..."}

# --- AUTOMAATIO (Jatkuva taustaprosessi) ---
# Simuloidaan uutta havaintoa
new_lat = np.random.uniform(*TOT_LAT_RANGE)
new_lon = np.random.uniform(*TOT_LON_RANGE)
conf = np.random.randint(75, 99)

new_entry = pd.DataFrame([{
    'lat': new_lat, 'lon': new_lon, 
    'type': 'Launch Site', 
    'confidence': f"{conf}%",
    'color': [255, 0, 0, 150] # RGBA punainen
}])

st.session_state.map_data = pd.concat([st.session_state.map_data, new_entry], ignore_index=True)
st.session_state.current_fpv = {"id": f"FPV-{np.random.randint(1000, 9999)}", "conf": f"{conf}%"}

# --- KÄYTTÖLIITTYMÄ ---
st.title("⚡ ISKRA Intelligence Suite")

# Välilehdet
tab1, tab2 = st.tabs(["🌐 Strategic Map", "🎥 Live FPV Intercept"])

with tab1:
    st.subheader("Autonomous Back-Casting Overview")
    st.caption("Hover over red zones to see AI Confidence Scores. Data is disseminated to DELTA automatically.")
    
    # Pydeck-kartta (Sallii hover-tiedon näyttämisen)
    view_state = pdk.ViewState(latitude=KHERSON_LAT, longitude=KHERSON_LON + 0.05, zoom=10.5, pitch=45)
    
    layer = pdk.Layer(
        "ScatterplotLayer",
        st.session_state.map_data,
        get_position='[lon, lat]',
        get_color='color',
        get_radius=400,
        pickable=True, # Tämä mahdollistaa tiedon näkemisen
    )

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v10',
        initial_view_state=view_state,
        layers=[layer],
        tooltip={"text": "Target: {type}\nConfidence: {confidence}"}
    ))
    
    st.info(f"System Status: Active | Targets identified: {len(st.session_state.map_data)}")

with tab2:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Simulated Video Feed")
        # Käytetään Kherson-aiheista kuvaa simuloimaan videota
        st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aerial_view_of_Kherson.jpg", use_container_width=True)
        st.caption(f"Analyzing horizon landmarks for feed: {st.session_state.current_fpv['id']}")
    
    with col2:
        st.subheader("Telemetry Analysis")
        st.metric("Signal ID", st.session_state.current_fpv['id'])
        st.metric("Back-casting Confidence", st.session_state.current_fpv['conf'])
        st.write("---")
        st.write("**AI Metadata Extraction:**")
        st.code("""
{
  "status": "Target_Identified",
  "sector": "South_Bank_Kherson",
  "dissemination": "AUTO_DELTA_PUSH"
}
        """)

# Automaattinen päivitys (St.rerun pitää huolen dynaamisuudesta)
time.sleep(5)
st.rerun()
