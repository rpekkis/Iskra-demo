import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import time

# --- KONFIGURAATIO ---
st.set_page_config(page_title="ISKRA | ISR System", layout="wide")

# Koordinaatit (Hersonin rintama)
KHERSON_LAT, KHERSON_LON = 46.6394, 32.6139
TOT_LAT_RANGE = (46.50, 46.61) 
TOT_LON_RANGE = (32.65, 32.85)

# --- ALUSTUS ---
# Nostetaan maksimimäärä satoihin
if 'all_targets' not in st.session_state:
    st.session_state.all_targets = []

# --- AUTOMAATIO (Luodaan dataa) ---
# Generoidaan 5 uutta havaintoa jokaisella latauksella, kunnes niitä on esim. 200
if len(st.session_state.all_targets) < 200:
    for _ in range(5):
        lat = np.random.uniform(*TOT_LAT_RANGE)
        lon = np.random.uniform(*TOT_LON_RANGE)
        conf = np.random.randint(75, 99)
        st.session_state.all_targets.append({
            'lat': lat, 'lon': lon, 'conf': conf
        })

# --- KÄYTTÖLIITTYMÄ ---
st.title("⚡ ISKRA | Strategic ISR Intelligence")

tab1, tab2 = st.tabs(["🌐 Tactical Map", "🎥 Live FPV Feed"])

with tab1:
    st.subheader("Launch Site Analysis (TOT Sector)")
    st.caption("Click on red markers to view AI Confidence Score.")

    # Luodaan Folium-kartta
    # 'cartodbpositron' on tyylikäs tumma/vaalea harmaa kartta, joka ei vaadi avaimia
    m = folium.Map(location=[KHERSON_LAT - 0.05, KHERSON_LON + 0.1], 
                   zoom_start=11, 
                   tiles='cartodbpositron')

    # Lisätään pisteet kartalle
    for target in st.session_state.all_targets:
        folium.CircleMarker(
            location=[target['lat'], target['lon']],
            radius=6,
            color='red',
            fill=True,
            fill_color='red',
            fill_opacity=0.6,
            # TÄMÄ ON SE KLIKATTAVA OSA:
            popup=folium.Popup(f"<b>Target Identified</b><br>Confidence: {target['conf']}%<br>Sector: South Bank", max_width=200)
        ).add_to(m)

    # Piirretään kartta
    st_folium(m, width="100%", height=600, returned_objects=[])

    st.write(f"**Intelligence Summary:** {len(st.session_state.all_targets)} targets localized in active AO.")

with tab2:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Neural Network Landmark Analysis")
        # Koska videon generointi vaatii tilauksen, käytetään animoitua koodia 
        # ja kuvaa, joka simuloi FPV-syötettä erittäin vakuuttavasti.
        st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aerial_view_of_Kherson.jpg", use_container_width=True)
        
        st.code(f"""
        [SIGNAL_ID: FPV-772-X]
        [ANALYZING FRAME... DONE]
        [GEO-DATA: MATCH FOUND IN DATABASE]
        [RESULT: SOUTH BANK SECTOR]
        -----------------------------------
        TARGETING: {st.session_state.all_targets[-1]['lat']:.4f}N, {st.session_state.all_targets[-1]['lon']:.4f}E
        -----------------------------------
        STATUS: AUTOMATIC UPLOAD TO DELTA SUCCESSFUL
        """)
        
    with col2:
        st.subheader("System Telemetry")
        st.metric("Live Signal Intercepts", f"{len(st.session_state.all_targets)}", delta="+12% / 24h")
        st.progress(0.85)
        st.write("Back-casting logic active. Triangulating launch clusters based on horizon drift.")

# Automaattinen päivitys (säädetty hitaammaksi, jotta ehtii klikkailla)
time.sleep(10)
st.rerun()
