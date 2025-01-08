import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
import os
import sys
import re
import matplotlib.pyplot as plt
import subprocess
import requests

#This segment checks if Streamlit is already running. If it's not, it sets an environment variable called
#STREAMLIT_RUNNING to indicate that Streamlit should be started. It then creates a command to run Streamlit 
#using the current script and executes that command. After that, the script stops running further, ensuring that 
#only the Streamlit app is launched and no additional code runs unintentionally. This setup helps ensure that
#the script starts the Streamlit app properly when executed. The reason I used this is because I had the problem
#where everytime I wanted to run this program I had to type in streamlit run in the terminal. This was my work around
#to make it where I didn't have to do that everytime and so that it is more user friendly.

if __name__ == "__main__":  # Check if the script is being run directly
    try:
        import streamlit  # Attempt to import the Streamlit library
    except ModuleNotFoundError:  # If Streamlit is not found
        print("Streamlit not found! Please ensure it's bundled correctly.")  # Display an error message
        sys.exit(1)  # Exit the program with an error code

    # Check if the script is already running under Streamlit
    if not os.getenv("STREAMLIT_RUNNING"):  # Check if the STREAMLIT_RUNNING environment variable is not set
        os.environ["STREAMLIT_RUNNING"] = "true"  # Set the STREAMLIT_RUNNING environment variable to "true" to flag the app as running
        
        # Get the base path for the executable or the script
        if getattr(sys, 'frozen', False):  # Check if the script is frozen (bundled as an executable)
            base_path = sys._MEIPASS  # This is where bundled files are located
        else:
            base_path = os.path.dirname(__file__)  # Use the directory where the current script is located

        app_file = os.path.join(base_path, "main.py")  # Create the full path to the main.py file

        if not os.path.exists(app_file):  # Check if the main.py file exists
            print(f"Error: App file not found: {app_file}")  # Display an error message if the file is missing
            sys.exit(1)  # Exit the program with an error code

        # Run Streamlit using subprocess
        command = f"streamlit run {app_file}"  # Create the command to run the Streamlit app
        subprocess.run(command, shell=True)  # Execute the command in the shell
        sys.exit()  # Exit the program after running Streamlit

# Your WeatherAPI key
api_key = "709d293f36ae43b0b1d212215250801"

# Function to get weather data from WeatherAPI.com
def get_weather():
    # Sarasota County, FL coordinates
    latitude = 27.384781315287853
    longitude = -82.55692362785341

    # WeatherAPI.com URL from documentation
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={latitude},{longitude}&aqi=no"

    try:
        # Send GET request to WeatherAPI to fetch weather data
        response = requests.get(url)
        
        # If response is successful, process the JSON data
        data = response.json()  # Converts the response to a Python dictionary

        # Extract relevant weather data through the nested JSON dictornary that we created
        #Referenced documentation to figure this bit out 
        weather_description = data['current']['condition']['text']  # Weather condition 
        temperature = data['current']['temp_f']  # Temperature in Fahrenheit
        humidity = data['current']['humidity']  # Humidity percentage
        wind_speed = data['current']['wind_mph']  # Wind speed in miles per hour

        # Return the extracted data as a tuple
        return weather_description, temperature, humidity, wind_speed

    except requests.exceptions.RequestException as e:
        # If there is any errors, display it
        st.error(f"Error fetching weather data: {e}")
        return None

# Fetch weather data for Sarasota County, should look like this ex. ("Clear sky", 75, 50, 10)
weather_data = get_weather()

# Check if weather data was successfully retrieved
if weather_data:
    # Unpack the weather data if it was successfully fetched in a variable 
    weather_description, temperature, humidity, wind_speed = weather_data
     # Display in a visually appealing format
    st.markdown("## 🌤️ Current Weather for Sarasota County, FL")
    st.write(f"Weather: {weather_description}")
    st.write(f"Temperature: {temperature}°F")
    st.write(f"Humidity: {humidity}%")
    st.write(f"Wind Speed: {wind_speed} mph")
else:
    # If the data wasn't fetched, display an error message
    st.error("Could not retrieve weather data.")


#This segement is trying to load data from a file called trip_data.csv. If the file exists, it reads the information
#inside and stores it in the program. However, if the file doesnt exist, it creates a new, empty table with 
#specific columns like "ID", "Latitude", and "Time" to hold data in the future. This ensures that the program 
#always has a place to store and work with data, even if the file is missing at first. I wanted to implement my 
#code this way so that it allows the user to always be able to run this program even if they do not have a csv called 
#"trip_data" on their laptop making it more user friendly 


