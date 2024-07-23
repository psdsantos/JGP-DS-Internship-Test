import plotly.express as px

fig = px.line(df, x=df['date'], y=['CPI All items, seasonally adjusted', 'CPI Gasoline (all types), seasonally adjusted'],
              labels={'value': 'Index Value', 'date': 'Date'},
              title='Comparison of CPI All Items and Gasoline Prices')
fig.update_layout(yaxis_title='Index Value')
fig.show()

correlation = df['CPI All items, seasonally adjusted'].corr(df['CPI Gasoline (all types), seasonally adjusted'])
print(f"Correlation coefficient: {correlation}")

import statsmodels.api as sm

# Prepare the data
X = df['CPI All items, seasonally adjusted']
y = df['CPI Gasoline (all types), seasonally adjusted']

# Add a constant to the independent variable matrix
X = sm.add_constant(X)

# Fit the regression model
model = sm.OLS(y, X).fit()

# Print the summary
print(model.summary())