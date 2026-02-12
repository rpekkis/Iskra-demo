import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import time

# --- Konfiguraatio ---
st.set_page_config(page_title="ISKRA | Strategic ISR Intelligence", layout="wide", initial_sidebar_state="collapsed")

# Koordinaatit (Herson / TOT-sektori)
KHERSON_LAT, KHERSON_LON = 46.6394, 32.6139
TOT_LAT_RANGE = (46.50, 46.61) 
TOT_LON_RANGE = (32.65, 32.85)

# --- Session State alustus (Aloitus nollasta) ---
if 'all_targets' not in st.session_state:
    st.session_state.all_targets = []
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()

# --- Automaattinen havaintojen generointi (Intercept & Ingest) ---
current_time = time.time()
if current_time - st.session_state.last_update > 5:
    new_id = f"FPV-{len(st.session_state.all_targets) + 101}"
    st.session_state.all_targets.append({
        'id': new_id,
        'lat': np.random.uniform(*TOT_LAT_RANGE),
        'lon': np.random.uniform(*TOT_LON_RANGE),
        'conf': np.random.randint(82, 98),
        'votes': 0,
        'status': 'Pending',
        'timestamp': time.strftime('%H:%M:%S')
    })
    st.session_state.last_update = current_time

# --- Yläosa ---
st.title("ISKRA | Battlefield Intelligence Suite")
st.markdown(f"System Status: Active | API Outbound: DELTA Integrated")

# Välilehdet prosessikaaviosi mukaisesti
tab1, tab2, tab3 = st.tabs([
    "Heatmap Aggregation", 
    "Intercept & Backcasting", 
    "Human Moderation Layer"
])

# --- VÄLILEHTI 1: Heatmap Aggregation & Dissemination ---
with tab1:
    st.subheader("Dissemination to Operational Picture")
    
    m = folium.Map(location=[KHERSON_LAT - 0.05, KHERSON_LON + 0.1], 
                   zoom_start=11, 
                   tiles='cartodbpositron')
    
    for t in st.session_state.all_targets:
        color = 'green' if t['status'] == 'Confirmed' else 'gray' if t['status'] == 'False Positive' else 'red'
        folium.CircleMarker(
            location=[t['lat'], t['lon']],
            radius=8,
            color=color,
            fill=True,
            fill_opacity=0.7,
            popup=f"ID: {t['id']} | Status: {t['status']}"
        ).add_to(m)
    
    st_folium(m, width="100%", height=550, returned_objects=[], key="main_map")
    
    # Tilastot (Operational Picture)
    c1, c2 = st.columns(2)
    c1.metric("Confirmed Targets", len([t for t in st.session_state.all_targets if t['status'] == 'Confirmed']))
    c2.metric("Pending Validation", len([t for t in st.session_state.all_targets if t['status'] == 'Pending']))

# --- VÄLILEHTI 2: Intercept & Backcasting ---
with tab2:
    col_v, col_d = st.columns([2, 1])
    
    with col_v:
        st.subheader("Raw Signal Ingest")
        st.video("https://www.sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4")
        st.caption("Video Processing & Frame Extraction Active")
        
    with col_d:
        st.subheader("Geospatial Backcasting")
        if st.session_state.all_targets:
            drone_ids = [t['id'] for t in st.session_state.all_targets]
            selected_drone_id = st.selectbox("Select Signal Stream", drone_ids, key="edge_select")
            
            selected_drone = next(t for t in st.session_state.all_targets if t['id'] == selected_drone_id)
            
            st.metric("Detection Confidence", f"{selected_drone['conf']}%")
            st.code(f"LAT: {selected_drone['lat']:.4f}\nLON: {selected_drone['lon']:.4f}\nTIME: {selected_drone['timestamp']}")
        else:
            st.write("Awaiting EW Trigger...")

# --- VÄLILEHTI 3: Human Moderation Layer ---
with tab3:
    st.subheader("Validator Consensus Engine")
    
    pending_targets = [t for t in st.session_state.all_targets if t['status'] == 'Pending']
    
    if not pending_targets:
        st.write("Consensus reached on all current intercepts. Waiting for new ingest data.")
    else:
        # Valinta moderation layerissa
        target_options = {f"{t['id']} (AI Confidence: {t['conf']}%)": t['id'] for t in pending_targets}
        selected_label = st.selectbox("Assign cluster for human verification:", options=list(target_options.keys()), key="mod_select")
        selected_id = target_options[selected_label]
        
        current = next(t for t in st.session_state.all_targets if t['id'] == selected_id)
        
        st.write(f"Vetting {current['id']} | Current Consensus: {current['votes']}/3 Votes")
        
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aerial_view_of_Kherson.jpg", caption="Frame Extraction (Still)")
        with v_col2:
            st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aerial_view_of_Kherson.jpg", caption="Satellite Reference (AO)")

        st.divider()
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("REJECT (Swipe Left)", use_container_width=True):
                current['status'] = 'False Positive'
                st.rerun()
        with c2:
            if st.button("VALIDATE (Swipe Right)", use_container_width=True):
                current['votes'] += 1
                if current['votes'] >= 3:
                    current['status'] = 'Confirmed'
                st.rerun()

# Automaattinen päivitys (pitää prosessin käynnissä)
time.sleep(1)
st.rerun()
