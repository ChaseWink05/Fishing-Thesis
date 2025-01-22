
from plotly import graph_objects as go
import plotly.express as px
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
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
    filtered_data = catch_data[(catch_data['tot_len_a'] > 0) & (catch_data['wgt_a'] > 0)]

    # Prepare the independent variable (X) and dependent variable (y)
    X = filtered_data['tot_len_a'].values.reshape(-1, 1)  # 'tot_len_a' represents fish length
    y = filtered_data['wgt_a'].values  # 'wgt_a' represents fish weight

    # Initialize the Decision Tree Regressor model with a maximum depth of 5
    regressor = DecisionTreeRegressor(random_state=0, max_depth=5)

    # Fit the decision tree model to the training data
    regressor.fit(X, y)

    # Predict the fish weights (y_pred) based on the trained model
    y_pred = regressor.predict(X)

    # Calculate R-squared score and Mean Squared Error
    r_squared = r2_score(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    st.write(f"R-squared: {r_squared}")
    st.write(f"Mean Squared Error: {mse}")

    # Predict the weight of a fish when the length is 50mm
    predicted_weight = regressor.predict([[50]])
    st.write(f"Predicted weight for length 50mm: {predicted_weight[0]}")

    # Create a high-resolution grid of lengths for visualization
    X_grid = np.arange(min(X), max(X), 0.1).reshape(-1, 1)

    # Create the interactive plot with Plotly
    fig = go.Figure()

    # Add scatter plot for actual data points
    fig.add_trace(go.Scatter(
        x=filtered_data['tot_len_a'], 
        y=filtered_data['wgt_a'], 
        mode='markers', 
        name='Actual Data', 
        marker=dict(color='red', size=8)
    ))

    # Add line for the predicted regression curve
    fig.add_trace(go.Scatter(
        x=X_grid.flatten(), 
        y=regressor.predict(X_grid), 
        mode='lines', 
        name='Predicted Curve', 
        line=dict(color='blue', width=2)
    ))

    # Update layout
    fig.update_layout(
        title='Length vs Weight (Decision Tree Regression)',
        xaxis_title='Length',
        yaxis_title='Weight',
        template='plotly_white',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )

    # Display the interactive plot in Streamlit
    st.plotly_chart(fig)

