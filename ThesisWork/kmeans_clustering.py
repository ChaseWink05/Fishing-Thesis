import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Load the dataset
file_path = r'C:\Users\c.wink27\Downloads\ps_2023_csv\catch_20236.csv'
catch_data = pd.read_csv(file_path)

# Filter for valid length and weight values
filtered_data = catch_data[(catch_data['tot_len_a'] > 0) & (catch_data['wgt_a'] > 0)]

# Select the features for clustering
X = filtered_data[['tot_len_a', 'wgt_a']]

# Scale the data
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Apply K-Means clustering
kmeans = KMeans(n_clusters=50, max_iter=100, random_state=42)
y_kmeans = kmeans.fit_predict(X_scaled)

# Transform the scaled data back to its original scale
X_transformed = scaler.inverse_transform(X_scaled)

# Create a DataFrame with the original scale data and cluster labels
result = pd.DataFrame(X_transformed, columns=X.columns)
result['Cluster'] = y_kmeans

# Visualize the clusters
plt.figure(figsize=(10, 6))
for cluster in np.unique(result['Cluster']):
    cluster_data = result[result['Cluster'] == cluster]
    plt.scatter(cluster_data['tot_len_a'], cluster_data['wgt_a'], label=f'Cluster {cluster}')

plt.xlabel('Total Length (mm)')
plt.ylabel('Weight (kg)')
plt.title('K-Means Clustering of Fish (Length vs. Weight)')
plt.legend()
plt.grid(True)
plt.show()
