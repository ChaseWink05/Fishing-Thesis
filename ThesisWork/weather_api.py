import streamlit as st  
# Requests library is used to make HTTP requests to external APIs
import requests  

# Function to display weather data and initialize the Streamlit app
def weather_api():
    # API key for accessing the WeatherAPI service
    api_key = "709d293f36ae43b0b1d212215250801"

    # Set the title of the Streamlit app
    st.title("Trip Logger with Interactive Map and Optimal Temperature Analysis")

    # Fetch weather data using the `get_weather` function
    weather_data = get_weather(api_key)

    # If weather data is successfully retrieved, display it
    if weather_data:
        # Unpack the weather data tuple into individual variables
        weather_description, temperature, humidity, wind_speed, last_updated = weather_data

        # Display the weather information using Streamlit
        st.markdown("## 🌤️ Current Weather for Sarasota County, FL")
        # Weather condition (e.g., Sunny, Rainy)
        st.write(f"Weather: {weather_description}")  
        st.write(f"🌡️ Temperature: {temperature}°F")  
        st.write(f"💧 Humidity: {humidity}%")  
        st.write(f"🌬️ Wind Speed: {wind_speed} mph")  
        #Timestamp of the last weather update
        st.write(f"**Last Updated:** {last_updated}")  
    else:
        # Display an error message if weather data could not be retrieved
        st.error("Could not retrieve weather data.")

# Function to fetch weather data from the WeatherAPI
def get_weather(api_key):
    # Latitude and longitude for Sarasota County, FL
    latitude = 27.384781315287853
    longitude = -82.55692362785341

    # Construct the API URL with the provided API key and coordinates
    # The `aqi=no` parameter disables air quality data to simplify the response
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={latitude},{longitude}&aqi=no"

    try:
        # Make an HTTP GET request to the WeatherAPI
        response = requests.get(url)

        # Convert the JSON response to a Python dictionary
        # JSON (JavaScript Object Notation) is a lightweight data-interchange format
        # The `response.json()` method parses the JSON response into a Python dictionary
        data = response.json()

        # Extract specific weather details from the dictionary and return them as a tuple
        return (
             # Weather condition (e.g., Sunny, Rainy)
            data['current']['condition']['text'], 
             # Temperature in Fahrenheit
            data['current']['temp_f'], 
            # Humidity percentage
            data['current']['humidity'], 
             # Wind speed in miles per hour 
            data['current']['wind_mph'], 
             # Timestamp of the last weather update
            data['current']['last_updated'] 
        )
    except requests.exceptions.RequestException as e:
        # Handle exceptions that occur during the HTTP request
        # For example, network errors or invalid API responses
        st.error(f"Error fetching weather data: {e}")
        # Return None if an error occurs
        return None  