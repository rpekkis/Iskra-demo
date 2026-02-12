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
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'last_spawn_time' not in st.session_state:
    st.session_state.last_spawn_time = time.time()
if 'ai_threshold' not in st.session_state:
    st.session_state.ai_threshold = 80 

# --- Tarkka Ajoituslogiikka ---
current_time = time.time()
total_elapsed = current_time - st.session_state.start_time
time_since_last = current_time - st.session_state.last_spawn_time

# Logiikka dronien ilmestymiselle
target_count = len(st.session_state.all_targets)

# 1. Ensimmäinen drone (FPV-101) 5 sekunnin kohdalla
if target_count == 0 and total_elapsed > 5:
    st.session_state.all_targets.append({
        'id': "FPV-101",
        'obs_pos': [46.645, 32.610], # Dnipro West
        'launch_pos': [46.560, 32.720], # TOT Side
        'conf': 75,
        'votes': 0,
        'status': 'Pending',
        'timestamp': time.strftime('%H:%M:%S')
    })
    st.session_state.last_spawn_time = current_time

# 2. Seuraavat dronet (FPV-102 ja muut) 17 sekunnin välein edellisestä
elif target_count > 0 and time_since_last > 17:
    new_id_num = 101 + target_count
    # Erityisasetus FPV-102:lle
    conf_value = 92 if new_id_num == 102 else np.random.randint(60, 99)
    
    st.session_state.all_targets.append({
        'id': f"FPV-{new_id_num}",
        'obs_pos': [np.random.uniform(*WEST_BANK_LAT_RANGE), np.random.uniform(*WEST_BANK_LON_RANGE)],
        'launch_pos': [np.random.uniform(*TOT_LAT_RANGE), np.random.uniform(*TOT_LON_RANGE)],
        'conf': conf_value,
        'votes': 0,
        'status': 'Pending',
        'timestamp': time.strftime('%H:%M:%S')
    })
    st.session_state.last_spawn_time = current_time

# --- UI ---
st.title("ISKRA | Battlefield Intelligence Suite")
st.markdown("System Status: Active | API Outbound: DELTA Integrated")

tab1, tab2, tab3 = st.tabs(["Heatmap Aggregation", "Intercept & Backcasting", "Human Moderation Layer"])

# --- TAB 1: Kartta ---
with tab1:
    m = folium.Map(location=[KHERSON_LAT - 0.05, KHERSON_LON + 0.1], zoom_start=11, tiles='cartodbpositron')
    
    for t in st.session_state.all_targets:
        # Värilogiikka: Vahvistettu/AI yli kynnyksen -> PUNAINEN, Muuten -> KELTAINEN (orange)
        if t['status'] == 'Confirmed' or t['conf'] >= st.session_state.ai_threshold:
            color = 'red'
        else:
            color = 'orange'
            
        folium.CircleMarker(location=t['obs_pos'], radius=4, color='blue', fill=True).add_to(m)
        folium.CircleMarker(location=t['launch_pos'], radius=8, color=color, fill=True, 
                            popup=f"{t['id']} (AI: {t['conf']}%)").add_to(m)
        folium.PolyLine(locations=[t['obs_pos'], t['launch_pos']], color=color, weight=2, dash_array='5, 10').add_to(m)
    
    st_folium(m, width="100%", height=550, returned_objects=[], key="main_map")

# --- TAB 2: Intercept ---
with tab2:
    if not st.session_state.all_targets:
        st.info("Searching for signal transients (T+5s)...")
    else:
        col_v, col_d = st.columns([2, 1])
        with col_d:
            st.subheader("Control Logic")
            st.session_state.ai_threshold = st.slider("AI Confidence Threshold (%)", 0, 100, st.session_state.ai_threshold)
            st.divider()
            drone_ids = [t['id'] for t in st.session_state.all_targets]
            selected_id = st.selectbox("Select Signal Stream", drone_ids, key="edge_select")
            current_drone = next(t for t in st.session_state.all_targets if t['id'] == selected_id)
            st.metric("AI Credibility", f"{current_drone['conf']}%")
            status_text = "CONFIRMED" if (current_drone['conf'] >= st.session_state.ai_threshold or current_drone['status'] == 'Confirmed') else "AWAITING HUMAN"
            st.write(f"**Status:** {status_text}")
        with col_v:
            suffix = selected_id.split('-')[1]
            video_file = f"video_{suffix}.mp4"
            if os.path.exists(video_file): st.video(video_file)
            else: st.video("https://www.sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4")

# --- TAB 3: Moderation ---
with tab3:
    pending_targets = [t for t in st.session_state.all_targets if t['status'] == 'Pending']
    if not pending_targets:
        st.write("No signals requiring human vetting.")
    else:
        mod_id = st.selectbox("Assign cluster for human verification:", [t['id'] for t in pending_targets], key="mod_select")
        current_mod = next(t for t in st.session_state.all_targets if t['id'] == mod_id)
        suffix = mod_id.split('-')[1]
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            still_file = f"still_{suffix}.png"
            if os.path.exists(still_file): st.image(still_file, caption=f"Still {mod_id}")
        with v_col2:
            sat_file = f"sat_{suffix}.png"
            if os.path.exists(sat_file): st.image(sat_file, caption=f"Sat Ref {mod_id}")
        c1, c2 = st.columns(2)
        if c1.button("REJECT (Delete)", use_container_width=True):
            st.session_state.all_targets = [t for t in st.session_state.all_targets if t['id'] != mod_id]
            st.rerun()
        if c2.button("VALIDATE (Confirm)", use_container_width=True):
            current_mod['status'] = 'Confirmed'
            st.rerun()

time.sleep(1)
st.rerun()
