import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# Page setup
st.set_page_config(page_title="NYC CitiBike Dashboard", layout="wide")
# Title
st.title("🚲 NYC CitiBike Dashboard")
st.markdown("An interactive dashboard exploring CitiBike usage patterns and weather impact in NYC (2022)")
# Load data
df = pd.read_csv("citibike_weather_2022.csv")
df['date'] = pd.to_datetime(df['date'])
# Bar chart
st.subheader("🔝 Top 20 Start Stations")
top_stations = df['start_station_name'].value_counts().nlargest(20).reset_index()
top_stations.columns = ['start_station_name', 'trip_count']
fig_bar = px.bar(top_stations, x='start_station_name', y='trip_count')
st.plotly_chart(fig_bar, use_container_width=True)
#  Line chart – Trips vs Temperature Over Time

# Convert to datetime if not done already
df['date'] = pd.to_datetime(df['date'])

# Group by date, count trips, and get mean temperature
df_daily = df.groupby('date').agg({
    'ride_id': 'count',       # trips
    'TAVG': 'mean'            # average temp
}).reset_index()

# Create figure
fig_line = go.Figure()

# Add Trips
fig_line.add_trace(go.Scatter(
    x=df_daily['date'],
    y=df_daily['ride_id'],
    name='Trips',
    yaxis='y1'
))

# Add Temperature
fig_line.add_trace(go.Scatter(
    x=df_daily['date'],
    y=df_daily['TAVG'],
    name='Avg Temp',
    yaxis='y2'
))

# Layout
fig_line.update_layout(
    title='Trips vs Avg Temperature Over Time',
    xaxis_title='Date',
    yaxis=dict(title='Trip Count'),
    yaxis2=dict(title='Avg Temp (°F)', overlaying='y', side='right'),
    legend=dict(x=0.01, y=0.99)
)

# Show in Streamlit
st.plotly_chart(fig_line, use_container_width=True)
df['date'] = pd.to_datetime(df['date'])

df_daily = df.groupby('date').agg({'ride_id': 'count', 'max_temp': 'mean'}).reset_index()

fig = go.Figure()
fig.add_trace(go.Scatter(x=df_daily['date'], y=df_daily['ride_id'], name='Trips', yaxis='y1'))
fig.add_trace(go.Scatter(x=df_daily['date'], y=df_daily['max_temp'], name='Temperature', yaxis='y2'))

fig.update_layout(
    title="Trips vs Temperature Over Time",
    yaxis=dict(title='Trips'),
    yaxis2=dict(title='Temperature (°F)', overlaying='y', side='right')
)

st.components.v1.iframe(file:///C:/Users/ALI%20HASSAN/Documents/work%20local/citibike-weather-ny-2022/kepler_custom_map.html, height=600)


