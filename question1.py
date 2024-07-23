import requests
import pandas as pd
import json

# Define the series IDs for the data I want to retrieve
# Series ID as specified in Data Tools > Help & Tutorials at bls.gov
series_ids = {
    'CPI All items, seasonally adjusted': 'CUSR0000SA0',
    'CPI All items, less food and energy, seasonally adjusted': 'CUSR0000SA0L1E',
    'CPI Gasoline (all types), seasonally adjusted': 'CUSR0000SETB01'
}

# Define the payload for the API request
payload = json.dumps({
    "seriesid": list(series_ids.values()),
    "startyear": "2003", 
    "endyear": "2023",
    "registrationkey": '263823f3339346b7978c67e2b0c5d8d4'
})

# Define the URL for the BLS API request
url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'

# Make the API request
response = requests.post(url, headers={'Content-Type': 'application/json'}, data=payload)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Initialize an empty DataFrame
    df = pd.DataFrame()
    
    # Process each series
    for series in data['Results']['series']:
        series_id = series['seriesID']
        series_name = [key for key, value in series_ids.items() if value == series_id][0]
        series_data = series['data']
        
        # Create a DataFrame for the current series
        series_df = pd.DataFrame(series_data)
        series_df['date'] = pd.to_datetime(series_df['year'] + '-' + series_df['period'].str.replace('M', '') + '-01')
        series_df = series_df[['date', 'value']]
        series_df.set_index('date', inplace=True)
        series_df.columns = [series_name]
        
        # Merge the current series DataFrame with the main DataFrame
        if df.empty:
            df = series_df
        else:
            df = df.merge(series_df, on='date', how='outer')
    
    # Save the DataFrame to a CSV file
    df.to_csv('bls_cpi_data.csv')
else:
    print(f"Failed to retrieve data: {response.status_code}")

print("Data retrieval and processing complete. The data has been saved to 'bls_cpi_data.csv'.")