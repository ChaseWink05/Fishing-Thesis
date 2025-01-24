
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import streamlit as st
import os
from sklearn.metrics import mean_squared_error


# Loading the dataset
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

    # Filter the data for rows with valid length and weight values 
    filtered_data = catch_data[(catch_data['tot_len_a'] > 0) & (catch_data['wgt_a'] > 0)]

    # Independent variable, adding a constant for intercept in the model
    X = sm.add_constant(filtered_data['tot_len_a'])

    # Dependent variable
    y = filtered_data['wgt_a']

    # Fit the linear regression model
    model = sm.OLS(y, X).fit()

     # Extract predictions and performance metrics
    filtered_data['predicted_wgt'] = model.predict(X)
    mse = round(mean_squared_error(y, filtered_data['predicted_wgt']), 3)
    r_squared = round(model.rsquared, 3)
    
    # Display metrics
    st.write(f"Linear Regression Metrics")
    st.write(f"R-squared: {r_squared}")
    st.write(f"Mean Squared Error: {mse}")

    # Print the regression results summary
    #print(model.summary())

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(filtered_data['tot_len_a'], filtered_data['wgt_a'], alpha=0.7, label='Data Points')
    ax.plot(filtered_data['tot_len_a'], model.predict(X), color='red', label='Regression Line')
    ax.set_title('Fish Length vs Weight (Linear Regression)')
    ax.set_xlabel('Fish Length (mm)')
    ax.set_ylabel('Fish Weight (kg)')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
