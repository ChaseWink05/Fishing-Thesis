import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
import os
import sys
import re
import matplotlib.pyplot as plt
import requests

def ensure_streamlit_running():
    if not os.getenv("STREAMLIT_RUNNING"):
        os.environ["STREAMLIT_RUNNING"] = "true"
        command = f"streamlit run {sys.argv[0]}"
        os.system(command)
        sys.exit()

def get_weather(api_key):
    latitude = 27.384781315287853
    longitude = -82.55692362785341
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={latitude},{longitude}&aqi=no"

    try:
        response = requests.get(url)
        data = response.json()
        return (
            data['current']['condition']['text'],
            data['current']['temp_f'],
            data['current']['humidity'],
            data['current']['wind_mph'],
            data['current']['last_updated']
        )
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        return None

def initialize_data(data_file):
    try:
        data = pd.read_csv(data_file)
    except FileNotFoundError:
        data = pd.DataFrame(columns=["ID", "Latitude", "Longitude", "Time", "Weather", "Type of Fish", "Weight", "Lure"])
    if "ID" not in data.columns:
        data["ID"] = range(1, len(data) + 1)
        data.to_csv(data_file, index=False)
    return data

def create_map(existing_data):
    map_obj = folium.Map(location=[27.384781315287853, -82.55692362785341], zoom_start=10)
    for _, row in existing_data.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            tooltip=(
                f"Time: {row['Time']}, Weather: {row['Weather']}, "
                f"Type of Fish: {row['Type of Fish']}, Weight: {row['Weight']} lbs, "
                f"Lure: {row['Lure']}, ID: {row['ID']}"
            )
        ).add_to(map_obj)

    if "last_clicked" in st.session_state:
        clicked_coords = st.session_state.last_clicked
        if clicked_coords:
            folium.Marker(
                location=[clicked_coords["lat"], clicked_coords["lng"]],
                tooltip="You clicked here!",
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(map_obj)

    return map_obj

def handle_map_click(map_obj):
    """Handle map clicks and avoid unnecessary reruns."""
    map_data = st_folium(map_obj, width=700, height=400)

    # Check if a valid map click occurred
    if map_data and "last_clicked" in map_data:
        clicked_coords = map_data["last_clicked"]

        if clicked_coords:
            #Updating what the actual last clicked is because if this executes than that means that there was another click so we 
            #have to update the variable
            st.session_state.last_clicked = clicked_coords  # Storing the clicked coordinates
            st.rerun()  # Trigger a rerun to refresh the map. Doing this so that it updates the map so it appears that 
            #the map is updating in real time no so where have to interact with the map to update it 

def reset_form_fields():
    """Reset all form fields in session state."""
    st.session_state.time = ""
    st.session_state.weather = ""
    st.session_state.fish_type = ""
    st.session_state.weight = 0.0
    st.session_state.lure = ""
    st.session_state.form_reset = False

def setup_form_fields():
    """Set up form fields with proper initialization."""
    if "form_reset" not in st.session_state:
        st.session_state.form_reset = False
        reset_form_fields()

    if st.session_state.form_reset:
        reset_form_fields()

    st.session_state.time = st.text_input("Time (HH:MM AM/PM)", value=st.session_state.time)
    st.session_state.weather = st.text_input("Weather", value=st.session_state.weather)
    st.session_state.fish_type = st.text_input("Type of Fish", value=st.session_state.fish_type)
    st.session_state.weight = st.number_input("Weight (lbs)", min_value=0.0, step=0.1, value=st.session_state.weight)
    st.session_state.lure = st.text_input("Lure", value=st.session_state.lure)

def is_valid_time(time_input):
    time_pattern = r"^(0?[1-9]|1[0-2]):[0-5][0-9]\s?(AM|PM|am|pm)$"
    return re.match(time_pattern, time_input.strip())

def handle_submission(existing_data, data_file):
    if "last_clicked" not in st.session_state:
        st.error("Please click on the map to select a location before submitting.")
        return

    clicked_coords = st.session_state.last_clicked
    lat, lng = clicked_coords["lat"], clicked_coords["lng"]

    if not all([st.session_state.time, st.session_state.weather, st.session_state.fish_type, st.session_state.weight, st.session_state.lure]):
        st.error("Please fill in all fields.")
        return

    if not is_valid_time(st.session_state.time):
        st.error("Invalid time format. Please enter time as HH:MM AM/PM.")
        return

    if any((existing_data["Latitude"] == lat) & (existing_data["Longitude"] == lng)):
        st.warning("A marker already exists at this location.")
        return

    new_entry = {
        "ID": len(existing_data) + 1,
        "Latitude": lat,
        "Longitude": lng,
        "Time": st.session_state.time,
        "Weather": st.session_state.weather,
        "Type of Fish": st.session_state.fish_type,
        "Weight": st.session_state.weight,
        "Lure": st.session_state.lure,
    }

    existing_data = pd.concat([existing_data, pd.DataFrame([new_entry])], ignore_index=True)
    existing_data.to_csv(data_file, index=False)
    st.success("Trip details saved!")
    st.session_state.form_reset = True
    if "last_clicked" in st.session_state:
        del st.session_state.last_clicked
    st.session_state.refresh = True
    st.rerun()

# Bar graph functionality
def display_bar_chart():
    # Path to the correct file location for GitHub and Streamlit Cloud
    destination_file = os.path.join('ThesisWork', 'optimum-ranges-f.csv')

    # Doing a simple check to see if the file is in the right location
    if not os.path.exists(destination_file):
        st.error(f"Error: The file 'optimum-ranges-f.csv' is missing in the 'ThesisWork' folder.")
        # Providing instructions to the user to place the file in the correct folder
        st.write(f"Please make sure the CSV file is placed in the 'ThesisWork' folder and try again.")

    # Proceed only if the file exists in the destination folder
    if os.path.exists(destination_file):  # Check again if the file exists
        df = pd.read_csv(destination_file)  # Load the CSV file into a pandas DataFrame for processing

    # Clean up column names by removing extra spaces
    df.columns = df.columns.str.strip()  # makes sure that there is no spaces

    # Check if the required columns exist in the DataFrame
    if "Species" in df.columns and "Temperature Range Preferendum" in df.columns:  # Ensure these columns are present
        # This is the title
        st.subheader("Temperature Range Preferendum for Species")
        st.dataframe(df)  # Show the DataFrame on the tab

        # Plotting the data from the DataFrame
        plt.figure(figsize=(10, 6))  # Set the figure size for the plot
        plt.bar(df["Species"], df["Temperature Range Preferendum"], color='skyblue')  # Creating a bar chart
        plt.xlabel("Species")  # Label for the x-axis
        plt.ylabel("Temperature Range Preferendum (°C)")  # Label for the y-axis
        plt.title("Temperature Range Preferendum by Species")  # Add a title to the plot
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
        st.pyplot(plt)  # Display the plot in the Streamlit app
    else:
        # If the necessary columns are missing, show an error
        st.error("The CSV file does not have the expected columns: 'Species' and 'Temperature Range Preferendum'.")

def main():
    #works
    ensure_streamlit_running()

    # Load weather data and initialize map
    api_key = "709d293f36ae43b0b1d212215250801"
    data_file = "trip_data.csv"

    st.title("Trip Logger with Interactive Map and Optimal Temperature Analysis")

    weather_data = get_weather(api_key)
    if weather_data:
        weather_description, temperature, humidity, wind_speed, last_updated = weather_data
        st.markdown("## 🌤️ Current Weather for Sarasota County, FL")
        st.write(f"Weather: {weather_description}")
        st.write(f"🌡️ Temperature: {temperature}°F")
        st.write(f"💧 Humidity: {humidity}%")
        st.write(f"🌬️ Wind Speed: {wind_speed} mph")
        st.write(f"**Last Updated:** {last_updated}")
    else:
        st.error("Could not retrieve weather data.")

    existing_data = initialize_data(data_file)
    #Havent got to yet
    st.subheader("Interactive Map")
    map_obj = create_map(existing_data)
    handle_map_click(map_obj)

    st.subheader("Log Your Trip Details (Click submit to make an entry)")
    setup_form_fields()

    if st.button("Submit"):
        handle_submission(existing_data, data_file)

    if not existing_data.empty:
        st.subheader("Existing Trip Data")
        st.markdown(existing_data.reset_index(drop=True).to_html(index=False, escape=False), unsafe_allow_html=True)
    display_bar_chart()

if __name__ == "__main__":
    main()
