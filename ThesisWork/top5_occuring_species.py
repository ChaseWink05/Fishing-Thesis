import pandas as pd 
import matplotlib.pyplot as plt  
import os
import streamlit as st
import plotly.express as px

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

    # Create a Plotly scatter plot
    fig = px.scatter(filtered_data, 
                     x='tot_len_a', 
                     y='wgt_a', 
                     color='common',  # Color points based on species
                     labels={'tot_len_a': 'Total Length', 'wgt_a': 'Weight'},
                     title="Clustering of Fish Data by Species (Excluding Unknown)",
                     category_orders={'common': top_species})  # Limit legend to top species
    st.title("Top 5 Occuring Species Cluster")
    # Show the interactive plot in Streamlit
    st.plotly_chart(fig) 
    # Display the explanation underneath the heatmap
    st.markdown("""
    This scatter plot visualizes the relationship between the total length and weight of the five most common fish species in the dataset. Each point represents a fish, with its color indicating the species. This interactive plot allows you to explore how different species vary in terms of size and weight, making it easier to identify patterns or clusters based on these two characteristics.
    """)

    
