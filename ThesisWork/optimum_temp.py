import os
import streamlit as st
import pandas as pd
import plotly.express as px  # Import plotly express

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

        # Create an interactive bar chart using Plotly Express
        fig = px.bar(
            df, 
            x="Species", 
            y="Temperature Range Preferendum",
            text="Temperature Range Preferendum",
            title="Temperature Range Preferendum by Species",
            labels={"Species": "Species", "Temperature Range Preferendum": "Temperature Range Preferendum (°F)"},
            color_discrete_sequence=["skyblue"]
        )

        # Rotate x-axis labels for better readability
        fig.update_layout(xaxis_tickangle=45)

        # Display the Plotly chart in the Streamlit app
        st.plotly_chart(fig)

    else:
        # Show an error if the necessary columns are missing
        st.error("The CSV file does not have the expected columns: 'Species' and 'Temperature Range Preferendum'.")

    st.markdown(""" 
        This bar chart displays the preferred temperature ranges for various fish species, showing the optimal conditions each species tends to favor. The data is sourced from The Scientific Fisherman (https://thescientificfisherman.com/) and authored by Mark C. Biesinger, a scientist specializing in X-ray photoelectron spectroscopy and surface analysis techniques. The chart helps visualize the temperature preferences that support the best living conditions for these species.
        """)

