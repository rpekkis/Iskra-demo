import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="ISKRA | ISR System", layout="wide", initial_sidebar_state="collapsed")

# Coordinates (Kherson South Bank / TOT)
KHERSON_LAT, KHERSON_LON = 46.6394, 32.6139
TOT_LAT_RANGE = (46.50, 46.61) 
TOT_LON_RANGE = (32.65, 32.85)

# --- INITIALIZE SESSION STATE ---
if 'all_targets' not in st.session_state:
    st.session_state.all_targets = []
    # Generate initial sample data
    for i in range(15):
        st.session_state.all_targets.append({
            'id': f"TRGT-{100+i}",
            'lat': np.random.uniform(*TOT_LAT_RANGE),
            'lon': np.random.uniform(*TOT_LON_RANGE),
            'conf': np.random.randint(80, 99),
            'status': 'Pending'
        })

# --- UI HEADER ---
st.title("⚡ ISKRA | Strategic ISR Intelligence")
st.markdown("Automated Interception → AI Back-Casting → **Volunteer Verification** → DELTA Dissemination")

tab1, tab2, tab3 = st.tabs(["🌐 Strategic Map", "🎥 Live FPV Intercept", "👥 Volunteer Verification"])

# --- TAB 1: STRATEGIC MAP ---
with tab1:
    st.subheader("Unified Operational Picture (UOP)")
    st.caption("Green = Confirmed, Red = Pending, Gray = False Positive")
    
    m = folium.Map(location=[KHERSON_LAT - 0.05, KHERSON_LON + 0.1], zoom_start=11, tiles='cartodbpositron')
    
    for t in st.session_state.all_targets:
        color_map = {'Confirmed': 'green', 'Pending': 'red', 'False Positive': 'gray'}
        color = color_map.get(t['status'], 'red')
        
        folium.CircleMarker(
            location=[t['lat'], t['lon']],
            radius=7,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
            popup=f"ID: {t['id']} | Status: {t['status']} | Confidence: {t['conf']}%"
        ).add_to(m)
    
    st_folium(m, width="100%", height=500, returned_objects=[])

# --- TAB 2: LIVE FPV INTERCEPT ---
with tab2:
    col_vid, col_meta = st.columns([2, 1])
    with col_vid:
        st.subheader("Signal Interception: Active Feed")
        st.info("💡 Presentation Tip: Play your YouTube-sourced FPV clips here.")
        st.video("https://www.sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4") 
    with col_meta:
        st.subheader("AI Metadata Extraction")
        st.metric("Horizon Triangulation", "94.2%")
        st.code(f"SIGNAL_ID: FPV-ALPHA-9\nSTATUS: AWAITING_VETTING")

# --- TAB 3: VOLUNTEER VERIFICATION ---
with tab3:
    st.subheader("Human-in-the-Loop: Verification Queue")
    
    # Selection for which target to verify
    pending_targets = [t for t in st.session_state.all_targets if t['status'] == 'Pending']
    
    if not pending_targets:
        st.success("All current observations have been processed.")
        if st.button("Generate More Observations"):
            new_id = f"TRGT-{len(st.session_state.all_targets)+100}"
            st.session_state.all_targets.append({
                'id': new_id, 'lat': np.random.uniform(*TOT_LAT_RANGE),
                'lon': np.random.uniform(*TOT_LON_RANGE), 'conf': np.random.randint(80, 99), 'status': 'Pending'
            })
            st.rerun()
    else:
        # Create a dropdown to select a target
        target_ids = [t['id'] for t in pending_targets]
        selected_id = st.selectbox("Select Target ID to Verify", target_ids)
        
        # Get selected target data
        current_target = next(item for item in st.session_state.all_targets if item["id"] == selected_id)
        
        col_info, col_action = st.columns([1, 1])
        with col_info:
            st.write(f"**Target ID:** {current_target['id']}")
            st.write(f"**AI Confidence:** {current_target['conf']}%")
            st.write(f"**Estimated Coordinates:** {current_target['lat']:.4f}, {current_target['lon']:.4f}")
        
        st.divider()
        
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aerial_view_of_Kherson.jpg", caption="POV Frame")
        with v_col2:
            st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aerial_view_of_Kherson.jpg", caption="Sat Reference")

        st.divider()
        
        # Actions to change status
        btn_conf, btn_fp, btn_skip = st.columns(3)
        with btn_conf:
            if st.button("✅ CONFIRM (Push to DELTA)", use_container_width=True):
                current_target['status'] = 'Confirmed'
                st.success(f"{selected_id} confirmed and disseminated.")
                st.balloons()
                time.sleep(1)
                st.rerun()
        with btn_fp:
            if st.button("❌ FALSE POSITIVE", use_container_width=True):
                current_target['status'] = 'False Positive'
                st.warning(f"{selected_id} marked as False Positive.")
                time.sleep(1)
                st.rerun()
        with btn_skip:
            st.button("➡️ Skip for Now", use_container_width=True)

# Small background update to keep map alive
if np.random.random() > 0.95:
    new_t = {
        'id': f"TRGT-{len(st.session_state.all_targets)+100}",
        'lat': np.random.uniform(*TOT_LAT_RANGE), 'lon': np.random.uniform(*TOT_LON_RANGE),
        'conf': np.random.randint(80, 99), 'status': 'Pending'
    }
    st.session_state.all_targets.append(new_t)

time.sleep(15)
