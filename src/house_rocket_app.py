import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st


st.set_page_config(layout='wide')
st.title('House Rocket Company')
st.markdown('Hellcome to House Rocket Data Analysis')


# Read data
@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)
    data['date'] = pd.to_datetime(data['date'])
    return data


# load data
data = get_data('./data/kc_house_data.csv')


# add new features
data['price_m2'] = data['price'] / data['sqft_lot']

# ==================
# Data Overview
# ==================
f_attributes = st.sidebar.multiselect('Enter columns', data.columns)
f_zipcode = st.sidebar.multiselect('Enter zipcode', data['zipcode'].unique())

st.title('Data Overview')

if f_attributes != [] and f_zipcode != []:
    data = data.loc[data['zipcode'].isin(f_zipcode), f_attributes]
elif f_attributes == [] and f_zipcode != []:
    data = data.loc[data['zipcode'].isin(f_zipcode), :]
elif f_attributes != [] and f_zipcode == []:
    data = data.loc[:, f_attributes]
else:
    data = data.copy()

st.dataframe(data)

## plot map
#st.title('House Rocket Map')
#is_check = st.checkbox('Display Map')
#
## filters
#price_min = int(data['price'].min())
#price_max = int(data['price'].max())
#price_avg = int(data['price'].mean())
#
#price_slider = st.slider('Price Range', price_min, price_max, price_avg)
#
#if is_check:
#    # select rows
#    houses = data[data['price'] < price_slider][['id', 'lat', 'long', 'price']]
#    #st.dataframe(houses)
#
#    # draw map
#    fig = px.scatter_mapbox(houses, lat='lat', lon='long', size='price', color_continuous_scale=px.colors.cyclical.IceFire, 
#                            size_max=15, zoom=10)
#    fig.update_layout(mapbox_style='open_street_map', height=600, margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
#    st.plotly_chart(fig)