# Path to the correct file location (for the bundled executable)
if getattr(sys, 'frozen', False):  # Check if running as a packaged executable
    data_file = os.path.join(sys._MEIPASS, 'trip_data.csv')
else:  # Running as a script during development
    data_file = "trip_data.csv"  # You can change this to a specific path if needed

# Initialize data storage
try:
    existing_data = pd.read_csv(data_file)
except FileNotFoundError:
    # DataFrame allows us to store and manipulate data in a table format, like Excel
    existing_data = pd.DataFrame(
        columns=["ID", "Latitude", "Longitude", "Time", "Weather", "Type of Fish", "Weight", "Lure"]
    )

# If no ID column exists, add one and re-save the data
if "ID" not in existing_data.columns:
    existing_data["ID"] = range(1, len(existing_data) + 1)
    # Save the DataFrame to the trip_data.csv file
    existing_data.to_csv(data_file, index=False)

#This is where I start making what the user will see on the browser, here I use st which is my streamlit package and
#folium for markers etc..

# The Title
st.title("Trip Logger with Interactive Map and Optimal Temperature Analysis")

# Map Section
st.subheader("Interactive Map")

# Creating the map, and setting the intial location of where the map is, made it start at New College
m = folium.Map(location=[27.384781315287853, -82.55692362785341], zoom_start=10)

# Adding existing markers to the map
# _ is a placeholder since we are not using it, row is a series that represents the data in that row where you can access
#each columns value by calling its name. iterrows is a method in pandas that returns each row of the DataFrame as a series
# A series is a data strcture in the panda libarary that represents like a single column or row
#For every row in the DataFrame existing_data, create a marker on the map using the data from that row, and add it to the map.
for _, row in existing_data.iterrows():
    #Creating a marker on the interactive map
    folium.Marker(
        #sets the location of the marker, doing this by row[] which extracts the value for each row in the DataFrame
        location=[row["Latitude"], row["Longitude"]],
        #Creates a tooltip which is when you hover over the marker it displays this information, Doing the same thing 
        #in how we retrieve the information with row[]
        tooltip=f"Time: {row['Time']}, Weather: {row['Weather']}, Type of Fish: {row['Type of Fish']}, "
                f"Weight: {row['Weight']} lbs, Lure: {row['Lure']}, ID: {row['ID']}"
    #add_to(m) adds the marker to the map object which we created
    ).add_to(m)

# Check for last clicked location and add a new marker if clicked this will be an indication that the user can see where they clicked
#if there was a click in the map
if "last_clicked" in st.session_state:
    #Store the coordinates on the last place the user clicked the lat and lng
    clicked_coords = st.session_state.last_clicked
    #check to see if there are coordinates to proceed
    if clicked_coords:
        #setting the values of lat and lng by storing the value from clicked_coords into a certain variable so we can use it later
        lat, lng = clicked_coords["lat"], clicked_coords["lng"]
        #This places a marker at the location with folium, shows the user where they clicked
        folium.Marker(
            #used to place the marker on the map, the location of the marker
            location=[lat, lng],
            #when you hover over the marker this appears
            tooltip="You clicked here!",
            #setting the maker to be red and have one of the default values of an information sign to show up, (has a little "i")
            icon=folium.Icon(color="red", icon="info-sign")
        #Adding all this to the map object which we already created 
        ).add_to(m)

# Capture Click Coordinates by setting the length and width of the map
map_data = st_folium(m, width=700, height=400)

# If the map is clicked, store the coordinates and update the map, had to make another block that was similar to the last
#because it wasn't allowing me to refresh the map like I wanted it to, to allow it to automatically refresh for the markers
if map_data and "last_clicked" in map_data:
    #Setting a variable for the last clicked location on the map
    clicked_coords = map_data["last_clicked"]
    #if there are coords then run
    if clicked_coords:
        #Setting two variables lat and lng like we did ealier
        lat, lng = clicked_coords["lat"], clicked_coords["lng"]
        #Updating what the actual last clicked is because if this executes than that means that there was another click so we 
        #have to update the variable
        st.session_state.last_clicked = clicked_coords  # Storing the clicked coordinates
        st.rerun()  # Trigger a rerun to refresh the map. Doing this so that it updates the map so it appears that 
        #the map is updating in real time no so where have to interact with the map to update it 

