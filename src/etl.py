import geopandas
import streamlit as st
import pandas as pd


@st.cache(allow_output_mutation=True)
def get_data(path):
    # Read and data format
    data = pd.read_csv(path)
    data['date'] = pd.to_datetime(data['date'])
    data['date'] = data['date'].dt.strftime('%Y-%m-%d')

    # Change dtypes
    data['id'] = data['id'].astype('str')

    # add new features
    # price_m²
    data['price_m2'] = data['price'] / data['sqft_lot']
    # price median
    price_median = data[['zipcode', 'price']].groupby('zipcode').median().reset_index()
    price_median.rename(columns={'price': 'price_median'}, inplace=True)
    data = data.merge(price_median, on='zipcode', how='inner')
    # recommendation
    data['recommendation'] = None
    for i in range(len(data)):
        if data['price'][i] < data['price_median'][i] and data['condition'][i] >= 3:
            data['recommendation'][i] = 'buy'
        else:
            data['recommendation'][i] = "don't buy"
    return data


# Get geofile
@st.cache(allow_output_mutation=True)
def get_geofile(url):
    return geopandas.read_file(url)
