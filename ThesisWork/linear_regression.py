
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import streamlit as st
import os
import plotly.express as px
from plotly import graph_objects as go

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

    # Extract regression line data
    filtered_data['predicted_wgt'] = model.predict(X)

    # Create a Plotly scatter plot with a regression line
    fig = px.scatter(filtered_data, 
                     x='tot_len_a', 
                     y='wgt_a', 
                     labels={'tot_len_a': 'Fish Length (mm)', 'wgt_a': 'Fish Weight (kg)'},
                     title="Fish Length vs Weight (Linear Regression)",
                     opacity=0.7)

    # Add the regression line to the plot
    fig.add_trace(go.Scatter(x=filtered_data['tot_len_a'], 
                             y=filtered_data['predicted_wgt'],
                             mode='lines',
                             name='Regression Line',
                             line=dict(color='red')))

    # Display the plot in Streamlit
    st.plotly_chart(fig)