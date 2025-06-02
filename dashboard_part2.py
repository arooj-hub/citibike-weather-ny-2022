import streamlit as st
import pandas as pd
import plotly.express as px

# Load your sample data
df = pd.read_csv("citibike_sample.csv")

# Create the date column
df['date'] = pd.to_datetime(df['started_at']).dt.date

# Sidebar menu
page = st.sidebar.selectbox("Choose a page", [
    "Intro",
    "Trips vs Temperature Over Time",
    "Top 20 Start Stations",
    "Kepler Map",
    "Recommendations"
])

# -------------------- PAGE 1: Intro --------------------
if page == "Intro":
    st.title("🚴 NYC CitiBike Strategy Dashboard")
    st.markdown("""
    This dashboard presents a comprehensive overview of CitiBike usage in NYC during 2022.
    
    It analyzes:
    - 📈 How weather (temperature) affects bike usage
    - 📍 Top stations used by riders
    - 🗺️ High-traffic locations via geospatial map
    - ✅ Final recommendations to improve supply
    
    Feel free to explore each page using the left sidebar.
    """)

# -------------------- PAGE 2: Line Chart --------------------
elif page == "Trips vs Temperature Over Time":
    st.subheader("📈 Trips vs Avg Temperature Over Time")
    df_daily = df.groupby('date').agg({
        'ride_id': 'count',
        'TAVG': 'mean'
    }).reset_index()
    df_daily.rename(columns={'ride_id': 'Trips', 'TAVG': 'Avg Temp'}, inplace=True)
    fig = px.line(df_daily, x='date', y=['Trips', 'Avg Temp'], title="Trips & Temperature Over Time")
    st.plotly_chart(fig)
    st.markdown("🔍 **Insight:** Warmer months clearly have more trips, showing weather affects ridership.")

# -------------------- PAGE 3: Bar Chart --------------------
elif page == "Top 20 Start Stations":
    st.subheader("🏆 Top 20 Start Stations")
    top_stations = df['start_station_name'].value_counts().nlargest(20).reset_index()
    top_stations.columns = ['Station', 'Trips']
    fig = px.bar(top_stations, x='Station', y='Trips', title="Top Start Stations")
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)
    st.markdown("📌 **Insight:** These are the busiest CitiBike stations — prioritize them for redistribution planning.")

# -------------------- PAGE 4: Kepler MAp -------------------
elif page == "Kepler Map":
    st.title("🗺️ Kepler.gl Map")
    try:
        with open("kepler_map.html", 'r', encoding='utf-8') as f:
            html_data = f.read()
        st.components.v1.html(html_data, height=600)
        st.markdown("📍 **Insight:** The map reveals high-density bike areas and supports rebalancing strategies.")
    except FileNotFoundError:
        st.error("❌ Map file not found. Please ensure `kepler_map.html` is in your project folder.")


# 6️⃣ RECOMMENDATION PAGE

# -------------------- PAGE 5: Recommendations --------------------
elif page == "Recommendations":
    st.subheader("📝 Final Recommendations")
    st.markdown("""
    Based on the analysis:

    - 🛠 **Optimize top 20 stations** for bike availability.
    - 🌡 **Weather planning**: usage drops in cold months — plan discounts or maintenance in winters.
    - 🗺 **Use Kepler map** to rebalance underused or overcrowded stations.
    - 📣 **Campaigns**: promote casual rider usage in less busy areas.
    """)
