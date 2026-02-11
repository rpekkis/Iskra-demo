import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="ISKRA | Strategic ISR Intelligence", layout="wide", initial_sidebar_state="collapsed")

# Coordinates (Kherson South Bank / TOT)
KHERSON_LAT, KHERSON_LON = 46.6394, 32.6139
TOT_LAT_RANGE = (46.50, 46.61) 
TOT_LON_RANGE = (32.65, 32.85)

# --- INITIALIZE SESSION STATE ---
if 'all_targets' not in st.session_state:
    st.session_state.all_targets = []
    # Generoidaan alkupisteitä, joilla on eri määrä konsensus-ääniä
    for i in range(20):
        st.session_state.all_targets.append({
            'id': f"TRGT-{100+i}",
            'lat': np.random.uniform(*TOT_LAT_RANGE),
            'lon': np.random.uniform(*TOT_LON_RANGE),
            'conf': np.random.randint(80, 95),
            'votes': np.random.randint(0, 3), # Consensus Engine: vaatii 3 ääntä
            'status': 'Pending'
        })

# --- UI HEADER ---
st.title("⚡ ISKRA | Battlefield Intelligence Suite")
st.markdown("_Collect > Interpret > Validate > Fuse > Publish_")

tab1, tab2, tab3 = st.tabs(["🌐 Strategic Map (UOP)", "🎥 Edge Layer: Intercept", "👥 Interface Layer: Moderator"])

# --- TAB 1: STRATEGIC MAP (Unified Operational Picture) ---
with tab1:
    st.subheader("Heatmap Aggregation & Dissemination")
    st.caption("Green = Verified by Consensus | Red = AI Predicted | Gray = Denied by Loop")
    
    m = folium.Map(location=[KHERSON_LAT - 0.05, KHERSON_LON + 0.1], zoom_start=11, tiles='cartodbpositron')
    
    for t in st.session_state.all_targets:
        # Arkkitehtuurin mukainen väri-logiikka
        if t['status'] == 'Confirmed':
            color = 'green'
        elif t['status'] == 'False Positive':
            color = 'gray'
        else:
            color = 'red'
            
        folium.CircleMarker(
            location=[t['lat'], t['lon']],
            radius=7,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
            popup=f"ID: {t['id']} | Consensus: {t['votes']}/3 | AI Conf: {t['conf']}%"
        ).add_to(m)
    
    st_folium(m, width="100%", height=500, returned_objects=[])
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    col_stat1.metric("Active Clusters", len([t for t in st.session_state.all_targets if t['status'] == 'Pending']))
    col_stat2.metric("Validated (DELTA)", len([t for t in st.session_state.all_targets if t['status'] == 'Confirmed']))
    col_stat3.info("Data is STANAG-aligned and encrypted for Uplink.")

# --- TAB 2: EDGE LAYER (Video Processing) ---
with tab2:
    col_vid, col_meta = st.columns([2, 1])
    with col_vid:
        st.subheader("Stream Capture & Sensitivity Masking")
        st.video("https://www.sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4") 
    with col_meta:
        st.subheader("Geospatial LLM Backcasting")
        st.code(f"PROCESSING_NODE: EDGE-04\nHASH: {np.random.get_state()[1][0]}\nSTATUS: STREAMING_TO_HEATMAP")
        st.progress(0.92, text="Triangulating Treelines...")

# --- TAB 3: INTERFACE LAYER (Moderator App) ---
with tab3:
    st.subheader("Validator Consensus Engine")
    st.write("Community-led local validation via Card-Swipe UI.")
    
    # Suodatetaan vain ne, jotka vaativat vielä ääniä
    queue = [t for t in st.session_state.all_targets if t['status'] == 'Pending']
    
    if queue:
        # Card-swipe UI: käsitellään jonoa yksi kerrallaan
        current = queue[0]
        
        # Simuloidaan arkkitehtuurin "Consensus Engineä"
        st.warning(f"ACTION REQUIRED: Target {current['id']} has {current['votes']}/3 confirmations.")
        
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aerial_view_of_Kherson.jpg", caption="Edge Layer Capture")
        with v_col2:
            st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aerial_view_of_Kherson.jpg", caption="Satellite AO Reference")

        st.divider()
        
        # "Card-Swipe" painikkeet
        swipe_left, swipe_right = st.columns(2)
        with swipe_left:
            if st.button("❌ REJECT (Swipe Left)", use_container_width=True):
                current['status'] = 'False Positive'
                st.toast(f"Feedback Loop updated: {current['id']} denied.")
                time.sleep(1)
                st.rerun()
        with swipe_right:
            if st.button("✅ VALIDATE (Swipe Right)", use_container_width=True):
                current['votes'] += 1
                if current['votes'] >= 3:
                    current['status'] = 'Confirmed'
                    st.success("Consensus reached. Disseminated to DELTA Integration API.")
                    st.balloons()
                else:
                    st.info(f"Vote recorded. {3 - current['votes']} more required.")
                time.sleep(1)
                st.rerun()
    else:
        st.success("Queue empty. Neural network and human layers are in sync.")

    # Feedback Loop -mittarit (Arkkitehtuurin alareuna)
    st.divider()
    st.subheader("🔄 Feedback Loop (Units + Model)")
    f1, f2, f3 = st.columns(3)
    f1.metric("Validator Accuracy", "96.8%", "+0.2%")
    f2.metric("False Positive Rate", "4.1%", "-1.2%")
    f3.metric("System Latency", "1.4s", "-0.1s")

# Taustapäivitys
if np.random.random() > 0.9:
    st.session_state.all_targets.append({
        'id': f"TRGT-{len(st.session_state.all_targets)+100}",
        'lat': np.random.uniform(*TOT_LAT_RANGE), 'lon': np.random.uniform(*TOT_LON_RANGE),
        'conf': np.random.randint(80, 99), 'votes': 0, 'status': 'Pending'
    })

time.sleep(15)
