import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import os

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

    # Filter rows with positive and reasonable values for tot_len_a and wgt_a
    fish_data = fish_data[(fish_data['tot_len_a'] > 0) & (fish_data['wgt_a'] > 0)]

    # Calculate the weight-to-length ratio
    fish_data['weight_length_ratio'] = fish_data['wgt_a'] / fish_data['tot_len_a']

    # Calculate the correlation matrix (including the new variable)
    corr_df = fish_data[['tot_len_a', 'wgt_a', 'weight_length_ratio']].corr()

    # Create a Plotly heatmap
    fig = go.Figure(data=go.Heatmap(
        z=corr_df.values,
        x=corr_df.columns,
        y=corr_df.columns,
        colorscale='RdBu',
        colorbar=dict(title='Correlation'),
        zmin=-1,
        zmax=1
    ))

    # Add titles and axis labels
    fig.update_layout(
        title="Correlation Heatmap of Fish Length, Weight, and Weight-to-Length Ratio (Filtered)",
        xaxis_title="Variables",
        yaxis_title="Variables",
        template="plotly_dark"
    )

    # Display the heatmap in Streamlit
    st.title('Fish Data Analysis')
    st.plotly_chart(fig)
    # Display the explanation underneath the heatmap
    st.markdown("""
    This heatmap is a visual tool that helps you understand the relationship between three different measurements of fish: their total length, weight, and a ratio of weight to length. It uses colors to show how these measurements are related: if the color is closer to blue, it means they are strongly linked in a positive way, while red shows a strong negative relationship. If the color is closer to white, it means there is little or no connection between them. This makes it easier to see patterns or connections at a glance.
    """)