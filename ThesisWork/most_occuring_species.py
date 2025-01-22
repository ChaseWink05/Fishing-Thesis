import pandas as pd 
import matplotlib.pyplot as plt  
import os
import streamlit as st
import mpld3
import streamlit.components.v1 as components

def run():  
    # Define the path to the CSV file in the GitHub/Streamlit environment
    destination_file = os.path.join('ThesisWork', 'catch_20236.csv')

    # Check if the file exists
    if not os.path.exists(destination_file):
        st.error(f"Error: The file 'catch_20236.csv' is missing in the 'ThesisWork' folder.")
        st.write("Please make sure the CSV file is placed in the 'ThesisWork' folder and try again.")
    else:
        # If the file exists, read the CSV data
        fish_data = pd.read_csv(destination_file)

    # Fill missing species names
    fish_data['common'] = fish_data['common'].fillna('Unknown')  
    # Replace any missing values in the 'common' column with the string 'Unknown' to avoid errors in processing

    # Count species occurrences and get the top 5 species excluding "Unknown"
    species_counts = fish_data['common'].value_counts()  
    # Count the number of occurrences for each species in the 'common' column and return a Series sorted by counts in descending order

    top_species = [species for species in species_counts.index[:6] if species != 'Unknown']  
    # Take the top 5 most common species by selecting the first 5 indices from `species_counts`
    # Use a list comprehension to exclude 'Unknown' from the list of top species

    # Filter data for only the top species
    filtered_data = fish_data[fish_data['common'].isin(top_species)]  
    # Create a new DataFrame `filtered_data` that includes only rows where the 'common' column matches one of the `top_species`

    colors = ['blue', 'green', 'red', 'orange', 'purple']  
    # Define a list of distinct colors to represent each species in the scatter plot

    plt.figure(figsize=(12, 8))  
    # Set the size of the figure to make the plot visually clear and large 

    for species, color in zip(top_species, colors):  
        # Loop through each species in `top_species` and its corresponding color
        species_data = filtered_data[filtered_data['common'] == species]  
        # Filter `filtered_data` to include only rows corresponding to the current species in the loop
        plt.scatter(
            species_data['tot_len_a'],  # X-axis Total length of the fish (column 'tot_len_a')
            species_data['wgt_a'],  # Y-axis Weight of the fish (column 'wgt_a')
            label=species,  # Label for the species, used in the plot legend
            color=color,  # Set the color of the scatter points to the species-specific color
            alpha=0.7  # Make the points slightly transparent to enhance visibility in overlapping regions
        )

    # Add titles, labels, and gridlines to the plot
    plt.title("Clustering of Fish Data by Species (Excluding Unknown)", fontsize=16)  
    # Title of the plot, indicating the data being visualized and the exclusion of 'Unknown'

    plt.xlabel("Total Length (tot_len_a)", fontsize=14)  
    # Label for the X-axis to represent the total length of the fish

    plt.ylabel("Weight (wgt_a)", fontsize=14)  
    # Label for the Y-axis to represent the weight of the fish

    plt.legend(title="Species", fontsize=12)  
    # Add a legend to the plot to show which color corresponds to which species

    plt.grid(alpha=0.3)  
    # Add gridlines to the plot for easier reading of the data points and making the gridlines slightly transparent
    fig = plt.figure()
    plt.plot()  
    
    fig_html = mpld3.fig_to_html(fig)
    components.html(fig_html, height=600)
    # Display the plot to the user
