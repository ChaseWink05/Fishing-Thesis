import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load the dataset
file_path = r'C:\Users\c.wink27\Downloads\ps_2023_csv\catch_20236.csv'
fish_data = pd.read_csv(file_path)

# Fill missing species names with 'Unknown' to handle missing data
fish_data['common'] = fish_data['common'].fillna('Unknown')

# Filter rows with valid values for tot_len_a (length) and wgt_a (weight)
# Ensures only rows with positive length and weight are used
fish_data = fish_data[(fish_data['tot_len_a'] > 0) & (fish_data['wgt_a'] > 0)]

# Create a new column for the length-to-weight ratio
# This feature helps capture the relationship between length and weight
fish_data['length_to_weight_ratio'] = fish_data['tot_len_a'] / fish_data['wgt_a']

# Select the features for clustering: length, weight, and length-to-weight ratio
# These features will be used to group the data into clusters
X = fish_data[['tot_len_a', 'wgt_a', 'length_to_weight_ratio']]

# Normalize the data for clustering
# StandardScaler standardizes features by scaling them to have a mean of 0 and a standard deviation of 1
scaler = StandardScaler()
# fit_transform: Computes the mean and standard deviation for each feature in X and scales the data accordingly
X_scaled = scaler.fit_transform(X)

# Custom function to calculate WSS (within-cluster sum of squares)
# This function computes the sum of squared distances of points to their cluster centers
def calculate_WSS(points, kmax):
    # List to store the WSS for each value of k
    sse = []  
    for k in range(1, kmax + 1):
        # Fit K-Means with k clusters
        kmeans = KMeans(n_clusters=k, random_state=42).fit(points)
         # Get cluster centers
        centroids = kmeans.cluster_centers_ 
        # Predicting the cluster assignments
        pred_clusters = kmeans.predict(points)
        # Initialize WSS for the current k  
        curr_sse = 0  

        # Calculate the sum of squared distances for each point
        for i in range(len(points)):
            # Get the center of the assigned cluster
            curr_center = centroids[pred_clusters[i]]  
            # Compute squared distance
            curr_sse += np.sum((points[i] - curr_center) ** 2)  
        # Append the WSS for the current k
        sse.append(curr_sse)  
    return sse

# Run elbow method
# Maximum number of clusters to test
kmax = 10  
# Compute WSS for k = 1 to kmax
wss = calculate_WSS(X_scaled, kmax)  

# Plot the elbow graph
# The elbow graph helps identify the optimal number of clusters
plt.figure(figsize=(10, 6))
 # Plot WSS vs. number of clusters
plt.plot(range(1, kmax + 1), wss, marker='o', linestyle='--') 
plt.title('Elbow Method (Custom WSS) for Optimal Number of Clusters', fontsize=16)
plt.xlabel('Number of Clusters (k)', fontsize=14)
plt.ylabel('WSS (Within-Cluster Sum of Squares)', fontsize=14)
# Add grid for better readability
plt.grid(True)  
plt.show()