import pandas as pd
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
        # If the file doesn't exist, show an error message to the user
        st.error(f"Error: The file 'catch_20236.csv' is missing in the 'ThesisWork' folder.")
        st.write("Please make sure the CSV file is placed in the 'ThesisWork' folder and try again.")
    else:
        # If the file exists, read the CSV data into a DataFrame
        fish_data = pd.read_csv(destination_file)

    # Fill missing species names with 'Unknown'
    fish_data['common'] = fish_data['common'].fillna('Unknown')

    # Filter rows with valid values for tot_len_a and wgt_a 
    # Only keep rows where length (tot_len_a) and weight (wgt_a) are greater than 0
    fish_data = fish_data[(fish_data['tot_len_a'] > 0) & (fish_data['wgt_a'] > 0)]

    # Create a new column for the length-to-weight ratio
    # This is calculated by dividing the total length by the total weight for each fish
    fish_data['length_to_weight_ratio'] = fish_data['tot_len_a'] / fish_data['wgt_a']

    # Select the features for clustering: length, weight, and length-to-weight ratio
    # These are the columns that will be used to group the fish into clusters
    X = fish_data[['tot_len_a', 'wgt_a', 'length_to_weight_ratio']]

    # Normalize the data for clustering
    # StandardScaler standardizes features by scaling them to have a mean of 0 and a standard deviation of 1
    scaler = StandardScaler()
    # fit_transform: Computes the mean and standard deviation for each feature in X and scales the data accordingly
    X_scaled = scaler.fit_transform(X)


    # Perform K-means clustering
    # The number of clusters is set to 4, so we group the fish into 4 distinct clusters
    k = 4
    # Random state ensures reproducibility
    kmeans = KMeans(n_clusters=k, max_iter=100, random_state=42)  
    # Perform clustering by assigning each fish to a cluster
    # kmeans.fit_predict(X_scaled) does two things:
    # 1. Fits the K-Means model to the scaled data (X_scaled), finding cluster centroids.
    # 2. Predicts the cluster each data point belongs to, returning an array of cluster labels.
    # The resulting cluster labels (e.g., 0, 1, 2, 3) are added as a new column ('cluster') in the fish_data DataFrame.
    fish_data['cluster'] = kmeans.fit_predict(X_scaled)  

    # Visualize the clusters using Plotly: Length vs Weight
    # Create an interactive scatter plot where each fish's length is plotted on the x-axis and weight on the y-axis
    fig = px.scatter(
        fish_data,
         # Length on the x-axis
        x='tot_len_a', 
        # Weight on the y-axis
        y='wgt_a',  
        # Color points by the cluster they belong to
        color='cluster',  
         # Set the title of the plot
        title='K-means Clustering (Length vs Weight)', 
        # Axis labels
        labels={'tot_len_a': 'Fish Length (tot_len_a)', 'wgt_a': 'Fish Weight (wgt_a)'},  
        # Color scale for the clusters
        color_continuous_scale='Viridis', 
        # Show length-to-weight ratio when hovering over each point 
        hover_data=['length_to_weight_ratio']  
    )

    # Customize the plot layout
    # Set marker size and border color
    fig.update_traces(marker=dict(size=10, line=dict(width=1, color='DarkSlateGrey')))  
    fig.update_layout(
         # x-axis title
        xaxis_title='Fish Length (tot_len_a)', 
        # y-axis title
        yaxis_title='Fish Weight (wgt_a)', 
        # Legend title for clusters 
        legend_title='Cluster',  
        #Set the font size for the title
        title_font_size=20, 
        # Set the layout template for a clean white background 
        template='plotly_white'  
    )

    # Display the title of the app
    st.title("K-Means Cluster")
    
    # Show the interactive plot in the Streamlit app
    st.plotly_chart(fig)

    # Provide a brief description of what the graph shows and the significance of K-means clustering
    st.markdown("""
   This graph shows the relationship between fish length and weight, along with a calculated "length-to-weight ratio." K-means clustering groups the fish into similar categories based on these measurements, with each color representing a different cluster. The length-to-weight ratio helps reveal patterns in the fish species. By organizing the fish into clusters, we can better understand how length, weight, and this ratio relate to one another, providing valuable information. This means you can spot different types or "profiles" of fish you’re catching—like one group that’s short and heavy, and another that’s long and lean. It helps you make sense of large datasets by showing patterns in fish size and build that aren’t obvious at first glance. Even though species aren’t labeled, this method helps us spot natural groupings in the fish population — such as common size ranges or shape profiles. It’s useful for understanding how fish vary and where outliers might exist.
    """)