# Trip Details Form. Setting the title for this section
st.subheader("Log Your Trip Details (Click submit to make an entry)")

# Initialize/reset form values if the reset flag is set. This way we can track it so that we can use it to reset text fields
if "form_reset" not in st.session_state:
    #Intially setting this to false so we can track
    st.session_state.form_reset = False

#Here I tried two different methods to reset the text fields it was giving me lots of issues but this approach worked for me

# Initializing the form values in session state to nothing so that way if there weren't there they are now 
if "time" not in st.session_state:
    st.session_state.time = ""
if "weather" not in st.session_state:
    st.session_state.weather = ""
if "fish_type" not in st.session_state:
    st.session_state.fish_type = ""
if "weight" not in st.session_state:
    st.session_state.weight = 0.0
if "lure" not in st.session_state:
    st.session_state.lure = ""

# if the form_reset bool is true then we execute this if statement 
if st.session_state.form_reset:
    #Setting all the values to nothing so that way it resets 
    st.session_state.time = ""
    st.session_state.weather = ""
    st.session_state.fish_type = ""
    st.session_state.weight = 0.0
    st.session_state.lure = ""
    st.session_state.form_reset = False  # Resetting the flag after resetting the fields
else:
    #if the form_reset bool is false than that means we don't have to reset the form and then we can proceed as normal
    #Here we are taking values from the user and setting them equal to variables 
    #The value =st.session_state.time automatically fills in the current value of time if it exists, the st.text_input
    #creates a text input field with a label which is letting the user know what to type in and then we are just updating
    #the st.session_state variable for each attribute of the catch 
    st.session_state.time = st.text_input("Time (HH:MM AM/PM)", value=st.session_state.time)
    st.session_state.weather = st.text_input("Weather", value=st.session_state.weather)
    st.session_state.fish_type = st.text_input("Type of Fish", value=st.session_state.fish_type)
    #The step states the value on which it can increase or decrease so I set it to .1 for the weight and the min has to be 0
    st.session_state.weight = st.number_input("Weight (lbs)", min_value=0.0, step=0.1, value=st.session_state.weight)
    st.session_state.lure = st.text_input("Lure", value=st.session_state.lure)


# Function for making sure time is correct
def is_valid_time(time_input):
    # 0?[1-9]: Allows hours 1 to 9, 1[0-2]: Matches hours 10, 11, and 12.[0-5][0-9]: Matches minutes from 00 to 59
    #\s?: Allows an optional space before AM/PM.
    time_pattern = r"^(0?[1-9]|1[0-2]):[0-5][0-9]\s?(AM|PM|am|pm)$"
    #.strip removes any whitespace so it doesn't cause an error. The re.match() function compares the time_input 
    # against the time_pattern. If the input matches the pattern, re.match() returns a match object if not it returns none
    return re.match(time_pattern, time_input.strip())


# Submit button logic, handles alot with map refreshing, form refreshing, and csv

