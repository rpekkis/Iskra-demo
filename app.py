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

# --- Session State alustus ---
if 'all_targets' not in st.session_state:
    st.session_state.all_targets = []
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()

# --- Automaattinen havaintojen generointi (5s välein) ---
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
st.markdown(f"System Status: Active | Live Intercepts: {len(st.session_state.all_targets)}")

tab1, tab2, tab3 = st.tabs(["Strategic Map (UOP)", "Edge Layer: Intercept", "Interface Layer: Moderator"])

# --- Tab 1: Strateginen kartta ---
with tab1:
    st.subheader("Real-Time Heatmap Aggregation")
    
    # Luodaan karttaobjekti vain kerran ja lisätään pisteet
    m = folium.Map(location=[KHERSON_LAT - 0.05, KHERSON_LON + 0.1], 
                   zoom_start=11, 
                   tiles='cartodbpositron',
                   control_scale=True)
    
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
    
    # st_folium piirtää kartan. key-parametri auttaa Streamlitiä tunnistamaan saman komponentin
    st_folium(m, width="100%", height=500, returned_objects=[], key="main_map")

# --- Tab 2: Edge Layer (Dronen valinta) ---
with tab2:
    col_v, col_d = st.columns([2, 1])
    
    with col_v:
        st.subheader("Live Signal Ingest")
        st.video("https://www.sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4")
        
    with col_d:
        st.subheader("Backcasting Telemetry")
        if st.session_state.all_targets:
            # Mahdollisuus valita drone tarkasteltavaksi edge layerissa
            drone_ids = [t['id'] for t in st.session_state.all_targets]
            selected_drone_id = st.selectbox("Select Intercept for Analysis", drone_ids, key="edge_select")
            
            selected_drone = next(t for t in st.session_state.all_targets if t['id'] == selected_drone_id)
            
            st.metric("Signal ID", selected_drone['id'])
            st.code(f"COORD: {selected_drone['lat']:.4f}, {selected_drone['lon']:.4f}\nTIME: {selected_drone['timestamp']}\nCONF: {selected_drone['conf']}%")
        else:
            st.write("Searching for EW transients...")

# --- Tab 3: Moderator ---
with tab3:
    st.subheader("Validator Consensus Engine")
    
    pending_targets = [t for t in st.session_state.all_targets if t['status'] == 'Pending']
    
    if not pending_targets:
        st.write("No unverified clusters in queue. New data arriving automatically.")
    else:
        # Dronen valinta validointia varten
        target_options = {f"{t['id']} (AI Conf: {t['conf']}%)": t['id'] for t in pending_targets}
        selected_label = st.selectbox("Assign cluster for verification:", options=list(target_options.keys()), key="mod_select")
        selected_id = target_options[selected_label]
        
        current = next(t for t in st.session_state.all_targets if t['id'] == selected_id)
        
        st.write(f"Reviewing {current['id']}: Current Consensus {current['votes']}/3 Votes")
        
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aerial_view_of_Kherson.jpg", caption="Intercept Still")
        with v_col2:
            st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aerial_view_of_Kherson.jpg", caption="Satellite Reference")

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
                    st.success(f"{current['id']} Confirmed")
                st.rerun()

# Automaattinen päivitys
time.sleep(1)
st.rerun()
