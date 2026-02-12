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
    # Lisätään heti kaksi ensimmäistä dronea, joille sinulla on materiaalia
    for i in [101, 102]:
        st.session_state.all_targets.append({
            'id': f"FPV-{i}",
            'obs_pos': [np.random.uniform(*WEST_BANK_LAT_RANGE), np.random.uniform(*WEST_BANK_LON_RANGE)],
            'launch_pos': [np.random.uniform(*TOT_LAT_RANGE), np.random.uniform(*TOT_LON_RANGE)],
            'conf': np.random.randint(88, 98),
            'votes': 0,
            'status': 'Pending',
            'timestamp': time.strftime('%H:%M:%S')
        })

if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()

# --- Automaattinen havaintojen generointi (17s välein) ---
current_time = time.time()
if current_time - st.session_state.last_update > 17:
    new_id = f"FPV-{len(st.session_state.all_targets) + 101}"
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
st.markdown(f"System Status: Active | API Outbound: DELTA Integrated")

tab1, tab2, tab3 = st.tabs(["Heatmap Aggregation", "Intercept & Backcasting", "Human Moderation Layer"])

# --- TAB 1: Kartta ---
with tab1:
    m = folium.Map(location=[KHERSON_LAT - 0.05, KHERSON_LON + 0.1], zoom_start=11, tiles='cartodbpositron')
    for t in st.session_state.all_targets:
        color = 'green' if t['status'] == 'Confirmed' else 'gray' if t['status'] == 'False Positive' else 'red'
        folium.CircleMarker(location=t['obs_pos'], radius=4, color='blue', fill=True).add_to(m)
        folium.CircleMarker(location=t['launch_pos'], radius=8, color=color, fill=True, 
                            popup=f"{t['id']} | AI Conf: {t['conf']}%").add_to(m)
        folium.PolyLine(locations=[t['obs_pos'], t['launch_pos']], color=color, weight=2, dash_array='5, 10').add_to(m)
    st_folium(m, width="100%", height=550, returned_objects=[], key="main_map")

# --- TAB 2: Intercept (Dynaaminen Video) ---
with tab2:
    col_v, col_d = st.columns([2, 1])
    drone_ids = [t['id'] for t in st.session_state.all_targets]
    selected_id = col_d.selectbox("Select Signal Stream", drone_ids, key="edge_select")
    current_drone = next(t for t in st.session_state.all_targets if t['id'] == selected_id)
    
    with col_v:
        # Haetaan video ID:n perusteella (esim. video_101.mp4)
        video_file = f"video_{selected_id.split('-')[1]}.mp4"
        if os.path.exists(video_file):
            st.video(video_file)
        else:
            st.info(f"Raaka-signaali {selected_id} toistetaan oletusstriiminä.")
            st.video("https://www.sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4")

    with col_d:
        st.metric("AI Credibility", f"{current_drone['conf']}%")
        st.code(f"LAT: {current_drone['launch_pos'][0]:.4f}\nLON: {current_drone['launch_pos'][1]:.4f}")

# --- TAB 3: Moderation (Dynaamiset Kuvat) ---
with tab3:
    pending_targets = [t for t in st.session_state.all_targets if t['status'] == 'Pending']
    if not pending_targets:
        st.write("Awaiting new data...")
    else:
        mod_id = st.selectbox("Assign cluster for verification:", [t['id'] for t in pending_targets], key="mod_select")
        current_mod = next(t for t in st.session_state.all_targets if t['id'] == mod_id)
        suffix = mod_id.split('-')[1]
        
        v_col1, v_col2 = st.columns(2)
        # Still-kuva
        with v_col1:
            still_file = f"still_{suffix}.png"
            if os.path.exists(still_file):
                st.image(still_file, caption=f"Frame Extraction {mod_id}")
            else:
                st.warning(f"Still-kuva {still_file} puuttuu.")
        # Satelliittikuva
        with v_col2:
            sat_file = f"sat_{suffix}.png"
            if os.path.exists(sat_file):
                st.image(sat_file, caption=f"Satellite AO {mod_id}")
            else:
                st.warning(f"Satelliittikuva {sat_file} puuttuu.")

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
