import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

# Load the dataset
file_path = r'C:\Users\c.wink27\Downloads\ps_2023_csv\catch_20236.csv'
fish_data = pd.read_csv(file_path)

# Fill missing species names
fish_data['common'] = fish_data['common'].fillna('Unknown')

# Filter rows with positive and reasonable values for tot_len_a and wgt_a
fish_data = fish_data[(fish_data['tot_len_a'] > 0) & (fish_data['wgt_a'] > 0)]

# Calculate the correlation matrix (only using numeric columns)
corr_df = fish_data[['tot_len_a', 'wgt_a']].corr()

# Define the custom colormap
colors = ["#4361EE", "#FFFFFF", "#B40051"]  # Blue, White, Magenta
cmap = LinearSegmentedColormap.from_list("custom_cmap", colors)

# Plotting the heatmap of the correlation matrix
plt.figure(figsize=(8, 8))
sns.heatmap(corr_df, cmap=cmap, center=0, vmin=-1, annot=True, linewidths=0.5)

# Add titles and axis labels
plt.title("Correlation Heatmap of Fish Length and Weight (Filtered)", fontsize=16)
plt.xlabel("Variables", fontsize=14)
plt.ylabel("Variables", fontsize=14)

# Display the plot
plt.show()
