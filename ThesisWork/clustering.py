import pandas as pd  
import matplotlib.pyplot as plt  

file_path = r'C:\Users\c.wink27\Downloads\ps_2023_csv\catch_20236.csv'  
df = pd.read_csv(file_path) 

# Replace empty rows (NaN values) in the 'common' column with the string 'NaN'
df['common'] = df['common'].fillna('NaN')  # This ensures that any missing species names are marked as 'NaN'

# Count occurrences of each species in the 'common' column, excluding 'NaN'
species_counts = {}  # Initialize an empty dictionary to store species counts
for species in df['common']:  # Loop through each species name in the 'common' column
    if species != 'NaN':  # Exclude rows where the species is 'NaN' (i.e., missing data)
        if species in species_counts:  # If the species is already in the dictionary, increment the count
            species_counts[species] += 1
        else:  # If the species is not in the dictionary, add it with an initial count of 1
            species_counts[species] = 1

# Convert the dictionary of species counts to a list of tuples
species_counts_items = list(species_counts.items())  # Convert the dictionary to a list of key-value pairs 

# Define a custom function to get the second element of a tuple the count of occurrences
def get_second_element(pair):
    return pair[1]  # Return the second element which is the count of the tuple

# Sort the list of tuples by the second element in descending order
sorted_species = sorted(species_counts_items, key=get_second_element, reverse=True)  # Sort by count in descending order

#Slice the list to get the top 20 species with the highest counts
top_20_species = sorted_species[:20]  # Select the first 20 species from the sorted list

# Extract species names and counts for plotting
species_names = [species[0] for species in top_20_species]  # Extract the species names first element of each tuple
species_counts = [species[1] for species in top_20_species]  # Extract the counts second element of each tuple

# Plot a bar chart with the species names on the x-axis and the counts on the y-axis
plt.figure(figsize=(12, 8))  # Set the figure size for the plot
bars = plt.bar(species_names, species_counts, color='skyblue')  # Create a bar chart with the species and their counts

# Add text labels (counts) above each bar on the chart
for bar, count in zip(bars, species_counts):  # Iterate over the bars and the counts
    plt.text(
        bar.get_x() + bar.get_width() / 2,  # x-coordinate: center of the bar
        bar.get_height(),  # y-coordinate: top of the bar (height of the bar)
        str(count),  # Display the count as text above the bar
        ha='center',  # Horizontal alignment: center the text horizontally over the bar
        va='bottom',  # Vertical alignment: place the text just above the top of the bar
        fontsize=10  # Set the font size for the text
    )

# Finalize the plot by adding labels and formatting
plt.xticks(rotation=90, fontsize=10)  # Rotate x-axis labels by 90 degrees to make them readable, and set the font size
plt.xlabel('Species', fontsize=14)  # Label the x-axis as 'Species' with a font size of 14
plt.ylabel('Count', fontsize=14)  # Label the y-axis as 'Count' with a font size of 14
plt.title('Top 20 Most Occurring Fish Species', fontsize=16)  # Set the plot title with a font size of 16
plt.tight_layout()  # Adjust the layout to avoid clipping of labels and titles
plt.show()  # Display the plot
