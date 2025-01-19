import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score, mean_squared_error


# Loading the dataset
file_path = 'C:\\Users\\c.wink27\\Downloads\\ps_2023_csv\\catch_20231.csv'
catch_data = pd.read_csv(file_path)

# Filter the data for rows with valid length and weight values 
filtered_data = catch_data[(catch_data['tot_len_a'] > 0) & (catch_data['wgt_a'] > 0)]

X = filtered_data['tot_len_a'].values.reshape(-1, 1)
y = filtered_data['wgt_a'].values

# Initialize the Decision Tree Regressor, intializing so it only has the max depth of 5
regressor = DecisionTreeRegressor(random_state=0, max_depth=5)

# Fit the regressor to your data
regressor.fit(X, y)

# Predict on the training data
y_pred = regressor.predict(X)

# Calculate R-squared
r_squared = r2_score(y, y_pred)
print(f"R-squared: {r_squared}")

# Calculate Mean Squared Error 
mse = mean_squared_error(y, y_pred)
print(f"Mean Squared Error: {mse}")


# Predicting a specific value this is for 50mm
predicted_weight = regressor.predict([[50]])
print(f"Predicted weight for length 50: {predicted_weight}")

# Create a grid for high-resolution visualization
X_grid = np.arange(min(X), max(X), 0.1).reshape(-1, 1)

# Scatter plot of the original data
plt.scatter(X, y, color='red', label='Actual Data')

# Line plot of the predictions
plt.plot(X_grid, regressor.predict(X_grid), color='blue', label='Predicted Curve')

# Add titles and labels
plt.title('Length vs Weight (Decision Tree Regression)')
plt.xlabel('Length')
plt.ylabel('Weight')
plt.legend()
plt.show()

