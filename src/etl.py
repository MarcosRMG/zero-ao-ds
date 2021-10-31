import geopandas
import streamlit as st
import pandas as pd


@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)
    data['date'] = pd.to_datetime(data['date'])
    data['date'] = data['date'].dt.strftime('%Y-%m-%d')
    # Change dtypes
    data['id'] = data['id'].astype('str')
    # add new features
    data['price_m2'] = data['price'] / data['sqft_lot']
    return data


# Get geofile
@st.cache(allow_output_mutation=True)
def get_geofile(url):
    return geopandas.read_file(url)
