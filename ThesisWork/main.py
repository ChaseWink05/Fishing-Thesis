import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import requests

# Load or initialize trip data
def load_trip_data():
    data_file = os.path.join('ThesisWork', 'trip_data.csv')
    try:
        data = pd.read_csv(data_file)
    except FileNotFoundError:
        data = pd.DataFrame(
            columns=["ID", "Latitude", "Longitude", "Time", "Weather", "Type of Fish", "Weight", "Lure"]
        )
    if "ID" not in data.columns:
        data["ID"] = range(1, len(data) + 1)
        data.to_csv(data_file, index=False)
    return data_file, data


# Display map with existing markers
def display_map(data):
    st.subheader("Interactive Map")
    m = folium.Map(location=[27.384781315287853, -82.55692362785341], zoom_start=10)
    for _, row in data.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            tooltip=f"Time: {row['Time']}, Weather: {row['Weather']}, Type of Fish: {row['Type of Fish']}, "
                    f"Weight: {row['Weight']} lbs, Lure: {row['Lure']}, ID: {row['ID']}"
        ).add_to(m)

    map_data = st_folium(m, width=700, height=400)
    if map_data and "last_clicked" in map_data:
        clicked_coords = map_data["last_clicked"]
        if clicked_coords:
            st.session_state.last_clicked = clicked_coords
            st.success(f"Clicked Coordinates: Latitude {clicked_coords['lat']}, Longitude {clicked_coords['lng']}")
            st.rerun()


# Validate time format
def is_valid_time(time_input):
    time_pattern = r"^(0?[1-9]|1[0-2]):[0-5][0-9]\s?(AM|PM|am|pm)$"
    return re.match(time_pattern, time_input.strip())


# Log trip details
def log_trip_details(data_file, data):
    st.subheader("Log Your Trip Details (Click submit to make an entry)")
    if st.session_state.get("form_reset", False):
        time, weather, fish_type, weight, lure = "", "", "", 0.0, ""
        st.session_state.form_reset = False
    else:
        time = st.text_input("Time (HH:MM AM/PM)", "")
        weather = st.text_input("Weather", "")
        fish_type = st.text_input("Type of Fish", "")
        weight = st.number_input("Weight (lbs)", min_value=0.0, step=0.1, value=0.0)
        lure = st.text_input("Lure", "")

    if st.button("Submit"):
        if "last_clicked" in st.session_state:
            clicked_coords = st.session_state.last_clicked
            if clicked_coords:
                lat, lng = clicked_coords["lat"], clicked_coords["lng"]
                if time and weather and fish_type and weight and lure:
                    if not is_valid_time(time):
                        st.error("Invalid time format. Please enter time as HH:MM AM/PM.")
                    elif any((data["Latitude"] == lat) & (data["Longitude"] == lng)):
                        st.warning("A marker already exists at this location. Please select a different spot.")
                    else:
                        new_entry = {
                            "ID": len(data) + 1,
                            "Latitude": lat,
                            "Longitude": lng,
                            "Time": time,
                            "Weather": weather,
                            "Type of Fish": fish_type,
                            "Weight": weight,
                            "Lure": lure,
                        }
                        data = pd.concat([data, pd.DataFrame([new_entry])], ignore_index=True)
                        data.to_csv(data_file, index=False)
                        st.success("Trip details saved!")
                        st.session_state.form_reset = True
                        st.session_state.refresh = True
        else:
            st.error("Please click on the map to select a location before submitting.")


# Display existing trip data
def display_existing_data(data_file, data):
    st.subheader("Existing Trip Data")
    if not data.empty:
        data = data.reset_index(drop=True)
        st.markdown(data.to_html(index=False, escape=False), unsafe_allow_html=True)


# Weather API integration
def get_weather():
    api_key = "709d293f36ae43b0b1d212215250801"
    latitude, longitude = 27.384781315287853, -82.55692362785341
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={latitude},{longitude}&aqi=no"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            return (
                data['current']['condition']['text'],
                data['current']['temp_f'],
                data['current']['humidity'],
                data['current']['wind_mph']
            )
    except Exception as e:
        st.error(f"Error fetching weather data: {str(e)}")
        return None


def display_weather():
    weather_data = get_weather()
    if weather_data:
        weather_description, temperature, humidity, wind_speed = weather_data
        st.markdown("### Current Weather in Sarasota County")
        st.write(f"🌡️ Temperature: {temperature}°F")
        st.write(f"💧 Humidity: {humidity}%")
        st.write(f"🌬️ Wind Speed: {wind_speed} mph")
        st.write(f"🌤️ Weather Condition: {weather_description}")
    else:
        st.error("Could not fetch weather data.")


# Display bar graph for CSV data
def display_bar_graph():
    destination_file = os.path.join('ThesisWork', 'optimum-ranges-f.csv')
    if os.path.exists(destination_file):
        df = pd.read_csv(destination_file)
        if "Species" in df.columns and "Temperature Range Preferendum" in df.columns:
            st.subheader("Temperature Range Preferendum by Species")
            st.dataframe(df)
            plt.figure(figsize=(10, 6))
            plt.bar(df["Species"], df["Temperature Range Preferendum"], color='skyblue')
            plt.xlabel("Species")
            plt.ylabel("Temperature Range Preferendum (°C)")
            plt.title("Temperature Range Preferendum by Species")
            plt.xticks(rotation=45, ha='right')
            st.pyplot(plt)
        else:
            st.error("CSV is missing the required columns.")
    else:
        st.error(f"CSV file not found at {destination_file}")


# Main flow
data_file, data = load_trip_data()
display_weather()
display_map(data)
log_trip_details(data_file, data)
display_existing_data(data_file, data)
display_bar_graph()
