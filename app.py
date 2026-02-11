import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import time

# Iskra Branding
st.set_page_config(page_title="Iskra Live Demo", layout="wide")

# Hersonin koordinaatit
KHERSON_LAT = 46.6394
KHERSON_LON = 32.6139

st.title("⚡ ISKRA - Live Drone Back-Casting Analysis")
st.markdown(f"**Location:** Kherson TOT (Temporarily Occupied Territories)")

# Alustetaan sovelluksen tila (Session State)
if 'stage' not in st.session_state:
    st.session_state.stage = 'idle'
if 'history_list' not in st.session_state:
    st.session_state.history_list = [] # Käytetään listaa DataFramen sijaan vakauden vuoksi

# --- SIVUPALKKI ---
st.sidebar.header("ISR Control Center")
if st.sidebar.button("🚀 Trigger New Drone Detection"):
    st.session_state.stage = 'detecting'
    st.rerun()

if st.sidebar.button("🧹 Reset System"):
    st.session_state.stage = 'idle'
    st.session_state.history_list = []
    st.rerun()

# --- SIMULAATIO LOGIIKKA ---
if 'target_lat' not in st.session_state or st.session_state.stage == 'idle':
    st.session_state.target_lat = KHERSON_LAT + np.random.uniform(-0.01, 0.01)
    st.session_state.target_lon = KHERSON_LON + np.random.uniform(0.02, 0.04)

# --- VISUALISOINTI ---
view_state = pdk.ViewState(
    latitude=KHERSON_LAT,
    longitude=KHERSON_LON + 0.02,
    zoom=12,
    pitch=45
)

layers = []

# 1. Historiallinen trendidata (Heatmap)
if len(st.session_state.history_list) > 0:
    history_df = pd.DataFrame(st.session_state.history_list)
    layers.append(pdk.Layer(
        "HeatmapLayer",
        history_df,
        get_position=["lon", "lat"],
        get_weight="confidence",
        radius_pixels=60,
        opacity=0.6,
    ))

# 2. Animaatiovaiheet
if st.session_state.stage == 'detecting':
    with st.spinner("INTERCEPTING FPV VIDEO FEED..."):
        time.sleep(2)
        st.session_state.stage = 'analyzing'
        st.rerun()

if st.session_state.stage == 'analyzing':
    # Drone-lento kaari
    arc_data = [{
        'start': [st.session_state.target_lon, st.session_state.target_lat],
        'end': [KHERSON_LON, KHERSON_LAT]
    }]
    layers.append(pdk.Layer(
        "ArcLayer",
        data=arc_data,
        get_source_position="start",
        get_target_position="end",
        get_source_color=[255, 0, 0, 200],
        get_target_color=[255, 255, 0, 200],
        get_width=5,
    ))
    
    # Back-casting haku (Scatter)
    points_data = pd.DataFrame({
        'lat': np.random.normal(st.session_state.target_lat, 0.003, 15),
        'lon': np.random.normal(st.session_state.target_lon, 0.003, 15),
        'confidence': np.random.uniform(0.7, 0.99, 15)
    })
    layers.append(pdk.Layer(
        "ScatterplotLayer",
        points_data,
        get_position=["lon", "lat"],
        get_color=[255, 255, 255, 200],
        get_radius=80,
    ))

# Piirretään kartta (lisätty varmistus tyhjille kerroksille)
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/satellite-streets-v11",
    initial_view_state=view_state,
    layers=layers if layers else [],
))

# --- ANALYYSI JA MODEROINTI ---
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("AI Video Extract")
    if st.session_state.stage == 'analyzing':
        st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Aerial_view_of_Kherson.jpg", caption="Landmark filtering active")
        st.caption("AI identifying launch origin based on horizon triangulation.")
    else:
        st.info("System standby. Awaiting signal from sensors...")

with col2:
    st.subheader("Probability Metrics")
    if st.session_state.stage == 'analyzing':
        conf = np.random.uniform(88.5, 96.2)
        st.metric("Source Confidence", f"{conf:.1f}%", "+2.4%")
        st.progress(conf/100)
        st.write("**Analysis result:** Probable launch site identified in TOT sector.")

with col3:
    st.subheader("Human-in-the-loop")
    if st.session_state.stage == 'analyzing':
        if st.button("✅ Validate & Log to Trend Map"):
            # Lisätään uusi havainto listaan
            st.session_state.history_list.append({
                'lat': st.session_state.target_lat,
                'lon': st.session_state.target_lon,
                'confidence': 0.9
            })
            st.session_state.stage = 'idle'
            st.success("Validated. Shared with DELTA system.")
            time.sleep(1)
            st.rerun()
    else:
        st.write("Ready for manual validation of AI results.")
