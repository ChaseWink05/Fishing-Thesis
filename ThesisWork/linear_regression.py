
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt


file_path = 'C:\\Users\\c.wink27\\Downloads\\ps_2023_csv\\catch_20231.csv'
catch_data = pd.read_csv(file_path)

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
plt.show()
