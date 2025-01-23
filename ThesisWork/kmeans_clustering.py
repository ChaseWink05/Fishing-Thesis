import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

# Load the dataset
file_path = r'C:\Users\c.wink27\Downloads\ps_2023_csv\catch_20236.csv'
fish_data = pd.read_csv(file_path)

# Fill missing values in the 'common' column with the string 'Unknown'
# This is important because missing values can affect the clustering process
fish_data['common'] = fish_data['common'].fillna('Unknown')

# Filter the rows where the values for 'tot_len_a' (fish length) and 'wgt_a' (fish weight) are positive
# This ensures that we only use valid data points for clustering (ignores rows with negative or zero values)
fish_data = fish_data[(fish_data['tot_len_a'] > 0) & (fish_data['wgt_a'] > 0)]

# Select only the columns 'tot_len_a' (length) and 'wgt_a' (weight) for clustering
# These are the features (attributes) that will be used to group the fish into clusters
X = fish_data[['tot_len_a', 'wgt_a']]

# Normalize the data using StandardScaler
# StandardScaler removes the mean and scales the data to unit variance, which is important for K-means
# This ensures that both features (length and weight) have the same scale and do not dominate the clustering
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # Apply scaling to the data

# Perform K-means clustering with 3 clusters
# The KMeans algorithm tries to divide the data into 'k' clusters by minimizing the distance between points within the same cluster
k = 3  # Set the number of clusters 
kmeans = KMeans(n_clusters=k, random_state=42)  # Create the KMeans model
fish_data['cluster'] = kmeans.fit_predict(X_scaled)  # Fit the model and assign cluster labels to each row in the data

# Plot the clusters
# This creates a scatter plot to visualize how the fish are grouped into clusters based on length and weight
plt.figure(figsize=(10, 6))  # Set the size of the plot
sns.scatterplot(
    x=fish_data['tot_len_a'],  # X-axis is fish length
    y=fish_data['wgt_a'],  # Y-axis is fish weight
    hue=fish_data['cluster'],  # Color points based on their cluster label
    palette='viridis',  
    style=fish_data['cluster'],  # Different marker styles for each cluster
    s=100  # Size of the points on the plot
)
plt.title('K-means Clustering (Length vs Weight)', fontsize=16)  # Add a title to the plot
plt.xlabel('Fish Length (tot_len_a)', fontsize=14)  # Label for the X-axis
plt.ylabel('Fish Weight (wgt_a)', fontsize=14)  # Label for the Y-axis
plt.legend(title='Cluster', fontsize=12)  # Add a legend showing the cluster labels
plt.grid(True)  # Add a grid to the plot for better visibility
plt.show()  # Display the plot