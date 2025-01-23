import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
import os
import sys
import re
import matplotlib.pyplot as plt
import requests
import statsmodels.api as sm
import linear_regression
import decision_tree
import top5_occuring_species 
import plotly.express as px
import optimum_temp
import weather_api as wapi
import top_20_species_interactive
import heatmap


#This segment checks if Streamlit is already running. If it's not, it sets an environment variable called
#STREAMLIT_RUNNING to indicate that Streamlit should be started. It then creates a command to run Streamlit 
#using the current script and executes that command. After that, the script stops running further, ensuring that 
#only the Streamlit app is launched and no additional code runs unintentionally. This setup helps ensure that
#the script starts the Streamlit app properly when executed. The reason I used this is because I had the problem
#where everytime I wanted to run this program I had to type in streamlit run in the terminal. This was my work around
#to make it where I didn't have to do that everytime and so that it is more user friendly.

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


#This segement is trying to load data from a file called trip_data.csv. If the file exists, it reads the information
#inside and stores it in the program. However, if the file doesnt exist, it creates a new, empty table with 
#specific columns like "ID", "Latitude", and "Time" to hold data in the future. This ensures that the program 
#always has a place to store and work with data, even if the file is missing at first. I wanted to implement my 
#code this way so that it allows the user to always be able to run this program even if they do not have a csv called 
#"trip_data" on their laptop making it more user friendly 

def initialize_data(data_file):
    # Initialize data storage
    try:
        data = pd.read_csv(data_file)
    except FileNotFoundError:
        # DataFrame allows us to store and manipulate data in a table format, like Excel
        data = pd.DataFrame(columns=["ID", "Latitude", "Longitude", "Time", "Weather", "Type of Fish", "Weight", "Lure"])
    #If no ID column exists, add one and re-save the data
    if "ID" not in data.columns:
        data["ID"] = range(1, len(data) + 1)
        # Save the DataFrame to the trip_data.csv file
        data.to_csv(data_file, index=False)
    #returning the data so we can use it in other parts of our code 
    return data

# Adding existing markers to the map
def create_map(existing_data):
     # Creating the map, and setting the intial location of where the map is, made it start at New College
    map_obj = folium.Map(location=[27.384781315287853, -82.55692362785341], zoom_start=10)
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
            tooltip=(
                f"Time: {row['Time']}, Weather: {row['Weather']}, "
                f"Type of Fish: {row['Type of Fish']}, Weight: {row['Weight']} lbs, "
                f"Lure: {row['Lure']}, ID: {row['ID']}"
            )
            #add_to(map_obj) adds the marker to the map object which we created
        ).add_to(map_obj)
    # Check for last clicked location and add a new marker if clicked this will be an indication that the user can see where they clicked
    #if there was a click in the map
    if "last_clicked" in st.session_state:
        #Store the coordinates on the last place the user clicked the lat and lng
        clicked_coords = st.session_state.last_clicked
        #check to see if there are coordinates to proceed
        if clicked_coords:
            #This places a marker at the location with folium, shows the user where they clicked
            folium.Marker(
                #used to place the marker on the map, the location of the marker
                location=[clicked_coords["lat"], clicked_coords["lng"]],
                #when you hover over the marker this appears
                tooltip="You clicked here!",
                #setting the maker to be red and have one of the default values of an information sign to show up, (has a little "i")
                icon=folium.Icon(color="red", icon="info-sign")
                #Adding all this to the map object which we already created 
            ).add_to(map_obj)
    #Returning everything that we added to the map
    return map_obj

def handle_map_click(map_obj):
     # Capture Click Coordinates by setting the length and width of the map
    map_data = st_folium(map_obj, width=700, height=400)

    # If the map is clicked, store the coordinates and update the map, had to make another block that was similar to the last
    #because it wasn't allowing me to refresh the map like I wanted it to, to allow it to automatically refresh for the markers
    if map_data and "last_clicked" in map_data:
        #Setting a variable for the last clicked location on the map
        clicked_coords = map_data["last_clicked"]
        #if there are coords then run
        if clicked_coords:
            #Updating what the actual last clicked is because if this executes than that means that there was another click so we 
            #have to update the variable
            st.session_state.last_clicked = clicked_coords  # Storing the clicked coordinates
            st.rerun()  # Trigger a rerun to refresh the map. Doing this so that it updates the map so it appears that 
            #the map is updating in real time no so where have to interact with the map to update it 

def reset_form_fields():
    #Setting all the values to nothing so that way it resets 
    st.session_state.time = ""
    st.session_state.weather = ""
    st.session_state.fish_type = ""
    st.session_state.weight = 0.0
    st.session_state.lure = ""
    # Resetting the flag after resetting the fields
    st.session_state.form_reset = False

