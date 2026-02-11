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
    # Generate 20 initial points for a dense look
    for _ in range(20):
        st.session_state.all_targets.append({
            'lat': np.random.uniform(*TOT_LAT_RANGE),
            'lon': np.random.uniform(*TOT_LON_RANGE),
            'conf': np.random.randint(80, 99),
            'verified': np.random.choice([True, False], p=[0.3, 0.7])
        })

# --- UI HEADER ---
st.title("⚡ ISKRA | Strategic ISR Intelligence")
st.markdown("Automated Interception → AI Back-Casting → **Volunteer Verification** → DELTA Dissemination")

# Tabs for the three different views
tab1, tab2, tab3 = st.tabs(["🌐 Strategic Map", "🎥 Live FPV Intercept", "👥 Volunteer Verification"])

# --- TAB 1: STRATEGIC MAP ---
with tab1:
    st.subheader("Unified Operational Picture (UOP)")
    st.caption("Monitoring launch clusters on the occupied South Bank. Green = Verified, Red = Unverified.")
    
    # Create Folium Map
    m = folium.Map(location=[KHERSON_LAT - 0.05, KHERSON_LON + 0.1], zoom_start=11, tiles='cartodbpositron')
    
    for t in st.session_state.all_targets:
        color = 'green' if t['verified'] else 'red'
        status = "Verified" if t['verified'] else "Unverified"
        folium.CircleMarker(
            location=[t['lat'], t['lon']],
            radius=7,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
            popup=folium.Popup(f"<b>Status: {status}</b><br>AI Confidence: {t['conf']}%", max_width=200)
        ).add_to(m)
    
    # Render map
    st_folium(m, width="100%", height=550, returned_objects=[])
    st.write(f"**Total Targets Detected:** {len(st.session_state.all_targets)}")

# --- TAB 2: LIVE FPV INTERCEPT ---
with tab2:
    col_vid, col_meta = st.columns([2, 1])
    
    with col_vid:
        st.subheader("Signal Interception: Active Feed")
        st.info("💡 Presentation Tip: Link your downloaded YouTube FPV clips here.")
        # Replace the URL below with your local file like "fpv_video.mp4"
        st.video("https://www.sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4") 
        
    with col_meta:
        st.subheader("AI Metadata Extraction")
        st.metric("Horizon Triangulation", "94.2%")
        st.code(f"""
{{
  "signal_id": "FPV-ALPHA-9",
  "est_origin": "{st.session_state.all_targets[-1]['lat']:.4f}N, {st.session_state.all_targets[-1]['lon']:.4f}E",
  "landmarking": "SUCCESS",
  "status": "AWAITING_HUMAN_VETTING"
}}
        """)

# --- TAB 3: VOLUNTEER VERIFICATION ---
with tab3:
    st.subheader("Citizen-in-the-Loop Verification")
    st.write("Cross-referencing AI detections with satellite imagery to ensure 100% precision.")
    
    v_col1, v_col2 = st.columns(2)
    
    with v_col1:
        st.markdown("**Intercepted Landmark (POV)**")
        st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aerial_view_of_Kherson.jpg", 
                 caption="Landmark extracted from drone feed", use_container_width=True)
        
    with v_col2:
        st.markdown("**Satellite Reference (AO)**")
        st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aerial_view_of_Kherson.jpg", 
                 caption="Satellite imagery of the predicted sector", use_container_width=True)

    st.divider()
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("✅ Confirm Launch Site", use_container_width=True):
            st.success("Target Validated. Data pushed to DELTA system.")
            st.session_state.all_targets[-1]['verified'] = True
            st.balloons()
    with c2:
        st.button("⚠️ Low Confidence", use_container_width=True)
    with c3:
        st.button("❌ False Positive", use_container_width=True)

# Add new simulated targets periodically
if np.random.random() > 0.8:
    new_t = {
        'lat': np.random.uniform(*TOT_LAT_RANGE),
        'lon': np.random.uniform(*TOT_LON_RANGE),
        'conf': np.random.randint(80, 99),
        'verified': False
    }
    st.session_state.all_targets.append(new_t)

# Refresh loop for demo dynamics
time.sleep(15)
st.rerun()
