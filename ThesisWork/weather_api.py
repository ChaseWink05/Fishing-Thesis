import streamlit as st
import main
import requests
# Load weather data and initialize map
def weather_api():
    api_key = "709d293f36ae43b0b1d212215250801"

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