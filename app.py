import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="ISS Tracker", page_icon="🛰️", layout="centered")

st.title("🛰️ Live ISS Tracker")
st.write("Tracks the International Space Station's current position in real time, with a trail of recent positions.")

# --- Fetch live ISS position ---
@st.cache_data(ttl=5)  # refresh every 5 seconds
def get_iss_position():
    # Try the primary API first, with a short timeout so it fails fast
    try:
        response = requests.get("https://api.open-notify.org/iss-now.json", timeout=5)
        data = response.json()
        lat = float(data["iss_position"]["latitude"])
        lon = float(data["iss_position"]["longitude"])
        timestamp = data["timestamp"]
        return lat, lon, timestamp
    except requests.exceptions.RequestException:
        # Fallback: wheretheiss.at, a reliable HTTPS alternative
        response = requests.get("https://api.wheretheiss.at/v1/satellites/25544", timeout=5)
        data = response.json()
        lat = float(data["latitude"])
        lon = float(data["longitude"])
        timestamp = data["timestamp"]
        return lat, lon, timestamp

try:
    lat, lon, timestamp = get_iss_position()
except requests.exceptions.RequestException as e:
    st.error("Couldn't reach any ISS API right now. This is usually a temporary network issue — try refreshing in a moment.")
    st.stop()

lat, lon, timestamp = get_iss_position()

#  Keep a trail of past positions using session_state 
if "trail" not in st.session_state:
    st.session_state.trail = []

# Only add a new point if it's different from the last one (avoids duplicate stacking)
if not st.session_state.trail or st.session_state.trail[-1] != (lat, lon):
    st.session_state.trail.append((lat, lon))

# Keep only the last 50 points so the trail doesn't grow forever
st.session_state.trail = st.session_state.trail[-50:]

# Display current stats 
col1, col2 = st.columns(2)
col1.metric("Latitude", f"{lat:.2f}°")
col2.metric("Longitude", f"{lon:.2f}°")

st.caption(f"Last updated: {pd.to_datetime(timestamp, unit='s')} UTC")
st.caption(f"Trail length: {len(st.session_state.trail)} points")

#  Map visualization with trail 
trail_df = pd.DataFrame(st.session_state.trail, columns=["lat", "lon"])
st.map(trail_df, zoom=1, size=100000)

# Controls 
col_a, col_b = st.columns(2)
if col_a.button("🔄 Refresh position"):
    st.cache_data.clear()
    st.rerun()
if col_b.button("🗑️ Clear trail"):
    st.session_state.trail = []
    st.rerun()

st.divider()
st.caption("Data from open-notify.org — the ISS orbits Earth roughly every 90 minutes. Click 'Refresh' repeatedly (or wait and re-run) to build up the trail over time.")