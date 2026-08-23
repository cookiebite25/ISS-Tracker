# ISS-Tracker
A Streamlit web app that tracks the International Space Station's real-time position and visualizes its recent path on an interactive world map.
<img width="754" height="440" alt="image" src="https://github.com/user-attachments/assets/51ca149a-3d13-4265-8c46-0e9e44fff945" />
<img width="755" height="416" alt="image" src="https://github.com/user-attachments/assets/028e5413-74d5-4cf3-9e31-29573071494f" />

What it does
Fetches the ISS's current latitude/longitude in real time from a public API
Displays the position on an interactive map, along with the exact coordinates and last-updated timestamp
Builds a trail of recent positions over time, so you can see the station's path rather than just a single point
Falls back to a secondary API automatically if the primary one is slow or unreachable, so the app stays usable even when one data source has issues
Why I built it

I wanted a project that combined backend fundamentals (API calls, error handling, data pipelines) with something visually satisfying to look at and interact with watching a real spacecraft move across a map in your browser felt like a good way to make that concrete.

How it works
The app calls the Open Notify API to get the ISS's current coordinates
If that fails or times out, it automatically falls back to wheretheiss.at, a second HTTPS-based tracking API
Each new position is stored in Streamlit's session_state, building a trail of the last 50 points
The trail is rendered on an interactive map using st.map()

Tech stack
Python
Streamlit - UI and interactivity
Pandas - data handling
Requests - API calls

Running it locally
bash
git clone https://github.com/YOUR-USERNAME/portfolio-dashboard.git
cd portfolio-dashboard
pip install -r requirements.txt
streamlit run app.py

Notes
The ISS travels at roughly 7.66 km/second and completes a full orbit of Earth about every 90 minutes. Because of this, its position can look noticeably different even a few seconds apart — so if you compare this app's output to another tracker at a slightly different moment, don't be surprised if the numbers don't match exactly. Both are correct; the station just moves fast.

What I'd add next[not right now tho]
Show which country/ocean the ISS is currently over
Predict the next visible pass time for a user-entered location
Auto-refresh on a timer instead of requiring a manual click
