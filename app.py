import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import time

# --- Konfiguraatio ---
st.set_page_config(page_title="ISKRA | Strategic ISR Intelligence", layout="wide", initial_sidebar_state="collapsed")

# Koordinaatit
KHERSON_LAT, KHERSON_LON = 46.6394, 32.6139
WEST_BANK_LAT_RANGE = (46.62, 46.68) # Dnipron länsipuoli (Havainto)
WEST_BANK_LON_RANGE = (32.58, 32.63)
TOT_LAT_RANGE = (46.50, 46.61)       # Dnipron itäpuoli / TOT (Laukaisupaikka)
TOT_LON_RANGE = (32.65, 32.85)

# --- Session State alustus ---
if 'all_targets' not in st.session_state:
    st.session_state.all_targets = []
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()

# --- Automaattinen havaintojen generointi (17s välein) ---
current_time = time.time()
if current_time - st.session_state.last_update > 17:
    new_id = f"FPV-{len(st.session_state.all_targets) + 101}"
    
    # Arvotaan havaintopaikka (Länsi) ja laukaisupaikka (Itä)
    obs_lat, obs_lon = np.random.uniform(*WEST_BANK_LAT_RANGE), np.random.uniform(*WEST_BANK_LON_RANGE)
    launch_lat, launch_lon = np.random.uniform(*TOT_LAT_RANGE), np.random.uniform(*TOT_LON_RANGE)
    
    st.session_state.all_targets.append({
        'id': new_id,
        'obs_pos': [obs_lat, obs_lon],
        'launch_pos': [launch_lat, launch_lon],
        'conf': np.random.randint(82, 98),
        'votes': 0,
        'status': 'Pending',
        'timestamp': time.strftime('%H:%M:%S')
    })
    st.session_state.last_update = current_time

# --- Yläosa ---
st.title("ISKRA | Battlefield Intelligence Suite")
st.markdown(f"System Status: Active | API Outbound: DELTA Integrated")

tab1, tab2, tab3 = st.tabs([
    "Heatmap Aggregation", 
    "Intercept & Backcasting", 
    "Human Moderation Layer"
])

# --- VÄLILEHTI 1: Heatmap Aggregation ---
with tab1:
    st.subheader("Dissemination to Operational Picture")
    
    m = folium.Map(location=[KHERSON_LAT - 0.05, KHERSON_LON + 0.1], zoom_start=11, tiles='cartodbpositron')
    
    for t in st.session_state.all_targets:
        color = 'green' if t['status'] == 'Confirmed' else 'gray' if t['status'] == 'False Positive' else 'red'
        
        # 1. Piirretään havaintopiste (Drone ilmassa)
        folium.CircleMarker(
            location=t['obs_pos'],
            radius=4,
            color='blue',
            fill=True,
            popup=f"Intercept: {t['id']}"
        ).add_to(m)
        
        # 2. Piirretään laukaisupaikka (Backcasted target)
        folium.CircleMarker(
            location=t['launch_pos'],
            radius=8,
            color=color,
            fill=True,
            fill_opacity=0.7,
            popup=f"ID: {t['id']} | AI Credibility: {t['conf']}% | Status: {t['status']}"
        ).add_to(m)
        
        # 3. Piirretään viiva havainnosta laukaisupaikkaan (Backcasting vector)
        folium.PolyLine(
            locations=[t['obs_pos'], t['launch_pos']],
            color=color,
            weight=2,
            dash_array='5, 10',
            opacity=0.5
        ).add_to(m)
    
    st_folium(m, width="100%", height=550, returned_objects=[], key="main_map")

# --- VÄLILEHTI 2: Intercept & Backcasting ---
with tab2:
    col_v, col_d = st.columns([2, 1])
    with col_v:
        st.subheader("Raw Signal Ingest")
        st.video("https://www.sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4")
    with col_d:
        st.subheader("Geospatial Backcasting")
        if st.session_state.all_targets:
            drone_ids = [t['id'] for t in st.session_state.all_targets]
            selected_drone_id = st.selectbox("Select Signal Stream", drone_ids, key="edge_select")
            selected_drone = next(t for t in st.session_state.all_targets if t['id'] == selected_drone_id)
            
            st.metric("AI Credibility", f"{selected_drone['conf']}%")
            st.write(f"**Intercept Pos:** {selected_drone['obs_pos'][0]:.4f}, {selected_drone['obs_pos'][1]:.4f}")
            st.write(f"**Est. Launch Pos:** {selected_drone['launch_pos'][0]:.4f}, {selected_drone['launch_pos'][1]:.4f}")
        else:
            st.write("Awaiting EW Trigger...")

# --- VÄLILEHTI 3: Human Moderation Layer ---
with tab3:
    st.subheader("Validator Consensus Engine")
    pending_targets = [t for t in st.session_state.all_targets if t['status'] == 'Pending']
    
    if not pending_targets:
        st.write("Awaiting new ingest data...")
    else:
        target_options = {f"{t['id']} (Credibility: {t['conf']}%)": t['id'] for t in pending_targets}
        selected_label = st.selectbox("Assign cluster for human verification:", options=list(target_options.keys()), key="mod_select")
        selected_id = target_options[selected_label]
        current = next(t for t in st.session_state.all_targets if t['id'] == selected_id)
        
        st.write(f"Vetting {current['id']} | Consensus: {current['votes']}/3 Votes")
        
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            try: st.image("drone_still.png", caption="Frame Extraction (Still)")
            except: st.error("Missing 'drone_still.png'")
        with v_col2:
            try: st.image("sat_ref.png", caption="Satellite Reference (AO)")
            except: st.error("Missing 'sat_ref.png'")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("REJECT (Swipe Left)", use_container_width=True):
                current['status'] = 'False Positive'; st.rerun()
        with c2:
            if st.button("VALIDATE (Swipe Right)", use_container_width=True):
                current['votes'] += 1
                if current['votes'] >= 3: current['status'] = 'Confirmed'
                st.rerun()

time.sleep(1)
st.rerun()
