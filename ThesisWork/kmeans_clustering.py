# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
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
    else:
        # If the file exists, read the CSV data
        catch_data = pd.read_csv(destination_file)

    # Fill missing species names
    fish_data['common'] = fish_data['common'].fillna('Unknown')

    # Filter rows with valid values for tot_len_a (length) and wgt_a (weight)
    fish_data = fish_data[(fish_data['tot_len_a'] > 0) & (fish_data['wgt_a'] > 0)]

    # Create a new column for the length-to-weight ratio
    fish_data['length_to_weight_ratio'] = fish_data['tot_len_a'] / fish_data['wgt_a']

    # Select the features for clustering: length, weight, and length-to-weight ratio
    X = fish_data[['tot_len_a', 'wgt_a', 'length_to_weight_ratio']]

    # Normalize the data for clustering
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Perform K-means clustering
    k = 4  # Number of clusters
    kmeans = KMeans(n_clusters=k, max_iter=100, random_state=42)
    fish_data['cluster'] = kmeans.fit_predict(X_scaled)

    # Visualize the clusters using Plotly: Length vs Weight
    fig = px.scatter(
        fish_data,
        x='tot_len_a',  # Length on the x-axis
        y='wgt_a',  # Weight on the y-axis
        color='cluster',  # Cluster labels for coloring
        title='K-means Clustering (Length vs Weight)',
        labels={'tot_len_a': 'Fish Length (tot_len_a)', 'wgt_a': 'Fish Weight (wgt_a)'},
        color_continuous_scale='Viridis',
        hover_data=['length_to_weight_ratio']  # Show length-to-weight ratio on hover
    )

    # Customize the layout
    fig.update_traces(marker=dict(size=10, line=dict(width=1, color='DarkSlateGrey')))
    fig.update_layout(
        xaxis_title='Fish Length (tot_len_a)',
        yaxis_title='Fish Weight (wgt_a)',
        legend_title='Cluster',
        title_font_size=20,
        template='plotly_white'
    )

    st.title("K-Means Cluster")
    # Show the interactive plot
    st.plotly_chart(fig)
