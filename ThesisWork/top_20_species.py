import os
import pandas as pd
import streamlit as st
from plotly import graph_objects as go

def display():
    # Define the path to the CSV file in the GitHub/Streamlit environment
    destination_file = os.path.join('ThesisWork', 'catch_20236.csv')

    # Check if the file exists
    if not os.path.exists(destination_file):
        st.error(f"Error: The file 'catch_20236.csv' is missing in the 'ThesisWork' folder.")
        st.write("Please make sure the CSV file is placed in the 'ThesisWork' folder and try again.")
        return  # Exit the function if the file is missing

    # Read the CSV data
    df = pd.read_csv(destination_file)

    # Replace empty rows (NaN values) in the 'common' column with the string 'NaN'
    df['common'] = df['common'].fillna('NaN')

    # Count occurrences of each species in the 'common' column, excluding 'NaN'
    species_counts = df['common'].value_counts().drop('NaN', errors='ignore')

    # Get the top 20 species with the highest counts
    top_20_species = species_counts.head(20)

    # Extract species names and counts for plotting
    species_names = top_20_species.index.tolist()
    species_counts = top_20_species.values.tolist()

    # Create an interactive bar chart using Plotly
    fig = go.Figure()

    # Add a bar trace
    fig.add_trace(go.Bar(
        x=species_names,
        y=species_counts,
        marker_color='skyblue',
        text=species_counts,
        textposition='auto',
        name="Species Counts"
    ))

    # Update layout for better visualization
    fig.update_layout(
        title="Top 20 Most Occurring Fish Species",
        xaxis_title="Species",
        yaxis_title="Count",
        xaxis=dict(tickangle=90),
        template="plotly_white",
        font=dict(size=12)
    )

    # Display the Plotly chart in the Streamlit app
    st.plotly_chart(fig)
