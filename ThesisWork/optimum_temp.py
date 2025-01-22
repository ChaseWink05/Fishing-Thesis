import os
import streamlit as st
import pandas as pd
import plotly as plt

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