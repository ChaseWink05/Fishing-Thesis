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

    top_species = [species for species in species_counts.index[:6] if species != 'Unknown']  

    # Filter data for only the top species
    filtered_data = fish_data[fish_data['common'].isin(top_species)]  

    colors = ['blue', 'green', 'red', 'orange', 'purple']  

    plt.figure(figsize=(12, 8))  # Set the size of the figure to make the plot visually clear and large 

    for species, color in zip(top_species, colors):  
        species_data = filtered_data[filtered_data['common'] == species]  
        plt.scatter(
            species_data['tot_len_a'],  
            species_data['wgt_a'],  
            label=species,  
            color=color,  
            alpha=0.7  
        )

    # Add titles, labels, and gridlines to the plot
    plt.title("Clustering of Fish Data by Species (Excluding Unknown)", fontsize=16)  
    plt.xlabel("Total Length (tot_len_a)", fontsize=14)  
    plt.ylabel("Weight (wgt_a)", fontsize=14)  
    plt.legend(title="Species", fontsize=12)  
    plt.grid(alpha=0.3)

    # Ensure the plot doesn't get clipped
    plt.tight_layout()

    # Convert the matplotlib figure to an interactive HTML using mpld3
    fig_html = mpld3.fig_to_html(plt.gcf())  

    # Display the interactive plot in Streamlit
    components.html(fig_html, height=600)