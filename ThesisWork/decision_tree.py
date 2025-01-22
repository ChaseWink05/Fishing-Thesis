import numpy as np 
import matplotlib.pyplot as plt  
import pandas as pd 
from sklearn.tree import DecisionTreeRegressor  # Decision Tree model from scikit-learn for regression
from sklearn.metrics import r2_score, mean_squared_error  # For evaluating the model's performance
import os
import streamlit as st

def run():
    # Define the path to the CSV file in the GitHub/Streamlit environment
    destination_file = os.path.join('ThesisWork', 'catch_20236.csv')

    # Check if the file exists
    if not os.path.exists(destination_file):
        st.error(f"Error: The file 'catch_20236.csv' is missing in the 'ThesisWork' folder.")
        st.write("Please make sure the CSV file is placed in the 'ThesisWork' folder and try again.")
    else:
        # If the file exists, read the CSV data
        catch_data = pd.read_csv(destination_file)

    # Filter the data for valid rows: keeping only rows where both 'tot_len_a' and 'wgt_a' are greater than 0
    # This ensures we don't have invalid or missing values for length and weight
    filtered_data = catch_data[(catch_data['tot_len_a'] > 0) & (catch_data['wgt_a'] > 0)]  # Filters valid data

    # Prepare the independent variable (X) and dependent variable (y)
    X = filtered_data['tot_len_a'].values.reshape(-1, 1)  # 'tot_len_a' represents fish length reshaping as a column for the decsion tree
    y = filtered_data['wgt_a'].values  # 'wgt_a' represents fish weight

    # Initialize the Decision Tree Regressor model with a maximum depth of 5
    regressor = DecisionTreeRegressor(random_state=0, max_depth=5)

    # Fit the decision tree model to the training data X for input features and y for output labels
    regressor.fit(X, y)

    # Predict the fish weights (y_pred) based on the trained model and input data X
    y_pred = regressor.predict(X)

    # Calculate the R-squared score which is how well the model's predictions match the actual data
    r_squared = r2_score(y, y_pred)
    print(f"R-squared: {r_squared}")  # Output the R-squared score

    # Calculate Mean Squared Error, which measures the average squared difference between predicted and actual values
    mse = mean_squared_error(y, y_pred)
    print(f"Mean Squared Error: {mse}")  # Output the Mean Squared Error value

    # Predict the weight of a fish when the length is 50mm
    predicted_weight = regressor.predict([[50]])  # Predict for length 50mm
    print(f"Predicted weight for length 50: {predicted_weight}")  # Output the predicted weight for 50mm length

    # Create a high res grid of lengths for visualization 
    X_grid = np.arange(min(X), max(X), 0.1).reshape(-1, 1)  # Generates values from min(X) to max(X) with small steps (0.1)

    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(X, y, color='red', label='Actual Data')
    ax.plot(X_grid, regressor.predict(X_grid), color='blue', label='Predicted Curve')
    ax.set_title('Length vs Weight (Decision Tree Regression)')
    ax.set_xlabel('Length')
    ax.set_ylabel('Weight')
    ax.legend()

    st.pyplot(fig)

