import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import time
import os

# --- Konfiguraatio ---
st.set_page_config(page_title="ISKRA | Strategic ISR Intelligence", layout="wide", initial_sidebar_state="collapsed")

KHERSON_LAT, KHERSON_LON = 46.6394, 32.6139
WEST_BANK_LAT_RANGE = (46.62, 46.68) 
WEST_BANK_LON_RANGE = (32.58, 32.63)
TOT_LAT_RANGE = (46.50, 46.61)       
TOT_LON_RANGE = (32.65, 32.85)

# --- Session State alustus ---
if 'all_targets' not in st.session_state:
    st.session_state.all_targets = []
if 'last_update' not in st.session_state:
    # Asetetaan alkuaika
    st.session_state.last_update = time.time()
if 'first_spawn_done' not in st.session_state:
    st.session_state.first_spawn_done = False

# --- Havaintojen logiikka ---
current_time = time.time()
time_passed = current_time - st.session_state.last_update

# 1. Ensimmäinen havainto (5 sekunnin kohdalla)
if not st.session_state.first_spawn_done and time_passed > 5:
    st.session_state.all_targets.append({
        'id': "FPV-101",
        'obs_pos': [np.random.uniform(*WEST_BANK_LAT_RANGE), np.random.uniform(*WEST_BANK_LON_RANGE)],
        'launch_pos': [np.random.uniform(*TOT_LAT_RANGE), np.random.uniform(*TOT_LON_RANGE)],
        'conf': 94,
        'votes': 0,
        'status': 'Pending',
        'timestamp': time.strftime('%H:%M:%S')
    })
    st.session_state.first_spawn_done = True
    st.session_state.last_update = current_time # Nollataan ajastin seuraavaa varten

# 2. Seuraavat havainnot (17 sekunnin välein)
elif st.session_state.first_spawn_done and time_passed > 17:
    new_id_num = 101 + len(st.session_state.all_targets)
    new_id = f"FPV-{new_id_num}"
    st.session_state.all_targets.append({
        'id': new_id,
        'obs_pos': [np.random.uniform(*WEST_BANK_LAT_RANGE), np.random.uniform(*WEST_BANK_LON_RANGE)],
        'launch_pos': [np.random.uniform(*TOT_LAT_RANGE), np.random.uniform(*TOT_LON_RANGE)],
        'conf': np.random.randint(82, 98),
        'votes': 0,
        'status': 'Pending',
        'timestamp': time.strftime('%H:%M:%S')
    })
    st.session_state.last_update = current_time

# --- UI ---
st.title("ISKRA | Battlefield Intelligence Suite")
st.markdown("System Status: Active | API Outbound: DELTA Integrated")

tab1, tab2, tab3 = st.tabs(["Heatmap Aggregation", "Intercept & Backcasting", "Human Moderation Layer"])

# --- TAB 1: Heatmap ---
with tab1:
    m = folium.Map(location=[KHERSON_LAT - 0.05, KHERSON_LON + 0.1], zoom_start=11, tiles='cartodbpositron')
    for t in st.session_state.all_targets:
        color = 'green' if t['status'] == 'Confirmed' else 'gray' if t['status'] == 'False Positive' else 'red'
        folium.CircleMarker(location=t['obs_pos'], radius=4, color='blue', fill=True).add_to(m)
        folium.CircleMarker(location=t['launch_pos'], radius=8, color=color, fill=True, popup=f"{t['id']}").add_to(m)
        folium.PolyLine(locations=[t['obs_pos'], t['launch_pos']], color=color, weight=2, dash_array='5, 10').add_to(m)
    st_folium(m, width="100%", height=550, returned_objects=[], key="main_map")

# --- TAB 2: Intercept ---
with tab2:
    if not st.session_state.all_targets:
        st.info("Awaiting initial signal intercept (T+5s)...")
    else:
        col_v, col_d = st.columns([2, 1])
        drone_ids = [t['id'] for t in st.session_state.all_targets]
        selected_id = col_d.selectbox("Select Signal Stream", drone_ids, key="edge_select")
        current_drone = next(t for t in st.session_state.all_targets if t['id'] == selected_id)
        
        with col_v:
            video_file = f"video_{selected_id.split('-')[1]}.mp4"
            if os.path.exists(video_file):
                st.video(video_file)
            else:
                st.info(f"Stream {selected_id} active. Playing proxy feed.")
                st.video("https://www.sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4")
        with col_d:
            st.metric("AI Credibility", f"{current_drone['conf']}%")
            st.code(f"LAT: {current_drone['launch_pos'][0]:.4f}\nLON: {current_drone['launch_pos'][1]:.4f}")

# --- TAB 3: Moderation ---
with tab3:
    pending_targets = [t for t in st.session_state.all_targets if t['status'] == 'Pending']
    if not pending_targets:
        st.write("Queue empty. Awaiting new signal processing.")
    else:
        mod_id = st.selectbox("Assign cluster for verification:", [t['id'] for t in pending_targets], key="mod_select")
        current_mod = next(t for t in st.session_state.all_targets if t['id'] == mod_id)
        suffix = mod_id.split('-')[1]
        
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            still_file = f"still_{suffix}.png"
            if os.path.exists(still_file): st.image(still_file, caption=f"Frame Extraction {mod_id}")
            else: st.warning(f"Still image {still_file} not found.")
        with v_col2:
            sat_file = f"sat_{suffix}.png"
            if os.path.exists(sat_file): st.image(sat_file, caption=f"Satellite AO {mod_id}")
            else: st.warning(f"Satellite reference {sat_file} not found.")

        st.divider()
        c1, c2 = st.columns(2)
        if c1.button("REJECT (Swipe Left)", use_container_width=True):
            current_mod['status'] = 'False Positive'; st.rerun()
        if c2.button("VALIDATE (Swipe Right)", use_container_width=True):
            current_mod['votes'] += 1
            if current_mod['votes'] >= 3: current_mod['status'] = 'Confirmed'
            st.rerun()

time.sleep(1)
st.rerun()
