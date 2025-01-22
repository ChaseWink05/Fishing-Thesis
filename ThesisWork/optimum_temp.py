import os
import streamlit as st
import pandas as pd
from plotly import graph_objects as go

# Bar graph functionality
def display_bar_chart():
    # Path to the correct file location for GitHub and Streamlit Cloud
    destination_file = os.path.join('ThesisWork', 'optimum-ranges-f.csv')

    # Doing a simple check to see if the file is in the right location
    if not os.path.exists(destination_file):
        st.error(f"Error: The file 'optimum-ranges-f.csv' is missing in the 'ThesisWork' folder.")
        st.write("Please make sure the CSV file is placed in the 'ThesisWork' folder and try again.")
        return  # Exit the function if the file is missing

    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(destination_file)

    # Clean up column names by removing extra spaces
    df.columns = df.columns.str.strip()

    # Check if the required columns exist in the DataFrame
    if "Species" in df.columns and "Temperature Range Preferendum" in df.columns:
        # Display the title and DataFrame in the Streamlit app
        st.subheader("Temperature Range Preferendum for Species")
        st.dataframe(df)

        # Create an interactive bar chart using Plotly
        fig = go.Figure()

        # Add bar trace
        fig.add_trace(go.Bar(
            x=df["Species"],
            y=df["Temperature Range Preferendum"],
            marker_color='skyblue',
            text=df["Temperature Range Preferendum"],
            textposition='auto',
            name="Temperature Range"
        ))

        # Update the layout for better presentation
        fig.update_layout(
            title="Temperature Range Preferendum by Species",
            xaxis_title="Species",
            yaxis_title="Temperature Range Preferendum (°F)",
            template="plotly_white",
            xaxis=dict(tickangle=45)  # Rotate x-axis labels
        )

        # Display the Plotly chart in the Streamlit app
        st.plotly_chart(fig)

    else:
        # Show an error if the necessary columns are missing
        st.error("The CSV file does not have the expected columns: 'Species' and 'Temperature Range Preferendum'.")
