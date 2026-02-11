import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import time

# --- KONFIGURAATIO ---
st.set_page_config(page_title="ISKRA | Strategic ISR Intelligence", layout="wide", initial_sidebar_state="collapsed")

# Koordinaatit (Herson / TOT-sektori)
KHERSON_LAT, KHERSON_LON = 46.6394, 32.6139
TOT_LAT_RANGE = (46.50, 46.61) 
TOT_LON_RANGE = (32.65, 32.85)

# --- SESSION STATE ALUSTUS (Aloitus nollasta) ---
if 'all_targets' not in st.session_state:
    st.session_state.all_targets = []
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()

# --- AUTOMAATTINEN HAVAINTOJEN GENERONTI (5s välein) ---
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

# --- KÄYTTÖLIITTYMÄN YLÄOSA ---
st.title("⚡ ISKRA | Battlefield Intelligence Suite")
st.markdown(f"**System Status:** Active | **Live Intercepts:** {len(st.session_state.all_targets)}")

tab1, tab2, tab3 = st.tabs(["🌐 Strategic Map (UOP)", "🎥 Edge Layer: Intercept", "👥 Interface Layer: Moderator"])

# --- TAB 1: STRATEGINEN KARTTA ---
with tab1:
    st.subheader("Real-Time Heatmap Aggregation")
    
    if not st.session_state.all_targets:
        st.info("Waiting for signal intercept... (New data every 5 seconds)")
        # Luodaan tyhjä kartta
        m = folium.Map(location=[KHERSON_LAT - 0.05, KHERSON_LON + 0.1], zoom_start=11, tiles='cartodbpositron')
    else:
        m = folium.Map(location=[KHERSON_LAT - 0.05, KHERSON_LON + 0.1], zoom_start=11, tiles='cartodbpositron')
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
    
    st_folium(m, width="100%", height=500, returned_objects=[])

# --- TAB 2: EDGE LAYER (Video) ---
with tab2:
    col_v, col_d = st.columns([2, 1])
    with col_v:
        st.subheader("Live Signal Ingest")
        st.video("https://www.sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4")
    with col_d:
        st.subheader("Backcasting Telemetry")
        if st.session_state.all_targets:
            latest = st.session_state.all_targets[-1]
            st.metric("Latest Intercept", latest['id'])
            st.code(f"COORD: {latest['lat']:.4f}, {latest['lon']:.4f}\nTIME: {latest['timestamp']}\nSTATUS: QUEUED_FOR_VETTING")
        else:
            st.write("Searching for EW transients...")

# --- TAB 3: MODERATOR (Vapaaehtoisnäkymä + Valinta) ---
with tab3:
    st.subheader("Validator Consensus Engine")
    
    pending_targets = [t for t in st.session_state.all_targets if t['status'] == 'Pending']
    
    if not pending_targets:
        st.write("No unverified clusters in queue. Please wait for the next 5s intercept.")
    else:
        # MAHDOLLISUUS VALITA TIETTY DRONE / CLUSTER
        target_options = {f"{t['id']} (Conf: {t['conf']}%)": t['id'] for t in pending_targets}
        selected_label = st.selectbox("Pick a drone cluster to verify:", options=list(target_options.keys()))
        selected_id = target_options[selected_label]
        
        current = next(t for t in st.session_state.all_targets if t['id'] == selected_id)
        
        st.warning(f"Reviewing {current['id']}: Current Consensus {current['votes']}/3 Votes")
        
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aerial_view_of_Kherson.jpg", caption="Edge Layer Capture")
        with v_col2:
            st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aerial_view_of_Kherson.jpg", caption="Satellite Reference")

        # Card-Swipe Logiikka
        c1, c2 = st.columns(2)
        with c1:
            if st.button("❌ REJECT (Swipe Left)", use_container_width=True):
                current['status'] = 'False Positive'
                st.rerun()
        with c2:
            if st.button("✅ VALIDATE (Swipe Right)", use_container_width=True):
                current['votes'] += 1
                if current['votes'] >= 3:
                    current['status'] = 'Confirmed'
                    st.success("Target Confirmed! Pushed to DELTA.")
                    st.balloons()
                st.rerun()

    # Arkkitehtuurin mukainen Feedback Loop
    st.divider()
    st.subheader("🔄 Feedback Loop")
    f1, f2 = st.columns(2)
    f1.metric("Model Precision", "94.1%", "+0.2%")
    f2.metric("Verification Latency", "2.8s", "-0.4s")

# Automaattinen päivitys (pitää kellon ja datan liikkeessä)
time.sleep(1)
st.rerun()
