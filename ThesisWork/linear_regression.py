import pandas as pd  
import statsmodels.api as sm  
import matplotlib.pyplot as plt  
import streamlit as st  
import os  # For file and directory operations
from sklearn.metrics import mean_squared_error  # For calculating the mean squared error (MSE)

# Main function to run the linear regression analysis
def run():
    # Define the path to the CSV file in the GitHub/Streamlit environment
    destination_file = os.path.join('ThesisWork', 'catch_20236.csv')

    # Check if the file exists
    if not os.path.exists(destination_file):
        # Display an error message if the file is missing
        st.error(f"Error: The file 'catch_20236.csv' is missing in the 'ThesisWork' folder.")
        st.write("Please make sure the CSV file is placed in the 'ThesisWork' folder and try again.")
    else:
        # If the file exists, read the CSV data into a pandas DataFrame
        catch_data = pd.read_csv(destination_file)

    # Filter the data for rows with valid length and weight values
    # Only include rows where 'tot_len_a' (fish length) and 'wgt_a' (fish weight) are greater than 0
    filtered_data = catch_data[(catch_data['tot_len_a'] > 0) & (catch_data['wgt_a'] > 0)]

    # Independent variable (X): Fish length ('tot_len_a')
    # Add a constant term to the model to account for the intercept since data might not pass through orgin
    X = sm.add_constant(filtered_data['tot_len_a'])

    # Dependent variable (y): Fish weight ('wgt_a')
    y = filtered_data['wgt_a']

    # Fit the linear regression model using Ordinary Least Squares (OLS)
    # This creates a linear model that predicts 'wgt_a' based on 'tot_len_a'
    #sm.OLS(y, X) creates an OLS regression model using the dependent variable (y, fish weight) and the independent variable (X, fish length with a constant term for the intercept).
    #OLS is a statistical method that minimizes the sum of squared differences between the observed values (y) and the predicted values from the linear model.
    #.fit() calculates the best-fit line that minimizes the residuals (differences between actual and predicted values).
    model = sm.OLS(y, X).fit()

    # Extract predictions and performance metrics
    # Use the fitted model to predict fish weight based on the independent variable
    filtered_data['predicted_wgt'] = model.predict(X)

    # Calculate the Mean Squared Error (MSE) between actual and predicted weights
    mse = mean_squared_error(y, filtered_data['predicted_wgt'])

    # Extract the R-squared value from the model
    # R-squared measures how well the independent variable explains the variance in the dependent variable
    r_squared = model.rsquared

    # Display the regression metrics in the Streamlit app
    st.write(f"Linear Regression Metrics")
    # Display R-squared value rounded to 3 decimal places
    st.write(f"R-squared: {r_squared:.3f}")  
    # Display MSE rounded to 3 decimal places
    st.write(f"Mean Squared Error: {mse:.3f}")  

    # Commenting out the summary display 
    # print(model.summary())

    # Create a scatter plot of the data points and the regression line
    fig, ax = plt.subplots(figsize=(8, 6))  # Set the figure size
    # Scatter plot of actual data
    ax.scatter(filtered_data['tot_len_a'], filtered_data['wgt_a'], alpha=0.7, label='Data Points')  
    # Regression line
    ax.plot(filtered_data['tot_len_a'], model.predict(X), color='red', label='Regression Line') 

    # Add titles and labels to the plot
    # Title of the plot
    ax.set_title('Fish Length vs Weight (Linear Regression)') 
    # Label for the x-axis
    ax.set_xlabel('Fish Length (mm)')  
    # Label for the y-axis
    ax.set_ylabel('Fish Weight (kg)')  

    # Add a legend to distinguish between data points and the regression line
    ax.legend()

    # Add a grid to the plot for better readability
    ax.grid(True)

    # Display the plot in the Streamlit app
    st.pyplot(fig)