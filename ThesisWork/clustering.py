
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = r'C:\Users\c.wink27\Downloads\ps_2023_csv\catch_20236.csv'
df = pd.read_csv(file_path) 
df.info()
df.describe()

# Replace empty rows in 'common' with NaN
df['common'] = df['common'].fillna('NaN')

# Get unique species and assign a simple x-axis position to each species
#Creates an array that looks like this unique_species = ['STRIPED BASS', 'TAUTOG', 'BLACK SEA BASS'] for example for every unique one
unique_species = df['common'].unique() 
# List of unique species, Each species gets a unique number for plotting on the x-axis.
#Creating a dictionary that maps each unique species from unique_species to a unique integer value which is the index of the species in the list.
#used to iterate through the unique_species list and return both the index (i) and the species (species) as a tuple.
#the species name is the key and the index is the value. This generates pairs like (0, 'STRIPED BASS') for example
species_positions = {}
for i, species in enumerate(unique_species):
    species_positions[species] = i

# iterates over every species in the df['common'] column. For each species, it looks up its corresponding position
# in species_positions, which gives you the x-axis value for that species.
x_values = []
for species in df['common']:
    x_values.append(species_positions[species])

y_values = []
for i in range(len(df)):
    y_values.append(i)
  # One dot for each row in the dataset

# Plot the scatter plot
plt.figure(figsize=(12, 8))
plt.scatter(x_values, y_values, color='blue', alpha=0.6, s=10)

# Add species names as labels on the x-axis
plt.xticks(ticks=list(species_positions.values()), labels=list(species_positions.keys()), rotation=90, fontsize=8)
plt.xlabel('Species', fontsize=14)
plt.ylabel('Occurrences (Row Index)', fontsize=14)
plt.title('One Dot for Every Fish Occurrence', fontsize=16)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.5)

# Show the plot
plt.show()
