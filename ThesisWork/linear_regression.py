
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import streamlit as st
import os

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

    # Print the regression results summary
    print(model.summary())

    # Create a scatter plot with the regression line using Matplotlib
    plt.figure(figsize=(10, 6))
    plt.scatter(filtered_data['tot_len_a'], filtered_data['wgt_a'], alpha=0.7, label='Data Points')
    plt.plot(filtered_data['tot_len_a'], model.predict(X), color='red', label='Regression Line')
    plt.title('Fish Length vs Weight')
    plt.xlabel('Fish Length (mm)')
    plt.ylabel('Fish Weight (kg)')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)
