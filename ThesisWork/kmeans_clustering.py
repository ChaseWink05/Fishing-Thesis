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

# Fill missing species names
fish_data['common'] = fish_data['common'].fillna('Unknown')

# Filter rows with valid values for tot_len_a and wgt_a
fish_data = fish_data[(fish_data['tot_len_a'] > 0) & (fish_data['wgt_a'] > 0)]

# Select only the columns for clustering
X = fish_data[['tot_len_a', 'wgt_a']]

# Normalize the data 
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Perform K-means clustering
k = 3  # Number of clusters
kmeans = KMeans(n_clusters=k, random_state=42)
fish_data['cluster'] = kmeans.fit_predict(X_scaled)

# Plot the clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(
    x=fish_data['tot_len_a'],
    y=fish_data['wgt_a'],
    hue=fish_data['cluster'],
    palette='viridis',
    style=fish_data['cluster'],
    s=100
)
plt.title('K-means Clustering (Length vs Weight)', fontsize=16)
plt.xlabel('Fish Length (tot_len_a)', fontsize=14)
plt.ylabel('Fish Weight (wgt_a)', fontsize=14)
plt.legend(title='Cluster', fontsize=12)
plt.grid(True)
plt.show()
