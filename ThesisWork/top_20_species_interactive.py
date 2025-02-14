import os
import pandas as pd
import streamlit as st
import plotly.express as px  

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

    # Create a bar chart using Plotly Express
    fig = px.bar(
        x=top_20_species.index,
        y=top_20_species.values,
        labels={'x': 'Species', 'y': 'Count'},
        title="Top 20 Most Occurring Fish Species",
        text=top_20_species.values,
        color_discrete_sequence=['skyblue']
    )

    # Update layout for better visualization
    fig.update_layout(
        xaxis=dict(tickangle=90),
        template="plotly_white",
        font=dict(size=30)
    )

    st.title("20 Most Occurring Species Bar Graph")
    # Display the Plotly chart in the Streamlit app
    st.plotly_chart(fig)
    # Display the explanation underneath the graph
    st.markdown("""
    This bar chart shows the top 20 most commonly occurring fish species in the dataset. The height of each bar represents the number of times each species appears. This interactive chart allows you to explore the distribution of fish species, making it easy to identify the most frequent species in the dataset.
    """)
