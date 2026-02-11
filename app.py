import streamlit as st
import pandas as pd
import numpy as np
import time

# --- KONFIGURAATIO ---
st.set_page_config(page_title="ISKRA | ISR System", layout="wide")

# Koordinaatit (Hersonin rintama)
KHERSON_LAT, KHERSON_LON = 46.6394, 32.6139
TOT_LAT_RANGE = (46.50, 46.61) # Eteläpuoli (Miehitetty)
TOT_LON_RANGE = (32.65, 32.85)

# --- ALUSTUS ---
if 'map_data' not in st.session_state:
    st.session_state.map_data = pd.DataFrame(columns=['lat', 'lon', 'confidence', 'hex_color', 'size'])
if 'fpv_status' not in st.session_state:
    st.session_state.fpv_status = "Scanning Frequencies..."

# --- AUTOMAATIO (Simuloidaan havaintoja) ---
new_lat = np.random.uniform(*TOT_LAT_RANGE)
new_lon = np.random.uniform(*TOT_LON_RANGE)
conf_val = np.random.randint(78, 99)

new_entry = pd.DataFrame([{
    'lat': new_lat, 
    'lon': new_lon, 
    'confidence': conf_val,
    'hex_color': '#FF0000', 
    'size': 400
}])

st.session_state.map_data = pd.concat([st.session_state.map_data, new_entry], ignore_index=True)
if len(st.session_state.map_data) > 20:
    st.session_state.map_data = st.session_state.map_data.iloc[1:]

# --- KÄYTTÖLIITTYMÄ ---
st.title("⚡ ISKRA | Geospatial ISR Suite")

tab1, tab2 = st.tabs(["🌐 Strategic Map", "🎥 Live FPV Back-Casting"])

with tab1:
    col_map, col_stats = st.columns([3, 1])
    
    with col_map:
        st.subheader("Autonomous Launch Site Identification")
        # Natiivi st.map on kaikkein varmin valinta tässä ympäristössä
        st.map(st.session_state.map_data, 
               latitude='lat', 
               longitude='lon', 
               size='size', 
               color='hex_color')
    
    with col_stats:
        st.subheader("Target Intelligence")
        if not st.session_state.map_data.empty:
            latest = st.session_state.map_data.iloc[-1]
            st.metric("Latest Target Confidence", f"{latest['confidence']}%")
            st.metric("Total Identified Clusters", len(st.session_state.map_data))
            st.write("---")
            st.write("**Recent Coordinates (TOT):**")
            st.dataframe(st.session_state.map_data[['lat', 'lon', 'confidence']].tail(5), hide_index=True)
        
with tab2:
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("Intercepted Video Stream (Simulated)")
        # Simuloidaan "videota" dynaamisella kohinalla ja tekstigrafiikalla
        placeholder = st.empty()
        
        # Luodaan visuaalinen "hacker/military" feed
        scan_line = "|" * np.random.randint(20, 50)
        st.code(f"""
        [SIGNAL_STRENGTH: {np.random.randint(60,95)}%]
        [DECODING_FRAME... OK]
        [LANDMARK_RECOGNITION: ACTIVE]
        [TRIANGULATING_HORIZON: {np.random.uniform(10,20):.2f}°]
        -----------------------------------------
        {scan_line}
        DETECTED: TREELINE_SECTOR_4
        MATCH_PROBABILITY: {conf_val}%
        ESTIMATED_ORIGIN: {new_lat:.4f}, {new_lon:.4f}
        -----------------------------------------
        STATUS: PUSHING_TO_DELTA_CORE...
        """)
        
        # Lisätään kuva Khersonista antamaan kontekstia "videolle"
        st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aerial_view_of_Kherson.jpg", 
                 caption="AI Perspective: Horizon landmarking from POV signal", use_container_width=True)

    with c2:
        st.subheader("Metadata Extraction")
        st.json({
            "sensor_id": f"ISR-NODE-{np.random.randint(100,999)}",
            "detected_at": time.strftime("%H:%M:%S"),
            "location_sector": "South_Bank_Kherson",
            "back_cast_result": "Success",
            "confidence_score": f"{conf_val}%"
        })
        st.success("Targeting data disseminated to DELTA automatically.")

# Automaattinen päivitys
time.sleep(5)
st.rerun()
