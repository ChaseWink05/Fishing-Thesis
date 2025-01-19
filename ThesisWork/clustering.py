import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = r'C:\Users\c.wink27\Downloads\ps_2023_csv\catch_20236.csv'
df = pd.read_csv(file_path)

# Replace empty rows in 'common' with NaN
df['common'] = df['common'].fillna('NaN')

# Step 1: Count occurrences of each species, excluding 'NaN'
species_counts = {}
for species in df['common']:
    if species != 'NaN':  # Exclude 'NaN'
        if species in species_counts:
            species_counts[species] += 1
        else:
            species_counts[species] = 1

# Step 2: Convert dictionary to a list of tuples
species_counts_items = list(species_counts.items())

# Step 3: Define a custom function to get the second element of a tuple
def get_second_element(pair):
    return pair[1]

# Step 4: Sort the list by the second element (the count) in descending order
sorted_species = sorted(species_counts_items, key=get_second_element, reverse=True)

# Step 5: Slice the first 20 items for the top 20 species
top_20_species = sorted_species[:20]

# Step 6: Extract species names and counts for plotting
species_names = [species[0] for species in top_20_species]
species_counts = [species[1] for species in top_20_species]

# Step 7: Plot a bar chart
plt.figure(figsize=(12, 8))
bars = plt.bar(species_names, species_counts, color='skyblue')

# Step 8: Add text labels (counts) above each bar
for bar, count in zip(bars, species_counts):
    plt.text(
        bar.get_x() + bar.get_width() / 2,  # x-coordinate center of the bar
        bar.get_height(),  # y-coordinate top of the bar
        str(count),  # Text to display
        ha='center',  # Horizontal alignment
        va='bottom',  # Vertical alignment
        fontsize=10 \
    )

# Finalize the plot
plt.xticks(rotation=90, fontsize=10)
plt.xlabel('Species', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.title('Top 20 Most Occurring Fish Species', fontsize=16)
plt.tight_layout()
plt.show()
