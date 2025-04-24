import pandas as pd
import plotly.express as px
import streamlit as st
import os

def run():
    # Define the path to the CSV file in the GitHub/Streamlit environment
    destination_file = os.path.join('ThesisWork', 'catch_20236.csv')

    # Check if the file exists
    if not os.path.exists(destination_file):
        st.error(f"Error: The file 'catch_20236.csv' is missing in the 'ThesisWork' folder.")
        st.write("Please make sure the CSV file is placed in the 'ThesisWork' folder and try again.")
        return  # Exit function if file is missing

    # Read the CSV data
    fish_data = pd.read_csv(destination_file)

    # Fill missing species names
    fish_data['common'] = fish_data['common'].fillna('Unknown')

    # Filter rows with positive values for tot_len_a and wgt_a
    fish_data = fish_data[(fish_data['tot_len_a'] > 0) & (fish_data['wgt_a'] > 0)]

    # Calculate the weight-to-length ratio
    fish_data['weight_length_ratio'] = fish_data['wgt_a'] / fish_data['tot_len_a']

    # Compute the correlation matrix
    corr_df = fish_data[['tot_len_a', 'wgt_a', 'weight_length_ratio']].corr()

    # Create a heatmap using Plotly Express
    fig = px.imshow(
        corr_df,
        color_continuous_scale='RdBu',
        zmin=-1,
        zmax=1,
        labels=dict(color="Correlation"),
        title="Correlation Heatmap of Fish Length, Weight, and Weight-to-Length Ratio (Filtered)"
    )

    # Display the heatmap in Streamlit
    st.title('Heat Map Correlation')
    st.plotly_chart(fig)

    # Display the explanation underneath the heatmap
    st.markdown("""
    This heatmap is a visual tool that helps you understand the relationship between three different measurements of fish: their total length, weight, and a ratio of weight to length. It uses colors to show how these measurements are related: if the color is closer to blue, it means they are strongly linked in a positive way, while red shows a strong negative relationship. If the color is closer to white, it means there is little or no connection between them. This makes it easier to see patterns or connections at a glance. This helps answer questions like: Do longer fish usually weigh more?  A weaker correlation here might suggest that as fish get longer, their shape (and weight-to-length ratio) varies more. It gives you a bird’s-eye view of how fish traits behave together. This can help spot patterns across species or identify what measurements matter most when trying to understand fish growth and condition.
    """)
