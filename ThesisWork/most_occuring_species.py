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
    # Create the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 8))

    # Define colors for each species
    colors = ['blue', 'green', 'red', 'orange', 'purple']

    # Loop through each species and plot the scatter
    for species, color in zip(top_species, colors):  
        species_data = filtered_data[filtered_data['common'] == species]  
        ax.scatter(
            species_data['tot_len_a'],  # X-axis Total length of the fish (column 'tot_len_a')
            species_data['wgt_a'],  # Y-axis Weight of the fish (column 'wgt_a')
            label=species,  # Label for the species, used in the plot legend
            color=color,  # Set the color of the scatter points to the species-specific color
            alpha=0.7  # Make the points slightly transparent to enhance visibility in overlapping regions
        )

    # Add titles, labels, and gridlines to the plot
    ax.set_title("Clustering of Fish Data by Species (Excluding Unknown)", fontsize=16)  
    ax.set_xlabel("Total Length (tot_len_a)", fontsize=14)  
    ax.set_ylabel("Weight (wgt_a)", fontsize=14)  
    ax.legend(title="Species", fontsize=12)  
    ax.grid(alpha=0.3)  

    # Convert the matplotlib figure to an interactive HTML using mpld3
    fig_html = mpld3.fig_to_html(fig)

    # Display the interactive plot in Streamlit
    components.html(fig_html, height=600)

    