#Creates a button that shows submit and when the user click submit then it executes this if statement
if st.button("Submit"):
    #Does a check to see if last_clicked is in the session state
    if "last_clicked" in st.session_state:
        #updating the clicked_coords again to make sure that we have the most updated version of where the user clicked last
        clicked_coords = st.session_state.last_clicked
        #again updating the lat and lng to have the most up date version in this section of code
        lat, lng = clicked_coords["lat"], clicked_coords["lng"]
        #Here we do a check to see if all of the sections are filled, if they are empty then we skip this if statement on move on
        #Doing this check because you cannot submit a entry without having all these filled out
        if st.session_state.time and st.session_state.weather and st.session_state.fish_type and st.session_state.weight and st.session_state.lure:
            #Checking the time to see if its valid or not, using the function that we defined earlier
            if not is_valid_time(st.session_state.time):  # Check for valid time format
                #Throws an error on the window tab
                st.error("Invalid time format. Please enter time as HH:MM AM/PM.")
            #if the time is valid then 
            else:
                # Check if the clicked coordinates already exist in the dataset
                #uses any to see if any of the lat or lng are true or not, so if any of all of the lat and lng 
                #in the dataset are the same than we throw an error
                if any((existing_data["Latitude"] == lat) & (existing_data["Longitude"] == lng)):
                    st.warning("A marker already exists at this location. Please select a different spot.")
                #if not the same then
                else:
                    # Save the new entry and saving the information as a dictonary 
                    new_entry = {
                        # len(existing_data) gives the total number of rows in the existing dataset adding 1 to make sure its a new id
                        "ID": len(existing_data) + 1,  # Automatically assign a new ID
                        "Latitude": lat,
                        "Longitude": lng,
                        "Time": st.session_state.time,
                        "Weather": st.session_state.weather,
                        "Type of Fish": st.session_state.fish_type,
                        "Weight": st.session_state.weight,
                        "Lure": st.session_state.lure,
                    }
                    #Append the new entry to the existing dataset. pd.DataFrame([new_entry]) converts the new_entry dictionary into a 
                    #DataFrame with one row. pd.concat([existing_data, pd.DataFrame([new_entry])]) combines the existing dataset (existing_data) with the new row.
                    #ignore_index=True ensures the row indices are recalculated to keep the numbering system that we have.
                    existing_data = pd.concat([existing_data, pd.DataFrame([new_entry])], ignore_index=True)
                    existing_data.to_csv(data_file, index=False)
                    #Showing that it was successful
                    st.success("Trip details saved!")

                    # Set session state flag to reset form fields after submission
                    st.session_state.form_reset = True  # Triggers the reset flag to clear the form

                    # Reset the last_clicked value to hide the red marker
                    if "last_clicked" in st.session_state:
                        del st.session_state.last_clicked  # Remove the red marker by deleting it 

                    # Update session state to trigger a "rerun" and refresh the map so that it can update on the map
                    st.session_state.refresh = True
    #Error handling
        else:
            st.error("Please fill in all fields.")
    else:
        st.error("Please click on the map to select a location before submitting.")

# Display Existing Trip Data with ID
st.subheader("Existing Trip Data")
# if there is something
if not existing_data.empty:
    # Reset the index and drop it completely. Resetting because we dont want to retain the old index as a new column in the DataFrame.
    existing_data_reset = existing_data.reset_index(drop=True)

    # Convert the DataFrame to HTML and use it to display without index. I choose this method because I ran into the issue
    # that when I was displaying it there was a column that I couldnt get rid of, so this was my workaround
    #to_html(index=False) converts the DataFrame into an HTML string, excluding the index column. st.markdown()
    # renders the HTML in the Streamlit app. unsafe_allow_html=True allows HTML formatting for better styling.
    
    st.markdown(existing_data_reset.to_html(index=False, escape=False), unsafe_allow_html=True)

    #Deletion logic
    # Option to delete an entry by ID doing by having an input where the user can choose what id they want by entering it in the text box
    #setting the min_value to 1 because that is the smallest id we have and max_value prevents user from entering an invalid amount that exceeds the id # we have
    delete_id = st.number_input("Enter the ID of the entry to delete", min_value=1, max_value=len(existing_data_reset), step=1)
    # if we click on the button then execute
    if st.button("Delete Entry"):
        # Remove entry by ID
        #existing_data_reset["ID"] != delete_id filters the dataset to exclude the row where the ID matches delete_id.
        #reset_index(drop=True) resets the index of the resulting DataFrame so that it doesn’t have gaps from the removed row.
        existing_data_reset = existing_data_reset[existing_data_reset["ID"] != delete_id].reset_index(drop=True)
        # Reset IDs to ensure they are in order
        # Generates new IDs starting from 1 up to the total number of rows in the updated DataFrame.
        existing_data_reset["ID"] = range(1, len(existing_data_reset) + 1)
        #Saves the updated dataset back to the original CSV file so changes are the same
        existing_data_reset.to_csv(data_file, index=False)
        #Shows that we are successful
        st.success("Entry deleted!")
        st.session_state.refresh = True  # Refresh the app after deletion to update the changes


# Path to the correct file location (for the bundled executable)
if getattr(sys, 'frozen', False):  # Check if running as a packaged executable
    destination_file = os.path.join(sys._MEIPASS, 'optimum-ranges-f.csv')
else:  # Running as a script during development
    destination_file = os.path.expanduser("~/Desktop/ThesisWork/optimum-ranges-f.csv")

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

#This triggers a refresh of the app's data when certain conditions are met, without having to manually interact with the app.
#Check for app refresh flag in session state
if "refresh" in st.session_state and st.session_state.refresh:  # Check if a refresh has been requested
    st.session_state.refresh = False  # Reset the refresh flag to prevent repetitive reruns
    st.rerun()  # Trigger the app to rerun and update the displayed data
