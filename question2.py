# Reading the previously fetched data
df = pd.read_csv('bls_cpi_data.csv')
df.tail()

# Calculate the year-over-year percentage variation
df['yoy_pct_variation'] = (df['CPI All items, less food and energy, seasonally adjusted'].pct_change(periods=12) * 100)

# Filter the data from 2019 to the present
df['date'] = pd.to_datetime(df['date'])
df_filtered = df[df['date'] >= '2019-01-01']

# Remove other data
df_filtered = df_filtered.drop(columns=['CPI All items, seasonally adjusted', 'CPI Gasoline (all types), seasonally adjusted'])
df_filtered.head()

import plotly.express as px

# Plot the data using Plotly
fig = px.line(df_filtered, x=df_filtered['date'], y='yoy_pct_variation', title='CPI All items, less food and energy, seasonally adjusted - Year-over-Year Percentage Variation')

fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Year-over-Year Variation (%)'
)

fig.show()