def setup_form_fields():
     # Initialize/reset form values if the reset flag is set. This way we can track it so that we can use it to reset text fields
    if "form_reset" not in st.session_state:
        #Intially setting this to false so we can track
        st.session_state.form_reset = False
        reset_form_fields()
    # if the form_reset bool is true then we execute this if statement 
    if st.session_state.form_reset:
        reset_form_fields()

    #Here we are taking values from the user and setting them equal to variables 
    #The value =st.session_state.time automatically fills in the current value of time if it exists, the st.text_input
    #creates a text input field with a label which is letting the user know what to type in and then we are just updating
    #the st.session_state variable for each attribute of the catch 
    st.session_state.time = st.text_input("Time (HH:MM AM/PM)", value=st.session_state.time)
    st.session_state.weather = st.text_input("Weather", value=st.session_state.weather)
    st.session_state.fish_type = st.text_input("Type of Fish", value=st.session_state.fish_type)
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

def handle_submission(existing_data, data_file):
    #Check to see if there was a click on the map
    if "last_clicked" not in st.session_state:
        st.error("Please click on the map to select a location before submitting.")
        return
    #updating the clicked_coords to make sure that we have the most updated version of where the user clicked last
    clicked_coords = st.session_state.last_clicked
    #updating the lat and lng to have the most up date version in this section of code
    lat, lng = clicked_coords["lat"], clicked_coords["lng"]
     #Here we do a check to see if all of the sections are filled, if they are empty then we skip this if statement on move on
    #Doing this check because you cannot submit a entry without having all these filled out
    if not all([st.session_state.time, st.session_state.weather, st.session_state.fish_type, st.session_state.weight, st.session_state.lure]):
        st.error("Please fill in all fields.")
        return
    #Checking the time to see if its valid or not, using the function that we defined earlier
    if not is_valid_time(st.session_state.time): # Check for valid time format
        st.error("Invalid time format. Please enter time as HH:MM AM/PM.") #Throws an error on the window tab
        return
    # Check if the clicked coordinates already exist in the dataset
    #uses any to see if any of the lat or lng are true or not, so if any of all of the lat and lng 
    #in the dataset are the same than we throw an error
    if any((existing_data["Latitude"] == lat) & (existing_data["Longitude"] == lng)):
        st.warning("A marker already exists at this location.")
        return
    # Save the new entry and saving the information as a dictonary 
    new_entry = {
        # len(data) gives the total number of rows in the existing dataset adding 1 to make sure its a new id
        "ID": len(existing_data) + 1, # Automatically assign a new ID
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
    st.session_state.form_reset = True
    # Reset the last_clicked value to hide the red marker
    if "last_clicked" in st.session_state:
        del st.session_state.last_clicked # Remove the red marker by deleting it 
    # Update session state to trigger a "rerun" and refresh the map so that it can update on the map
    st.session_state.refresh = True
    st.rerun()


def main():
    # Load weather data and initialize map
    api_key = "709d293f36ae43b0b1d212215250801"
    ensure_streamlit_running()
    wapi.get_weather(api_key)
    wapi.weather_api()
    data_file = "trip_data.csv"

    existing_data = initialize_data(data_file)
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

    optimum_temp.display_bar_chart()
    st.title("Fish Length vs Weight Analysis")

    # Create two columns for side-by-side display
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Linear Regression")
        linear_regression.run()

    with col2:
        
        st.markdown("### Decision Tree Regression")
        decision_tree.run()  
    
    # Display the explanation underneath the heatmap
    st.markdown("""
    Linear regression is a statistical method used to understand the relationship between two variables by fitting a straight line to the data. In this case, we're using fish length (tot_len_a) to predict fish weight (wgt_a). The red line in the plot represents the linear regression line, showing the how weight increases with length. It helps us understand the behavior of the data, assuming a linear relationship.
    A decision tree regressor is a machine learning model that makes predictions by splitting the data into segments based on feature values. It works by creating a tree-like structure, where each decision point leads to a prediction. In this case, the decision tree predicts fish weight based on length, but instead of a straight line, it creates decision points that better fit the data. This works especially when relationships are non-linear. The predicted curve in the plot is the result of the decision tree's predictions. Something to note is that mean squared error (MSE) which measures how far off the model's predictions are from the actual values, the lower MSE means better accuracy. R-squared tells you how much of the variation in the data is explained by the model, values closer to 1 mean a better fit, and values closer to 0 mean the model does not explain much. I have placed the linear regression and decision tree regressor side by side to allow you to compare two different approaches. The linear regression gives a simple, straight-line estimate, while the decision tree captures more complex, non-linear patterns in the data. Looking at the r value and mean squared value for the linear regression we can determine that the relationship between fish length and weight, as modeled by the linear regression, is weak. The R-squared value of 0.28 means that only 28% of the variation in weight is explained by the length of the fish meaning that other factors might be influencing weight. The relatively high mean squared error (65.07) indicates that the model's predictions are not very accurate. This is why we are comparing it to the decision tree regressor which is more optimal for data that is not as linear. Looking at the decision tree regressor we see that with an R-squared value of 0.79, the decision tree explains about 79% of the variation in fish weight based on length, suggesting a much stronger relationship between the two variables. The mean squared error of 18.66 indicates more accurate predictions compared to the linear model, meaning the decision tree provides a better fit for the data which is why I displayed them side by side for comparison. 
    """)
    top5_occuring_species.run()
    top_20_species_interactive.display()
    heatmap.run()
    st.title("K-Means Cluster")
    
    

if __name__ == "__main__":
    main()
